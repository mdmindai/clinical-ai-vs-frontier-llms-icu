# Study 3 — Reference quality (100 questions, 5 systems)

Quality of the references each system cited when answering the same 100 ICU questions as Study 2
(same answers, October 2026). Outcome: a blinded panel of three LLM judges grades each system's
reference list.

## Result

| System | Relevance | Evidence level | Recency | Sufficiency | **Overall** |
|---|---|---|---|---|---|
| OpenEvidence | 3.44 | 3.26 | 3.60 | 3.27 | **3.39** |
| MDmind | 3.55 | 3.15 | 3.21 | 3.29 | **3.30** |
| gpt-5.5 | 3.41 | 3.37 | 3.31 | 2.80 | **3.22** |
| Gemini 3.1 Pro | 2.00 | 1.46 | 2.21 | 1.67 | **1.83** |
| Claude Opus 4.8 | 1.97 | 1.54 | 1.97 | 1.74 | **1.81** |

Mean of the 3 judges, scale 1–4; overall = mean of the 4 axes (exact means, rounded half-up).

- **Friedman χ² = 193.4, p < 0.001.** Paired Wilcoxon, Holm-adjusted: **MDmind vs OpenEvidence
  Δ −0.09, p = 0.16**; MDmind vs gpt-5.5 Δ +0.08, p = 0.53; OpenEvidence > gpt-5.5 (Δ +0.17,
  p = 0.042); OpenEvidence, MDmind and gpt-5.5 > Claude and Gemini (p < 0.001); Claude vs Gemini
  p = 0.78.
- MDmind vs OpenEvidence by axis (unadjusted p): relevance +0.11 (p = 0.26), sufficiency +0.02
  (p = 1.00), evidence level −0.12 (p = 0.14), recency −0.39 (p < 0.001).
- **Answers without any reference** score 1 on every axis (all three judges did so in all 110 such
  lists): Claude 59/100, Gemini 48/100, OpenEvidence 3/100, MDmind and gpt-5.5 0/100. With web search
  optional, Claude searched in 41 and Gemini in 52 of the 100 questions; their answers carry
  references only when they searched. Among lists that have references, the overall scores are
  OpenEvidence 3.47 (n = 97), MDmind 3.30, gpt-5.5 3.22, Claude 2.97 (n = 41) and Gemini 2.60 (n = 52):
  the gap of Claude and Gemini comes mostly, but not only, from answers without sources.
- Overall by judge (MDmind / OpenEvidence / gpt-5.5 / Claude / Gemini) — gpt-5.5 judge: 3.13 / 3.32 /
  3.27 / 1.76 / 1.81; Gemini judge: 3.26 / 3.38 / 3.15 / 1.79 / 1.80; Claude judge: 3.51 / 3.47 / 3.25 /
  1.87 / 1.89. The order among OpenEvidence, MDmind and gpt-5.5 depends on the judge; the gap to Claude
  and Gemini holds with any one judge left out (p < 0.001). Leaving out the Claude judge, OpenEvidence
  is ahead of MDmind (unadjusted p = 0.009).
- **Sensitivity analyses** (same conclusions):
  - *Judges without web search* (graded October 19, 2026; Claude `max_tokens` 4,096): OpenEvidence 3.42, MDmind 3.34, gpt-5.5 3.28,
    Gemini 1.85, Claude 1.83; MDmind vs OpenEvidence Δ −0.08, Holm p = 0.25; OpenEvidence > gpt-5.5,
    p = 0.047 (`data/panel_sensitivity_no_search/`).
  - *Coarse types* (no web search; only four coarse types — paper / guideline/society / drug/label /
    other — titles truncated at 140 characters and no current year; graded October 18, 2026):
    OpenEvidence 3.51, MDmind 3.45, gpt-5.5 3.35, Gemini 1.90, Claude 1.85 (MDmind vs OpenEvidence
    Δ −0.06, Holm p = 0.24; OpenEvidence > gpt-5.5, p = 0.003) (`data/panel_sensitivity_coarse_types/`).

