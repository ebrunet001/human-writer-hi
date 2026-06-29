# Stylistic Tells — Hindi (Devanagari)

> Doctrine for the `human-writer-hi` skill, Hindi side. Same axes as the rest of the `human-writer` family (`tells-stylistic-en.md` / `tells-stylistic-fr.md`), specialized to Hindi. Doctrine is written in English; the Hindi words, phrases, and examples are the surface the analyzer matches against.

Hindi ChatGPT/Gemini output runs *louder and more Sanskritized* than its English counterpart, for three reasons:

1. **The over-Sanskritized "manak Hindi" register.** The model leans on a formal, tatsama-heavy register learned from government gazettes, Doordarshan-style news, textbooks, and Wikipedia. That register inflates everything — "यह ध्यान देने योग्य है", "निःसंदेह", "अत्याधुनिक", "क्रांतिकारी" — and reads as a press-release the moment it lands on anything concrete. Real spoken/written Hindi mixes in everyday Hindustani vocabulary and English loanwords freely; pure tatsama prose is the AI fingerprint.
2. **English formulas leak through as calques.** `in today's world` → "आज के युग में", `it is worth noting` → "यह ध्यान देने योग्य है", `dive deep` → "गहराई में उतरें", `unlock the potential` → "क्षमता को अनलॉक करें", `robust` → "मजबूत", `let's explore` → "आइए जानें". A native ear catches these instantly; the model never does.
3. **Script + punctuation tells.** Devanagari has its own sentence terminator, the **danda `।` (U+0964)**. AI plain-text output frequently terminates Hindi sentences with a Latin full stop `.` (English habit), and sprinkles the Anglo em-dash `—` (which Hindi has no native use for). Both are typographic tells, and the Latin-period one is a wired detector (`detect_latin_period_in_devanagari`).

This file codifies which words, phrases, openers, closers, and typographic choices are tells in Hindi, with severity and rewrite.

### A note on register: two opposite tells

Hindi prose can betray AI authorship at **both ends** of the register spectrum, and you must judge which applies:

- **Over-Sanskritization (the formal tell).** Default ChatGPT Hindi over-reaches for tatsama vocabulary and Sanskritized connectors (तथा, एवं, अतः, यथा, तदनुसार) where a native writer would use everyday words (और, इसलिए, तो). This is the **dominant** AI tell and what the suspect-vocabulary list mostly targets. Applies to: marketing, editorial, formal docs.
- **Hinglish code-mixing (the casual tell).** The opposite failure: AI asked for "casual Hindi" over-applies a thin layer of English loanwords ("बेसिकली", "एक्चुअली", "गाइज़", random English nouns in Latin script) in an otherwise stiff sentence, producing an uncanny register no real bilingual writer uses. Authentic Hinglish is *fluent and selective*; AI Hinglish is *decorative and uniform*. Applies to: social copy, youth-targeted marketing, chat.

The rule of thumb: **a real Hindi writer's register is internally consistent and context-appropriate.** Pure tatsama in a casual blog, or sprinkled English in a government notice, are both tells. Match the register to the audience and hold it.

---

## Suspect vocabulary (HI)

The list is calibrated against typical ChatGPT/Gemini Hindi output across marketing, editorial, and corporate copy.

**Hard rule.** Never use 2+ tier-1 items in the same paragraph. Cap any single tier-1 item at 1 per 500 words. Treat tier-1 items the way you would treat "delve" or "tapestry" in English: even one is suspicious; two is a giveaway.

**Soft rule.** Tier-2 items are legitimate in their domain. Track frequency: 3+ tier-2 items in a 300-word paragraph = the paragraph reads as AI-generated. Cap any single tier-2 item at 2 per 500 words.

**Pure-frequency rule.** Tier-3 items are individually invisible but flag the prose when 5+ co-occur in a single paragraph. The analyzer does NOT list tier-3 (false-positive risk on common Hindi words is too high for a per-word matcher); the human reviewer does.

### Tier 1 — High signal (always avoid)

These are the Hindi equivalents of English `delve`, `tapestry`, `realm`. Each line: the phrase, why it's a tell, a human alternative.

#### Connectors and meta-comments

