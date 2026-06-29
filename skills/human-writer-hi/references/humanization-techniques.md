# Humanization Techniques

> Doctrine for the `human-writer-hi` skill. The ten moves that turn AI-shaped prose into human-shaped prose. Apply in WRITE mode while drafting; apply in CLEAN mode as a targeted checklist. The worked examples are written in Hindi (some EN examples kept for cross-reference). Doctrine is written in English; the Hindi examples are the surface.

The techniques are ordered by impact-per-edit. If you can only apply one, apply #1. If you can apply two, add #5. If you have time for everything, the full ten will cut analyzer score by 30–50 points on a typical AI draft.

Each technique below answers the same four questions:

1. **Definition.** What is it?
2. **Why it works.** Which statistical / stylistic signal does it disrupt?
3. **Worked examples.** Before and after, in EN plus HI where applicable.
4. **How to apply.** Proactive in WRITE mode, targeted in CLEAN mode.

> Hindi note: every Hindi sentence below terminates with a danda `।` (not a Latin `.`), per the typography doctrine. The analyzer flags Latin periods on Devanagari sentences.

---

## 1. Vary sentence length deliberately

**Definition.** Alternate short (≤ 6 words) and long (≥ 25 words) sentences. Aim for a standard deviation of sentence lengths ≥ 8.

**Why it works.** AI prose averages 18–22 words per sentence with a low standard deviation (typically 3–5). The analyzer measures this via `sentence_length_stdev` and flags anything under ~8. Variance is the cheapest, highest-signal humanization edit available.

### Rhythm patterns to build in

| Pattern | Shape | Use case |
|---|---|---|
| **Short-short-long** | 5w + 4w + 28w | Set up a claim, then expand |
| **Long-short** | 30w + 4w | Build then punch (very human) |
| **Fragment-long** | 2w + 25w | Topic + dump |
| **Short-medium-fragment** | 6w + 15w + 3w | Cadence variation |
| **Run-on with semicolon** | 35w with `;` | One thought, two beats |

Use periods/dandas to reset hard. Use commas to slow without breaking. Explicit fragments ("बस इतना।", "और हो गया।", "बात ख़त्म।") are the strongest rhythm breakers.

### Worked example (EN)

Bad (uniform; lengths 13, 13, 11, 12; stdev ~1):

<!-- human-writer:ignore-start (before-example, deliberately AI) -->
> The pricing tool exports a CSV file with margin tiers per SKU. It updates daily based on competitor data scraped from major marketplaces. Users can filter by category, region, or supplier. The dashboard shows historical price evolution over the past 90 days.
<!-- human-writer:ignore-end -->

Good (varied; lengths 2, 8, 25, 18, 5, 8; stdev ~9):

> CSV out. One row per SKU, one column per marker. The pricing tool updates the file every night, pulling competitor data from Amazon, eBay, and three regional marketplaces I won't name in public. Filter it in Excel — category, region, supplier — and you get the same view our procurement team uses. Ninety days of history. That's usually enough to spot a competitor stockout.

### Worked example (HI)

Bad (uniform; lengths ~13, 12, 14, 11; stdev ~1.2):

<!-- human-writer:ignore-start (before-example, deliberately AI) -->
> हमारा विश्लेषण टूल कैटलॉग की हर रेफ़रेंस के लिए एक CSV फ़ाइल निर्यात करता है। यह प्रतिस्पर्धी डेटा के आधार पर हर रात अपडेट होता है। उपयोगकर्ता श्रेणी, क्षेत्र या आपूर्तिकर्ता के अनुसार फ़िल्टर कर सकते हैं। डैशबोर्ड 90 दिनों की क़ीमत का इतिहास दिखाता है।
<!-- human-writer:ignore-end -->

Good (lengths 3, 12, 28, 5, 18; stdev ~10):

> CSV बाहर। हर रेफ़रेंस के लिए एक पंक्ति, हर मार्कर के लिए एक कॉलम। टूल हर रात चलता है और Amazon, eBay तथा तीन क्षेत्रीय मार्केटप्लेस से दाम उठाता है, जिनके नाम मैं यहाँ नहीं लिखूँगा। Excel में फ़िल्टर करो और हो गया। नब्बे दिन का इतिहास, जो 2025 में देखी गई लगभग हर स्टॉक-आउट को पकड़ लेता है।

### Worked example (HI) (second pattern)

Bad:

