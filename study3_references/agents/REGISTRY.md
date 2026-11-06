# LLM agents used in the Study 3 reference classification

Every agent run that produced classification data, with the model ID recorded in each agent transcript, the number of agents, the exact instruction (`prompts/*.prompt.txt`) and the output (`prompts/*.saida.txt`). Orchestration scripts are in `scripts_workflow/`. Dates are 2026 (day/month). Prompts and outputs are in Portuguese or English as run; local paths are replaced by `<internal_repo>`. The input batch files referenced in the prompts are internal.

## Workflow runs (several agents in parallel)

| Date | Workflow | Purpose | Agents | Model(s) | Files |
|---|---|---|---|---|---|
| 16/10 22:50 | `ler-paginas-referencias` (wf_a6c25b67-616) | Agents open 776 LLM reference pages (20 batches) and record bibliographic metadata | 20 | lote #: claude-opus-5-5 | `prompts/2026-10-16_ler-paginas-referencias_*` |
| 17/10 12:08 | `refs-inacessiveis-e-diretrizes` (wf_f67d3b78-852) | Identify 75 inaccessible LLM references and re-classify 212 guideline/consensus documents | 10 | diretriz #: claude-opus-5-5; inacess #: claude-opus-5-5 | `prompts/2026-10-17_refs-inacessiveis-e-diretrizes_*` |
| 17/10 20:30 | `tipo-generico-2-leitores-v2` (wf_918e9c81-0ca) | Two independent agents classify 434 records item-by-item | 10 | lote # A: claude-opus-5-5; lote # B: claude-opus-5-5 | `prompts/2026-10-17_tipo-generico-2-leitores-v2_*` |
| 18/10 07:59 | `segundo-leitor-referencias` (wf_8f50b9e2-85a) | Blind 2nd reader (Opus) re-opens 776 LLM reference pages and re-reviews 212 guideline/consensus documents | 28 | diretriz #: claude-opus-5-5; páginas #: claude-opus-5-5 | `prompts/2026-10-18_segundo-leitor-referencias_*` |
| 18/10 19:24 | `releitura-desenho-estudo3` (wf_4b69f6f7-090) | Blind re-reading (2 independent readers) of ~312 documents: observational × case series × trial, with the design checklist (used in the final classification) | 8 | lote#-leitorA: claude-opus-5-5; lote#-leitorB: claude-fable-5-1 | `prompts/2026-10-18_releitura-desenho-estudo3_*` |
| 18/10 20:38 | `subtipo-ensaio-estudo3` (wf_e4c6d2b4-c69) | 2 blind readers decide randomized × non-randomized trial for 20 documents without a PubMed label | 2 | leitorA: claude-opus-5-5; leitorB: claude-fable-5-1 | `prompts/2026-10-18_subtipo-ensaio-estudo3_*` |

Notes: some `.saida.txt` files hold only a summary of the agent's reply or a pointer to the internal output file (item-level outputs, keyed by internal codes, are internal); `2026-10-17_refs-inacessiveis-e-diretrizes_inacess 1.saida.txt` is empty and `inacess 2` holds only a progress line. Model column: "lote#" = batch number, A/B = reader. Agents ran in Claude Code with web access.

Not included: a run comparing two copies of the OpenEvidence answers (its inputs/outputs contain OpenEvidence answer text, which cannot be redistributed).
