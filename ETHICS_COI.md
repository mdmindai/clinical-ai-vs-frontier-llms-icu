# Ethics, data protection and conflict of interest (all three studies)

## Conflict of interest
One of the authors (T. C. Carnin) develops **MDmind**, one of the evaluated systems. This study received no funding. MDmind's
answer synthesis uses OpenAI models; gpt-5.5 is both an evaluated system and one of the judges.
To keep the evaluation defensible despite this conflict:
- **Objective scoring where possible** — Study 1 is scored against the official exam answer keys.
- **Blinded grading** — in Studies 2 and 3, answers and reference lists are anonymized and shuffled
  per question; the judges do not know which system produced them.
- **Published rubrics** — Study 2 uses the RCQ instrument (Vishwanath et al., *Nature Medicine*
  2026) with its axes and scoring anchors verbatim; the additions to the judge prompt are listed in
  `study2_quality/code/rubric.md`. Study 3 uses a study-specific rubric (`study3_references/code/rubric_panel.md`).
- **Three independent judges** from three vendors (OpenAI, Google, Anthropic), averaged.
- **Open data and code** — everything needed to recompute the results ships in this repository.
- A **human-expert (intensivist) validation** of the LLM-judge panel is the planned follow-up and is
  required before any strong clinical claim.

## Questions and ethics review (Studies 2 and 3)
- The 100 questions were typed by health-care professionals (intensivists / ICU residents) in the
  MDmind product. Only the question text is published — no user identity, dates or other metadata.
  The questions are clinical questions and contain no patient-identifiable information (no names,
  dates of birth, record numbers or bed identifiers), so no de-identification step was needed.
- MDmind's terms of use allow this use of the questions.
- The question text was sent to each evaluated system (OpenAI, Google and Anthropic APIs,
  OpenEvidence's web interface, and MDmind's own pipeline) to generate the answers.
- **Ethics review:** the study has not yet been submitted to the Brazilian research-ethics system
  (CEP/CONEP, Plataforma Brasil).

## Exam material (Study 1)
- The TEMI/AMIB exam items are copyrighted and not licensed for redistribution. Item stems, answer options, the official
  answer keys, the letters chosen and the systems' full response texts are **not** published; only
  item identifiers, provenance (exam/year) and whether each system answered correctly.

## Third-party terms of use
- **OpenEvidence** answer text is **not redistributed** (its Terms of Use prohibit it). Published:
  per-question scores, aggregate metrics and the bibliographic metadata of the references
  OpenEvidence cited (Study 3). OpenEvidence was used manually through its web interface (no
  automated access or scraping), with default settings.
- **Frontier LLM** answers were generated through the providers' official APIs.

## Versioning
AI systems evolve. Model versions and collection dates are recorded; results are a point-in-time
snapshot (Study 1: July 2026, with re-runs in October 2026; Studies 2 and 3: October 2026).