<!-- human-writer:ignore-start (before-example, deliberately AI) -->
> स्क्रेपर स्रोत साइट से डेटा प्राप्त करता है। यह कॉन्फ़िगर किए गए नियमों के अनुसार उसे साफ़ करता है। यह उसे एक PostgreSQL डेटाबेस में सहेजता है। यह उसे एक REST API के माध्यम से उपलब्ध कराता है।
<!-- human-writer:ignore-end -->

Good:

> स्क्रेपर पूरा पन्ना निगलता है, हमारे घरेलू नियमों से साफ़ करता है (जो टारगेट के हर रीडिज़ाइन में टूट जाते हैं) और Postgres में ठेल देता है। तीन कॉलम। बस। बाक़ी सब REST API निकालती है — और आउटपुट JSON में रखते हैं क्योंकि फ़्रंटएंड को बस यही चाहिए।

### How to apply

**WRITE mode (proactive).** As you draft, force yourself to drop a one- or two-word sentence after every long one. If you've written three sentences of similar length, the next one *must* be a fragment or a 30+ word run-on.

**CLEAN mode (targeted edit).** Run `analyze.py` and look at `sentence_length_stdev`. If under 8, identify the three longest paragraphs and rewrite them by:
1. Splitting one mid-length sentence into a fragment + a sentence.
2. Joining two short sentences into one long, comma-spliced or semicolon-linked sentence.
3. Adding one explicit fragment ("बस।", "और हो गया।", "बात ख़त्म।").

---

## 2. Inject one opinion or specific anecdote per ~300 words

**Definition.** Every 300 words or so, insert one of: a first-person take, a named entity, a specific number, or a small concrete story.

**Why it works.** AI prose is information-dense but opinion-empty and entity-light. LLMs default to generic claims because generic claims minimize the chance of being wrong. Specific entities ("Rioja 2018", "47 req/s", "सोमवार की सुबह की तैयारी") are statistically rare in AI output; they're high-signal markers of authored prose because they couldn't be generated without first-hand context.

### What counts as an "opinion"

A take that someone could disagree with. Not "X, Y के लिए अच्छा है"; that's a fact-claim. But "मैं 100 SKU से नीचे किसी भी चीज़ के लिए X छोड़ दूँगा क्योंकि ROI नहीं बनता" is an opinion: opinionated, specific, defensible.

| Not an opinion | Opinion |
|---|---|
| "प्रदर्शन मायने रखता है" | "1k QPS से नीचे प्रदर्शन ही एकमात्र चीज़ है जो मायने रखती है; बाक़ी समय की बर्बादी है।" |
| "सही टूल चुनें" | "स्थिर पन्नों के लिए Playwright मत इस्तेमाल करो। Cheerio तेज़ है और रखरखाव कम।" |
| "प्राइसिंग ज़रूरी है" | "ज़्यादातर प्राइसिंग रणनीतियाँ इसलिए फेल होती हैं क्योंकि उन्हें तय करने वाली टीम कभी कोट करने वाले से बात नहीं करती।" |

### What counts as "specific"

A named entity (person, place, product, version), a date, a number with units, or a concrete event. Not "एक बड़ा मार्केटप्लेस"; कहो Amazon। Not "हाल ही में"; कहो "मार्च 2024"। Not "उपयोगकर्ता"; कहो "वह ऑन-कॉल इंजीनियर जिसे रात 3 बजे पेज आया"।

### How to inject without breaking flow

Three placements work:

1. **Mid-paragraph aside.** "यह एक्टर (हमने 2 GB इंस्टेंस पर 47 req/s नापा) पैकेज संभालता है…"
2. **End-of-paragraph kicker.** "…और बस। सच कहूँ तो यहीं ज़्यादातर लोग रुक जाते हैं — और यहीं हम शुरू करते हैं।"
3. **New sentence between two claims.** "प्राइसिंग टूल को रेट लिमिट चाहिए। वैसे, अपस्ट्रीम API आपको 60/मिनट पर रोक देता है। तो आप उसी के हिसाब से डिज़ाइन करते हो।"

### Bad vs good (HI)

Bad (अस्पष्ट कथन):

<!-- human-writer:ignore-start (before-example, deliberately AI) -->
> बड़े पैमाने पर स्क्रेपिंग के लिए सावधानी से चुने गए टूल चाहिए। सही फ़्रेमवर्क चुनना प्रदर्शन में महत्वपूर्ण अंतर ला सकता है।
<!-- human-writer:ignore-end -->

