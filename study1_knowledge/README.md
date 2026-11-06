# Study 1 — Knowledge (360 items, TEMI 2020–2025)

Accuracy of five AI systems on objective-format items from the Brazilian intensive care board
examination, scored against the official answer keys.

> **Note on exam content.** The TEMI/AMIB exam items are copyrighted and not licensed for
> redistribution. For that reason, **item stems and answer options are not published
> here, nor the official answer keys or the letters chosen**: only the item identifier, provenance
> (exam/year) and whether each system answered correctly. The chosen letters are omitted because,
> together with the correct/incorrect flag, they would reveal the answer key. This preserves full statistical
> reproducibility — `analysis.py` uses only these fields — without redistributing copyrighted
> content.
>
> All items and answer keys come from the book below (the 2025 items and key were taken directly from
> the official exam PDF, which the book also covers):
> SANTOS, Yuri de Albuquerque Pessoa dos; LADEIRA, José Paulo; AZEVEDO, Luciano César Pontes de
> (eds.). *Questões comentadas para o TEMI: Título de Especialista em Medicina Intensiva*. 1st ed.
> ISBN 978-85-204-7330-6. Anyone wishing to reproduce the analysis with the original item text can
> obtain the book and cross-reference by `orig_q`/`source` in each row of
> `questions/bench360_questions.csv`.

## Result

| System | Accuracy | Correct | 95% CI |
|---|---|---|---|
| Gemini 3.1 Pro | 93.3% | 336/360 | 90.3–95.5 |
| gpt-5.5 | 91.9% | 331/360 | 88.7–94.3 |
| Claude Opus 4.8 | 86.7% | 312/360 | 82.8–89.8 |
| OpenEvidence | 86.1% | 310/360 | 82.2–89.3 |
| MDmind | 85.3% | 307/360 | 81.2–88.6 |

*Wilson 95% CI*

**Cochran's Q = 36.6; p < 0.001.** Two groups: {Gemini, gpt-5.5} above {Claude, OpenEvidence,
MDmind}. All pairs *between* groups are significant (exact McNemar, Holm-adjusted p ≤ 0.004); all
pairs *within* each group show no significant difference (p = 1.00). MDmind vs OpenEvidence: 21 items
only MDmind got right vs 24 only OpenEvidence got right.

## How to reproduce

```bash
cd results && python analysis.py
```
No external dependencies. Reads `questions/bench360_questions.csv` + `answers/*_360.jsonl` and
recomputes accuracy, CIs, Cochran's Q, pairwise McNemar with Holm correction, and the per-exam
breakdown. The frozen output is in `results/results.txt`.

## Experimental condition

- **Bare question, no preamble** for all five systems — just the stem and options A–D, exactly as
  OpenEvidence receives it through the web interface.
- **Three LLMs only:** a minimal instruction to state the letter at the end, sent as a *system
  prompt* (not appended to the question), to make extraction reliable. MDmind and OpenEvidence
  received the bare question with no instruction (OpenEvidence's web interface has no system
  prompt).
- **Web search available** to the three LLMs (optional — the model decides whether to use it).
- **Models pinned by version ID**: `claude-opus-4-8`, `gpt-5.5`, `gemini-3.1-pro-preview`.
- **Default API parameters**: gpt-5.5 at its default reasoning effort (medium); Claude without
  extended thinking; Gemini with its default thinking. No temperature set.
- **Single-answer rule.** When a system did **not commit to a single option** (rejected all four or
  endorsed more than one), the item was **re-asked once with a forced-choice instruction**:
  *"You MUST choose exactly one option (A, B, C or D). Even if no option seems perfect, choose the
  most correct one — you may not say that none is correct nor point to more than one. End with the
  exact line: RESPOSTA: X"* (sent in Portuguese). The re-asked answer is the one scored. This
  happened for **13 MDmind items** (q59, q62, q72, q86, q94, q118, q120, q125, q158, q165, q304,
  q352, q356; 10 correct after re-asking) and **1 OpenEvidence item** (q13; correct). The three
  LLMs always committed to one letter. In `answers/*.jsonl`, `condition` records which path each
  item took.

## Structure

```
questions/         bench360_questions.csv — id and provenance (exam/year) per item
                   (no stem, options or answer key — copyrighted)
answers/           the results — 5 files, one per system
results/           analysis.py (reproducible), results.txt
```

### Column/field legend

`questions/bench360_questions.csv`:

| Column | Meaning |
|---|---|
| `q` | Item identifier (1–361; see note below on numbering) |
| `source` | Which exam the item came from: `AMIB2020`–`AMIB2024` and `TEMI2025` (the exam is the TEMI, run by AMIB; the label follows the source document) |
| `orig_q` | The item's original number within that specific exam |

