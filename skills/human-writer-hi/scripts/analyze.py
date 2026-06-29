#!/usr/bin/env python3
"""
human-writer-hi / analyze.py — deterministic AI-tell detector (Hindi, Devanagari).

Specialization of the master human-writer analyzer for Hindi. Differences vs
the master (everything else is identical):
  - --lang choices=["hi"].
  - count_sentences / sentence_lengths split on the Devanagari danda (। U+0964)
    and double danda (॥ U+0965) as well as the Latin terminators .?! — Hindi
    sentences end with a danda, not a period.
  - detect_tricolons uses a Hindi conjunction (और|तथा|एवं) with a Latin comma.
  - NEW detect_latin_period_in_devanagari: flags sentences that contain
    Devanagari characters but terminate with a Latin "." instead of a danda "।"
    (a Hindi-only typography tell), wired as a low-weight branch.

httpx is permitted ONLY for --external detector POSTs.
It MUST NEVER be used to fetch the input text. Input comes from --input or stdin only.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
from collections import Counter
from pathlib import Path

import yaml

RULES_PATH = Path(__file__).parent / "rules.yaml"

# Module-level httpx import: deferred to call sites because httpx is only
# permitted for outbound POSTs to external detector APIs (no-local-scraping policy).
# We import lazily inside the call_* helpers so that a missing httpx install
# does not break offline use of the analyzer.


def load_rules() -> dict:
    with RULES_PATH.open(encoding="utf-8") as f:
        return yaml.safe_load(f)


IGNORE_REGION_RX = re.compile(
    # The start marker tolerates a trailing annotation (e.g. the reason for the
    # exemption) between the marker name and the closing `-->`.
    r"<!--\s*human-writer:ignore-start\b[^>]*-->.*?<!--\s*human-writer:ignore-end\b[^>]*-->",
    flags=re.DOTALL | re.IGNORECASE,
)
FENCED_CODE_RX = re.compile(r"```.*?```", flags=re.DOTALL)
# A markdown table row is a line whose content is pipe-delimited. This matches
# the header, the `| --- | --- |` separator, and every data row. Table cells are
# data, not prose, and would otherwise skew lexical diversity (many unique tokens)
# and burstiness (rows split oddly on sentence boundaries).
TABLE_ROW_RX = re.compile(r"^[ \t]*\|.*\|[ \t]*$\n?", flags=re.MULTILINE)

# Devanagari-aware word tokenizer. CRITICAL Hindi delta: Python's default `\w`
# matches Devanagari BASE letters but NOT the combining vowel signs (matras like
# े ो ं ़ ्, U+093A–U+094F + nukta/anusvara), so `\b\w+\b` shatters a single Hindi
# word ("तेज़" → "त","ज") and inflates the word count ~2–3×. We therefore tokenize
# a Devanagari word as a contiguous run over the Devanagari letter+sign range,
# DELIBERATELY EXCLUDING the danda U+0964 (।) and double danda U+0965 (॥), which
# are sentence punctuation, not letters — if they were included, every sentence
# would glue its terminator onto its last word (e.g. "हैं।"), wrecking
# bullet-parallelism and TTR. We keep the Devanagari digits (U+0966–U+096F) and
# the extended Devanagari block (U+0971–U+097F). We fall back to the normal `\w+`
# run for Latin/Arabic-numeral tokens (brand names, code, English snippets).
# Every word-counting site (count_words, sentence_lengths, detect_ttr,
# detect_bullet_parallelism) uses this, so word counts are sane on Hindi.
_DEVA_WORD_CHARS = r"ऀ-ॣ०-ॿ"  # Devanagari minus the two dandas
WORD_RX = re.compile(rf"[{_DEVA_WORD_CHARS}]+|\w+")


def _words(text: str) -> list[str]:
    return WORD_RX.findall(text)


# HTML comments (e.g. provenance headers) are metadata, never prose. Strip them
# before scoring so the `<!--` opener can't reach the detectors and phantom-fire.
# Ordered after IGNORE_REGION_RX so the human-writer:ignore region keeps its meaning.
HTML_COMMENT_RX = re.compile(r"<!--.*?-->", flags=re.DOTALL)


def strip_non_prose(text: str) -> str:
    """Remove non-prose regions before any detector runs.

    Honors the prose-only contract documented in references/adapter-technical.md:
    fenced code blocks, config samples, CLI examples, and data tables are not
    prose and must not be scored. Opt-in ignore regions let doctrine files quote
    intentionally AI-flavored bad examples without self-flagging. Ignore regions
    are stripped first so a fenced block nested inside one is removed as part of
    the region.
    """
    text = IGNORE_REGION_RX.sub("", text)
    text = HTML_COMMENT_RX.sub("", text)
    text = FENCED_CODE_RX.sub("", text)
    text = TABLE_ROW_RX.sub("", text)
    return text


def count_words(text: str) -> int:
    return len(_words(text))


def count_sentences(text: str) -> int:
    # Hindi sentence terminators include the Devanagari danda (। U+0964) and
    # double danda (॥ U+0965), plus the Latin .?! that web Hindi sometimes uses.
    # We split on a run of terminators followed by OPTIONAL whitespace (a danda
    # is often written tight against the following word with no space), so the
    # split must not require a trailing \s.
    sentences = re.split(r"[।॥.?!]+\s*", text.strip())
    return len([s for s in sentences if s.strip()])


def sentence_lengths(text: str) -> list[int]:
    sentences = re.split(r"[।॥.?!]+\s*", text.strip())
    lengths = []
    for s in sentences:
        s = s.strip()
        if s:
            lengths.append(len(_words(s)))
    return lengths


def detect_sentence_stdev(text: str, threshold: float) -> dict:
    lengths = sentence_lengths(text)
    if len(lengths) < 2:
        stdev = 0.0
    else:
        mean = sum(lengths) / len(lengths)
        var = sum((x - mean) ** 2 for x in lengths) / len(lengths)
        stdev = var ** 0.5
    flag = stdev < threshold
    if stdev < threshold / 2:
        severity = "high"
    elif stdev < threshold:
        severity = "medium"
    else:
        severity = "low"
    return {
        "value": round(stdev, 2),
        "threshold": threshold,
        "flag": flag,
        "severity": severity,
    }


BULLET_RX = re.compile(r"^\s*[-*+]\s+(.+?)\s*$", flags=re.MULTILINE)
H2_RX = re.compile(r"^##\s+\S", flags=re.MULTILINE)
H3_RX = re.compile(r"^###\s+\S", flags=re.MULTILINE)


def detect_bullet_parallelism(text: str, threshold: float) -> dict:
    """Parallelism = max(ratio sharing first word, ratio sharing last word).
    AI lists often share either an opening verb or a repeated trailing noun phrase.
    """
    bullets = [b.strip() for b in BULLET_RX.findall(text) if b.strip()]
    if len(bullets) < 2:
        return {
            "value": 0.0,
            "threshold": threshold,
            "flag": False,
            "severity": "low",
            "bullet_count": len(bullets),
        }
    # Extract the first/last *word token* of each bullet. Using WORD_RX (rather
    # than splitting on \W+) skips leading markdown markup such as **bold** or
    # _italic_, which would otherwise yield an empty first token and make every
    # markup-led bullet falsely share it (parallelism = 1.0). WORD_RX also keeps
    # Devanagari words whole (a bare `\w+` would shatter them on matras).
    firsts = []
    lasts = []
    for b in bullets:
        toks = _words(b.lower())
        if toks:
            firsts.append(toks[0])
            lasts.append(toks[-1])
    first_ratio = Counter(firsts).most_common(1)[0][1] / len(firsts) if firsts else 0.0
    last_ratio = Counter(lasts).most_common(1)[0][1] / len(lasts) if lasts else 0.0
    ratio = max(first_ratio, last_ratio)
    flag = ratio >= threshold
    if ratio >= threshold + 0.1:
        severity = "high"
    elif ratio >= threshold:
        severity = "medium"
    else:
        severity = "low"
    return {
        "value": round(ratio, 3),
        "threshold": threshold,
        "flag": flag,
        "severity": severity,
        "bullet_count": len(bullets),
    }


def detect_header_pyramid(text: str) -> bool:
    """Pyramid = >=2 H2 blocks each containing exactly 3 H3s."""
    lines = text.splitlines()
    blocks: list[int] = []  # count of H3s in current H2 block
    current: int | None = None
    for line in lines:
        if re.match(r"^##\s+\S", line) and not line.startswith("###"):
            # H2 found
            if current is not None:
                blocks.append(current)
            current = 0
        elif re.match(r"^###\s+\S", line):
            if current is not None:
                current += 1
    if current is not None:
        blocks.append(current)
    pyramid_blocks = [b for b in blocks if b == 3]
    return len(pyramid_blocks) >= 2


def build_recommendations(tells: dict) -> list[dict]:
    recs: list[dict] = []
    styl = tells.get("stylistic", {})
    stat = tells.get("statistical", {})
    struct = tells.get("structural", {})

    em = styl.get("em_dash_count")
    if em and em.get("flag"):
        priority = "high" if em.get("severity") == "high" else "medium"
        recs.append({
            "priority": priority,
            "action": (
                f"Reduce em-dash usage: found {em.get('value')} em-dashes "
                f"({em.get('per_1000_words')} per 1000 words). Replace with commas, "
                "parentheses, or full sentences (keep only genuine dialogue rayas)."
            ),
        })

    danda = styl.get("latin_period_in_devanagari")
    if danda and danda.get("flag"):
        recs.append({
            "priority": "medium" if danda.get("severity") == "high" else "low",
            "action": (
                f"Replace the Latin period with a danda: {danda.get('value')} "
                "Devanagari sentence(s) end in a Latin '.' instead of the danda '।'. "
                "Use '।' (U+0964) to terminate Hindi sentences (keep '?'/'!' only "
                "for genuine questions/exclamations)."
            ),
        })

    vocab = styl.get("suspect_vocabulary") or []
    if vocab:
        top = sorted(vocab, key=lambda v: -v.get("count", 0))[:5]
        words = ", ".join(f"{v['word']} (x{v['count']})" for v in top)
        recs.append({
            "priority": "high" if len(vocab) >= 4 else "medium",
            "action": f"Rewrite suspect vocabulary: {words}.",
        })

    constrs = styl.get("ai_constructions") or []
    if constrs:
        recs.append({
            "priority": "high" if len(constrs) >= 2 else "medium",
            "action": (
                f"Remove formulaic constructions ({len(constrs)} detected). "
                "Rephrase opener and closing sentences in your own voice."
            ),
        })

    sd = stat.get("sentence_length_stdev")
    if sd and sd.get("flag"):
        recs.append({
            "priority": "medium",
            "action": (
                f"Increase sentence-length variance (stdev={sd.get('value')}). "
                "Mix short punchy sentences with longer ones."
            ),
        })

    tr = stat.get("lexical_diversity_ttr")
    if tr and tr.get("flag"):
        recs.append({
            "priority": "low",
            "action": (
                f"Lift lexical diversity (TTR={tr.get('value')} < {tr.get('threshold')}). "
                "Avoid repeating the same nouns and verbs."
            ),
        })

    bp = struct.get("bullet_parallelism_ratio")
    if bp and bp.get("flag"):
        recs.append({
            "priority": "medium",
            "action": (
                f"Break bullet parallelism (ratio={bp.get('value')}). "
                "Vary bullet length, structure, and ending."
            ),
        })

    if struct.get("header_pyramid_detected"):
        recs.append({
            "priority": "medium",
            "action": "Break the header pyramid: collapse or merge symmetric H2/H3 blocks.",
        })

    priority_rank = {"high": 0, "medium": 1, "low": 2}
    recs.sort(key=lambda r: priority_rank.get(r["priority"], 3))
    return recs


def compute_score(tells: dict, weights: dict) -> int:
    """Composite AI-likelihood score in [0, 100], weighted by content-type."""
    stat = tells.get("statistical", {})
    styl = tells.get("stylistic", {})
    struct = tells.get("structural", {})

    # Statistical (max 30 raw)
    statistical_pts = 0
    sd = stat.get("sentence_length_stdev")
    if sd and sd.get("flag"):
        statistical_pts += 10
    tr = stat.get("lexical_diversity_ttr")
    if tr and tr.get("flag"):
        statistical_pts += 8

    # Stylistic (max 50 raw)
    stylistic_pts = 0
    em = styl.get("em_dash_count")
    if em and em.get("flag"):
        stylistic_pts += 15 if em.get("severity") == "high" else 8
    vocab = styl.get("suspect_vocabulary") or []
    vocab_total = sum(v.get("count", 0) for v in vocab)
    stylistic_pts += min(20, vocab_total * 3)
    constrs = styl.get("ai_constructions") or []
    constr_total = sum(c.get("count", 0) for c in constrs)
    stylistic_pts += min(10, constr_total * 3)
    tricolons = styl.get("tricolon_count", 0)
    if tricolons >= 3:
        stylistic_pts += 5
    # NEW: Latin-period-in-Devanagari typography tell — SMALL low-weight branch
    # (Hindi). A Devanagari sentence ending in a Latin "." instead of a danda "।"
    # is a real surface signature of machine/Hinglish output, but it is
    # register-sensitive (some modern web Hindi legitimately uses "."), so it
    # contributes only a few points and never dominates the score.
    danda = styl.get("latin_period_in_devanagari")
    if danda and danda.get("flag"):
        stylistic_pts += 5 if danda.get("severity") == "high" else 3

    # Structural (max 20 raw)
    structural_pts = 0
    bp = struct.get("bullet_parallelism_ratio")
    if bp and bp.get("flag"):
        structural_pts += 10
    if struct.get("header_pyramid_detected"):
        structural_pts += 10

    weighted = (
        statistical_pts * weights.get("statistical", 1.0)
        + stylistic_pts * weights.get("stylistic", 1.0)
        + structural_pts * weights.get("structural", 1.0)
    )
    return max(0, min(100, int(round(weighted))))


def verdict_for(score: int, bands: dict) -> str:
    for name, (lo, hi) in bands.items():
        if lo <= score <= hi:
            return name
    return "LOW_RISK"


# Hindi tricolon: "X, Y और Z" / "X, Y, तथा Z" / "X, Y एवं Z". Hindi prose uses the
# Latin comma "," as the list separator and a coordinating conjunction
# (और "and" / तथा / एवं, the latter two being the formal/Sanskritized register)
# before the final item. NOTE: a bare `\w+` for the list items would shatter a
# Devanagari word on its matras (े ो ़ …, which `\w` does not match), so we match
# a word as a whole Devanagari run (matra-safe) OR a Latin run, capturing the
# same comma-comma-conjunction rhythm the master EN/FR detectors look for.
_W = rf"[{_DEVA_WORD_CHARS}\w]+"
TRICOLON_HI = re.compile(rf"{_W},\s*{_W},?\s*(?:और|तथा|एवं)\s+{_W}")


def detect_tricolons(text: str) -> int:
    return len(TRICOLON_HI.findall(text))


# Split text into orthographic sentences for the Latin-period check. We split on
# ANY terminator — the Devanagari danda ।, double danda ॥, or the Latin . ? ! —
# but KEEP the terminator with its sentence so we can see which character ended
# each sentence. `[^...]*[...]` greedily consumes everything up to and including
# one terminator.
_SENTENCE_SPLIT_RX = re.compile(r"[^।॥.?!]*[।॥.?!]", flags=re.DOTALL)

# Devanagari block is U+0900–U+097F. A sentence "is Hindi" for the purpose of the
# danda check if it contains at least one Devanagari letter.
_DEVANAGARI_RX = re.compile(r"[ऀ-ॿ]")


def detect_latin_period_in_devanagari(text: str, threshold: int) -> dict:
    """Hindi typography tell: a sentence written in Devanagari should terminate
    with a danda (। U+0964), not a Latin full stop (".").

    For every sentence that contains at least one Devanagari character, we look
    at its terminator. If it ends in a Latin "." (rather than a danda ।/॥, or a
    ?/! which Hindi does borrow for questions/exclamations), it is counted as a
    Latin-period-in-Devanagari miss. The detector flags when the count exceeds
    `threshold`.

    This is register-sensitive: a fair amount of modern web/Hinglish Hindi uses
    the Latin "." as a sentence-ender, so the detector is LOW weight and the
    threshold is calibrated so a clean danda-using fixture scores 0 misses and
    never fires.
    """
    missing = 0
    total = 0
    for m in _SENTENCE_SPLIT_RX.finditer(text):
        chunk = m.group(0)
        stripped = chunk.rstrip()
        if not stripped:
            continue
        if not _DEVANAGARI_RX.search(chunk):
            # Pure-Latin sentence (e.g. an English snippet, code, a brand name) —
            # the danda rule does not apply, so skip it entirely.
            continue
        total += 1
        if stripped[-1] == ".":
            missing += 1
    flag = missing > threshold
    if missing > threshold + 2:
        severity = "high"
    elif missing > threshold:
        severity = "medium"
    else:
        severity = "low"
    return {
        "value": missing,
        "devanagari_sentences": total,
        "threshold": threshold,
        "flag": flag,
        "severity": severity,
    }


def _pattern_label(pat: str) -> str:
    """Human-readable label: collapse [' ’] apostrophe classes to a single '."""
    label = re.sub(r"\[['’]+\]", "'", pat)
    return label


def detect_ai_constructions(text: str, patterns: list[dict]) -> list[dict]:
    out = []
    for entry in patterns:
        pat = entry["pattern"]
        severity = entry.get("severity", "medium")
        try:
            rx = re.compile(pat, flags=re.IGNORECASE)
        except re.error:
            continue
        matches = list(rx.finditer(text))
        if matches:
            out.append({
                "pattern": _pattern_label(pat),
                "count": len(matches),
                "positions": [m.start() for m in matches],
                "severity": severity,
            })
    return out


# Devanagari-aware word boundary. The master uses \b...\b, but \b is WRONG for
# Devanagari: a trailing matra (े ो ं ा …, which `\w` does not match) sits at the
# end of most Hindi words, so there is no \b between the matra and the next space
# — `\b<phrase>\b` then never matches a phrase ending in a matra (में, तथा, …).
# Instead we bound the phrase with lookarounds over the combined word-char class
# [ऀ-ॿ\w]: a match must NOT be glued to another letter/matra on either side
# (so "मजबूत" does not fire inside "मजबूती"), but spaces, punctuation, the danda,
# and string edges are all valid boundaries.
_BOUND_BEFORE = rf"(?<![{_DEVA_WORD_CHARS}\w])"
_BOUND_AFTER = rf"(?![{_DEVA_WORD_CHARS}\w])"


def detect_suspect_vocab(text: str, vocab: list[str]) -> list[dict]:
    out = []
    for word in vocab:
        pat = re.compile(
            _BOUND_BEFORE + re.escape(word) + _BOUND_AFTER, flags=re.IGNORECASE
        )
        matches = list(pat.finditer(text))
        if matches:
            out.append({
                "word": word,
                "count": len(matches),
                "positions": [m.start() for m in matches],
            })
    return out


def detect_ttr(text: str, threshold: float) -> dict:
    words = [w.lower() for w in _words(text)]
    if not words:
        ttr = 0.0
    else:
        ttr = len(set(words)) / len(words)
    flag = ttr < threshold
    if ttr < threshold * 0.6:
        severity = "high"
    elif ttr < threshold:
        severity = "medium"
    else:
        severity = "low"
    return {
        "value": round(ttr, 3),
        "threshold": threshold,
        "flag": flag,
        "severity": severity,
    }


def detect_em_dashes(text: str, word_count: int, threshold: float) -> dict:
    count = text.count("—")
    per_1000 = (count / word_count * 1000.0) if word_count else 0.0
    flag = per_1000 > threshold
    if per_1000 > threshold * 2:
        severity = "high"
    elif per_1000 > threshold:
        severity = "medium"
    else:
        severity = "low"
    return {
        "value": count,
        "per_1000_words": round(per_1000, 2),
        "threshold": threshold,
        "flag": flag,
        "severity": severity,
    }


# ---------------------------------------------------------------------------
# External AI-detector providers (Copyleaks, GPTZero, Originality.ai)
#
# Constraint (no-local-scraping policy):
#   - httpx is permitted ONLY for these outbound POSTs.
#   - The INPUT TEXT must NEVER be fetched over HTTP by this script.
#     Input arrives via --input <file> or stdin; the orchestrator (Claude)
#     is responsible for fetching any URL with Firecrawl / Tavily / Exa MCP.
#
# Each call_<provider> returns either:
#   - {"ai_probability": float in [0.0, 1.0], "raw_response": dict}
#   - {"status": "skipped_no_key"}           — env var missing
#   - {"status": "error", "message": str}    — wrapped at dispatch level
#
# Endpoints below are the most likely current endpoints as of 2026-05.
# Verify against current provider docs before deploying — these APIs change.
# Unit tests mock call_<provider>, so they don't depend on the live API.
# ---------------------------------------------------------------------------

# Copyleaks uses a two-step auth (verified against docs.copyleaks.com 2026-06):
#   1. POST email+key to the login endpoint -> short-lived access_token (48h).
#   2. POST text to writer-detector/{scanId}/check with Authorization: Bearer.
# The detector response carries summary.ai (0..1) as the AI probability.
COPYLEAKS_LOGIN_ENDPOINT = "https://id.copyleaks.com/v3/account/login/api"
COPYLEAKS_ENDPOINT = "https://api.copyleaks.com/v2/writer-detector"
GPTZERO_ENDPOINT = "https://api.gptzero.me/v2/predict/text"
ORIGINALITY_ENDPOINT = "https://api.originality.ai/api/v1/scan/ai"
HTTP_TIMEOUT_S = 30.0


def _copyleaks_login(email: str, key: str) -> str:
    """Exchange (email, API key) for a short-lived access token.

    httpx is permitted ONLY for external detector POSTs. Split out as its own
    helper so call_copyleaks is unit-testable without touching the network.
    """
    import httpx
    resp = httpx.post(
        COPYLEAKS_LOGIN_ENDPOINT,
        json={"email": email, "key": key},
        headers={"Content-Type": "application/json", "Accept": "application/json"},
        timeout=HTTP_TIMEOUT_S,
    )
    resp.raise_for_status()
    return resp.json()["access_token"]


def _copyleaks_detect(token: str, text: str, scan_id: str, sandbox: bool = False) -> dict:
    """POST text to the writer-detector endpoint with a Bearer access token."""
    import httpx
    resp = httpx.post(
        f"{COPYLEAKS_ENDPOINT}/{scan_id}/check",
        json={"text": text, "sandbox": sandbox},
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "Accept": "application/json",
        },
        timeout=HTTP_TIMEOUT_S,
    )
    resp.raise_for_status()
    return resp.json()


def call_copyleaks(text: str, sandbox: bool = False) -> dict:
    """Run Copyleaks AI detection via its two-step auth flow.

    Requires BOTH COPYLEAKS_EMAIL and COPYLEAKS_API_KEY. Returns
    {ai_probability, raw_response} on success, or {status: "skipped_no_key"}
    if either credential is unset. With sandbox=True the API returns simulated
    results without consuming credits (used to smoke-test the flow).
    """
    key = os.environ.get("COPYLEAKS_API_KEY")
    email = os.environ.get("COPYLEAKS_EMAIL")
    if not key or not email:
        return {"status": "skipped_no_key"}
    token = _copyleaks_login(email, key)
    scan_id = os.urandom(8).hex()
    data = _copyleaks_detect(token, text, scan_id, sandbox=sandbox)
    summary = data.get("summary") or {}
    ai_prob = summary.get("ai")
    if ai_prob is None:
        # Defensive fallback if the response shape changes
        ai_prob = data.get("ai_probability") or 0.0
    return {"ai_probability": float(ai_prob), "raw_response": data}


def call_gptzero(text: str) -> dict:
    """POST text to GPTZero v2 predict endpoint.

    httpx is permitted ONLY for external detector POSTs (this function).
    Input text MUST NOT be fetched via HTTP — see module docstring.
    """
    key = os.environ.get("GPTZERO_API_KEY")
    if not key:
        return {"status": "skipped_no_key"}
    import httpx
    headers = {
        "x-api-key": key,
        "Content-Type": "application/json",
        "Accept": "application/json",
    }
    payload = {"document": text}
    with httpx.Client(timeout=HTTP_TIMEOUT_S) as client:
        resp = client.post(GPTZERO_ENDPOINT, headers=headers, json=payload)
        resp.raise_for_status()
        data = resp.json()
    # GPTZero shape (verify): documents[0].class_probabilities.ai
    docs = data.get("documents") or []
    ai_prob = 0.0
    if docs:
        cp = docs[0].get("class_probabilities") or {}
        ai_prob = cp.get("ai", 0.0)
        if not ai_prob:
            # Older shape: completely_generated_prob
            ai_prob = docs[0].get("completely_generated_prob", 0.0)
    return {"ai_probability": float(ai_prob), "raw_response": data}


def call_originality(text: str) -> dict:
    """POST text to Originality.ai AI scan endpoint.

    httpx is permitted ONLY for external detector POSTs (this function).
    Input text MUST NOT be fetched via HTTP — see module docstring.
    """
    key = os.environ.get("ORIGINALITY_AI_API_KEY")
    if not key:
        return {"status": "skipped_no_key"}
    import httpx
    headers = {
        "X-OAI-API-KEY": key,
        "Content-Type": "application/json",
        "Accept": "application/json",
    }
    payload = {"content": text}
    with httpx.Client(timeout=HTTP_TIMEOUT_S) as client:
        resp = client.post(ORIGINALITY_ENDPOINT, headers=headers, json=payload)
        resp.raise_for_status()
        data = resp.json()
    # Originality shape (verify): score.ai (0..1)
    score = data.get("score") or {}
    ai_prob = score.get("ai")
    if ai_prob is None:
        ai_prob = data.get("ai_score") or 0.0
    return {"ai_probability": float(ai_prob), "raw_response": data}


def call_external(text: str, provider: str) -> dict | None:
    """Dispatch to the chosen provider, wrapping all exceptions.

    Returns None for an unknown provider (caller can decide what to do).
    Returns the provider's dict otherwise, possibly with status="error".
    """
    dispatch = {
        "copyleaks": call_copyleaks,
        "gptzero": call_gptzero,
        "originality": call_originality,
    }
    fn = dispatch.get(provider)
    if not fn:
        return None
    try:
        return fn(text)
    except Exception as exc:  # noqa: BLE001 — intentional broad catch
        return {"status": "error", "message": str(exc)}


def analyze(text: str, lang: str, content_type: str) -> dict:
    rules = load_rules()
    lang_rules = rules[lang]
    thresholds = lang_rules["thresholds"]
    text = strip_non_prose(text)
    wc = count_words(text)
    sc = count_sentences(text)
    em_dash = detect_em_dashes(text, wc, thresholds["em_dash_per_1000_words"])
    stdev = detect_sentence_stdev(text, thresholds["sentence_stdev_min"])
    ttr = detect_ttr(text, thresholds["lexical_diversity_min"])
    suspects = detect_suspect_vocab(text, lang_rules.get("suspect_vocabulary") or [])
    constructions = detect_ai_constructions(text, lang_rules.get("ai_constructions") or [])
    tricolons = detect_tricolons(text)
    danda = detect_latin_period_in_devanagari(
        text, thresholds["latin_period_in_devanagari_max"]
    )
    bullet_par = detect_bullet_parallelism(text, thresholds["bullet_parallelism_max"])
    header_pyramid = detect_header_pyramid(text)
    tells = {
        "statistical": {"sentence_length_stdev": stdev, "lexical_diversity_ttr": ttr},
        "stylistic": {
            "em_dash_count": em_dash,
            "suspect_vocabulary": suspects,
            "ai_constructions": constructions,
            "tricolon_count": tricolons,
            "latin_period_in_devanagari": danda,
        },
        "structural": {
            "bullet_parallelism_ratio": bullet_par,
            "header_pyramid_detected": header_pyramid,
        },
    }
    weights = rules.get("content_type_weights", {}).get(content_type, {
        "statistical": 1.0, "stylistic": 1.0, "structural": 1.0,
    })
    score = compute_score(tells, weights)
    bands = rules.get("verdict_bands", {})
    verdict = verdict_for(score, bands)
    return {
        "language": lang,
        "content_type": content_type,
        "word_count": wc,
        "sentence_count": sc,
        "ai_probability_score": score,
        "verdict": verdict,
        "tells": tells,
        "recommendations": build_recommendations(tells),
        "_config": {
            "em_dash_threshold_per_1000_words": thresholds["em_dash_per_1000_words"],
        },
    }


def analyze_with_external(
    text: str,
    lang: str,
    content_type: str,
    external: str | None = None,
) -> dict:
    """Wrap analyze() and (if requested) attach an external_detector block.

    Backward-compatible: analyze() is unchanged; this is the function CLI uses.
    """
    result = analyze(text, lang, content_type)
    if external:
        ext = call_external(text, external)
        if ext is not None:
            result["external_detector"] = {"provider": external, **ext}
    return result


def render_human(result: dict) -> str:
    lines: list[str] = []
    lines.append("=" * 60)
    lines.append(f"  human-writer-hi / analyze.py — {result.get('input_file', '<stdin>')}")
    lines.append("=" * 60)
    lines.append(
        f"Score: {result['ai_probability_score']}/100  →  {result['verdict']}  "
        f"({result['language']}, {result['content_type']})"
    )
    lines.append(
        f"Words: {result['word_count']}  |  Sentences: {result['sentence_count']}"
    )
    lines.append("")

    tells = result.get("tells", {})
    styl = tells.get("stylistic", {})
    stat = tells.get("statistical", {})
    struct = tells.get("structural", {})

    lines.append("-- Top tells -----------------------------------------------")
    em = styl.get("em_dash_count") or {}
    em_flag = "FLAG" if em.get("flag") else "ok"
    lines.append(
        f"em-dash      : {em.get('value', 0)} "
        f"({em.get('per_1000_words', 0)} per 1000 words)  [{em_flag}]"
    )
    danda = styl.get("latin_period_in_devanagari") or {}
    danda_flag = "FLAG" if danda.get("flag") else "ok"
    lines.append(
        f"danda vs '.' : {danda.get('value', 0)} Latin-period of "
        f"{danda.get('devanagari_sentences', 0)} Devanagari sentences  [{danda_flag}]"
    )
    sd = stat.get("sentence_length_stdev") or {}
    sd_flag = "FLAG" if sd.get("flag") else "ok"
    lines.append(
        f"sentence stdev: {sd.get('value', 0)}  threshold>={sd.get('threshold', 0)}  [{sd_flag}]"
    )
    tr = stat.get("lexical_diversity_ttr") or {}
    tr_flag = "FLAG" if tr.get("flag") else "ok"
    lines.append(
        f"TTR (lex div): {tr.get('value', 0)}  threshold>={tr.get('threshold', 0)}  [{tr_flag}]"
    )

    vocab = styl.get("suspect_vocabulary") or []
    if vocab:
        top = sorted(vocab, key=lambda v: -v.get("count", 0))[:5]
        joined = ", ".join(f"{v['word']} (x{v['count']})" for v in top)
        lines.append(f"vocab (top 5): {joined}")
    constrs = styl.get("ai_constructions") or []
    if constrs:
        top = sorted(constrs, key=lambda c: -c.get("count", 0))[:3]
        joined = " | ".join(f"{c['pattern']} (x{c['count']})" for c in top)
        lines.append(f"constructions: {joined}")

    tri = styl.get("tricolon_count", 0)
    lines.append(f"tricolons   : {tri}")
    bp = struct.get("bullet_parallelism_ratio") or {}
    if bp.get("bullet_count", 0):
        bp_flag = "FLAG" if bp.get("flag") else "ok"
        lines.append(
            f"bullets     : {bp.get('bullet_count')} items, "
            f"parallelism={bp.get('value', 0)} [{bp_flag}]"
        )
    if struct.get("header_pyramid_detected"):
        lines.append("headers     : pyramid detected [FLAG]")
    lines.append("")

    recs = result.get("recommendations") or []
    if recs:
        lines.append("-- Recommendations (top 5) ---------------------------------")
        for r in recs[:5]:
            lines.append(f"[{r['priority'].upper():6}] {r['action']}")
        lines.append("")

    ext = result.get("external_detector")
    if ext:
        lines.append("-- External detector --------------------------------------")
        provider = ext.get("provider", "?")
        if "ai_probability" in ext:
            ai_pct = round(float(ext["ai_probability"]) * 100, 1)
            lines.append(f"provider: {provider}  →  AI probability: {ai_pct}%")
        elif ext.get("status") == "skipped_no_key":
            lines.append(f"provider: {provider}  →  skipped (no API key set)")
        elif ext.get("status") == "error":
            lines.append(f"provider: {provider}  →  error: {ext.get('message')}")
        else:
            lines.append(f"provider: {provider}  →  {ext}")
        lines.append("")
    return "\n".join(lines)


def main() -> int:
    p = argparse.ArgumentParser(description="Deterministic AI-tell analyzer (Hindi)")
    p.add_argument("--input", type=Path, help="Input file (markdown/txt). Stdin if omitted.")
    p.add_argument("--lang", choices=["hi"], required=True)
    p.add_argument("--type", dest="content_type",
                   choices=["marketing", "short-comms", "technical", "editorial-seo"],
                   required=True)
    p.add_argument("--external", choices=["copyleaks", "gptzero", "originality"])
    p.add_argument("--format", choices=["json", "human"], default="json")
    args = p.parse_args()

    text = args.input.read_text(encoding="utf-8") if args.input else sys.stdin.read()
    result = analyze_with_external(text, args.lang, args.content_type, external=args.external)
    result["input_file"] = str(args.input) if args.input else "<stdin>"

    if args.format == "json":
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print(render_human(result))
    return 0


if __name__ == "__main__":
    sys.exit(main())
