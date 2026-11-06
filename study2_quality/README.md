# Study 2 — Answer quality (RCQ rubric), 100 real ICU questions

Blinded evaluation of **MDmind** (a Brazilian PubMed-RAG clinical tool), **OpenEvidence** and three
frontier general-purpose LLMs (**gpt-5.5**, **Gemini 3.1 Pro**, **Claude Opus 4.8**) on 100 **real**
clinical questions asked by intensivists and ICU residents in the MDmind product (question text only, no user data).

Answers are graded on the **RCQ rubric** of Vishwanath et al., *Nature Medicine* 2026
(doi:10.1038/s41591-026-04431-5), axes and anchors used verbatim: correctness, safety, completeness and clarity
(1–4 each), by a **blinded panel of three LLM judges**
(gpt-5.5, Gemini 3.1 Pro, Claude Opus 4.8), averaged.

> **Conflict of interest.** One of the authors (T. C. Carnin) develops MDmind. Mitigations: blinded and shuffled grading,
> the published rubric (axes and anchors verbatim; see `code/rubric.md` for the additions), three
> independent judges from three vendors, and full release of data and code. See `../ETHICS_COI.md`.

## Result (October 2026, n = 100)

| System | Correctness | Safety | Completeness | Clarity | **Overall** |
|---|---|---|---|---|---|
| gpt-5.5 | 3.92 | 3.97 | 3.74 | 3.94 | **3.89** |
| Gemini 3.1 Pro | 3.44 | 3.53 | 3.47 | 3.93 | **3.59** |
| Claude Opus 4.8 | 3.59 | 3.46 | 3.35 | 3.78 | **3.54** |
| MDmind | 3.50 | 3.54 | 3.65 | 3.31 | **3.50** |
| OpenEvidence | 3.44 | 3.42 | 3.41 | 3.57 | **3.46** |

Overall = mean of the 4 axes, averaged over the 3 judges.

- **Friedman χ² = 101.4, p < 0.001.** gpt-5.5 is ahead of every other system (paired Wilcoxon,
  Holm p < 0.001).
- **No significant difference among Gemini, Claude, MDmind and OpenEvidence** (all Holm p > 0.08).
  **MDmind vs OpenEvidence: Δ +0.04, Holm p = 0.90.**
- MDmind has the second-highest completeness (after gpt-5.5) and the lowest clarity (axis differences
  not tested).
- Overall by judge (gpt-5.5 / Gemini / Claude / MDmind / OpenEvidence) — gpt-5.5 judge: 3.97 / 3.49 /
  3.42 / 3.41 / 3.32; Gemini judge: 3.84 / 3.75 / 3.56 / 3.55 / 3.49; Claude judge: 3.87 / 3.55 / 3.66 /
  3.55 / 3.57. Each judge rates its own model above the other two judges do (most for Gemini: 3.75 vs
  3.49–3.55); averaging the three judges dilutes this. gpt-5.5's lead holds with any one judge left out.

## Question selection
The 100 questions were drawn from questions actually asked in MDmind by users identified as
intensivists or ICU residents, after excluding test/development accounts, duplicates and oversized
pastes. Sampling was stratified across 11 ICU sub-domains (`sub_domain`) and weighted by real usage.
The question text is published as typed (Portuguese); it contains no patient-identifiable
information.

## Experimental condition

- **Bare question** (no preamble, no system prompt), exactly as typed by the clinician.
- **Default API parameters for every model**: gpt-5.5 (Responses API, default reasoning effort; the
  API returned `gpt-5.5-2026-04-23`), Gemini 3.1 Pro (`gemini-3.1-pro-preview`, default thinking),
  Claude Opus 4.8 (`claude-opus-4-8`, no extended thinking; `max_tokens`, which the Anthropic
  API requires and has no default, set to 16,000). No temperature set.
- **Web search available and optional** — the model decides whether to search (gpt-5.5 `web_search`,
  Gemini `google_search`, Claude `web_search_20250305`). gpt-5.5 searched in 100, Gemini in 52 and
  Claude in 41 of the 100 questions.
- **MDmind**: its PubMed-RAG backend (the production code; not public) run locally at commit
  `b0b150b` with default settings, bare question, one question at a time. Graded as returned, with its
  reference list at the top of the answer. With the list moved to the end (no other change), MDmind
  scored 3.53 instead of 3.50 (clarity 3.43 vs 3.31), with the same conclusions (that grading is not
  shipped).