- **"यह ध्यान देने योग्य है"** / **"यह उल्लेखनीय है"** / **"ध्यान देने वाली बात यह है कि"** — Why: meta-textual hedge ("it is worth noting"); reads as report-writing. The single most frequent HI AI topic-sentence opener of 2025-2026. Alternative: drop the prefix, state the claim. "यह ध्यान देने योग्य है कि बिक्री बढ़ी" → "बिक्री 12% बढ़ी।"
- **"गौरतलब है कि"** — Same family, journalistic flavor. Alternative: state the fact inline.
- **"यह कहना गलत नहीं होगा कि"** — Pompous double-negative hedge. Alternative: just say it.
- **"निःसंदेह"** / **"बिना किसी संदेह के"** / **"इसमें कोई संदेह नहीं"** / **"इसमें कोई दो राय नहीं"** — Why: heavy "without a doubt" assertion AI sprinkles on any claim. Alternative: drop, or back the claim with a number.
- **"निश्चित रूप से"** (as an opener) — AI's "certainly" reflex. Alternative: drop.
- **"जैसा कि हम सब जानते हैं"** / **"जैसा कि सर्वविदित है"** — Why: appeal to phantom consensus no native writer uses unless ironically. Alternative: drop.
- **"इस संदर्भ में"** / **"इस संबंध में"** / **"इस दृष्टि से"** — Why: meta-textual signpost AI uses to glue paragraphs ("in this context"). Alternative: drop; the next sentence carries the logic.
- **"इस प्रकार"** (as a paragraph connector) — Schoolbook "thus". Alternative: "तो", "इसलिए", restructure.
- **"इसके अतिरिक्त"** / **"इसके अलावा"** (overused) — Formal "moreover". Alternative: "और", "साथ ही".
- **"दूसरी ओर"** / **"वहीं दूसरी तरफ"** (as connectors) — Schoolbook "on the other hand". Alternative: "पर", restructure.

#### Spatial-temporal abstractions

- **"आज के युग में"** / **"आज के इस युग में"** / **"आज के दौर में"** / **"आज के समय में"** — Why: meta-frame opener ("in today's era") with no date, event, or actor. The canonical HI editorial cliché. Alternative: name the year, the event. "आज के युग में डेटा सब कुछ है" → "2018 के डेटा कानून के बाद…"
- **"वर्तमान समय में"** / **"वर्तमान युग में"** — Same family, bureaucratic. Alternative: a date.
- **"डिजिटल युग में"** / **"आज के डिजिटल युग में"** / **"तकनीक के इस युग में"** / **"आधुनिक युग में"** — Calque of "in the digital age". Alternative: a date, a fact.
- **"एक ऐसी दुनिया में जहाँ"** — Lyrical "in a world where" opener. Alternative: name the actual situation.
- **"इक्कीसवीं सदी में"** — Editorial cliché ("in the 21st century"). Alternative: drop.
- **"तेजी से बदलती दुनिया में"** — "in a rapidly changing world" cliché. Alternative: drop, or name what changed.

#### Metaphorical inflators

- **"क्रांतिकारी"** / **"क्रांति"** (outside literal politics) — Calque of "revolutionary". Alternative: "नया", "जो तरीका बदल दे".
- **"अभूतपूर्व"** — "unprecedented", AI's go-to amplifier. Alternative: name what's actually new.
- **"अत्याधुनिक"** / **"अत्याधुनिक तकनीक"** / **"नवीनतम तकनीक"** — Calque of "cutting-edge / state-of-the-art". Alternative: "नया", with a date.
- **"विश्वस्तरीय"** — Calque of "world-class". Alternative: cite a benchmark or number.
- **"अग्रणी"** / **"बेजोड़"** / **"अद्वितीय"** / **"अविस्मरणीय"** — Marketing inflators ("leading / unmatched / unique / unforgettable"). Alternative: name what makes it notable.
- **"मजबूत"** (non-physical, calque of "robust") — Why: "मजबूत समाधान" / "मजबूत प्लेटफ़ॉर्म" is the canonical AI rendering of "robust". Alternative: "भरोसेमंद", "ठोस", "जो टिके".
- **"सशक्त"** / **"परिवर्तनकारी"** — Calques of "empowered / empowering" and "transformative". Alternative: "मज़बूत", "जो असली फ़र्क़ लाए".
- **"गेम-चेंजर"** — English buzzword transliterated. Alternative: name the change.
- **"मील का पत्थर"** (metaphorical) — "milestone" cliché. Alternative: name the event.
- **"आधारशिला"** / **"रीढ़ की हड्डी"** (metaphorical "cornerstone / backbone") — Why: AI scatters heroic structural nouns. Alternative: name the function ("X, Y पर टिका है").
- **"महत्वपूर्ण भूमिका निभाता है"** / **"…निभाती है"** — "plays an important role" — the emptiest AI predicate. Alternative: say what it actually does.

#### Verbs and verbal phrases

