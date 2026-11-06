#!/usr/bin/env python3
"""Versão limpa das respostas do OE para o rejulgamento do Estudo 2 (decisão do pesquisador, 19/out/2026).
Fonte: recoleta pelo botão "copiar" (oe/recoleta_referencias_oe.md) — mesmo conteúdo da resposta, referências completas
com DOI e sem os selos colados ("Review", "RecentSR"…). Limpeza: remove os blocos de figura/tabela que a cópia traz sem a
imagem (linha "Figure N"/"Table N"/"Visual Abstract"/"Relevant images" + legenda e a linha de fonte logo abaixo).
Nada mais do texto é alterado. Saída: respostas/respostas_oe_limpa.jsonl"""
import json, re
from pathlib import Path

EXP = Path(__file__).resolve().parent.parent
FIG = re.compile(r"^(Figure|Table|Figura|Tabela|Visual Abstract|Relevant images|Imagens relevantes)\b", re.I)
FONTE = re.compile(r"^[^\[\]]{10,}\.\s*(19|20)\d\d[;.].*doi:\S+\.?\s*$", re.S)


def limpa(txt):
    par = re.split(r"\n\s*\n", txt.strip())
    out, removidos, anterior_fig = [], 0, False
    for p in par:
        s = p.strip()
        if FIG.match(s) or (anterior_fig and FONTE.match(s) and "\n" not in s):
            removidos += 1
            anterior_fig = True
            continue
        anterior_fig = False
        out.append(p)
    return "\n\n".join(out), removidos


def main():
    t = open(EXP / "oe/recoleta_referencias_oe.md").read()
    B = dict(re.findall(r"<!-- REFS (\d+) — INÍCIO -->\n(.*?)<!-- REFS \1 — FIM -->", t, re.S))
    tot = 0
    with open(EXP / "respostas/respostas_oe_limpa.jsonl", "w") as f:
        for l in open(EXP / "respostas/respostas_oe.jsonl"):
            r = json.loads(l)
            txt, n = limpa(B[str(r["idx"])])
            tot += n
            r.update(answer=txt, fonte_texto="recoleta (botão copiar) sem blocos de figura", blocos_figura_removidos=n)
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    print("blocos removidos:", tot)


if __name__ == "__main__":
    main()
