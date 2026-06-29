# Pre-Publish Checklists (human-writer-hi)

> Ready-to-paste self-review checklists, one per content-type, for Hindi prose. Run `analyze.py --lang hi` first, then walk through the relevant checklist before delivery. Each checklist is short, actionable, and covers the tells most likely to trigger AI detectors for that specific format. The Hindi quick-triage at the end is the Hindi-specific addition. Doctrine is written in English; the Hindi phrases are the surface to look for.

---

## Marketing Long-Form

Before publishing blogs, READMEs, landing pages, or long-form newsletters in Hindi, confirm:

- [ ] Analyzer score ≤ 24 with `--lang hi --type marketing`
- [ ] First 100 words contain zero Tier-1 suspect vocabulary
<!-- human-writer:ignore-start (checklist quotes the tells to look for) -->
- [ ] First paragraph does not open with "आज के युग में", "डिजिटल युग में", "यह ध्यान देने योग्य है", or "चाहे आप X हों या Y"
- [ ] Closing paragraph does not start with "अंत में", "निष्कर्ष में", "अंततः", or "संक्षेप में"
<!-- human-writer:ignore-end -->
- [ ] Em-dash "—" count is 0 (foreign to Devanagari; stricter than other languages — run `analyze.py`)
- [ ] Every Devanagari sentence ends with a danda "।", not a Latin "."
- [ ] At least one specific number, named entity, or first-person opinion per ~300 words
- [ ] Bulleted lists vary opening AND closing words (≤ 80% share the first/last word — watch the "…है" ending)
- [ ] No H2 has exactly 3 H3 children (if 2+ H2s exist, vary H3 counts)
<!-- human-writer:ignore-start (checklist quotes the tells to look for) -->
- [ ] No "मुख्य बिंदु" / "आप क्या सीखेंगे" / "टॉप X" standalone block
<!-- human-writer:ignore-end -->
- [ ] No emoji as section header
- [ ] Register is consistent: not over-Sanskritized (तथा/एवं/अतः everywhere) for a casual audience

If any item fails: fix before delivery. If analyzer score is 25–49 after fixes, apply the top 3 recommendations and re-score. If 50+, reconsider your angle.

---

## Short-Form Communications

Before sending emails, LinkedIn posts, or customer replies in Hindi, confirm:

- [ ] Analyzer score ≤ 24 with `--lang hi --type short-comms`
<!-- human-writer:ignore-start (checklist quotes the tells to look for) -->
- [ ] No "आशा है यह संदेश आपको स्वस्थ पाएगा" opening
- [ ] No "आपके उत्तर की प्रतीक्षा में" / "सादर" boilerplate closing
- [ ] No "मैं आपसे संपर्क कर रहा हूँ ताकि", "किसी भी प्रश्न के लिए संकोच न करें"
<!-- human-writer:ignore-end -->
- [ ] Em-dashes "—": 0 (always — foreign to Devanagari)
- [ ] At least one contraction-of-register, sentence fragment, or first-person verb in replies over 30 words
- [ ] Signoff is first name, short phrase, or nothing, not corporate boilerplate ("सादर" on every email)
- [ ] First line is not "मैं आपको लिख रहा हूँ" / "इस ईमेल का उद्देश्य"