- **"अनलॉक करें"** / **"क्षमता को अनलॉक करें"** — Calque of "unlock / unlock the potential". Alternative: "इस्तेमाल करें", "काम में लाएँ".
- **"सशक्त बनाता है"** / **"सशक्त बनाने"** — Calque of "empowers". Outside genuine social/HR contexts, empty. Alternative: "के लिए ज़रिया देता है", "करने देता है".
- **"गहराई से जानें"** / **"गहराई में उतरें"** — AI's "dive deep / immerse" opener. Banned as an introduction. Alternative: state the subject directly.
- **"आइए जानें"** / **"आइए समझते हैं"** / **"आइए जानते हैं"** / **"आइए एक नज़र डालते हैं"** — AI's "let's explore / let's understand" pedagogical reflex. Alternative: just present the thing.
- **"खोज करें"** / **"अन्वेषण करें"** (metaphorical "explore") — Alternative: "देखें", "जाँचें".
- **"परिदृश्य"** (metaphorical "landscape/scenario") — Buzzword. Alternative: name the situation.

### Tier 2 — Medium signal (contextual)

Legitimate in domain (e.g. "अनुकूलित करें" in an SRE post is fine). Flag when 3+ co-occur in 300 words.

#### Verbs

- **"अनुकूलित करें"** / **"अनुकूलित"** / **"सुव्यवस्थित"** / **"सरल बनाना"** — "optimize / streamline / simplify". Domain-fine, AI filler otherwise. Alt: name the concrete change.
- **"सुनिश्चित करता है"** / **"सुनिश्चित करना"** — "ensures". Overused. Alt: "देता है", or state the condition.
- **"प्रदान करता है"** — "provides", bureaucratic. Alt: "देता है".
- **"बढ़ावा देता है"** / **"बढ़ावा देना"** / **"सुगम बनाता है"** / **"सुविधा प्रदान करता है"** — hedge-y "promotes / facilitates" verbs. Alt: verb of the actual mechanism.
- **"लागू करना"** / **"क्रियान्वित करना"** — "implement". Alt: "चालू करना", "अमल में लाना".
- **"उजागर करना"** / **"प्रकट करना"** — "reveal / unveil" marketing verbs. Alt: "दिखाना".
- **"रूपांतरित करना"** — "transform". Alt: "बदलना".

#### Adjectives of importance / intensity

- **"महत्वपूर्ण"** / **"अत्यंत महत्वपूर्ण"** / **"आवश्यक"** / **"अनिवार्य"** / **"अपरिहार्य"** — all inflators ("important / essential / indispensable"). AI sprays them. Alt: drop, or quantify.
- **"उल्लेखनीय"** / **"उत्कृष्ट"** / **"असाधारण"** / **"अविश्वसनीय"** / **"शानदार"** / **"बेहतरीन"** / **"प्रभावशाली"** / **"अद्भुत"** — AI's intensifier toolkit ("notable / excellent / extraordinary / incredible"). Alt: name the specific quality.
- **"नवीन"** / **"नवाचार"** — "novel / innovation", empty self-praise. Alt: "नया", and show why.
- **"शक्तिशाली"** (marketing "powerful") — Alt: a benchmark or number.
- **"सहज"** / **"उपयोगकर्ता-अनुकूल"** / **"सुरुचिपूर्ण"** — product-copy cliché ("seamless/intuitive / user-friendly / elegant"). Alt: name the design choice.

#### Abstract nouns

- **"तालमेल"** — "synergy" buzzword. Alt: name the relationship.
- **"पारिस्थितिकी तंत्र"** (metaphorical "ecosystem") — Calque. Alt: "बाज़ार", "नेटवर्क", "समुदाय".
- **"ब्रह्मांड"** (metaphorical "universe") / **"दुनिया"** (metaphorical "the world of X") — Alt: "क्षेत्र", "का संसार" → "का क्षेत्र", or drop.
- **"यात्रा"** (metaphorical "journey") — UX/tourism cliché. Alt: name the steps.
- **"समाधान"** (vague "our solution") — Alt: the actual thing: "पैनल", "क्रॉन जॉब", "CSV एक्सपोर्ट".
- **"अनुभव"** (vague "an unforgettable experience") — Alt: name what the user actually does.
- **"संभावनाओं की दुनिया"** / **"विकल्पों की एक विस्तृत श्रृंखला"** — "a world of possibilities / a wide range of options". Alt: a number, "कई".
- **"असंख्य"** / **"अनेक"** / **"प्रचुरता"** — "countless / numerous / abundance". Alt: a number.
- **"दृष्टिकोण"** / **"रणनीति"** — "approach / strategy", corporate filler. Alt: name the actual plan.

