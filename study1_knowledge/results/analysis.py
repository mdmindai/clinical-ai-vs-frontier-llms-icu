#!/usr/bin/env python3
"""Recomputes the full Study 1 result from the answers in ../answers/.

Usage: python analysis.py           (prints the report)
No external dependencies — standard library only.
"""
import json,csv,math,glob,os
from itertools import combinations
from math import exp,sqrt

AQUI=os.path.dirname(os.path.abspath(__file__))
BASE=os.path.dirname(AQUI)
R={int(r['q']):r for r in csv.DictReader(open(f'{BASE}/questions/bench360_questions.csv',encoding='utf-8'))}
QS=sorted(R); N=len(QS)
NOME={'gemini':'Gemini 3.1 Pro','gpt-5.5':'gpt-5.5','claude':'Claude Opus 4.8',
      'mdmind':'MDmind','openevidence':'OpenEvidence'}
S={}
for f in sorted(glob.glob(f'{BASE}/answers/*_360.jsonl')):
    k=os.path.basename(f).replace('_360.jsonl','')
    S[NOME.get(k,k)]={o['q']:bool(o['correct']) for o in (json.loads(l) for l in open(f))}
names=list(S)
corr={n:{q:S[n][q] for q in QS} for n in names}
assert all(len(S[n])==N for n in names)
acc={n:sum(corr[n].values()) for n in names}

print(f"=== ACCURACY — {N} items (TEMI 2020-2025) ===")
for n in sorted(names,key=lambda x:-acc[x]):
    a=acc[n]/N; z=1.96                      # Wilson 95% CI (better than Wald near the extremes)
    d=1+z*z/N; c=a+z*z/(2*N); h=z*sqrt(a*(1-a)/N + z*z/(4*N*N))
    print(f"  {n:16s} {acc[n]:>3}/{N} = {a*100:5.1f}%   95%CI {100*(c-h)/d:.1f}-{100*(c+h)/d:.1f}")

k=len(names); mat=[[1 if corr[n][q] else 0 for n in names] for q in QS]
Cj=[sum(r[j] for r in mat) for j in range(k)]; Ri=[sum(r) for r in mat]
Q=(k-1)*(k*sum(c*c for c in Cj)-sum(Cj)**2)/(k*sum(Ri)-sum(r*r for r in Ri))
print(f"\nCochran's Q (df={k-1}) = {Q:.1f}, p = {exp(-Q/2)*(1+Q/2):.2e}")

def mcnemar(a,b):
    x=sum(corr[a][q] and not corr[b][q] for q in QS)
    y=sum(not corr[a][q] and corr[b][q] for q in QS); n=x+y
    p=min(1.0,2*sum(math.comb(n,i) for i in range(min(x,y)+1))*0.5**n) if n else 1.0
    return x,y,p
res=[(a,b,*mcnemar(a,b)) for a,b in combinations(names,2)]
rs=sorted(res,key=lambda t:t[4]); m=len(res); holm={}; mx=0
for i,(a,b,x,y,p) in enumerate(rs):
    adj=max(min(1.0,p*(m-i)),mx); mx=adj; holm[(a,b)]=adj
print(f"\n=== Exact McNemar + Holm ({m} pairs) ===")
print(f"{'pair':38s}{'A>B':>5}{'B>A':>5}{'p(Holm)':>10}")
for a,b,x,y,p in rs:
    ph=holm[(a,b)]; sig='***' if ph<.001 else '**' if ph<.01 else '*' if ph<.05 else 'ns'
    print(f"{a+' vs '+b:38s}{x:>5}{y:>5}{ph:>10.4f} {sig}")

print("\n=== by exam ===")
hdr=sorted(names,key=lambda x:-acc[x])
print(f"{'exam':12s}{'n':>5}"+"".join(f"{n[:12]:>14s}" for n in hdr))
for s in ['AMIB2020','AMIB2021','AMIB2022','AMIB2023','AMIB2024','TEMI2025']:
    qs=[q for q in QS if R[q]['source']==s]
    if not qs: continue
    lab='TEMI '+s[-4:]
    print(f"{lab:12s}{len(qs):>5}"+"".join(f"{sum(corr[n][q] for q in qs)/len(qs)*100:>13.0f}%" for n in hdr))