If any item fails: revise before sending. (Note: in casual chat/messaging register, ending a sentence with a Latin "." is acceptable; the analyzer's `latin_period_in_devanagari_max` is to be read loosely under `--type short-comms`.)

---

## Technical Documentation

Before publishing internal READMEs, RFCs, or technical journals in Hindi, confirm:

- [ ] Analyzer score ≤ 24 with `--lang hi --type technical`
<!-- human-writer:ignore-start (checklist quotes the tells to look for) -->
- [ ] First sentence states the WHY (problem this doc solves), not "इस दस्तावेज़ में, हम जानेंगे..."
- [ ] No "तो चलिए शुरू करते हैं!" / "बिना किसी देरी के" filler
- [ ] No "निष्कर्ष" section (unless >500 words and earns a summary)
- [ ] Every instance of "मजबूत", "स्केलेबल", "क्षमता को अनलॉक करें", "सुरुचिपूर्ण", "शक्तिशाली" passes the "replace with 'अच्छा'" test
<!-- human-writer:ignore-end -->
- [ ] Code blocks are not surrounded by paragraphs that re-explain them line-by-line
- [ ] One sentence per concept: no restating or hedging the same idea twice
<!-- human-writer:ignore-start (checklist quotes the tells to look for) -->
- [ ] Zero hedging openers ("यह ध्यान देने योग्य है", "गौरतलब है कि", "ध्यान देने वाली बात")
<!-- human-writer:ignore-end -->
- [ ] Every Devanagari sentence ends in a danda "।" (code/CLI tokens excepted)

If any item fails: revise. Technical docs should be direct and economical.

---

## Editorial-SEO Articles

Before publishing ranking-optimized articles in Hindi, confirm:

- [ ] Analyzer score ≤ 24 with `--lang hi --type editorial-seo`
- [ ] Target keyword appears in: title, first 100 words, and ≥1 H2
- [ ] First 100 words contain a specific data point or opinion (not just the keyword)
- [ ] H2 hierarchy is varied, not pyramid (not 3 H3s per H2 uniformly)
- [ ] At least 1 internal link with natural anchor text (not "यहाँ क्लिक करें")
<!-- human-writer:ignore-start (checklist quotes the tells to look for) -->
- [ ] No "आज के युग में," / "डिजिटल युग में," opener
- [ ] No "निष्कर्ष" that just restates the intro / tl;dr
<!-- human-writer:ignore-end -->
- [ ] At least one opinion that someone could reasonably disagree with
<!-- human-writer:ignore-start (checklist quotes the tells to look for) -->
- [ ] No "संपूर्ण गाइड", "वह सब जो आपको जानना चाहिए", "अंतिम गाइड" UNLESS your keyword data demands it
<!-- human-writer:ignore-end -->
- [ ] Sentence-length standard deviation ≥ 8 (mix short and long)
- [ ] Every Devanagari sentence ends in a danda "।"; digit set (Latin vs Devanagari) is consistent

If any item fails: fix before publishing.

---

## Universal Baseline

Apply to **all** content types before delivery:

- [ ] Final `analyze.py --lang hi` run; score ≤ 24
- [ ] No Tier-1 suspect vocabulary in the first 100 words (check `rules.yaml` for the list)
- [ ] Every Devanagari sentence ends in a danda "।" (keep "?"/"!" for genuine questions/exclamations; "." excepted in casual messaging register)
- [ ] Zero em-dashes "—" (foreign to Devanagari)
- [ ] At least one specific element: number, name, date, fact, quote, not generic claims
- [ ] At least one stylistic asymmetry: a short sentence after long ones, a varied list length, unexpected structure
- [ ] Doesn't end with a summary or call-to-action that merely restates the opening

---

## Hindi quick-triage (Hindi-specific)

A 60-second eyeball pass for any Hindi draft, in priority order — the fastest path from "looks AI" to "reads human". Mirrors the order in `tells-stylistic-hi.md` § Quick triage:

1. **Danda vs Latin period.** Every Devanagari sentence should end with "।", not ".". Replace any "." (or it flags). Keep "?"/"!" for genuine questions/exclamations.
2. **Em-dashes.** Count "—" anywhere. >0 in expository prose → replace with comma/colon/danda/parentheses. "—" is foreign to Hindi (stricter than other languages).
3. **Register.** Over-Sanskritized (तथा/एवं/अतः everywhere) for a casual audience, or thin decorative Hinglish in a formal one? Match register to audience.
4. **Opener.** First sentence starts with "आज के युग में / डिजिटल युग में / यह ध्यान देने योग्य है / गौरतलब है कि"? Rewrite.
5. **Closer.** Last paragraph starts with "अंत में / अंततः / निष्कर्ष में / संक्षेप में"? Rewrite.
6. **Tier-1 vocab.** "मजबूत (robust), क्रांतिकारी, अत्याधुनिक, क्षमता को अनलॉक करें, परिवर्तनकारी, सशक्त बनाता है" — cap 1 per paragraph.
7. **Constructions.** "यह न केवल…, बल्कि…", "गहराई से जानें", "आइए जानें", "चाहे आप… हों या…".
8. **Tricolons.** Count "X, Y और/तथा/एवं Z"; cap 1 per 200 words.
9. **Calques.** "निर्बाध" (seamless), "कार्रवाई योग्य अंतर्दृष्टि" (actionable), "महत्वपूर्ण भूमिका निभाता है" (plays a role), "गेम-चेंजर".
10. **POV / consistency.** At least one first-person mark if opinion. Consistent आप/तुम and digit set throughout.

A passing piece: 0 tier-1, ≤2 tier-2, 0 constructions, ≤1 tricolon/200w, every Devanagari sentence danda-terminated, 0 em-dashes, consistent register, one first-person mark if opinion. That lands LOW_RISK (≤ 24) and survives Copyleaks/GPTZero at sub-25 % in most domains.

---

## How to Use These Checklists

1. Write or clean your draft.
2. Run `python3 scripts/analyze.py --input <draft> --lang hi --type <type> --format human` from the skill root.
3. If score > 24, apply the analyzer's top recommendations until ≤ 24.
4. Walk through the relevant checklist above (marketing, short-form, technical, or editorial-SEO) plus the Hindi quick-triage.
5. Check off each item; revise any failures.
6. Re-run the analyzer if you made major changes.
7. Deliver only when both gates pass (analyzer ≤ 24 AND checklist complete).

---

## See Also

- `tells-stylistic-hi.md`: vocabulary, constructions, calques, punctuation tells (Hindi)
- `adapter-marketing.md`: doctrine specific to long-form marketing
- `adapter-short-comms.md`: doctrine specific to short communications
- `humanization-techniques.md`: positive techniques for adding human voice (Hindi examples)
- `scripts/analyze.py`: deterministic analyzer (run before checklist)
- `external-detectors.md`: optional integration with Copyleaks, GPTZero, etc.