Good (ठोस राय):

> बड़े पैमाने की स्क्रेपिंग एक फ़ैसले पर टिकती है: Cloudflare का बॉट-चेक मान लो या उससे लड़ो? एक स्टेल्थ ब्राउज़र लड़ता है (~$0.30/1k पन्ने रेज़िडेंशियल पर)। सादा Crawlee + undici मान लेता है (~$0.05/1k, पर दूसरे महीने ब्लॉक हो जाते हो)। कड़े टारगेट के लिए लड़ो; आसान टारगेट के लिए मान लो।

### How to apply

**WRITE mode.** Before writing, list 3 specific facts/anecdotes/opinions you can drop into the piece. Place one every ~300 words.

**CLEAN mode.** Search the draft for paragraphs that contain zero proper nouns, zero numbers, and zero first-person markers. Each such paragraph needs one injection.

---

## 3. Use asymmetric bullets

**Definition.** In any bulleted list, deliberately vary the length, structure, opening word, and grammatical shape of each item.

**Why it works.** AI bullets are parallel by default: same verb, same length (8–12 words each), same shape. The analyzer flags this when > 80% of bullets share the same first or last word. Asymmetry breaks the fingerprint. (In Hindi, watch the *last* word too — the verb "है/हैं" glued to every line is a parallelism tell.)

### Three asymmetry axes

| Axis | Bad (symmetric) | Good (asymmetric) |
|---|---|---|
| **Length** | All 6–8 words | Mix of 2-word fragments and 25-word callouts |
| **Opener** | All start with a verb | Mix verbs, nouns, questions, fragments |
| **Shape** | All `object + verb` | Mix commands, observations, questions, mini-paragraphs |

### Worked example (HI)

Bad (लंबाई और क्रिया में सममित):

```
- प्रोडक्ट पेज स्क्रेप करें
- क़ीमत डेटा निकालें
- नतीजे डेटासेट में सहेजें
- CSV में निर्यात करें
```

Good (असममित):

```
- प्रोडक्ट पेज स्क्रेप करें (स्थिर के लिए Cheerio, जो अड़े उसके लिए एक हेडलेस ब्राउज़र — देखें `selectors.ts`)
- क़ीमत: सूची, ऑफ़र और "आप बचाते हैं" अलग-अलग पकड़ते हैं क्योंकि Amazon अपने हिसाब से राउंड करता है
- डेटासेट → CSV: `apify run --output-csv`, बस
- और उसके बाद? ज़्यादातर लोग यहीं रुकते हैं। हम इसे ट्रेंड-व्यू के लिए Metabase से जोड़ देते हैं।
```

What changed: bullet 1 has a parenthetical with a code path; bullet 2 opens with a noun and a colon callout; bullet 3 is one short clause with an arrow; bullet 4 is a rhetorical question + two sentences.

### When symmetric bullets ARE appropriate

Parallel lists where the reader compares like-with-like deserve symmetric formatting: step-by-step procedures, API reference tables, comparison matrices, pricing tiers. There, parallelism is *informational*. The rule: **prose-embedded lists should be asymmetric; reference/comparison structures can stay symmetric**.

### How to apply

**WRITE mode.** When you reach for a bullet list, draft it normally, then deliberately rewrite at least 2 of the 4 bullets to use a different shape (and a different ending word — not all "…है")।

**CLEAN mode.** Check `bullet_parallelism_ratio` from `analyze.py`. If ≥ 0.80, rewrite half the bullets so they don't share the dominant first OR last word.

---

## 4. Break tricolons: vary list sizes

**Definition.** Resist the "rule of three" reflex. Use lists of 2, 4, or 5 items. Cap the explicit three-item और-joined tricolon at 1 per 200 words. (The Sanskritized conjunctions तथा / एवं are themselves register tells — see `tells-stylistic-hi.md`.)

**Why it works.** AI prose is saturated with tricolons. Typical specimens:

<!-- human-writer:ignore-start (citation: tricolon tells quoted, not used) -->
"तेज़, भरोसेमंद और स्केलेबल", "बनाएँ, जाँचें और तैनात करें", "छोटा, मध्यम और बड़ा"।
<!-- human-writer:ignore-end -->

The cadence is comforting and tidy, which is exactly why LLMs default to it. The analyzer flags density above 1 per 200 words.

