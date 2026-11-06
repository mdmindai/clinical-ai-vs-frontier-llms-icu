export const meta = {
  name: 'refs-inacessiveis-e-diretrizes',
  description: 'Identify 75 inaccessible LLM references and re-classify 212 guideline/consensus documents',
  phases: [{ title: 'Inacessíveis' }, { title: 'Diretriz x consenso' }],
}
const DIR = '<internal_repo>/experimentos/rodada_v3_out2026/referencias/lotes_v2'
const CATS = 'diretriz | consenso_especialistas | revisao_sistematica_metanalise | ensaio_clinico | estudo_observacional | revisao_narrativa | relato_caso | bula_label | livro_capitulo | site_educativo | noticia_blog | outro'
const RULE = `"diretriz" = society/agency document whose recommendations carry FORMAL evidence grading (GRADE, class of recommendation I/IIa/IIb/III, level of evidence A/B/C, strength strong/weak with certainty of evidence, Oxford levels). "consenso_especialistas" = guidance, consensus statement, position paper, expert-panel recommendations WITHOUT formal evidence grading. A consensus that uses GRADE is "diretriz". Judge by the document's methods, not its name.`

const p1 = b => `You are identifying references for a research study. Read ${DIR}/inacess_${b}.json — web references (ref_id, url, titulo_citado) whose pages could NOT be opened directly (403/Cloudflare/captcha). Many have no useful cited title (only a domain).
For EACH, establish which document it is WITHOUT guessing, using: the URL itself (slug, path, PMC/NBK/PII ids), web search for the URL or slug, NCBI E-utilities (StatPearls NBK ids: db=books; PubMed title search), Crossref (PII/title), or the publisher/society listing page. Try opening once more with curl and a browser User-Agent if useful.
Record: ref_id, url, identificado ("sim"|"nao"), titulo, organizacao_ou_revista, ano (null if not established — never guess), tipo (one of: ${CATS}), fonte_metadados (where the metadata came from, e.g. "PubMed 12345678", "search snippet", "NICE guidance index"), confere ("sim"/"parcial"/"nao"/"nd" vs titulo_citado; "nd" if titulo_citado is only a domain or empty), nota.
Rule for tipo: ${RULE}
Write the JSON list to ${DIR}/inacess_${b}_out.json. Reply only with counts of identificado and of ano null.`

const p2 = b => `You are classifying clinical documents for a research study. Read ${DIR}/diretriz_${b}.json — documents (doc_id, titulo, organizacao_ou_revista, ano, link, url_citada, tipos_pubmed) currently labeled guideline/consensus.
Rule: ${RULE}
For EACH document, open it (link or url_citada; PMC full text, publisher page, society PDF; for PubMed records find the full text or at least the abstract/methods) and look for formal evidence grading in the recommendations or methods. Record:
doc_id, tipo_revisado ("diretriz" | "consenso_especialistas" | other category from: ${CATS} if it is clearly not a guideline/consensus at all, e.g. a narrative review or a news page about a guideline), evidencia_graduada ("sim"|"nao"|"nd"), sistema_graduacao (e.g. "GRADE", "ACC/AHA COR/LOE", null), base ("texto_completo"|"resumo"|"pagina"|"nao_acessado"), nota (brief).
If the document cannot be accessed at all, keep its current label as tipo_revisado and set base "nao_acessado". Never invent.
Write the JSON list to ${DIR}/diretriz_${b}_out.json. Reply only with counts of tipo_revisado and of base.`

const a = parallel([1, 2].map(b => () => agent(p1(b), { label: `inacess ${b}`, phase: 'Inacessíveis' })))
const c = parallel([1, 2, 3, 4, 5, 6, 7, 8].map(b => () => agent(p2(b), { label: `diretriz ${b}`, phase: 'Diretriz x consenso' })))
return { inacessiveis: await a, diretrizes: await c }
