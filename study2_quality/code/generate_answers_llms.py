#!/usr/bin/env python3
"""Rodada out/2026 — 3 LLMs via API, pergunta CRUA, busca web OPCIONAL (o modelo decide), parâmetros PADRÃO.

Espelha o artigo de referência (Nature Medicine, clinical_tools_extract/evaluation_pipeline.py):
sem system prompt, sem tool_choice, sem esforço de raciocínio / thinking / temperatura definidos.

  gpt5   : gpt-5.5, Responses API, tools=[web_search]               -> fontes = url_citation
  claude : claude-opus-4-8, tools=[web_search_20250305] (a do artigo) -> fontes = citations dos blocos de texto
  gemini : gemini-3.1-pro-preview, tools=[google_search]            -> fontes = groundingChunks
           (o link de redirect do Google expira: é resolvido para a URL final NA HORA da geração)

Saída: respostas/respostas_<sistema>.jsonl (retomável por idx) + brutos/<sistema>_<idx>.json (resposta crua da API).
  python gerar_respostas.py --sistema gpt5 --n 10
"""
import os, json, csv, time, argparse
from datetime import datetime, timezone
from pathlib import Path
import httpx

EXP = Path(__file__).resolve().parent.parent
ROOT = EXP.parent.parent
QCSV = ROOT / "estudo2_qualidade/data/questions/questions_icu_100.csv"
for line in open(ROOT / ".env"):
    if "=" in line and not line.strip().startswith("#"):
        k, v = line.strip().split("=", 1)
        os.environ.setdefault(k, v)


def gpt5(q):
    from openai import OpenAI
    r = OpenAI(api_key=os.environ["OPENAI_API_KEY"]).responses.create(
        model="gpt-5.5", input=q, tools=[{"type": "web_search"}])
    refs, vistos, nbusca = [], set(), 0
    for it in r.output:
        if it.type == "web_search_call":
            nbusca += 1
        for ct in getattr(it, "content", None) or []:
            for a in getattr(ct, "annotations", None) or []:
                if a.type == "url_citation" and a.url not in vistos:
                    vistos.add(a.url)
                    refs.append({"title": a.title or "", "url": a.url})
    return r.output_text, refs, nbusca, r.model, r.model_dump(mode="json", warnings=False)


def claude(q):
    import anthropic
    cli = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
    msgs, blocos, brutos = [{"role": "user", "content": q}], [], []
    for _ in range(5):  # continua se a API pausar o turno (pause_turn)
        r = cli.messages.create(model="claude-opus-4-8", max_tokens=16000, messages=msgs,
                                tools=[{"type": "web_search_20250305", "name": "web_search"}])
        brutos.append(r.model_dump(mode="json"))
        blocos += r.content
        if r.stop_reason != "pause_turn":
            break
        msgs = msgs + [{"role": "assistant", "content": r.content}]
    txt, refs, vistos, nbusca = [], [], set(), 0
    for b in blocos:
        if b.type == "server_tool_use":
            nbusca += 1
        elif b.type == "text":
            txt.append(b.text)
            for c in b.citations or []:
                u = getattr(c, "url", None)
                if u and u not in vistos:
                    vistos.add(u)
                    refs.append({"title": getattr(c, "title", "") or "", "url": u})
    return "".join(txt), refs, nbusca, r.model, brutos


def gemini(q):
    key, model = os.environ["GEMINI_API_KEY"], os.getenv("GEMINI_MODEL", "gemini-3.1-pro-preview")
    r = httpx.post(f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={key}",
                   json={"contents": [{"parts": [{"text": q}]}], "tools": [{"google_search": {}}]}, timeout=300)
    r.raise_for_status()
    j = r.json()
    cand = j["candidates"][0]
    gm = cand.get("groundingMetadata", {})
    refs, vistos = [], set()
    for ch in gm.get("groundingChunks", []):
        w = ch.get("web", {})
        final = w.get("uri", "")
        try:  # lê só o Location do redirect: não depende de o site de destino responder
            loc = httpx.get(final, follow_redirects=False, timeout=20).headers.get("location")
            if loc:
                final = loc
        except Exception:
            pass
        if final not in vistos:
            vistos.add(final)
            refs.append({"title": w.get("title", ""), "url": final, "redirect": w.get("uri", "")})
    txt = "".join(p.get("text", "") for p in cand.get("content", {}).get("parts", []))
    return txt, refs, len(gm.get("webSearchQueries", [])), j.get("modelVersion", model), j


FN = {"gpt5": gpt5, "claude": claude, "gemini": gemini}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--sistema", required=True, choices=FN)
    ap.add_argument("--n", type=int, default=0)
    a = ap.parse_args()
    out = EXP / "respostas" / f"respostas_{a.sistema}.jsonl"
    feitas = {json.loads(l)["idx"] for l in open(out)} if out.exists() else set()
    perguntas = list(csv.DictReader(open(QCSV, encoding="utf-8")))
    if a.n:
        perguntas = perguntas[: a.n]
    with open(out, "a") as f:
        for row in perguntas:
            idx = int(row["idx"])
            if idx in feitas:
                continue
            t0, err = time.time(), None
            for tent in range(4):
                try:
                    txt, refs, nbusca, modelo, bruto = FN[a.sistema](row["pergunta"])
                    if not txt.strip():
                        raise RuntimeError("resposta vazia")
                    err = None
                    break
                except Exception as e:
                    err = f"{type(e).__name__}: {str(e)[:200]}"
                    txt, refs, nbusca, modelo, bruto = "", [], 0, None, None
                    time.sleep(10 * 2 ** tent)
            if bruto is not None:
                json.dump(bruto, open(EXP / "brutos" / f"{a.sistema}_{idx}.json", "w"), ensure_ascii=False)
            rec = {"idx": idx, "model": a.sistema, "sub_domain": row["sub_domain"], "pergunta": row["pergunta"],
                   "answer": txt, "refs": refs, "n_buscas": nbusca, "modelo_api": modelo,
                   "latency": round(time.time() - t0, 1), "gerado_em": datetime.now(timezone.utc).isoformat(),
                   "error": err}
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")
            f.flush()


if __name__ == "__main__":
    main()
