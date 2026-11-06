#!/usr/bin/env python3
"""Builds the blind reference lists for the 3-judge panel (Study 3): per question, each system's list as
"[j] title — year, coarse type, source", labels A–E ordered by sha256(idx:system); duplicates excluded,
system labels and our annotations removed. Run as in the internal working repository (Portuguese column
names; see README). Output: blind_map.json, blind_sets.json."""
import csv, hashlib, json, re
from urllib.parse import urlparse
from collections import defaultdict
from pathlib import Path

EXP = Path(__file__).resolve().parent.parent
SYS = ["mdmind", "oe", "gpt5", "gemini", "claude"]
GROSSO = {"diretriz": "guideline/society", "consenso_especialistas": "guideline/society", "orientacao_oficial": "guideline/society",
          "bula_label": "drug/label"}
ARTIGO = {"revisao_sistematica_metanalise", "ensaio_clinico", "estudo_observacional", "relato_serie_casos", "revisao_narrativa"}


def tipo_grosso(r):
    t = r["tipo_final"]
    if t in GROSSO:
        return GROSSO[t]
    if t in ARTIGO or (t == "outro" and r["pmid"]):
        return "paper"
    return "other"


ANOTACAO = re.compile(r"\s*\((?:com Full Prescribing|Guideline Essentials —|bulário veterinário|PDF anexo|figura/tabela isolada|figura isolada|"
                      r"tabela isolada|tabela enviada|cuidados de enfermagem)[^)]*\)?", re.I)


def titulo(r):
    """Título como o juiz vê: sem as anotações que a nossa classificação acrescentou entre parênteses."""
    return ANOTACAO.sub("", (r["titulo_verificado"] or r["titulo_citado"] or r["url"] or "")).strip()[:140]


def fonte(r):
    """Fonte mostrada ao juiz (opção b, 18/out/2026): revista (do PubMed) para referências indexadas; domínio da URL para
    páginas web; o nome dado pelo próprio sistema quando não há URL (OE). Nunca as anotações da nossa classificação."""
    if r["pmid"]:
        return (r["revista_ou_organizacao"] or "").strip()[:60]
    if r["url"]:
        return urlparse(r["url"]).netloc.removeprefix("www.")
    return (r["revista_ou_organizacao"] or "").strip()[:60]


def main():
    Q = {int(q["idx"]): q["pergunta"] for q in csv.DictReader(open(EXP.parent.parent / "estudo2_qualidade/data/questions/questions_icu_100.csv", encoding="utf-8"))}
    refs = defaultdict(list)
    for r in csv.DictReader(open(EXP / "referencias/auditoria_referencias.csv", encoding="utf-8-sig")):
        if r["duplicata_de"]:
            continue
        refs[(r["sistema"], int(r["pergunta_idx"]))].append(r)
    bmap, bsets = {}, {}
    for idx in Q:
        blocks = {}
        for s in SYS:
            L = sorted(refs.get((s, idx), []), key=lambda r: int(r["ref_n"]))
            if not L:
                blocks[s] = "(no references provided)"
                continue
            linhas = []
            for j, r in enumerate(L, 1):
                tit = titulo(r)
                ano = (r["ano"] or "?")[:4]
                fo = fonte(r)
                linhas.append(f"[{j}] {tit} — {ano}, {tipo_grosso(r)}" + (f", {fo}" if fo else ""))
            blocks[s] = "\n".join(linhas)
        ordem = sorted(SYS, key=lambda s: hashlib.sha256(f"{idx}:{s}".encode()).hexdigest())
        lab = dict(zip("ABCDE", ordem))
        bmap[str(idx)] = lab
        bsets[str(idx)] = {"pergunta": Q[idx], **{L: blocks[s] for L, s in lab.items()}}
    (EXP / "painel").mkdir(exist_ok=True)
    json.dump(bmap, open(EXP / "painel/blind_map.json", "w"), ensure_ascii=False, indent=1)
    json.dump(bsets, open(EXP / "painel/blind_sets.json", "w"), ensure_ascii=False, indent=1)
    print(len(bsets))


if __name__ == "__main__":
    main()
