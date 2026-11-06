#!/usr/bin/env python3
"""MDmind answers (October 2026): the 100 questions, bare, current backend pipeline; POST /pergunta,
skip_cache, empty history, sequential. Writes `answer_raw` (the text exactly as MDmind returns it, reference
list at the top: this is the published and graded text, shipped as `answer`) and `answer` = reorder(answer_raw)
(reference list moved to the end; used only for the refs-at-end sensitivity grading).

  MDMIND_TOKEN=... python generate_answers_mdmind.py [--n 10]
"""
import os, json, csv, re, time, argparse, subprocess
from datetime import datetime, timezone
from pathlib import Path
import httpx

EXP = Path(__file__).resolve().parent.parent
ROOT = EXP.parent.parent
QCSV = ROOT / "estudo2_qualidade/data/questions/questions_icu_100.csv"
URL = os.getenv("MDMIND_URL", "http://localhost:8000").rstrip("/")
BACKEND = Path.home() / "Documents/MDmind/Backend/MDmind-backend"


def reorder(a):
    """Moves the reference block that MDmind returns at the top ("## Referências" + "[N]. ..." lines) to the end.
    Not used in the published analysis: the published answers are `answer_raw`, graded as returned (reference
    list at the top). This corrected version (Oct 19, 2026) was used only for the sensitivity grading with the
    list at the end; the first version cut at the first "##" heading and misplaced the opening paragraph."""
    lines = a.split("\n")
    if not lines or not lines[0].startswith("## Referências"):
        return a
    k = 1
    while k < len(lines) and (re.match(r"^\[\d+\]\.", lines[k]) or not lines[k].strip()):
        k += 1
    return "\n".join(lines[k:]).strip() + "\n\n" + "\n".join(lines[:k]).strip()


def perguntar(q, idx):
    out = []
    with httpx.Client(timeout=400) as c:
        with c.stream("POST", f"{URL}/pergunta",
                      json={"pergunta": q, "contexto_id": f"out2026_{idx}", "skip_cache": True, "historico": []},
                      headers={"Authorization": f"Bearer {os.environ['MDMIND_TOKEN']}"}) as r:
            r.raise_for_status()
            for ln in r.iter_lines():
                if ln and not ln.startswith("[STATUS]"):
                    out.append(ln)
    return "\n".join(out)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=0)
    a = ap.parse_args()
    commit = subprocess.run(["git", "-C", str(BACKEND), "log", "-1", "--format=%h"],
                            capture_output=True, text=True).stdout.strip()
    out = EXP / "respostas" / "respostas_mdmind.jsonl"
    feitas = {json.loads(l)["idx"] for l in open(out)} if out.exists() else set()
    perguntas = list(csv.DictReader(open(QCSV, encoding="utf-8")))
    if a.n:
        perguntas = perguntas[: a.n]
    with open(out, "a") as f:
        for row in perguntas:
            idx = int(row["idx"])
            if idx in feitas:
                continue
            t0, err, raw = time.time(), None, ""
            for tent in range(3):
                try:
                    raw = perguntar(row["pergunta"], idx)
                    if not raw.strip():
                        raise RuntimeError("resposta vazia")
                    err = None
                    break
                except Exception as e:
                    err = f"{type(e).__name__}: {str(e)[:200]}"
                    time.sleep(15 * (tent + 1))
            rec = {"idx": idx, "model": "mdmind", "sub_domain": row["sub_domain"], "pergunta": row["pergunta"],
                   "answer": reorder(raw), "answer_raw": raw, "backend_commit": commit,
                   "latency": round(time.time() - t0, 1), "gerado_em": datetime.now(timezone.utc).isoformat(),
                   "error": err}
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")
            f.flush()


if __name__ == "__main__":
    main()