### Specific alternatives

| Reflex | Alternative | Example |
|---|---|---|
| Tricolon (3 items, "और") | **List of 2** | "तेज़ और सस्ता।" |
| Tricolon | **List of 4** | "तेज़, सस्ता, कैश्ड और ऑडिट किया हुआ।" |
| Tricolon | **List of 5 with asyndeton** | "तेज़, सस्ता, कैश्ड, ऑडिट किया हुआ, एक कमांड में तैनात।" |
| Tricolon | **List of 3 with asyndeton (no "और")** | "तेज़, भरोसेमंद, स्केलेबल।" |
| Tricolon | **Pair + parenthetical** | "तेज़ और भरोसेमंद (सस्ता भी, पर वह बोनस है)।" |

Asyndeton — dropping the final "और" — is the cheapest variation. It keeps the three-beat rhythm but loses the AI-signature `, और` connector.

### Worked example (HI)

Bad (दो वाक्यों में तीन ट्राइकोलन):

<!-- human-writer:ignore-start (before-example, deliberately AI) -->
> टूल तेज़, भरोसेमंद और सटीक है। यह पैकेज, वैरिएंट और लोकेल संभालता है। यह रोज़, हफ़्ते और माँग पर चलता है।
<!-- human-writer:ignore-end -->

Good (एक ट्राइकोलन बजट ख़र्च; सूची के आकार बदले हुए):

> टूल 12 लोकेल में पैकेज और वैरिएंट संभालता है। रोज़ चलता है, या किसी ख़ास ऑडिट के लिए माँग पर। तेज़, भरोसेमंद, सटीक: इसी क्रम में हम इसे ऑप्टिमाइज़ करते हैं।

### How to apply

**WRITE mode.** Keep a mental "tricolon budget" of 1 per 200 words. If you've already used one, force the next list into 2 or 4 items, or use asyndeton, and avoid the तथा/एवं reflex.

**CLEAN mode.** Search the draft for `, और ` / `, तथा ` / `, एवं ` followed by a word ending the clause. Count instances. If > 1 per 200 words, rewrite the lowest-impact occurrences first.

---

## 5. Cut all hedging openers

**Definition.** Delete the AI-templated qualifier phrases that front-load sentences. State the claim directly.

**Why it works.** Hedging openers are the most distinctive AI signature in long-form prose. They're space-filler with zero information value. Removing them is the highest words-saved-per-edit move available.

### Full forbidden list (HI)

<!-- human-writer:ignore-start (citation table: tells quoted, not used) -->
| Forbidden opener | Why it's a tell |
|---|---|
| "यह ध्यान देने योग्य है कि" | The #1 HI topic-sentence tell |
| "गौरतलब है कि" | Journalistic AI register |
| "यह उल्लेखनीय है कि" | Same family |
| "निःसंदेह," | Empty certainty assertion |
| "इसमें कोई संदेह नहीं कि" | Same |
| "जैसा कि हम सब जानते हैं," | Phantom consensus |
| "इस संदर्भ में," | Meta-textual signpost |
| "अंत में," (as opener) | Conclusion template |
| "अंततः," | Calque of "ultimately" |
<!-- human-writer:ignore-end -->

### Worked example (HI)

Bad:

<!-- human-writer:ignore-start (before-example, deliberately AI) -->
> यह ध्यान देने योग्य है कि एक्टर को कम से कम 1 GB मेमोरी चाहिए। गौरतलब है कि पैकेज के साथ प्रदर्शन घटता है। ध्यान देने वाली बात यह है कि स्कीमा बदल सकता है।
<!-- human-writer:ignore-end -->

Good (सीधा):

> एक्टर को कम से कम 1 GB चाहिए। पैकेज के साथ प्रदर्शन गिरता है (v2 में ठीक करेंगे)। स्कीमा बदल सकता है।

Same content. Half the words. Sounds like someone actually wrote it.

### How to apply

**WRITE mode.** Never start a sentence with a hedging opener. If you catch yourself typing "यह ध्यान देने योग्य है", delete and rewrite.

**CLEAN mode.** Grep the draft for every entry in the forbidden list. Delete each occurrence and rewrite the remaining sentence. This is the single highest-ROI CLEAN-mode operation.

---

## 6. Use idiosyncratic markers

**Definition.** Deliberately build 1–2 recurring tics per piece (a favored conjunction, a pet phrase, a quirky structural pattern) that the analyzer cannot fingerprint but that human readers attribute to authorial personality.