| | Unique references | Per question | Answers with ≥1 reference | Indexed in PubMed | Non-scientific sources |
|---|---|---|---|---|---|
| MDmind | 710 | 7.1 | 100 | 94% | 0% (0 answers) |
| OpenEvidence | 675 | 6.8 | 97 | 92% | 0% (0 answers) |
| gpt-5.5 | 358 | 3.6 | 100 | 58% | 3% (9 answers) |
| Claude Opus 4.8 | 302 | 3.0 | 41 | 52% | 20% (31 answers) |
| Gemini 3.1 Pro | 427 | 4.3 | 52 | 24% | 34% (45 answers) |

"Unique" = after removing duplicates within the same answer; "per question" divides by all 100
questions. Non-scientific sources = educational websites/blogs, social media, wikis, exam-question
sites, file-sharing platforms and AI-generated content (share of the system's references, and number
of answers citing at least one). Claude: 52 blogs/educational sites, 5 AI-generated, 3 wikis; Gemini:
102 blogs/educational sites, 17 exam-question sites, 17 file-sharing platforms, 7 social media, 2
wikis, 1 AI-generated; gpt-5.5: 10 blogs/educational sites.

## Method

**What counts as a cited reference.** MDmind: the reference list returned with the answer (at the
top of the text). OpenEvidence: the numbered reference list (copied with OpenEvidence's copy button,
with DOIs). gpt-5.5: the `url_citation` annotations of the response; Gemini: the grounding chunks
(redirect links resolved to the target page); Claude: the citations attached to its text blocks.
Duplicates within the same answer (same PMID or same page, including proxy URLs of the same page)
count once: 36 removed, 2,472 unique references.

**Classification of each reference** (`data/references.csv`, and the publication type shown to the
judges). Identifiers were resolved in PubMed (PMID/PMC/DOI in the link; OpenEvidence by DOI; LLM web
pages by URL, page metadata or title; LLM agents opened 776 of these pages to record their metadata).
Articles take the PubMed *Publication Type* when it describes the design. Otherwise the type was
assigned by two independent LLM agents (Claude Opus 5.5 and, in the design re-reading, Claude Fable
5.1; agreement on design κ = 0.86), with disagreements decided by the researcher; the researcher also
classified or checked the boundary categories (e.g. guideline vs consensus vs other). Non-article
sources have their own categories. `type_assigned_by` records the route for each reference:
- `pubmed_design_label`: PubMed Publication Type;
- `design_rereading_two_blind_readers`, `two_readers_from_pubmed_abstract`: two independent agents
  (in the design re-reading, blind to the citing system), disagreements decided by the researcher;
- `researcher_classification_or_check`: classified or checked by the researcher;
- `fda_label_rule`: drug-label pages (DailyMed/FDA) → drug label; `domain_rule`: type fixed by the
  website domain (e.g. social media, wikis, drug databases);
- `reader_opened_page_validated_by_sample`: an agent opened the page and assigned the type (a blind
  second agent re-read the pages; see `agents/REGISTRY.md`);
- `inaccessible_confirmed_by_researcher`, `propagated_from_same_document`.

Every LLM agent used (model, exact instruction, output) is listed in `agents/REGISTRY.md`.

**Panel.** Judges: gpt-5.5, Gemini 3.1 Pro (`gemini-3.1-pro-preview`) and Claude Opus 4.8
(`claude-opus-4-8`), through their APIs on October 21, 2026, with the same settings as the Study 2
judges: default parameters (Claude: `max_tokens`, which the Anthropic API requires and has no default, set to
16,000; no reply was truncated) and **optional web
search** (the judge decides whether to search; how often it searched was not recorded). Each judge saw the question and the five reference lists, anonymized as A–E in a
per-question order fixed by a hash of question and system (`data/panel/blind_map.json`). Each item is
shown as *title — year, type, source* (`data/panel/blind_sets.json`):
- **title**: the full verified title, without our annotations (one title, `claude_178_9`, kept an
  internal note, "Guideline Essentials — resumo da diretriz ATS 2024", and was shown with it);
