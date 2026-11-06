export const meta = {
  name: 'segundo-leitor-referencias',
  description: 'Blind 2nd reader (Opus) re-opens 776 LLM reference pages and re-reviews 212 guideline/consensus documents',
  phases: [{ title: 'Ler páginas (leitor 2)' }, { title: 'Diretriz x consenso (leitor 2)' }],
}
const DIR = '<internal_repo>/experimentos/rodada_v3_out2026/referencias/lotes_leitor2'
const BLIND = `You are an INDEPENDENT second reader. Work only from the input file named below and the web. Do NOT open, list or read any other file in the referencias folder or its subfolders (in particular nothing named *_out.json, refs_*.json, auditoria_*.csv, or the folders lotes_agentes / lotes_v2) — another reader's answers are there and you must not see them.`
const CATS = 'diretriz | consenso_especialistas | revisao_sistematica_metanalise | ensaio_clinico | estudo_observacional | revisao_narrativa | relato_caso | bula_label | livro_capitulo | site_educativo | noticia_blog | outro'
const RULE = `"diretriz" = society/agency document whose recommendations carry FORMAL evidence grading (GRADE, class of recommendation I/IIa/IIb/III, level of evidence A/B/C, strength strong/weak with certainty of evidence, Oxford levels). "consenso_especialistas" = guidance, consensus statement, position paper, expert-panel recommendations WITHOUT formal evidence grading. A consensus that uses GRADE is "diretriz". Judge by the document's methods, not its name.`

const pA = b => `${BLIND}

You are collecting bibliographic metadata for a research study. Read the file
${DIR}/lote_${b}.json — a list of web references (ref_id, url, titulo_citado = the title the AI system gave it).

For EACH reference, open the URL (use WebFetch; if blocked/403/timeout, try ONE alternative: the same URL without query string, or a web search for the exact title to find the same document elsewhere — record which you used). From the page itself (not from your memory) record:
- acessou: "sim" | "via_alternativa" | "nao" (couldn't read the page at all)
- titulo_pagina: the document's actual title as shown on the page
- organizacao_ou_revista: publisher/journal/society/agency/site
- ano: year of publication or last update shown on the page (null if none shown — do NOT guess)
- tipo: one of: diretriz | revisao_sistematica_metanalise | ensaio_clinico | estudo_observacional | revisao_narrativa | relato_caso | bula_label | livro_capitulo (incl. StatPearls) | site_educativo | noticia_blog | outro
- confere: "sim" if the page is the document described by titulo_citado, "parcial" if same topic but different/generic page, "nao" if unrelated, "nd" if not accessed
- nota: brief note (e.g., "403, found on PMC", "veterinary content", "search results page")

Rules: never invent metadata; if not visible, null. Process every item in the file.
Write the result as a JSON list (same order, include ref_id and url) to ${DIR}/lote_${b}_out.json
Reply with only: number processed, counts of acessou, counts of confere.`

const pB = b => `${BLIND}

You are classifying clinical documents for a research study. Read ${DIR}/diretriz_${b}.json — documents (doc_id, titulo, organizacao_ou_revista, ano, link, url_citada, tipos_pubmed) currently labeled guideline/consensus.
Rule: ${RULE}
For EACH document, open it (link or url_citada; PMC full text, publisher page, society PDF; for PubMed records find the full text or at least the abstract/methods) and look for formal evidence grading in the recommendations or methods. Record:
doc_id, tipo_revisado ("diretriz" | "consenso_especialistas" | other category from: ${CATS} if it is clearly not a guideline/consensus at all, e.g. a narrative review or a news page about a guideline), evidencia_graduada ("sim"|"nao"|"nd"), sistema_graduacao (e.g. "GRADE", "ACC/AHA COR/LOE", null), base ("texto_completo"|"resumo"|"pagina"|"nao_acessado"), nota (brief).
If the document cannot be accessed at all, keep its current label as tipo_revisado and set base "nao_acessado". Never invent.
Write the JSON list to ${DIR}/diretriz_${b}_out.json. Reply only with counts of tipo_revisado and of base.`

const lotes = Array.from({ length: 20 }, (_, i) => String(i + 1).padStart(2, '0'))
const a = parallel(lotes.map(b => () => agent(pA(b), { label: `páginas ${b}`, phase: 'Ler páginas (leitor 2)', model: 'opus' })))
const c = parallel([1, 2, 3, 4, 5, 6, 7, 8].map(b => () => agent(pB(b), { label: `diretriz ${b}`, phase: 'Diretriz x consenso (leitor 2)', model: 'opus' })))
return { paginas: await a, diretrizes: await c }
