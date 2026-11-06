#!/usr/bin/env python3
"""Builds the blind reference lists for the 3-judge panel (Study 3) from the shipped data: per question, each
system's list as "[j] title — year, type, source", with the detailed publication type of our final
classification, the full title and "n.d." when there is no date. Labels A–E ordered by sha256(idx:system)
(same blind map as before); within-answer duplicates excluded; system labels are not shown.
Usage: python build_panel_lists_detailed.py [out_dir]   (default: data/panel)"""
import csv, hashlib, json, sys
from collections import defaultdict
from pathlib import Path
from urllib.parse import urlparse

BASE = Path(__file__).resolve().parent.parent
OUT = Path(sys.argv[1]) if len(sys.argv) > 1 else BASE / "data" / "panel"
SYS = ["mdmind", "oe", "gpt5", "gemini", "claude"]
TYPE = {"diretriz": "Practice guideline", "consenso_especialistas": "Consensus statement",
        "orientacao_oficial": "Government guidance", "revisao_sistematica_metanalise": "Systematic review/meta-analysis",
        "estudo_observacional": "Observational study", "relato_serie_casos": "Case report/series",
        "revisao_narrativa": "Narrative review", "livro_capitulo": "Book/chapter", "bula_label": "Drug label/database",
        "referencia_clinica": "Point-of-care reference", "site_educativo_blog": "Educational website/blog",
        "rede_social": "Social media", "wiki": "Wiki", "plataforma_upload": "File-sharing platform",
        "questao_prova": "Exam-question site", "inacessivel": "Inaccessible (could not be opened)"}
QUALIFIER = {"conference_abstract": "conference abstract", "preprint": "preprint", "preclinical_study": "preclinical study",
             "ai_generated_content": "AI-generated content"}


def type_label(r):
    t = r["type_code"]
    if t == "ensaio_clinico":
        lab = "Randomized controlled trial" if r["trial_subtype"] == "randomized" else "Non-randomized trial"
    elif t == "outro":
        lab = "Letter/editorial/comment" if r["category"].startswith("Letter") else "Other"
    else:
        lab = TYPE[t]
    q = QUALIFIER.get(r["flag"])
    return f"{lab} ({q})" if q else lab


def source(r):
    """Journal for PubMed-indexed items; website domain for web pages; otherwise the name given by the system."""
    if r["pmid"]:
        return r["journal_or_organization"].strip()
    if r["url"]:
        return urlparse(r["url"]).netloc.removeprefix("www.")
    return r["journal_or_organization"].strip()


def main():
    Q = {int(q["idx"]): q["pergunta"] for q in csv.DictReader(open(BASE / "data/questions_icu_100.csv", encoding="utf-8"))}
    refs = defaultdict(list)
    for r in csv.DictReader(open(BASE / "data/references.csv", encoding="utf-8")):
        if not r["duplicate_of"]:
            refs[(r["system"], int(r["question_idx"]))].append(r)
    bmap, bsets = {}, {}
    for idx in Q:
        blocks = {}
        for s in SYS:
            L = sorted(refs.get((s, idx), []), key=lambda r: int(r["ref_n"]))
            if not L:
                blocks[s] = "(no references provided)"
                continue
            lines = []
            for j, r in enumerate(L, 1):
                title = (r["verified_title"] or r["cited_title"] or r["url"]).strip()
                src = source(r)
                lines.append(f"[{j}] {title} — {r['year'][:4] or 'n.d.'}, {type_label(r)}" + (f", {src}" if src else ""))
            blocks[s] = "\n".join(lines)
        order = sorted(SYS, key=lambda s: hashlib.sha256(f"{idx}:{s}".encode()).hexdigest())
        lab = dict(zip("ABCDE", order))
        bmap[str(idx)] = lab
        bsets[str(idx)] = {"pergunta": Q[idx], **{k: blocks[s] for k, s in lab.items()}}
    OUT.mkdir(parents=True, exist_ok=True)
    json.dump(bmap, open(OUT / "blind_map.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    json.dump(bsets, open(OUT / "blind_sets.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(len(bsets), "questions ->", OUT)


if __name__ == "__main__":
    main()