**Why it works.** Human writers have tics. AI prose is *too clean*. A deliberate tic registers as personality. One tic per ~500 words is invisible to the analyzer (which thresholds on density) but registers to readers. Two tics per 200 words is noise.

### HI-specific tics

| Tic | Cadence | Use case |
|---|---|---|
| "देखो," as sentence pivot | 1 per ~1000 words | Pivot to a strong claim |
| "बस," as paragraph closer | 1 per ~800 words | Casual register |
| "मतलब," as connector | 1 per ~400 words | Spoken register |
| "सच कहूँ तो," as opener | 1 per ~600 words | First-person take |
| "और बस।" / "बात ख़त्म।" as fragment | 1 per ~600 words | Hard stop after a claim |
| "वैसे," as aside marker | 1 per ~1000 words | Casual digression |

### Worked example (HI)

Without tic (साफ़, AI जैसा):

<!-- human-writer:ignore-start (before-example, deliberately AI) -->
> प्राइसिंग टूल हर 15 मिनट में चलता है। यह डिफ़ॉल्ट रूप से 50 रेफ़रेंस पर नज़र रखता है। नतीजे एक Postgres व्यू में जाते हैं जिसे टीम Metabase से देखती है।
<!-- human-writer:ignore-end -->

With "देखो," and "मतलब":

> टूल हर 15 मिनट में चलता है। देखो, हमने 5 से शुरू किया था और रेट लिमिट ने मार डाला — 15 ही फ़र्श है। डिफ़ॉल्ट रूप से 50 रेफ़रेंस पर नज़र रखता है। मतलब, नतीजे वैसे भी एक Postgres व्यू में जाते हैं जिसे टीम Metabase से देखती है।

The two tics are invisible to bot detection but read as a person with a voice.

### How to apply

**WRITE mode.** Before drafting, pick one or two tics. Use them at the cadence listed. Resist adding more.

**CLEAN mode.** If the piece is otherwise good but reads as bot-clean, inject *one* tic at *one* natural insertion point. Re-run the analyzer.

---

## 7. Inject digressions and parentheticals

**Definition.** Humans wander. AI stays on-track relentlessly. Insert one short digression per ~500 words. Use parentheses for genuine asides (NOT the em-dash, which is foreign to Hindi).

**Why it works.** LLMs are trained to follow the prompt without drift. The result is unnaturally focused prose. Human writers tangent constantly. The drift is the signal of authentic thought. The key constraint: the digression must *return* to the main thread.

### Worked example (HI)

<!-- human-writer:ignore-start (before-example, deliberately AI) -->
Without digression:

> वाइन की प्राइसिंग अस्थिर रहती है। उत्पादक बाज़ार संकेतों पर नज़र रखकर ढलते हैं।
<!-- human-writer:ignore-end -->

With digression:

> वाइन की प्राइसिंग अस्थिर रहती है (Burgundy 2020 तीन हफ़्ते में 11% गिरा)। उत्पादक ढलते हैं — कम से कम वे जो हर हफ़्ते बाज़ार संकेत देखते हैं।

### Worked example (HI) (longer)

<!-- human-writer:ignore-start (before-example, deliberately AI) -->
Without digression:

> स्क्रेपिंग को अच्छे इन्फ़्रास्ट्रक्चर की ज़रूरत होती है। प्रॉक्सी, फ़िंगरप्रिंट और रेट लिमिट सब ठीक होने चाहिए वरना टारगेट एक घंटे में काट देता है।
<!-- human-writer:ignore-end -->

With digression:

> स्क्रेपिंग को अच्छे इन्फ़्रास्ट्रक्चर की ज़रूरत होती है। प्रॉक्सी, फ़िंगरप्रिंट, रेट लिमिट — एक भी ख़राब और टारगेट एक घंटे से पहले काट देता है। (यह हमने मार्च 2024 के एक काम में ठोकर खाकर सीखा: रेज़िडेंशियल प्रॉक्सी बढ़िया, फ़िंगरप्रिंट बढ़िया, पर sleep रैंडमाइज़ करना भूल गए। 47 मिनट में बैन।) बस, हर परत पर बेल्ट और सस्पेंडर दोनों।

### How to apply

**WRITE mode.** Plan one digression per major section (every ~500 words). Mark insertion points in your outline.