#### Connectors (overuse) — the Sanskritization tell

- **"तथा"** / **"एवं"** — Why: the formal/Sanskritized "and". A native writer mostly uses **"और"**; AI over-reaches for तथा/एवं in *every* list. Heavy density of तथा/एवं is itself a register tell. Alt: "और".
- **"अतः"** / **"इसलिए"** / **"परिणामस्वरूप"** / **"फलस्वरूप"** / **"तदनुसार"** — formal "therefore / consequently / accordingly". Alt: "तो", "इसलिए" (sparingly).
- **"हालांकि"** / **"तथापि"** / **"किंतु"** / **"परंतु"** (every paragraph) — "however / but" in heavy register. Alt: "पर", "लेकिन", restructure.
- **"वस्तुतः"** / **"दरअसल"** (as filler "in fact / actually") — Alt: drop.

#### Conclusion / summary openers

- **"अंत में"** / **"निष्कर्ष में"** / **"निष्कर्षतः"** / **"संक्षेप में"** / **"सारांश में"** / **"कुल मिलाकर"** / **"अंततः"** / **"समापन में"** — Conclusion templates ("in the end / in conclusion / in summary / ultimately"). **"अंत में" and "अंततः" are the strongest HI closing tells.** Cap all at 0 as paragraph openers.

### Tier 3 — Low signal (frequency-only)

Individually fine. Flag a paragraph if 5+ co-occur. (The analyzer does not list these; the reviewer does.)

प्रक्रिया, पहलू, घटक, तत्व, आयाम, क्षेत्र, ढांचा, दायरा, परिप्रेक्ष्य, संभावना, अवसर, चुनौती, लक्ष्य, उद्देश्य, प्रभाव, परिणाम, क्षमता, दक्षता, उत्पादकता, गुणवत्ता, पारदर्शिता, जवाबदेही, स्थिरता, सततता, मापनीयता, लचीलापन, अनुकूलन, एकीकरण, स्वचालन, मॉड्यूलरता, अंतरसंचालनीयता, मूल्यवर्धन, लाभ, सुविधा, संसाधन, गतिशीलता, संरेखण, सुसंगतता.

**Why low signal**: each appears naturally in honest Hindi B2B prose. **Why they still matter**: a paragraph with 5+ of them is corporate AI सरकारी-Hindi.

### Replacements (consolidated)

| Tell | Human alternative |
|---|---|
| यह ध्यान देने योग्य है / गौरतलब है कि | drop and state the claim |
| निःसंदेह / इसमें कोई संदेह नहीं | drop, or back with a number |
| आज के युग में / आज के दौर में | आज / [date] से / यहाँ |
| डिजिटल युग में | आज / [concrete date] से |
| एक ऐसी दुनिया में जहाँ | name the actual situation |
| गहराई से जानें / गहराई में उतरें | देखें / जाँचें / यहाँ है |
| आइए जानें / आइए समझते हैं | just present the thing |
| क्षमता को अनलॉक करें | इस्तेमाल करें / काम में लाएँ |
| मजबूत (non-physical) | भरोसेमंद / ठोस / जो टिके |
| परिवर्तनकारी / क्रांतिकारी | अहम / जो तरीका बदल दे |
| अत्याधुनिक / नवीनतम तकनीक | नया / अभी का (with a date) |
| विश्वस्तरीय | cite a benchmark or number |
| महत्वपूर्ण भूमिका निभाता है | say what it actually does |
| आधारशिला / रीढ़ की हड्डी | name the function literally |
| पारिस्थितिकी तंत्र | बाज़ार / नेटवर्क / समुदाय |
| ब्रह्मांड / दुनिया (metaphorical) | क्षेत्र / का संसार |
| संभावनाओं की दुनिया / असंख्य | a number / कई |
| तथा / एवं | और |
| अतः / परिणामस्वरूप | तो / इसलिए |
| हालांकि / तथापि / किंतु | पर / लेकिन |
| अंत में / अंततः | end on a concrete action, number, or sharp opinion |

---

## AI constructions (HI)

Patterns the analyzer matches via regex. Severity drives scoring.

### High severity

#### "यह न केवल X है, बल्कि Y भी" / "न केवल X बल्कि Y भी"

Calque of "It's not just X, it's Y". Never use. Replace with a concrete claim.

