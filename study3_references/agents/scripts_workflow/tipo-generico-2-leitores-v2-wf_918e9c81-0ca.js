export const meta = {
  name: 'tipo-generico-2-leitores-v2',
  description: 'Re-run: two independent agents classify 434 records item-by-item (no default labels)',
  phases: [{ title: 'Leitor A' }, { title: 'Leitor B' }],
}
const DIR = '<internal_repo>/experimentos/rodada_v3_out2026/referencias/lotes_tipo_generico'
const prompt = (b, leitor) => `You are classifying the publication type of medical articles for a research study. Read ${DIR}/lote_${b}.json — PubMed records (ref_id, pmid, titulo, revista, ano, tipos_pubmed, resumo). PubMed labeled these only generically, so classify from title + abstract. Work ONLY from the provided text (no browsing). Do NOT open any other file in that folder (other readers' outputs are off-limits — independence matters).

STRICT RULES (a previous run was rejected for violating these):
- Judge EVERY item individually. NO default/fallback label for "the rest". Do not write code that assigns a label to several items at once.
- "motivo" must cite the specific design evidence from THAT item's text (e.g. "randomized 120 pts to X vs placebo", "retrospective cohort of 304 ICU pts", "single 54-year-old woman"); generic phrases like "observational study" alone are not acceptable.
- If abstract is empty, say so in motivo and judge from title/journal with confianca "baixa".

Categories (exactly one):
- diretriz: society/agency guideline WITH formal evidence grading (GRADE, class/level of evidence) — a consensus that uses GRADE counts as diretriz
- consenso_especialistas: guidance/consensus/position statement/expert recommendations WITHOUT formal grading
- revisao_sistematica_metanalise: systematic review and/or meta-analysis (explicit systematic search)
- ensaio_clinico: interventional trial (randomized or not) or trial protocol
- estudo_observacional: cohort, case-control, cross-sectional, case series, registry/database, pharmacokinetic, diagnostic accuracy, survey, modeling of patient data
- revisao_narrativa: narrative/clinical review, overview, "how I treat", clinical update without systematic search
- relato_caso: one or a few individual patients (incl. NEJM Case Records)
- livro_capitulo: book or book chapter
- outro: editorial, letter, commentary, opinion, patient-education page, news, erratum, review protocol, basic-science/animal/in vitro, other

Write a JSON list (same order) to ${DIR}/lote_${b}_leitor${leitor}2.json with {"ref_id","tipo","confianca":"alta"|"media"|"baixa","motivo"}. Reply only with counts per tipo.`
const A = parallel([1,2,3,4,5].map(b => () => agent(prompt(b,'A'), { label: `lote ${b} A`, phase: 'Leitor A' })))
const B = parallel([1,2,3,4,5].map(b => () => agent(prompt(b,'B'), { label: `lote ${b} B`, phase: 'Leitor B' })))
return { A: await A, B: await B }