**CLEAN mode.** Read each paragraph and ask: "Did the writer think of anything specific while writing this?" If every paragraph is locked to its topic, inject one parenthetical with a real specific fact.

---

## 8. Choose concrete over abstract

**Definition.** When given the choice between a generic noun and a specific one, always pick the specific. AI defaults to abstractions ("समाधान", "कंपनियाँ", "वर्कफ़्लो"); humans default to concrete examples ("14 टैब वाली एक्सेल शीट", "ग्राहक की खरीद टीम", "सोमवार सुबह की तैयारी")।

**Why it works.** AI prose lives in the abstraction layer because abstractions are safer. Concrete nouns ("Postgres", "Amazon", "12 मिनट") commit to facts that must be true. Their presence is a strong signal of first-hand writing.

### Abstract → concrete substitution table (HI)

<!-- human-writer:ignore-start (citation table: abstract AI nouns quoted, not used) -->
| Abstract (AI default) | Concrete (human alternative) |
|---|---|
| "कंपनियाँ" | "एक मँझोला रिटेलर" / "12 लोगों की खरीद टीम" |
| "समाधान" | the actual thing: "पैनल", "क्रॉन", "CSV एक्सपोर्ट" |
| "वर्कफ़्लो" | the concrete step: "सोमवार की तैयारी", "इम्पोर्ट स्क्रिप्ट" |
| "उपयोगकर्ता" | "Carrefour का खरीदार" / "ट्रेडिंग डेस्क का विश्लेषक" |
| "डेटा" | "SKU + क़ीमत + प्रतिस्पर्धी + टाइमस्टैम्प के 47 कॉलम" |
| "प्रदर्शन" | "2 GB इंस्टेंस पर 47 req/s" |
| "मापनीयता" | "9 घंटे में 23 लाख URL पर चलाया" |
| "मूल्यवान जानकारी" | "वह ठोस नंबर जो पहले आपके पास नहीं था" |
| "हितधारक" | name them: "CFO", "खरीद टीम" |
| "पारिस्थितिकी तंत्र" | name it: "Apify Store", "Postgres एक्सटेंशन" |
<!-- human-writer:ignore-end -->

### Worked example (HI)

Bad (अमूर्त):

<!-- human-writer:ignore-start (before-example, deliberately AI) -->
> हमारा समाधान कंपनियों को अपनी प्रक्रियाओं को अनुकूलित करने में मदद करता है।
<!-- human-writer:ignore-end -->

Good (ठोस):

> हमने अपने ग्राहक की 14 टैब वाली एक्सेल शीट को एक ही पैनल से बदल दिया। सोमवार सुबह की तैयारी 2 घंटे से घटकर 12 मिनट रह गई।

### Worked example (HI) (longer)

Bad:

<!-- human-writer:ignore-start (before-example, deliberately AI) -->
> यह प्लेटफ़ॉर्म संगठनों को बेहतर निर्णय लेने के लिए वास्तविक समय के डेटा का उपयोग करने में सक्षम बनाता है।
<!-- human-writer:ignore-end -->

Good:

> यह प्लेटफ़ॉर्म 8 मार्केटप्लेस की क़ीमत-हलचल को Slack में भेजता है, चैनल-दर-चैनल और क्षेत्र-दर-क्षेत्र। जब Rioja 2018 5% से ज़्यादा गिरता है, ट्रेडिंग डेस्क को 90 सेकंड में पता चल जाता है। पिछली तिमाही उन्होंने तीन ख़रीद ऑर्डर ब्रोकर के ईमेल से पहले टूल के संकेत पर बंद किए।

### How to apply

**WRITE mode.** Each time you reach for an abstract noun ("समाधान", "उपयोगकर्ता", "डेटा"), pause: "What's the concrete version?" Write that.

**CLEAN mode.** Grep the draft for the abstract nouns in the table above. Replace each with a concrete equivalent or rewrite the sentence around it.

---

## 9. Vary transitions, drop the formal connectors

**Definition.** AI-generated transitions are predictable and connector-heavy. Humans transition with simple conjunctions, restructure sentences, or skip transitions entirely.

**Why it works.** The connector-class AI tells are the formal/Sanskritized conjunctions below. They appear when an LLM tries to make logical structure visible at the surface, which humans rarely do. In Hindi this overlaps with the over-Sanskritization tell.

### Forbidden transitions (HI)