- **OpenEvidence**: no API; answers collected manually through the web interface (new conversation
  per question, October 16–17, 2026).
- **Answers are graded exactly as each system returned them** (e.g., some Claude answers begin with
  its search narration).
- **Judges**: same three models and settings as above (web search optional; how often the judges
  searched was not recorded), each seeing the question
  and the five answers anonymized as A–E in a per-question shuffled order (`data/blind_map.json`).
  The Study 3 judges use the same settings.

### OpenEvidence: text version graded
OpenEvidence answers were first copied by **selecting the rendered text**, because in an earlier
collection OpenEvidence's copy button had truncated some answers. That copy carries
artifacts that the other systems' answers do not have: reference lists without links/DOIs and with
OpenEvidence's labels glued to them ("…et al.Observational", "RecentSR"), and **figure captions
without the figure** ("Figure 2 … Used under license from Wiley"). The answers were therefore
re-copied from the **same conversations** with OpenEvidence's own **copy button** (complete reference
list with DOIs, no labels), and the figure/table blocks that arrive without their image were removed
(`code/oe_clean_version.py`; nothing else in the text was changed). A content-level comparison of
the two copies (all 100 answers) found the same text and the same reference lists, i.e. the copy
button did not truncate any of these answers. The analysis grades this version.

Grading the text-selection copy instead lowered OpenEvidence by about 0.1 (mostly clarity) in an
earlier grading of these answers, without changing the conclusions; the main analysis therefore uses
the version most favourable to OpenEvidence (that grading is not shipped).

## Limitations
- **LLM judges that are also evaluated systems** (self-preference noted above); no
  human-expert grading yet. Agreement between judges on per-answer overall scores is moderate
  (Spearman 0.44–0.53), and scores cluster near the ceiling (most gpt-5.5 scores are 4).
- **The judge prompt asks to grade the medicine, not the language or formatting**, while the clarity
  axis grades structure and readability; this may damp clarity differences.
- **Blinding is by label only**: style can reveal the system (MDmind's reference block at the top, OpenEvidence's
  DOI list, Claude's search narration). Judges graded raw markdown, not rendered output.
- **Questions come from MDmind users**, which may favour MDmind's domain.
- **No significant difference is not equivalence**; no equivalence margin was tested.

## Reproduce

```bash
cd code
python aggregate.py        # -> results/results.json
```
Requires `numpy` and `scipy` (published results produced with Python 3.9, numpy 2.0.2, scipy 1.13.1).
No API keys: everything is recomputed from the judge scores shipped here.

To regenerate answers or grades (API keys needed): `code/generate_answers_llms.py`,
`code/generate_answers_mdmind.py`, `code/judge.py` (prompt = `code/rubric.md`). These are the scripts
exactly as run; their input/output paths point to the internal working repository.

## Files

```
data/questions/questions_icu_100.csv                 the 100 questions
data/answers/answers_{mdmind,gpt5,gemini,claude}.jsonl   answers as returned (OpenEvidence withheld)
data/blind_map.json                                  per question: A–E -> system
data/grades/grades_{openai,gemini,claude}.jsonl      scores per question, per system
results/                                             outputs of aggregate.py
code/                                                aggregate.py, rubric.md (judge prompt), judge.py,
                                                     generate_answers_*.py, oe_clean_version.py
```
Questions and answers are in Portuguese.

`questions_icu_100.csv`: `idx` (question identifier, non-contiguous, 4–1258), `sub_domain` (ICU
sub-area), `smart_score` (curation score from the question-selection step; "(pick)" = hand-picked;
empty for idx 789), `pergunta` (question text).

`answers_*.jsonl`, one line per question: `idx`, `model`, `sub_domain`, `pergunta` (question),
`answer` (text graded), `latency` (s), `gerado_em` (generation time, UTC), `error`. LLMs only:
`refs` (sources cited: list of `{title, url}`; Gemini also `redirect`), `n_buscas` (number of web
searches), `modelo_api` (model ID returned by the API). MDmind only: `backend_commit`. For MDmind, `answer` is the text exactly as returned (the
`answer_raw` of `generate_answers_mdmind.py`), which is what the judges received.

`grades_*.jsonl`, one line per question: `idx`, `judge`, `scores` (keyed by system name, already
un-blinded: the 4 axes, 1–4), `modelo_api`, `error`.

OpenEvidence answers are **not redistributed** (its Terms of Use); their scores are included.

## License
See `../LICENSE`.