- Avoid: "यह न केवल एक प्राइसिंग टूल है, बल्कि एक रणनीतिक संपत्ति भी है।"
- Prefer: "टूल हर रेफ़रेंस का मार्जिन दिखाता है — वही नंबर जो खरीदार देखते हैं।"

#### "गहराई से जानें…" / "गहराई में उतरें…" / "आइए जानें…"

Never use as an introduction. State the subject directly.

- Avoid: "डायनैमिक प्राइसिंग की रोचक दुनिया में गहराई से जानें।"
- Prefer: "डायनैमिक प्राइसिंग — मार्जिन की हदों से शुरू करते हैं।"

#### "आज के युग में…" / "डिजिटल युग में…" / "वर्तमान समय में…"

Never open with a temporal abstraction. Use a date, an event, or jump straight in.

- Avoid: "आज के युग में, जहाँ डेटा नया तेल है…"
- Prefer: "2018 के डेटा कानून के बाद, ग्राहक-सूची एक्सपोर्ट करना महँगा पड़ता है।"

#### "एक ऐसी दुनिया में जहाँ…" / "कल्पना कीजिए एक ऐसी दुनिया की…"

Conference-bro openers. Banned.

- Avoid: "कल्पना कीजिए एक ऐसी दुनिया की जहाँ ग्राहक खरीदने से पहले भुगतान करें।"
- Prefer: "प्री-पेमेंट पहले से मौजूद है — Wine.com 2003 से ऐसा करता है।"

#### "यह ध्यान देने योग्य है कि…" / "गौरतलब है कि…"

The strongest single-phrase HI topic-sentence tell of 2025-2026. Pattern-matched because it fronts a claim.

- Avoid: "यह ध्यान देने योग्य है कि माइग्रेशन से प्रदर्शन सुधरा।"
- Prefer: "माइग्रेशन से लेटेंसी 40% गिरी।"

#### "निःसंदेह…" / "इसमें कोई संदेह नहीं…" / "क्षमता को अनलॉक करें"

Cf. suspect vocab. Pattern-matched separately because they act as topic-sentence openers / CTAs.

### Medium severity

#### "चाहे आप X हों या Y" 

Avoid unless the branching is real. By default, pick one reader and write for them.

- Banned by default: "चाहे आप एक स्टार्टअप हों या एक बड़ी कंपनी…"
- Acceptable if real: "चाहे आप EUR में बिल करें या USD में, एक्सपोर्ट एक जैसा रहता है।"

#### "क्या आपने कभी सोचा है…" / "तो देर किस बात की…"

AI's "have you ever wondered / so what are you waiting for". Cut them; the sentence after is the actual content.

#### "आइए इसे विस्तार से समझते हैं।" / "तो चलिए शुरू करते हैं।"

Meta-sentences that perform thinking instead of doing it. Skip to the content.

#### "इस लेख में हम…" / "इस ब्लॉग में हम…"

Academic intent statement ("in this article we will…"). Drop; just start.

### Low / conclusion severity

#### Conclusion openers: "अंत में," / "निष्कर्ष में," / "संक्षेप में," / "कुल मिलाकर," / "अंततः,"

Conclusion templates. **"अंत में" and "अंततः" are the strongest HI closing tells** (the latter a direct calque of "ultimately"). Cap all at 0 as paragraph openers. End on a concrete action, a number, or a sharp opinion.

---

## Em-dash discipline — `—` is foreign to Devanagari

**Ban the em-dash "—" (U+2014). Target 0; hard cap is STRICTER than the master (≤ 0.5 per 1000 words).** Hindi has **no native em-dash**. Devanagari prose marks asides with the danda, the comma, parentheses, or (for a hard break) a new sentence. The wide "—" appears in Hindi text almost exclusively as a translation artifact or as direct machine output, so any occurrence reads as non-native on sight. This is why `em_dash_per_1000_words` is set to `0.5` for Hindi (vs `1.0` for Spanish, which has a legitimate dialogue raya — Hindi has no equivalent native use).

When cleaning or writing HI, sweep for "—" explicitly and convert **every** occurrence:

| AI overuse | Human HI |
|---|---|
| "तेज़ — कारगर — सरल।" | "तेज़, कारगर, सरल।" or "तेज़। कारगर। सरल।" |
| "यह टूल — बोदेगा के लिए बना — रोज़ चलता है।" | "यह टूल, जो बोदेगा के लिए बना है, रोज़ चलता है।" |
| "काम करता है — ज़्यादातर बार।" | "काम करता है (ज़्यादातर बार)।" |
| "सरल है — और चलता है।" | "सरल है। और चलता है।" |
| "तीन विकल्प — A, B और C — सब सही।" | "तीन विकल्प: A, B और C। सब सही।" |
| "लचीली प्राइसिंग — पे-पर-इवेंट।" | "लचीली प्राइसिंग: पे-पर-इवेंट।" |

