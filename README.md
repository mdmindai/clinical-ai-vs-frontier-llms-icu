# MDmind vs. frontier LLMs & OpenEvidence — Intensive Care Medicine

Comparative evaluation of **MDmind** (a Brazilian PubMed-RAG clinical tool), **OpenEvidence** (a
commercial clinical-RAG tool) and three frontier general-purpose LLMs (**gpt-5.5**, **Gemini 3.1
Pro**, **Claude Opus 4.8**) in Intensive Care Medicine, in three studies. The methodology follows
Vishwanath et al., *Nature Medicine* 2026 (doi:10.1038/s41591-026-04431-5).

> **Conflict of interest.** One of the authors (T. C. Carnin) develops MDmind. See `ETHICS_COI.md`.

## Results

| | Measures | n | Result |
|---|---|---|---|
| **[Study 1](study1_knowledge/)** | Knowledge (multiple choice, official keys) | 360 board-exam items (TEMI 2020–2025) | Gemini 93.3% and gpt-5.5 91.9% **ahead of** Claude 86.7%, OpenEvidence 86.1% and MDmind 85.3% (Holm p ≤ 0.004); MDmind vs OpenEvidence p = 1.00 |
| **[Study 2](study2_quality/)** | Answer quality (RCQ rubric, blinded 3-LLM panel) | 100 real ICU questions | **gpt-5.5 3.89** ahead of all (p < 0.001); Gemini 3.59, Claude 3.54, MDmind 3.50 and OpenEvidence 3.46 with no significant difference (MDmind vs OpenEvidence p = 0.90) |
| **[Study 3](study3_references/)** | Reference quality (blinded 3-LLM panel) | the same 100 questions | **OpenEvidence 3.39, MDmind 3.30 and gpt-5.5 3.22** ahead of Gemini 1.83 and Claude 1.81 (p < 0.001); MDmind vs OpenEvidence p = 0.16; OpenEvidence > gpt-5.5 (p = 0.042); non-scientific sources (blogs, social media, exam-question sites…) 0% for MDmind and OpenEvidence, 3% gpt-5.5, 20% Claude, 34% Gemini |

In Studies 2 and 3 every system answered the bare question; the three LLMs used default API
parameters with optional web search (Claude and Gemini chose to search, and therefore cited sources,
in 41 and 52 of the 100 questions). Results are from October 2026.

## Reproduce

Each study runs from its own folder (Python ≥ 3.9; Studies 2 and 3 need `numpy` and `scipy`):

```bash
(cd study1_knowledge/results && python analysis.py)
(cd study2_quality/code && python aggregate.py)
(cd study3_references/code && python aggregate_panel.py)
```

The scripts recompute the main results (tables and tests) from the answers and judge scores shipped
here; the other descriptive numbers can be derived from the shipped files. No API keys are needed. Each study's README describes its data files and fields.

## Layout

```
study1_knowledge/    360-item knowledge benchmark (no exam text or answer keys — copyrighted)
study2_quality/      100 questions, answers, judge scores (RCQ rubric)
study3_references/   classification of every cited reference (2,472 unique), judge scores of the reference lists
ETHICS_COI.md        conflict of interest, ethics, third-party terms (all studies)
```

## Notes

- **Judges are LLMs, not human experts**; a human-intensivist validation is the planned next step.
- **OpenEvidence answer text is not redistributed** (its Terms of Use); its scores and the
  bibliographic metadata of the references it cited are included.

## Citation

Carnin TC, Westphal GA, Salluh JIF. Clinical AI tools vs. frontier LLMs in intensive care medicine:
three-study benchmark. https://github.com/mdmindai/clinical-ai-vs-frontier-llms-icu (2026).

Please also cite Vishwanath et al., *Nat Med* 2026, doi:10.1038/s41591-026-04431-5.

## License

Code: MIT. Data: CC-BY-4.0.