<!-- human-writer:ignore-start (citation list: tells quoted, not used) -->
- इसके अतिरिक्त (as paragraph opener)
- इसके अलावा
- तथा / एवं (as the default "and")
- अतः / परिणामस्वरूप / फलस्वरूप
- तदनुसार
- तथापि (overused)
- दूसरी ओर (as paragraph opener)
- इस प्रकार (as paragraph opener)
- इस संदर्भ में (as paragraph opener)
<!-- human-writer:ignore-end -->

### HI alternatives

- **"और"**: the everyday "and" — use it instead of तथा/एवं.
- **"पर" / "लेकिन"**: sharp pivot instead of तथापि/किंतु।
- **"तो"**: informal "so" instead of अतः/इसलिए।
- **"बात यह है कि"**: human framing.
- **"वैसे," / "देखो,"**: Hindi rhythm markers.
- **Restructure**: often the cleanest transition is no transition — rewrite the next sentence to flow without a connector.

### Worked example (HI)

Bad (कनेक्टर-भारी):

<!-- human-writer:ignore-start (before-example, deliberately AI) -->
> एक्टर Amazon से क़ीमतें लाता है। इसके अतिरिक्त, यह स्टॉक स्तर पर नज़र रखता है। तथा, यह Slack के साथ एकीकृत होता है। दूसरी ओर, यह दैनिक निर्यात का समर्थन करता है।
<!-- human-writer:ignore-end -->

Good (विविध):

> एक्टर Amazon से क़ीमतें लाता है। स्टॉक पर भी नज़र रखता है। Slack से जुड़ाव v2 में आएगा। दैनिक निर्यात — या घंटे-दर-घंटे अगर माँगो।

### How to apply

**WRITE mode.** Never use the forbidden list. At a transition point, pick from the human alternatives or restructure.

**CLEAN mode.** Grep for every forbidden transition (especially तथा/एवं). Delete and rewrite. One of the fastest, highest-impact CLEAN-mode operations.

---

## 10. Build in productive imperfection

**Definition.** Humans pause, repeat for emphasis, change midstream, use casual interjections. AI hyper-corrects. A light imperfection ratio (1–2 instances per 500 words) registers as human without seeming sloppy.

**Why it works.** LLMs are trained out of the small imperfections real writing carries. Self-corrections, repetitions for emphasis, and casual interjections are statistically scarce in AI output and common in human prose. A small dose flips the signal.

### Imperfection categories (HI)