The en-dash `–` (U+2013) in number ranges ("पृष्ठ 12–14") and the hyphen `-` in compounds ("टेक्नो-आर्थिक") are fine. Only the wide "—" misused as an emphasis/parenthetical dash is the tell.

---

## अंग्रेज़ी कैल्क़ (English calques in AI Hindi)

These English-origin patterns leak into Hindi ChatGPT output. They're stronger tells in Hindi than in English because they read as unnatural to a native ear.

### Lexical calques

- **"मजबूत"** (robust, non-physical) → "भरोसेमंद", "ठोस", "टिकाऊ"
- **"सहज" / "निर्बाध"** (seamless) → "बिना रुकावट", "सीधे", "बिना झंझट". "निर्बाध एकीकरण" is the canonical AI rendering of "seamless integration" — a heavy tell.
- **"परिवर्तनकारी"** (transformative) → "अहम", "निर्णायक"
- **"स्केलेबल"** (scalable, transliterated in marketing) → state the capacity number
- **"क्षमता को अनलॉक करें"** (unlock the potential) → "इस्तेमाल करें", "काम में लाएँ"
- **"महत्वपूर्ण भूमिका निभाता है"** (plays an important role) → say what it actually does
- **"के संदर्भ में"** (in the context of, calque of "in terms of") → "के मामले में", restructure
- **"अंत में" / "दिन के अंत में"** (at the end of the day, calque) → "आख़िरकार" (sparingly), or just the conclusion
- **"यह सुनिश्चित करना कि"** (to ensure that) → "ताकि", "इसलिए कि"

### Calques of translation (EN→HI)

When **translating** EN source into HI (not writing fresh), domain terms get rendered word-for-word into Hindi strings that pass every "fluency" check yet read as machine output to a native professional.

| EN source | Calque (avoid) | Idiomatic HI | Note |
|---|---|---|---|
| seamless integration | "निर्बाध एकीकरण" | **"सीधा जुड़ाव" / "बिना झंझट जुड़ जाता है"** | "निर्बाध" is the AI fingerprint for "seamless" |
| actionable insights | "कार्रवाई योग्य अंतर्दृष्टि" | **"काम की जानकारी" / "जो आँकड़े आप इस्तेमाल कर सकें"** | nobody says "कार्रवाई योग्य अंतर्दृष्टि" out loud |
| robust platform | "मजबूत प्लेटफ़ॉर्म" | **"भरोसेमंद प्लेटफ़ॉर्म"** | "मजबूत" = physically strong |
| cutting-edge | "अत्याधुनिक" | **"नया" / "अभी का"** (with restraint) | acceptable but AI-overused |
| empower users | "उपयोगकर्ताओं को सशक्त बनाना" | name what they can now do | "सशक्त बनाना" is empty unless social/HR |
| game-changer | "गेम-चेंजर" | name the change | don't leave English buzzwords in body copy |

**Doctrine.** These need a native judgment call, not a blind find-replace. In translated marketing/editorial copy aimed at a Hindi professional audience, prefer the idiomatic column. The tell is strongest when the calque is the **central concept** of the piece.

### Syntactic / register calques

- **Passive overuse** — AI overuses the passive ("X किया जाता है") where Hindi prefers active voice or the subject. Prefer the active.
- **Gerund-as-title** ("अपने वर्कफ़्लो को ऑप्टिमाइज़ करना") — English progressive-title calque. HI prefers a question or noun: "वर्कफ़्लो कैसे सुधारें", "वर्कफ़्लो में सुधार".
- **Over-nominalization** — stacking tatsama abstract nouns ("कार्यान्वयन की प्रक्रिया का अनुकूलन") where a verb would do ("इसे कैसे चालू करें").

---

## Hindi typography tells (the danda detector + more)

### The danda `।` vs the Latin period `.` — the signature HI tell

The **danda `।` (U+0964)** is the correct terminator for a Hindi sentence; the **double danda `॥` (U+0965)** terminates verses/couplets. **Native Hindi prose ends sentences with a danda; AI plain-text output frequently ends a Devanagari sentence with a Latin full stop `.`** (English habit). A Devanagari sentence terminated by `.` instead of `।` is a strong typographic tell.

- AI output: "यह एक वाक्य है."  →  Latin period on a Devanagari sentence (tell)
- Native HI: "यह एक वाक्य है।"

