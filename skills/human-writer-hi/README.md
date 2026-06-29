# Human Writer — Hindi (hi) — a Claude skill

A Claude Code skill that produces **Hindi** prose (Devanagari) reading as human-authored, sanitizes Hindi AI drafts to remove detector tells, and scores any Hindi draft for AI-detection risk before publication.

This is the **Hindi member** of the `human-writer` per-language family — one autonomous skill per language (`en`, `fr`, `es`, `pt`, `de`, `ar`, `hi`), all built on the same architecture. They install side by side and do not conflict: each activates on its own language triggers.

## Why this skill exists

`mr-bridge.com` ships localized marketing and editorial copy in Hindi. Modern Sonnet / Opus / GPT-class Hindi output is fluent enough to ship, but it carries fingerprints that commercial detectors (Copyleaks, GPTZero, Originality.ai) latch onto, and Hindi carries its own tells the EN/FR analyzer never checked:

- **Statistical:** low burstiness, narrow type-token ratio (language-agnostic).
- **Stylistic:** the same inflated Sanskritized words repeated across drafts ("यह ध्यान देने योग्य है", "आज के युग में", "मजबूत", "क्रांतिकारी"), formulaic frames ("यह न केवल X है, बल्कि Y भी").
- **Typographic (Hindi-specific):** a Latin full stop "." used instead of the Devanagari danda "।", the Anglo em-dash "—" (which has no native use in Devanagari), EN→hi calques ("निर्बाध", "कार्रवाई योग्य अंतर्दृष्टि"), and inconsistent Latin vs Devanagari digits.

A draft drops, a client runs it through a detector, the score comes back at 70%+, and it's rejected. The fix is a disciplined sweep of the specific Hindi tells detectors weight. This skill encodes that doctrine plus a deterministic analyzer so any Claude Code session can produce, clean, or audit Hindi prose to a target score before delivery.

## What it can do

**Three modes:**
- **Write (लिखना):** produce new Hindi content already engineered to score LOW_RISK.
- **Clean (साफ़ करना):** rewrite an existing Hindi AI draft to strip tells, preserving meaning.
- **Audit (ऑडिट करना):** score a Hindi draft, surface the top offending tells, recommend fixes without rewriting it.

