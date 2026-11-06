#!/usr/bin/env python3
"""Aggregates Study 2 (answer quality, RCQ rubric): 3 judges x 5 systems x 100 questions.

- Per question: mean of the 4 axes for each judge, then mean of the 3 judges (floats, never truncated).
- Tests run on the exact integer sum of the 12 scores (3 judges x 4 axes), so equal scores tie exactly.
- Friedman across the 5 systems; paired Wilcoxon for every pair, Holm-adjusted.
Usage: python aggregate.py   (reads data/grades; writes results/results.json)"""
import itertools, json, sys
from pathlib import Path
import numpy as np
from scipy import stats

BASE = Path(__file__).resolve().parent.parent
FOLDER = sys.argv[1] if len(sys.argv) > 1 else "grades"
JUDGES = ["openai", "gemini", "claude"]
SYSTEMS = ["gpt5", "claude", "gemini", "mdmind", "oe"]
AX = ["correctness", "safety", "completeness", "clarity"]

g = {j: {json.loads(l)["idx"]: json.loads(l)["scores"] for l in open(BASE / "data" / FOLDER / f"grades_{j}.jsonl")
         if not json.loads(l)["error"]} for j in JUDGES}
idxs = sorted(set.intersection(*(set(g[j]) for j in JUDGES)))
assert len(idxs) == 100, f"expected 100 questions graded by all 3 judges, found {len(idxs)}"
axis = {s: {a: np.array([np.mean([g[j][i][s][a] for j in JUDGES]) for i in idxs]) for a in AX} for s in SYSTEMS}
total = {s: np.array([sum(g[j][i][s][a] for j in JUDGES for a in AX) for i in idxs]) for s in SYSTEMS}  # integers
overall = {s: total[s] / (len(JUDGES) * len(AX)) for s in SYSTEMS}
per_judge = {j: {s: round(float(np.mean([np.mean([g[j][i][s][a] for a in AX]) for i in idxs])), 3) for s in SYSTEMS} for j in JUDGES}
fr = stats.friedmanchisquare(*[total[s] for s in SYSTEMS])
pairs = []
for a, b in itertools.combinations(SYSTEMS, 2):
    d = overall[a] - overall[b]
    p = stats.wilcoxon(total[a], total[b]).pvalue if np.any(total[a] != total[b]) else 1.0
    pairs.append([a, b, float(d.mean()), float(p)])
prev = 0.0
for k, ix in enumerate(np.argsort([p[3] for p in pairs])):
    prev = max(prev, min(1.0, (len(pairs) - k) * pairs[ix][3]))
    pairs[ix].append(prev)
res = {"n": len(idxs), "judges": JUDGES, "grades_folder": FOLDER,
       "by_system": {s: {**{a: round(float(axis[s][a].mean()), 3) for a in AX}, "overall": round(float(overall[s].mean()), 3)} for s in SYSTEMS},
       "overall_by_judge": per_judge,
       "friedman": {"chi2": float(fr.statistic), "p": float(fr.pvalue)},
       "pairs": [{"a": a, "b": b, "delta": round(d, 3), "p": p, "p_holm": ph} for a, b, d, p, ph in pairs]}
out = BASE / "results" / ("results.json" if FOLDER == "grades" else f"results_{FOLDER}.json")
json.dump(res, open(out, "w"), indent=1)
print(f"n={len(idxs)} | Friedman chi2={fr.statistic:.1f}, p={fr.pvalue:.1e}\n")
print(f"{'system':8s} " + " ".join(f"{a[:7]:>8}" for a in AX) + "  overall")
for s in sorted(SYSTEMS, key=lambda s: -overall[s].mean()):
    r = res["by_system"][s]
    print(f"{s:8s} " + " ".join(f"{r[a]:8.2f}" for a in AX) + f"     {r['overall']:.2f}")
print("\npairs (paired Wilcoxon, Holm):")
for a, b, d, p, ph in sorted(pairs, key=lambda x: x[4]):
    print(f"  {a:7s} x {b:7s}  delta {d:+.2f}  p={p:.1e}  Holm={ph:.3g}")