The detector (`detect_latin_period_in_devanagari`) checks every sentence that contains at least one Devanagari character: if it terminates with a Latin `.` rather than a danda `।` (or a `?`/`!`, which Hindi does borrow for genuine questions/exclamations), it counts a miss. It is **low-weight** and **register-sensitive**: a fair amount of modern web/Hinglish/messaging Hindi legitimately uses `.`, so the detector contributes only a few points and is calibrated NOT to fire on clean danda-using prose. For casual web register use `--type short-comms` and tolerate a higher count.

**Cleanup rule.** When cleaning AI Hindi for publication, sweep every Latin `.` at the end of a Devanagari sentence and replace it with a danda `।` (keep `?`/`!` for genuine questions/exclamations).

### Latin digits vs Devanagari digits

Hindi can be written with either Latin (Arabic) digits `0-9` or Devanagari digits `०-९`. Both are common and acceptable; the tell is **inconsistency** — a document that mixes "साल 2026" in one line and "साल २०२६" in the next betrays stitched-together output. Pick one digit set for your target publication and hold it. (The analyzer counts both as word characters via WORD_RX, so word counts are unaffected either way.)

### The em-dash, en-dash, and hyphen

- **Hyphen `-`** — compound words ("टेक्नो-आर्थिक"), word-break. Fine.
- **En-dash `–`** — number ranges ("पृष्ठ 12–14"). Rare; fine.
- **Em-dash `—`** — **foreign to Devanagari** (see em-dash section). The tell.

AI conflates these. Cleanup includes replacing inappropriate "—" with "," "(" or "।".

### Matras and conjuncts must be intact

A file with broken matras, missing nukta (़), or mangled conjuncts ("कष्ट" rendered as "कषट") reads as broken Hindi on sight — usually a font/encoding failure. If you see systematic matra loss, the file was mangled — fix the encoding before publishing. (Note for tooling: Python's default `\w` does NOT match Devanagari matras, which is why this skill's analyzer uses a Devanagari-aware tokenizer — see `WORD_RX` in `analyze.py`.)

---

## Pedantic / सरकारी turns (schoolbook Hindi)

The training corpus is heavy with government documents, textbooks, and formal journalism, so the model defaults to phrases a सरकारी अधिसूचना (government notice) or a board-exam essay would use.

Banned by default:

- **"प्रस्तुत लेख में"** / **"प्रस्तुत दस्तावेज़ में"** — bureaucratic self-reference ("the present article"). Drop.
- **"उपरोक्त"** / **"निम्नलिखित"** (as prose connectors, "the aforementioned / the following") — gazette register. Restructure.
- **"यह कहना अतिशयोक्ति नहीं होगी कि"** — "it would not be an exaggeration to say". Pompous. Drop.
- **"सर्वप्रथम, संदर्भ को समझना आवश्यक है"** — meta-textual scene-setting ("first, it is necessary to understand the context"). Drop.
- **"इस प्रकार हम देखते हैं कि"** — fake academic transition ("thus we see that"). Drop.
- **"अंत में यह कहा जा सकता है कि"** — fake academic closer. Drop.

Rewrite by **stating** instead of **announcing**. Avoid: "इस प्रकार हम देखते हैं कि मार्जिन गिर रहे हैं।" Prefer: "मार्जिन गिर रहे हैं। दो साल में चार अंक।"

---

## Voice and POV tells (HI)

### Absence of first person in 800+ words

AI defaults to detached third-person or the impersonal passive ("देखा जा सकता है कि"). A native author of an opinion piece **uses first person ("मैं", "मैंने", "मुझे", or inclusive "हम") at least once per 500 words**. Cleanup rule: insert one first-person sentence per 500 words to break the impersonal register.

- Avoid (throughout): "यह देखा जा सकता है कि मार्जिन गिरते हैं। यह संभव है कि…"
- Prefer: "मैं तीन में से दस ग्राहकों के मार्जिन गिरते देख रहा हूँ। शायद…"

### Over-use of the pedagogical "हम"

The "we" of a textbook ("हम देखेंगे कि…"). AI defaults to this when asked to explain. Replace with direct address ("आप") or first-person singular.

- Avoid: "हम देखेंगे कि माइग्रेट कैसे करें।"
- Prefer: "माइग्रेट ऐसे करते हैं।" / "तीन कदम में माइग्रेट हो जाता है।"

### Honorific / register consistency (आप / तुम / तू)