**One language, fully specialized:**
- **Hindi (hi):** ~140-entry suspect vocabulary (Tier 1 + Tier 2), Hindi AI-construction regex bank, a Devanagari-aware word tokenizer (Python's `\w` shatters Hindi words on their matras — see below), danda-aware sentence splitting, a Hindi tricolon detector (`और` / `तथा` / `एवं`), and a dedicated **danda-vs-Latin-period** typography detector — calibrated NOT to false-fire on clean native prose.

**Four content-types** (each with its own adapter): marketing long-form, short-comms, technical, editorial-SEO.

**Optional external integration:** live scoring via Copyleaks, GPTZero, or Originality.ai (`--external <provider>`). Lazy `httpx` import, so the analyzer works fully offline.

## What's inside

```
human-writer-hi/
├── SKILL.md                          # Orchestration hub: routing + master checklist + anti-patterns (hi)
├── README.md                         # This file
├── INSTALL.md                        # Installation instructions
├── requirements.txt                  # pyyaml (required) + httpx (optional)
├── references/
│   ├── tells-stylistic-hi.md         # ⭐ CORE: HI suspect vocab + AI constructions + danda/em-dash typography + calques + register
│   ├── tells-statistical.md          # burstiness / TTR (language-agnostic)
│   ├── tells-structural.md           # bullets / headers / tricolons / emoji
│   ├── humanization-techniques.md    # the ten humanization moves (Hindi worked examples)
│   ├── adapter-marketing.md          # marketing long-form adapter
│   ├── adapter-short-comms.md        # short-form comms adapter
│   ├── adapter-technical.md          # technical-docs adapter (prose-only contract)
│   ├── adapter-editorial-seo.md      # editorial-SEO adapter
│   ├── external-detectors.md         # Copyleaks / GPTZero / Originality.ai integration notes
│   └── checklists.md                 # pre-publish checklists + Hindi quick-triage
└── scripts/
    ├── rules.yaml                    # ⭐ hi: vocab + constructions + thresholds (incl. latin_period_in_devanagari_max)
    └── analyze.py                    # ⭐ hi-adapted: danda splitting + WORD_RX tokenizer + tricolon (और|तथा|एवं) + detect_latin_period_in_devanagari
```

## Installation

See `INSTALL.md`. TL;DR for macOS/Linux:

```bash
mkdir -p ~/.claude/skills
unzip human-writer-hi.zip -d ~/.claude/skills/
pip install --user -r ~/.claude/skills/human-writer-hi/requirements.txt
```

## How to invoke

Once installed, the skill auto-activates on Hindi prose requests. Example prompts:

- "वाइन फ़्यूचर्स की प्राइसिंग पर 600 शब्दों का एक लेख लिखो, जो इंसान जैसा लगे, एआई जैसा नहीं"
- "इस एआई ड्राफ़्ट को साफ़ करो ताकि इसका कॉपीलीक्स स्कोर 25 से नीचे आए"
- "इस हिंदी ईमेल को भेजने से पहले एआई टेल्स के लिए ऑडिट करो"
- "इस टेक्स्ट को मानवीय बनाओ, यह बहुत ChatGPT जैसा लगता है"
- "Make this Hindi landing-page copy read human, not AI"

If auto-activation misses, force it: "Use the `human-writer-hi` skill to..."

## The analyzer

`scripts/analyze.py` is a deterministic scorer that runs offline. It loads `scripts/rules.yaml` (Hindi vocab lists, regex patterns, thresholds) and emits a 0-100 score plus a list of flagged tells.

```bash
# Audit mode (default, JSON output for tooling)
python3 scripts/analyze.py --input draft.md --lang hi --type marketing

# Human-readable report
python3 scripts/analyze.py --input draft.md --lang hi --type editorial-seo --format human

# Pipe via stdin
cat draft.md | python3 scripts/analyze.py --lang hi --type technical --format human
```

Required flags: `--lang hi`, `--type` (`marketing` / `short-comms` / `technical` / `editorial-seo`). `--input` is optional; stdin otherwise.

**Score bands** (4-band YAML, canonical):
- `0-24` **LOW_RISK:** ship it.
- `25-49` **MEDIUM_RISK:** apply the top 3 recommendations, re-score.
- `50-74` **HIGH_RISK:** in WRITE mode restart; in CLEAN mode apply a stronger rewrite.
- `75-100` **CRITICAL:** major rewrite.

**Detectors implemented:** em-dash density (foreign to Devanagari, stricter threshold), sentence-length stdev (burstiness, danda-aware), TTR (lexical diversity, Devanagari-tokenized), Hindi suspect-vocabulary, Hindi AI-construction regex bank, Hindi tricolon (`और` / `तथा` / `एवं`), bullet parallelism, header pyramid, and the Hindi-only **danda-vs-Latin-period** detector (low-weight, register-calibrated).

**Devanagari word counting (the critical Hindi fix).** Python's default `\w` matches Devanagari *base* letters but NOT the combining vowel signs (matras like े ो ं ़), so a naive `\b\w+\b` shatters a single Hindi word ("तेज़" → "त", "ज") and inflates word counts ~2–3×. This analyzer uses a Devanagari-aware tokenizer (`WORD_RX`) that treats a Devanagari run as one word (excluding the danda) and falls back to `\w+` for Latin/digit tokens, so word counts, TTR, tricolons, and vocabulary boundaries are all correct on Hindi.

**Prose-only scoring.** The analyzer strips fenced code blocks, markdown data tables, and opt-in ignore regions before scoring. Wrap any intentionally AI-flavored citation so it doesn't count against you:

```
<!-- human-writer:ignore-start (बुरे उदाहरण का उद्धरण) -->
आज के युग में, यह ध्यान देने योग्य है कि निर्बाध और मजबूत समाधान…
<!-- human-writer:ignore-end -->
```

## What's NOT inside

- **English / French content:** use `human-writer-en` / `human-writer-fr`. Other locales: `human-writer-es` / `-pt` / `-de` / `-ar`.
- **Document structure** (which sections, which schemas, which headings): use a dedicated structure/content tool. This skill is the stylistic filter applied on top of whatever produces the structure.
- **Technical SEO audit of a web project:** use a dedicated SEO tool. This skill handles content style only.

This skill is a stylistic filter invoked on top of structure-producing tools, never as a replacement.

## Part of the mr-bridge.com toolkit

This skill is part of the [mr-bridge.com](https://mr-bridge.com) toolkit for scraping, data, and content automation. Related resources:

- [mr-bridge.com](https://mr-bridge.com) — home
- [Scrapers](https://mr-bridge.com/scrapers) — the Apify Actor portfolio
- [MCP servers](https://mr-bridge.com/mcp-servers) — Model Context Protocol servers
- [AI workflows](https://mr-bridge.com/ai-workflows) — agents and automation
- [Studies](https://mr-bridge.com/studies) — data studies and one-pagers
- [Articles](https://mr-bridge.com/articles) — write-ups and guides
- [Solutions](https://mr-bridge.com/solutions) — end-to-end solutions

## License

Personal use. Customize freely. No warranty. The external-detector endpoints in `analyze.py` are copied verbatim from the master skill (language-agnostic POSTs) and carry `# (verify)` markers; they were not re-verified for Hindi specifically.