| Category | Example | Cadence |
|---|---|---|
| **Repetition for emphasis** | "ठीक है। बिल्कुल ठीक है।" | 1 per ~500 words |
| **Self-correction** | "क़ीमत 11% गिरी — अच्छा, कमीशन जोड़ो तो 12%।" | 1 per ~700 words |
| **Casual interjections** | "सच कहूँ तो,", "देखो,", "अरे,", "ख़ैर," | 1 per ~400 words (overlaps with #6) |
| **Mid-sentence pivot** | "सबसे सस्ता प्रॉक्सी आज़माया, पर — ख़ैर, समझ ही गए होगे।" | 1 per ~800 words |
| **Trailing "वग़ैरह"** | "…या जो भी आपके स्टैक में हो, वग़ैरह।" | 1 per ~1000 words (informal only) |

> Note: the self-correction example uses an em-dash for illustration only — in published Hindi, prefer a comma or parentheses, since `—` is foreign to Devanagari.

### Worked example (HI)

<!-- human-writer:ignore-start (before-example, deliberately AI) -->
Without imperfection (AI hyper-correct):

> क़ीमत तीन हफ़्ते में 11% गिरी। यह महत्वपूर्ण है। मूल कारण की जाँच करना उचित होगा।
<!-- human-writer:ignore-end -->

With imperfection (self-correction + interjection):

> क़ीमत तीन हफ़्ते में 11% गिरी, अच्छा, कमीशन जोड़ो तो 12%। यह बहुत है। सच कहूँ तो, इसे देखने लायक है।

### Calibration warning

Imperfection is dosed. Too much and you cross from "human writer" to "sloppy draft". The cadences above are upper bounds. In a technical doc, lean low. In casual marketing copy, the upper end works.

### How to apply

**WRITE mode.** Use natural interjections where the register allows. Add one self-correction or casual interjection per ~500 words.

**CLEAN mode.** Identify one paragraph that reads as too-polished and inject a single self-correction.

---

## Bonus: how to combine techniques

The techniques compound. Applying #1 alone drops `sentence_length_stdev` flags. Applying #1 + #5 + #9 drops the three most common AI signatures simultaneously. Below is a worked example showing the cumulative effect on a Hindi paragraph.

### Starting paragraph (vanilla AI output, ~75 words)

<!-- human-writer:ignore-start (citation: deliberately AI) -->
> आज के युग में, प्रतिस्पर्धी क़ीमतों पर नज़र रखना अत्यंत महत्वपूर्ण है. हमारा प्राइस-इंटेलिजेंस टूल एक सहज, मजबूत और सुरुचिपूर्ण समाधान प्रदान करता है. यह न केवल क़ीमतें ट्रैक करता है, बल्कि आपकी टीम को कार्रवाई योग्य अंतर्दृष्टि से सशक्त बनाता है. चाहे आप एक स्टार्टअप हों या एक बड़ी कंपनी, हमारा प्लेटफ़ॉर्म आपकी मदद करता है. अंत में, आप डेटा-आधारित निर्णय ले पाएँगे.
<!-- human-writer:ignore-end -->

**Analyzer baseline:** Latin periods on every Devanagari sentence (danda tell), suspect vocab (`आज के युग में`, `अत्यंत महत्वपूर्ण`, `सहज`, `मजबूत`, `सुरुचिपूर्ण`, `समाधान`, `सशक्त बनाता है`), tricolon ("सहज, मजबूत और सुरुचिपूर्ण"), construction "यह न केवल … बल्कि", "चाहे आप … हों या", conclusion "अंत में". Estimated AI-probability: HIGH/CRITICAL.

### Final humanized version (same content, ~75 words)

> Amazon पर त्योहारी सीज़न में क़ीमतें हर घंटे बदलती हैं। देखो — हमारा टूल हर 15 मिनट में आपके 50 सबसे महँगे SKU पर चलता है और 3% से बड़ी कोई भी हलचल पकड़ लेता है। बस। पैनल एक Postgres व्यू है (कोई सुंदर UI नहीं) क्योंकि जिस टीम को यह चाहिए वह वैसे भी Metabase में रहती है। हमने इसे 2024 में एक मँझोले रिटेलर के लिए बनाया, जब छह हफ़्ते उनकी क़ीमत गिरती रही और उन्हें देर से पता चला। वही सेटअप चाहिए? पूरी चीज़ क्रॉन पर लगभग 200 लाइन पायथन है।

What changed: temporal abstraction → concrete season + marketplace; danda everywhere (no Latin `.`); tricolon and suspect vocab gone; "यह न केवल…" and "चाहे आप…" gone; "अंत में" gone; added a "देखो —" tic (em-dash here is illustrative; prefer comma in final copy), a "बस।" fragment, a real 2024 anecdote, concrete numbers (15 मिनट, 50 SKU, 3%), and a closing pointer.

### Order of operations summary

| Order | Technique | Reason |
|---|---|---|
| 1 | #5 Cut hedging openers | Highest words-saved, fastest fix |
| 2 | #9 Vary transitions (drop तथा/एवं) | Cuts the connector + Sanskritization class in one pass |
| 3 | #1 Vary sentence length | Statistical signal most analyzers test |
| 4 | #4 Break tricolons | Density signal — easy to target |
| 5 | Danda sweep | Replace every Latin `.` on a Devanagari sentence with `।` |
| 6 | #3 Asymmetric bullets | Only if the piece has lists |
| 7 | #8 Concrete over abstract | Compounds with #2 |
| 8 | #2 Inject opinion/anecdote | Highest authorial-signal move |
| 9 | #7 Digressions | Adds drift |
| 10 | #6/#10 Idiosyncratic markers + imperfection | Final personality + humanity layer |

The first five fix the statistical + script signature. The last five inject the authorial signal.

---

## See also

- `tells-stylistic-hi.md` — Hindi vocabulary, constructions, calques, and typography (danda, em-dash) that techniques #4, #5, #8, #9 reference directly.
- `tells-statistical.md` — the metrics (sentence-length stdev, bullet parallelism, tricolon density, em-dash density) these techniques target.
- `tells-structural.md` — bullet, header, conclusion anti-patterns that techniques #3 and #4 disrupt.
- `adapter-marketing.md` / `adapter-short-comms.md` / `adapter-technical.md` / `adapter-editorial-seo.md` — content-type-specific calibration.
