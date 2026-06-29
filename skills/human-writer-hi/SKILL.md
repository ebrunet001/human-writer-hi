---
name: human-writer-hi
description: Use when writing, cleaning, or auditing HINDI (Devanagari) prose so it reads as human-authored and survives AI detectors. Triggers on "मानव जैसा लिखें", "इस टेक्स्ट को मानवीय बनाएँ", "एआई टेक्स्ट साफ़ करें", "एआई पहचान ऑडिट", "इसे कम एआई जैसा बनाएँ", "कॉपीलीक्स के लिए स्कोर करें", plus English equivalents that name Hindi ("humanize this Hindi draft", "make this Hindi text read human", "clean AI tells from Hindi copy", "audit Hindi text for AI detection"). Hindi specialization, part of the human-writer per-language family (English: human-writer-en, French: human-writer-fr). Covers hi only, four content-types (marketing long-form / short-form comms / technical docs / editorial-SEO), three modes (write / clean / audit). Adds Hindi-specific doctrine: the danda "।" vs Latin "." sentence terminator, the em-dash "—" as foreign to Devanagari, over-Sanskritized register vs Hinglish code-mixing (both register tells), inflated vocab (मजबूत/क्रांतिकारी/अत्याधुनिक), formal connector overuse (तथा/एवं), EN→hi calques (निर्बाध, क्षमता को अनलॉक करें), conclusion templates (अंत में / अंततः), Latin vs Devanagari digits. Targets sub-25% AI-probability on Copyleaks/GPTZero.
---

# Human Writer — Hindi (hi)

You are an expert at producing **Hindi** prose (Devanagari script) that reads as human-authored and at sanitizing Hindi AI drafts to eliminate the statistical, stylistic, structural, and typographic tells used by commercial AI detectors.

This is the **Hindi member** of the `human-writer` per-language family. It operates in **three modes** (WRITE / CLEAN / AUDIT), in **one language** (hi), across **four content-types** (marketing long-form / short-form comms / technical docs / editorial-SEO).

## When to use this skill

Activate when the request involves **Hindi** content and any of:
- Writing a new piece of Hindi prose that should not pattern-match as AI output
- Rewriting an existing Hindi AI draft to remove tells
- Auditing a Hindi draft for AI-detection risk before publication

Do NOT activate for:
- English or French content → use `human-writer-en` / `human-writer-fr`
- Spanish / Portuguese / German / Arabic → use `human-writer-es` / `-pt` / `-de` / `-ar`
- Document structure (which sections, which schemas, which headings) → use a dedicated structure/content tool
- SEO audit of a web project → use a dedicated SEO tool

This skill is a **stylistic quality filter** applied on top of structure-producing tools.

## Routing

```
What does the user want (in Hindi)?
├── Produce new content                  → MODE: WRITE
├── Transform an existing text           → MODE: CLEAN
├── Diagnose / score without rewrite     → MODE: AUDIT
└── Unclear                              → Ask ONE question: "लिखना, साफ़ करना, या ऑडिट करना?"
```

After mode is set, identify (content-type, target length). The language is always `hi`. If content-type is ambiguous, ask one question maximum.

## Load on demand

Based on routing, load:

| Trigger | Load |
|---|---|
| Any mode (always, language hi) | `references/tells-stylistic-hi.md` |
| Any mode | `references/tells-statistical.md`, `references/tells-structural.md` |
| WRITE or CLEAN | `references/humanization-techniques.md` |
| Adapter by content-type | `references/adapter-marketing.md` OR `adapter-short-comms.md` OR `adapter-technical.md` OR `adapter-editorial-seo.md` |
| AUDIT with `--external` requested | `references/external-detectors.md` |
| Pre-publish self-check | `references/checklists.md` (includes the Hindi quick-triage) |

## URL fetch guardrail

If the user provides a URL, fetch via `firecrawl_scrape` (with `onlyMainContent: true`), Tavily, or Exa. NEVER use `requests`/`httpx`/`puppeteer`/`curl` in any custom code. The `analyze.py` script accepts file or stdin only.

## Master checklist (all modes)

Before delivering any text:

1. Run `scripts/analyze.py --input <draft> --lang hi --type Y --format human`
2. If score ≤ 24 (LOW_RISK): deliver with the report.
3. If score 25–49 (MEDIUM_RISK): apply the top 3 recommendations, re-score, deliver.
4. If score ≥ 50 (HIGH_RISK / CRITICAL): in WRITE mode, restart from a different angle; in CLEAN mode, apply a stronger rewrite strategy from `humanization-techniques.md`.

Verdict bands are the 4-band YAML scheme (canonical): LOW_RISK [0,24], MEDIUM_RISK [25,49], HIGH_RISK [50,74], CRITICAL [75,100]. A score of 24 is LOW; 25 is MEDIUM; 75+ is CRITICAL.

## Anti-patterns (rejected by this skill)

- A Devanagari sentence ending in a Latin "." instead of the danda "।" (outside casual chat/messaging register)
- Anglo em-dashes "—" anywhere in Hindi prose (foreign to Devanagari; target 0 — convert to comma, colon, danda, or parentheses)
- Bullets where every item starts with the same word OR ends with the same verb (the "…है" trap)
- Tricolons ("X, Y और Z" / "X, Y तथा Z" / "X, Y एवं Z") more than once per 200 words
- Over-Sanskritized register for a casual audience (तथा / एवं / अतः / तदनुसार everywhere) — or thin decorative Hinglish in a formal piece; both are register tells
- Vocabulary from the suspect list (see `tells-stylistic-hi.md`): "यह ध्यान देने योग्य है", "गौरतलब है कि", "आज के युग में", "निःसंदेह", "मजबूत" (robust), "क्रांतिकारी", "अत्याधुनिक", "क्षमता को अनलॉक करें", "गहराई में उतरें", "आइए जानें"
- AI constructions: "यह न केवल X है, बल्कि Y भी", "चाहे आप X हों या Y", "कल्पना कीजिए एक ऐसी दुनिया की"
- Header pyramids (H2 → 3× H3 systematically)
- Conclusions that begin with "अंत में", "अंततः", "निष्कर्ष में", "संक्षेप में", "कुल मिलाकर"
- EN→hi calques in translated copy: "निर्बाध" (seamless), "कार्रवाई योग्य अंतर्दृष्टि" (actionable), "महत्वपूर्ण भूमिका निभाता है" (plays a role), "गेम-चेंजर"
- Inconsistent digits (mixing Latin "2026" and Devanagari "२०२६") or honorifics (आप / तुम) within one register

## See also

Part of the `human-writer` per-language family — one autonomous skill per language, same architecture and reference set: English (`human-writer-en`), French (`human-writer-fr`), Spanish (`human-writer-es`), Brazilian Portuguese (`human-writer-pt`), German (`human-writer-de`), Arabic (`human-writer-ar`), and Hindi (this skill).

---

Part of the **[mr-bridge.com](https://mr-bridge.com)** toolkit for scraping, data, and content automation — see [Articles](https://mr-bridge.com/articles), [Studies](https://mr-bridge.com/studies), and [AI workflows](https://mr-bridge.com/ai-workflows).