> **Note on numbering.** `q` runs from 1 to 361 but has exactly 360 unique values — `q=246` was
> never assigned. An item originally given that number was dropped during curation (duplicate or
> image-dependent) after IDs had already been handed out; rather than renumber everything, the gap
> was left in place. It has no effect on the analysis, which matches records by `q`, not by
> sequence.

Each line of `answers/*.jsonl` carries:

| Field | Meaning |
|---|---|
| `q` | Item identifier, joins to `questions/bench360_questions.csv` |
| `exam` | Same as `source` above |
| `orig_q` | Same as `orig_q` above |
| `correct` | Whether the system's answer matched the official key |
| `condition` | `direct answer (no preamble)`; `direct answer (no preamble), re-run Oct 2026` (MDmind q1–q42); or `re-asked with forced single choice (no single option committed in the direct answer)` (13 MDmind items, OpenEvidence q13) |
| `latency_s` | Response latency in seconds (not recorded for OpenEvidence) |
| `tokens` | Token usage (recorded only for some LLM items; null for MDmind and OpenEvidence) |

Each system's full response text is not published, for the same reason as the item stems —
free-text answers to multiple-choice items tend to reproduce enough of the stem to reconstruct it.

## How the item set was built

Of the **540 items** across the six exams, excluded were:
- items that **require a figure, chart, ECG, or image** to answer;
- items **annulled** by the official key;
- **duplicate** items across years.

That left **360 text-answerable items**. Items and keys for 2020–2024 come from the book cited
above; the 2022–2024 keys were transcribed from page images and cross-checked by **independent
double reading** (two agents, each with no access to the other's work): 100% agreement across all
90 lines of each exam. The 2025 exam and its answer key were extracted directly from the official
PDF.

## Collection
- Three LLMs, MDmind and OpenEvidence: July 25–31, 2026. MDmind was queried through its production
  pipeline; OpenEvidence manually through its web interface.
- MDmind q1–q42 re-run under the bare condition: October 14, 2026. Forced-choice re-asks (13 MDmind
  items, OpenEvidence q13): October 15, 2026.

## Limitations

- **Letter extraction.** The LLMs end with the instructed line "RESPOSTA: X" (checked: 360/360
  consistent for each). MDmind and OpenEvidence answer in prose without a format instruction, so
  their letters were read from the full text by LLM agents (no regex). Every answer of both tools, right or wrong, was then re-checked, finding 13 MDmind items and 1
  OpenEvidence item with no single committed option; they were re-asked under the single-answer rule
  above.
- **MDmind items q1–q42** were originally scored from an older run that used a preamble; they
  were re-run in October 2026 under the same bare condition as the other items and read by three
  agents independently. **This lowered MDmind's score:** 40/42 correct with the preamble, 37/42
  under the bare condition.
- **Net effect of the October 2026 corrections on MDmind: 311 → 307/360 (86.4% → 85.3%).** Besides
  the −3 above, the single-answer rule cost one more item: of the 13 items where MDmind had not
  committed to one option, 11 had been counted correct because the extracted letter matched the key
  by chance; after re-asking, 10 were correct. OpenEvidence went from 309 to 310/360 (its one
  re-asked item, q13, was answered correctly).
- **Independent check.** Running all 360 MDmind items with the forced-choice instruction from the
  start gives the same total, 307/360.
- **Not verifiable from the shipped files:** the pre-correction scores (40/42, 311, 309), the
  forced-choice-from-the-start run and the letter-extraction and double-reading checks come from
  internal working data that is not published here (it contains the full response texts).
- **Asymmetric instructions.** The LLMs were told from the start to end with a letter; MDmind and
  OpenEvidence received only the bare item and were asked to choose only when they did not commit.
- **Possible contamination.** Items from earlier exams circulate in books and online and may be in
  the models' training data or reachable through web search (available to the three LLMs); the 2025
  exam (q1–q42) is the least exposed. Per-exam accuracy is in `results/results.txt`.
- **Deduplication is lexical.** Pairs testing the same fact with different wording are not
  detected, introducing mild dependence between items.
- **Power.** With n = 360, differences of a few percentage points may not reach significance after
  Holm correction (the smallest significant gap here is 5.3 points); the MDmind-vs-OpenEvidence tie
  means "if there is an advantage, it is small," not "they are identical."
- **Disputable answer keys may exist.** All five systems missed the same 8 items (q175, q194, q232,
  q252, q257, q260, q287, q302), which may indicate a problem with the key; they were kept (no
  sensitivity analysis excluding them).

## Ethics and conflict of interest
See `../ETHICS_COI.md` (applies to all three studies).