- **year**: "n.d." when the source has no date (145 items, all outside PubMed); the prompt states that
  the current year is 2026;
- **type**: the publication type from our final classification — Practice guideline, Consensus
  statement, Government guidance, Systematic review/meta-analysis, Randomized controlled trial,
  Non-randomized trial, Observational study, Case report/series, Narrative review,
  Letter/editorial/comment, Point-of-care reference, Book/chapter, Drug label/database, Educational
  website/blog, Social media, Wiki, File-sharing platform, Exam-question site, Inaccessible (could not be
  opened), Other —
  with "(conference abstract)", "(preprint)", "(preclinical study)" or "(AI-generated content)" added
  when applicable;
- **source**: the journal for PubMed-indexed items, the website domain for web pages, otherwise the
  name given by the system.

Prompt: `code/rubric_panel.md` (study-specific rubric). Replies that could not be parsed were re-asked
(up to 5 attempts).

**Statistics.** Per question and list, the 12 scores (3 judges × 4 axes) are summed; Friedman across
the 5 systems and paired Wilcoxon (two-sided, zero differences dropped) on these integer sums, Holm
correction across the 10 pairs.

## Limitations
- **LLM judges that are also evaluated systems**; no human-expert grading yet. The order among the top
  three depends on the judge (see above).
- **The no-reference rule** (score 1) drives most of Claude's and Gemini's gap; it reflects that these
  models often answered without searching.
- **Judges are shown metadata only** (title, year, publication type, source), not the documents; they
  could search the web, but how much they checked is unknown.
- **The publication type shown to the judges comes from our classification.** Most MDmind and OpenEvidence
  references carry PubMed labels, whereas most LLM web sources were classified by agents and the
  researcher.
- **The researcher who classified or checked 628 of the 2,472 types directly (Gemini 261, gpt-5.5 179,
  Claude 145, OpenEvidence 40, MDmind 3), and also decided the readers' disagreements and confirmed the
  8 inaccessible items, develops MDmind** and was not blinded to the citing system.
- **No significant difference is not equivalence** (MDmind vs OpenEvidence).
- **Questions come from MDmind users.**

## Reproduce

```bash
cd code
python aggregate_panel.py                                 # -> results/panel_results.json
python aggregate_panel.py panel_sensitivity_no_search      # -> results/panel_results_sensitivity_no_search.json
python aggregate_panel.py panel_sensitivity_coarse_types   # -> results/panel_results_sensitivity_coarse_types.json
python build_panel_lists_detailed.py                      # rebuilds data/panel/blind_map.json and blind_sets.json
```
Requires `numpy` and `scipy` (`code/requirements.txt`; published results produced with Python 3.9,
numpy 2.0.2, scipy 1.13.1); no API keys. `judge_panel.py` (runs the judges; API keys needed) and
`build_panel_lists.py` (coarse-type lists of the sensitivity analysis) are included as run: they read
the internal working files, whose columns are the Portuguese originals of `references.csv`
(`tipo_final` = `type_code`, `titulo_verificado` = `verified_title`, `titulo_citado` = `cited_title`, `revista_ou_organizacao` =
`journal_or_organization`, `ano` = `year`, `duplicata_de` = `duplicate_of`, `sistema` = `system`,
`pergunta_idx` = `question_idx`), and write `notas_{judge}.json`, shipped here as
`grades_{judge}.json`.

## Files

```
data/questions_icu_100.csv   the 100 questions (same as Study 2)
data/references.csv          one row per cited reference, all 5 systems (dictionary below)
data/panel/blind_map.json    per question: A–E -> system
data/panel/blind_sets.json   per question: the question and the five anonymized reference lists
data/panel/grades_{openai,gemini,claude}.json   scores per question, per list (A–E), per axis
data/panel_sensitivity_no_search/      same lists, judges without web search (sensitivity)
data/panel_sensitivity_coarse_types/   coarse-type lists, judges without web search (sensitivity)
results/                     outputs of aggregate_panel.py (main and sensitivity)
code/                        aggregate_panel.py, rubric_panel.md, build_panel_lists_detailed.py,
                             build_panel_lists.py, judge_panel.py
agents/                      REGISTRY.md, prompts/ (instruction + output of each agent), scripts_workflow/
```