A Hindi piece mixing आप (formal) with तुम (familiar) or तू (intimate) within the same register is a tell of stitched-together output. Pick one address form for your audience and hold it. (Most professional/marketing copy uses आप.)

### Prescriptive future overuse

"आप जान जाएँगे", "आप समझ पाएँगे", "आप सक्षम होंगे" — AI's prescriptive future ("you will discover / you will be able to"). Replace with present or imperative. Avoid: "आप हमारे तीन स्तंभ जानेंगे।" Prefer: "तीन स्तंभ। देखते हैं।"

---

## Tricolon rationing (HI)

Same rule as EN/FR: **cap at 1 tricolon per 200 words.** Hindi has a strong pull toward triadic lists, so a high count reads as borrowed rhythm rather than authored prose. The analyzer's `detect_tricolons` matches the "X, Y और Z" pattern, where the final conjunction is **और** (everyday) or the Sanskritized **तथा / एवं** (which are *themselves* register tells — see suspect vocab).

Vary list sizes (2, 4, 5 items). Use asyndeton ("तेज़, भरोसेमंद, साफ़" without "और"). Don't close every list with ", और Z".

- Avoid: "टूल तेज़, भरोसेमंद और सटीक है। यह पैकेज, वैरिएंट और लोकेल संभालता है। यह रोज़, हफ़्ते और माँग पर चलता है।"
- Prefer: "टूल 12 लोकेल में पैकेज और वैरिएंट संभालता है। रोज़ चलता है — या किसी ख़ास ऑडिट के लिए माँग पर।"

---

## Quick triage (for the human reviewer)

When auditing a 500-word HI piece, scan in this order:

1. **Danda vs Latin period.** For every sentence written in Devanagari, does it end with `।` (not `.`)? If `.`, replace with `।` (or it flags). Keep `?`/`!` for genuine questions/exclamations.
2. **Em-dashes.** Count "—" anywhere. >0 in expository prose → replace with comma/colon/danda/parentheses. `—` is foreign to Hindi (stricter than Spanish).
3. **Register.** Is it over-Sanskritized (तथा/एवं/अतः everywhere) for a casual audience, or thin decorative Hinglish in a formal one? Match register to audience.
4. **Opener.** First sentence starts with a temporal abstraction ("आज के युग में", "डिजिटल युग में") or a meta-frame ("यह ध्यान देने योग्य है", "गौरतलब है कि")? Rewrite.
5. **Closer.** Last paragraph starts with a conclusion template ("अंत में", "अंततः", "निष्कर्ष में", "संक्षेप में")? Rewrite.
6. **Tier-1 vocab.** "मजबूत (robust), क्रांतिकारी, अत्याधुनिक, क्षमता को अनलॉक करें, परिवर्तनकारी, सशक्त बनाता है" — cap 1 per paragraph.
7. **Constructions.** "यह न केवल…, बल्कि…", "गहराई से जानें", "आइए जानें", "चाहे आप… हों या…".
8. **Tricolons.** Count "X, Y और/तथा/एवं Z"; cap 1 per 200 words.
9. **Calques.** "निर्बाध" (seamless), "कार्रवाई योग्य अंतर्दृष्टि" (actionable), "महत्वपूर्ण भूमिका निभाता है" (plays a role), "गेम-चेंजर".
10. **POV.** At least one first-person mark if it's opinion. Consistent आप/तुम and digit set throughout.

A passing HI piece, by this skill's bar:

- 0 em-dashes per 500 words.
- 0 tier-1 vocab items, ≤ 2 tier-2.
- 0 AI constructions.
- ≤ 1 tricolon per 200 words.
- Every Devanagari sentence ends in a danda `।`.
- Consistent register (not over-Sanskritized, not decorative Hinglish).
- At least one first-person mark if opinion.

That piece will score LOW_RISK (≤ 24) on the deterministic analyzer and survive Copyleaks / GPTZero at sub-25 % AI probability in most domains.

---

## See also

- `tells-statistical.md` — burstiness, TTR, comma density doctrine (language-agnostic)
- `tells-structural.md` — bullets, headers, tricolons, emoji
- `humanization-techniques.md` — how to write with intentional asymmetry, with Hindi worked examples
- `scripts/analyze.py` — `detect_suspect_vocab`, `detect_ai_constructions`, `detect_tricolons`, `detect_latin_period_in_devanagari`, the Devanagari-aware `WORD_RX` tokenizer
- `scripts/rules.yaml` — HI thresholds, suspect vocabulary, content-type weights
- the `human-writer` per-language family — EN + FR members carry the equivalent doctrine for their languages
