#!/usr/bin/env python3
"""Aggregates the reference-quality panel (3 judges x 5 systems x 100 questions): un-blinds A-E, averages the 3 judges per
axis per question, overall = mean of the 4 axes; per-system means; Friedman across the 5 systems; paired Wilcoxon for every
pair with Holm correction (tests on exact integer sums of the judges' scores); MDmind vs OpenEvidence by axis (unadjusted). Output: results/panel_results.json"""
import json
from decimal import Decimal, ROUND_HALF_UP
from itertools import combinations
from pathlib import Path
import numpy as np
from scipy import stats

BASE = Path(__file__).resolve().parent.parent
import sys
FOLDER = sys.argv[1] if len(sys.argv) > 1 else "panel"
P = BASE / "data" / FOLDER
OUTD = BASE / "results"
AX = ["relevance", "evidence_level", "recency", "sufficiency"]
S = ["mdmind", "oe", "gpt5", "claude", "gemini"]


def r2(num, den):
    """Exact mean num/den rounded half-up to 2 decimals (avoids float rounding of values like 3.345)."""
    return float((Decimal(num) / Decimal(den)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP))


def main():
    bmap = json.load(open(P / "blind_map.json", encoding="utf-8"))
    J = {j: json.load(open(P / f"grades_{j}.json", encoding="utf-8")) for j in ("openai", "gemini", "claude") if (P / f"grades_{j}.json").exists()}
    assert len(J) == 3, f"expected 3 judge files, found {list(J)}"
    idxs = sorted(set.intersection(*[set(v) for v in J.values()]), key=int)
    assert len(idxs) == 100, f"expected 100 questions graded by all judges, found {len(idxs)}"
    per = {}   # idx -> sistema -> {eixo: média dos juízes, overall}
    for i in idxs:
        per[i] = {}
        for L, s in bmap[i].items():
            d = {a: float(np.mean([J[j][i][L][a] for j in J])) for a in AX}
            d["overall"] = float(np.mean([d[a] for a in AX]))
            d["_tot"] = sum(J[j][i][L][a] for j in J for a in AX)          # exact integer, used by the tests
            d.update({f"_{a}": sum(J[j][i][L][a] for j in J) for a in AX})
            per[i][s] = d
    res = {"judges": list(J), "n": len(idxs), "by_system": {}, "overall_by_judge": {}}
    for s in S:
        res["by_system"][s] = {a: r2(sum(per[i][s][f"_{a}"] for i in idxs), len(J) * len(idxs)) for a in AX}
        res["by_system"][s]["overall"] = r2(sum(per[i][s]["_tot"] for i in idxs), len(J) * len(AX) * len(idxs))
    for j in J:
        res["overall_by_judge"][j] = {s: r2(sum(J[j][i][L][a] for i in idxs for L, ss in bmap[i].items() if ss == s for a in AX), len(AX) * len(idxs)) for s in S}
    fr = stats.friedmanchisquare(*[[per[i][s]["_tot"] for i in idxs] for s in S])
    res["friedman"] = {"chi2": round(float(fr.statistic), 1), "p": float(fr.pvalue)}
    pares = []
    for a, b in combinations(S, 2):
        d = [per[i][a]["overall"] - per[i][b]["overall"] for i in idxs]
        dt = [per[i][a]["_tot"] - per[i][b]["_tot"] for i in idxs]
        pares.append({"pair": f"{a}×{b}", "delta": round(float(np.mean(d)), 3), "p": float(stats.wilcoxon(dt).pvalue) if any(dt) else 1.0})
    ordem = sorted(range(len(pares)), key=lambda k: pares[k]["p"])
    prev = 0
    for r, k in enumerate(ordem):
        prev = max(prev, min(1, pares[k]["p"] * (len(pares) - r)))
        pares[k]["p_holm"] = prev
    res["pairs"] = pares
    eixos = {}
    for ax in AX:
        d = [per[i]["mdmind"][ax] - per[i]["oe"][ax] for i in idxs]
        dt = [per[i]["mdmind"][f"_{ax}"] - per[i]["oe"][f"_{ax}"] for i in idxs]
        eixos[ax] = {"delta": round(float(np.mean(d)), 3), "p": float(stats.wilcoxon(dt).pvalue) if any(dt) else 1.0}
    res["mdmind_vs_oe_by_axis"] = eixos
    OUTD.mkdir(exist_ok=True)
    json.dump(res, open(OUTD / ("panel_results.json" if FOLDER == "panel" else f"panel_results_{FOLDER.removeprefix('panel_')}.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(json.dumps(res, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