### `data/references.csv`
Rows with a non-empty `duplicate_of` are within-answer duplicates (they carry the type of the first
occurrence); exclude them to get the 2,472 unique references.

| Column | Meaning |
|---|---|
| `ref_id` | `<system>_<question_idx>_<position>` |
| `system` | mdmind, oe (OpenEvidence), gpt5, claude, gemini |
| `question_idx` | Question identifier (joins to `idx` in `questions_icu_100.csv`) |
| `ref_n` | Position of the reference in the answer |
| `cited_title` | Reference as cited by the system |
| `verified_title` | Resolved title (PubMed when indexed) |
| `journal_or_organization` | Journal (PubMed) or publishing organization |
| `year` | Publication year (empty when unknown) |
| `pmid`, `doi`, `url` | Identifiers (`url` empty for OpenEvidence, which gives no links) |
| `indexed_pubmed` | True if the reference has a PubMed record |
| `type_code` | Internal category code (Portuguese; mapping below) |
| `category` | Source category (PubMed-style names for articles; see below) |
| `trial_subtype` | For trials: randomized / non_randomized |
| `system_label_removed` | Label the system attached to the reference (removed before judging) |
| `duplicate_of` | `ref_id` of the first occurrence when duplicated within the same answer |
| `drug_subtype` | For drug labels: official_label / drug_database / institutional_formulary |
| `web_subtype` | For websites: institutional / independent / news |
| `flag` | Extra qualifier: letter, editorial, expert_opinion, committee_opinion, conference_abstract, preprint, thesis, preclinical_study, diagnostic_accuracy, before_after_or_historical_control, case_series_from_literature, trial_protocol, review_protocol, technology_assessment, guideline_or_consensus, guideline_key_points, guideline_summary_third_party, institutional_protocol, institutional_guide, implementation_toolkit, management_algorithm, drug_formulary, regulatory_document, legislation, technical_opinion_for_court, patent, workshop_report, experience_report, journal_issue, book, slides, course_handout, teaching_material, laboratory_manual, professional_audience, lay_audience, veterinary_content, veterinary_handout, ai_generated_content, aggregator, copy_of_article, copy_of_point_of_care_reference, questionable_republication, isolated_figure, author_profile |
| `government_issuer` | True for practice guidelines or consensus statements issued by a government body (Government guidance is a category of its own) |
| `type_assigned_by` | Route by which the type was assigned (see *Method*); unique references: pubmed_design_label 1,223 · researcher_classification_or_check 628 · design_rereading_two_blind_readers 364 · two_readers_from_pubmed_abstract 113 · fda_label_rule 63 · domain_rule 42 · reader_opened_page_validated_by_sample 30 · inaccessible_confirmed_by_researcher 8 · propagated_from_same_document 1 (2 duplicate rows: reader_guideline_vs_consensus) |

`type_code` → `category`: diretriz → Practice Guideline (requires formal evidence grading when there
is no PubMed label) · consenso_especialistas → Consensus Statement · revisao_sistematica_metanalise →
Systematic Review / Meta-Analysis · ensaio_clinico → Randomized Controlled Trial or Clinical Trial
(non-randomized) · estudo_observacional and relato_serie_casos → Observational Study / Case Reports ·
revisao_narrativa → Review · outro → Letter / Editorial / Comment or Other · livro_capitulo → Book /
chapter · bula_label → Drug label / drug database · referencia_clinica → Point-of-care reference
(UpToDate, DynaMed, BMJ Best Practice, Medscape Reference, Merck Manual) · orientacao_oficial →
Government guidance · site_educativo_blog → Educational website / blog · rede_social → Social media ·
wiki → Wiki · plataforma_upload → File-sharing platform · questao_prova → Exam-question site ·
inacessivel → Inaccessible.

## Ethics and conflict of interest
See `../ETHICS_COI.md` (applies to all three studies).
