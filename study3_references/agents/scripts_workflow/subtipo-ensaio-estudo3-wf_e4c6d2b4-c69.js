export const meta = {
  name: 'subtipo-ensaio-estudo3',
  description: '2 leitores cegos decidem RCT × ensaio não randomizado em 20 documentos sem rótulo do PubMed',
  phases: [{ title: 'Leitura' }],
}
const SCHEMA = { type: 'object', properties: { itens: { type: 'array', items: { type: 'object', properties: {
  codigo: { type: 'string' }, subtipo: { type: 'string', enum: ['rct','nao_randomizado','nao_e_ensaio'] },
  confianca: { type: 'string', enum: ['alta','media','baixa'] }, justificativa: { type: 'string' } },
  required: ['codigo','subtipo','confianca','justificativa'] } } }, required: ['itens'] }
const P = `Você é um leitor metodológico; trabalhe de forma independente. Leia SOMENTE o arquivo <internal_repo>/experimentos/rodada_v3_out2026/referencias/subtipo_ensaio_lote.json (não abra arquivos com "chave" no nome). Todos os itens foram classificados como ensaio clínico (intervenção alocada pelos investigadores). Para cada um, decida:
- "rct": os participantes foram alocados ALEATORIAMENTE (randomizado; inclui cluster-randomizado e cruzado randomizado);
- "nao_randomizado": intervenção alocada pelos investigadores sem randomização (braço único com protocolo prospectivo, controle histórico, alocação não aleatória);
- "nao_e_ensaio": se claramente não houve intervenção alocada pelos investigadores (explique).
Use título, revista e resumo; se faltar resumo, você pode abrir a url ou https://pubmed.ncbi.nlm.nih.gov/<pmid>/. Responda todos os itens com justificativa de 1 frase em português.`
phase('Leitura')
return await parallel(['A','B'].map(l => () => agent(P, { label: `leitor${l}`, phase: 'Leitura', schema: SCHEMA, ...(l === 'B' ? { model: 'fable' } : {}) }).then(r => ({ leitor: l, itens: r ? r.itens : null }))))