export const meta = {
  name: 'ler-paginas-referencias',
  description: 'Agents open 776 LLM reference pages (20 batches) and record bibliographic metadata',
  phases: [{ title: 'Ler páginas' }],
}
const DIR = '<internal_repo>/experimentos/rodada_v3_out2026/referencias/lotes_agentes'
const batches = Array.from({ length: 20 }, (_, i) => String(i + 1).padStart(2, '0'))
const prompt = b => `You are collecting bibliographic metadata for a research study. Read the file
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
const res = await parallel(batches.map(b => () => agent(prompt(b), { label: `lote ${b}`, phase: 'Ler páginas' })))
return res
