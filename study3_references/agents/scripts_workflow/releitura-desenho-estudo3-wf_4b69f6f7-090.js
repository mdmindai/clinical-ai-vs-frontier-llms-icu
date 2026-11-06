export const meta = {
  name: 'releitura-desenho-estudo3',
  description: 'Releitura cega (2 leitores independentes) de ~312 documentos observacional × série × ensaio com o checklist de desenho',
  phases: [{ title: 'Leitura', detail: '4 lotes × 2 leitores independentes' }],
}

const CATS = ['ensaio_clinico','estudo_observacional','relato_serie_casos','revisao_sistematica_metanalise','revisao_narrativa','diretriz','consenso_especialistas','livro_capitulo','outro']
const SCHEMA = {
  type: 'object',
  properties: {
    itens: {
      type: 'array',
      items: {
        type: 'object',
        properties: {
          codigo: { type: 'string' },
          intervencao_alocada_pelos_investigadores: { type: 'boolean' },
          q1_grupo_comparacao_por_exposicao: { type: 'boolean' },
          q2_base_populacional_com_denominador: { type: 'boolean' },
          tipo: { type: 'string', enum: CATS },
          flag: { type: 'string', enum: ['nenhuma','acuracia_diagnostica','estudo_pre_clinico','serie_casos_literatura','antes_depois_controle_historico'] },
          confianca: { type: 'string', enum: ['alta','media','baixa'] },
          fonte_lida: { type: 'string', enum: ['resumo_fornecido','pagina_aberta','so_titulo'] },
          justificativa: { type: 'string' },
        },
        required: ['codigo','intervencao_alocada_pelos_investigadores','q1_grupo_comparacao_por_exposicao','q2_base_populacional_com_denominador','tipo','flag','confianca','fonte_lida','justificativa'],
      },
    },
  },
  required: ['itens'],
}

const REGRA = `Você é um leitor metodológico classificando o DESENHO de artigos citados como referência. Trabalhe de forma independente. Não procure nem leia nenhum outro arquivo além do lote indicado (em especial, NÃO abra arquivos com "chave" no nome). Não há informação sobre quem citou o artigo, e isso é proposital.

CHECKLIST (decida pelo desenho, NUNCA pelo nome que o autor dá — "retrospective study", "cohort", "observational study" não decidem — e NUNCA pelo número de pacientes):
0. Os investigadores ALOCARAM/aplicaram uma intervenção para estudá-la (prospectivamente, randomizado ou não, incluindo antes-depois e controle histórico)? → tipo "ensaio_clinico" (se for antes-depois ou controle histórico, flag "antes_depois_controle_historico"). Tratamento dado na rotina e depois analisado retrospectivamente NÃO é intervenção alocada.
1. Q1: há grupo de comparação definido por EXPOSIÇÃO/INTERVENÇÃO/característica (ex.: tratados com A × B; expostos × não expostos; casos × controles sem a doença)? → "estudo_observacional". Comparar pacientes pelo DESFECHO (sobreviventes × óbitos, respondedores × não) NÃO conta como Q1.
2. Q2: a inclusão vem de uma população de base / sampling frame com DENOMINADOR reportado (ex.: "de N admissões, k tiveram…", incidência, prevalência, vigilância populacional com denominador, registro populacional, estudo transversal/inquérito)? → "estudo_observacional".
3. Nem 0, nem Q1, nem Q2: pacientes com a mesma condição/tratamento apenas descritos (qualquer n), surto sem denominador, farmacovigilância/notificações → "relato_serie_casos". Compilado de relatos publicados (mesmo com busca sistemática, sem metanálise) → "relato_serie_casos" + flag "serie_casos_literatura".
Casos especiais: acurácia diagnóstica (sensibilidade/especificidade de teste vs referência) → "estudo_observacional" + flag "acuracia_diagnostica". Farmacocinética medida EM PACIENTES/voluntários → "estudo_observacional". Sem humanos vivos (in vitro, animal, cadáver, modelagem/simulação) → "outro" + flag "estudo_pre_clinico".
Se o documento NÃO for estudo primário: revisão sem método sistemático → "revisao_narrativa"; revisão sistemática/metanálise de estudos → "revisao_sistematica_metanalise"; recomendação de sociedade com graduação formal de evidência → "diretriz", sem graduação → "consenso_especialistas"; capítulo/livro → "livro_capitulo"; carta/editorial/comentário/outros → "outro".

FONTE: use o título, tipos do PubMed, MeSH e resumo fornecidos. Se o resumo estiver ausente e houver url ou pmid, você PODE abrir a página (WebFetch na url, ou https://pubmed.ncbi.nlm.nih.gov/<pmid>/) para ler o resumo/métodos; registre fonte_lida. Se não conseguir, decida pelo título e marque confianca "baixa" e fonte_lida "so_titulo".

Responda TODOS os itens do lote, um por código, com justificativa curta (1 frase, em português, citando o elemento de desenho decisivo).`

const LOTES = [1,2,3,4]
const BASE = '<internal_repo>/experimentos/rodada_v3_out2026/referencias/releitura_desenho/'

phase('Leitura')
const res = await parallel(LOTES.flatMap(n => ['A','B'].map(leitor => () =>
  agent(`${REGRA}\n\nLote: leia o arquivo ${BASE}lote_${n}.json (lista de itens com codigo, titulo, revista, ano, tipos_pubmed, mesh, resumo, url, pmid) e classifique cada item.`,
    { label: `lote${n}-leitor${leitor}`, phase: 'Leitura', schema: SCHEMA, ...(leitor === 'B' ? { model: 'fable' } : {}) })
    .then(r => ({ lote: n, leitor, itens: r ? r.itens : null }))
)))
return res