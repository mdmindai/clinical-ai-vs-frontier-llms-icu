#!/usr/bin/env python3
"""Runs one judge of the reference-quality panel (Study 3): API, pinned model, default parameters, optional web
search (as the Study 2 judges); resumable; prompt = rubric_panel.md. Usage: JUIZ=openai|gemini|claude [SHARD=k/N]
python judge_panel.py. Internal paths: reads <PAINEL_DIR>/blind_sets.json, writes notas_{judge}.json (shipped as
data/panel/grades_{judge}.json). The no-search sensitivity run used the same script without the `tools` argument
(Claude: max_tokens=4096)."""
import json, os, re, sys, time
from pathlib import Path
import httpx

EXP = Path(__file__).resolve().parent.parent
for line in (open(EXP.parent.parent / ".env") if (EXP.parent.parent / ".env").exists() else []):
    if "=" in line and not line.strip().startswith("#"):
        k, v = line.strip().split("=", 1)
        os.environ.setdefault(k, v)
JUIZ = os.environ.get("JUIZ", "openai")
PAINEL = EXP / os.environ.get("PAINEL_DIR", "painel_busca")   # 21/out: igual ao detalhado + busca web opcional (como os juízes do Estudo 2)   # 19/out: tipo detalhado, título completo, n.d., ano 2026
SHARD = os.environ.get("SHARD")   # "k/N"
SUF = f"_s{SHARD.split('/')[0]}" if SHARD else ""
OUT = PAINEL / f"notas_{JUIZ}{SUF}.json"
BRUTO = PAINEL / f"brutos_{JUIZ}{SUF}.jsonl"
AX = ["relevance", "evidence_level", "recency", "sufficiency"]

PROMPT = """You are a senior physician judging the QUALITY OF THE REFERENCE LIST each tool returned for a real clinical question (judge the references, not any answer). Below are up to five anonymised reference lists (A-E). "(no references provided)" means the tool cited nothing.
Each item shows: title — year (n.d. = no date), publication type, source (journal, website domain or publisher).

Score EACH list on four axes, integer 1-4:
- relevance: on-topic and specific to THIS question (1 off-topic .. 4 tightly on-point)
- evidence_level: strength of evidence — guidelines/systematic reviews/RCTs high; case reports/blogs/generic sites low (1 weak .. 4 strong)
- recency: how up to date, from the years (1 old .. 4 current); the current year is 2026
- sufficiency: enough to answer the question well (1 insufficient .. 4 fully sufficient)
Non-scientific sources (blogs, social media, wikis, exam-question sites, file-sharing platforms, AI-generated content) count as weak evidence.
A "(no references provided)" list scores 1 on every axis.

QUESTION:
{pergunta}

{blocks}

Return ONLY JSON: {{"A":{{"relevance":N,"evidence_level":N,"recency":N,"sufficiency":N}},"B":{{...}},"C":{{...}},"D":{{...}},"E":{{...}}}}"""


def j_openai(p):
    from openai import OpenAI
    r = OpenAI(api_key=os.environ["OPENAI_API_KEY"]).responses.create(
        model="gpt-5.5", input=p, tools=[{"type": "web_search"}])
    return r.output_text, r.model


def j_gemini(p):
    key, model = os.environ["GEMINI_API_KEY"], os.getenv("GEMINI_MODEL", "gemini-3.1-pro-preview")
    r = httpx.post(f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={key}",
                   json={"contents": [{"parts": [{"text": p}]}], "tools": [{"google_search": {}}]}, timeout=600)
    r.raise_for_status()
    j = r.json()
    txt = "".join(x.get("text", "") for x in j["candidates"][0]["content"]["parts"])
    return txt, j.get("modelVersion", model)


def j_claude(p):
    import anthropic
    cli = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
    msgs, blocos, brutos = [{"role": "user", "content": p}], [], []
    for _ in range(5):  # continua se a API pausar o turno (pause_turn)
        r = cli.messages.create(model="claude-opus-4-8", max_tokens=16000, messages=msgs,
                                tools=[{"type": "web_search_20250305", "name": "web_search"}])
        brutos.append(r.model_dump(mode="json"))
        blocos += r.content
        if r.stop_reason != "pause_turn":
            break
        msgs = msgs + [{"role": "assistant", "content": r.content}]
    return "".join(b.text for b in blocos if b.type == "text"), r.model


JUIZES = {"openai": j_openai, "gemini": j_gemini, "claude": j_claude}


def parse(t, labels):
    d = None
    for m in reversed(list(re.finditer(r'\{\s*"A"\s*:', t))):   # com busca, pode haver texto antes do JSON
        try:
            d = json.JSONDecoder().raw_decode(t[m.start():])[0]; break
        except Exception:
            continue
    if d is None:
        raise ValueError("JSON não encontrado")
    out = {}
    for L in labels:
        out[L] = {a: int(d[L][a]) for a in AX}
        if not all(1 <= v <= 4 for v in out[L].values()):
            raise ValueError("nota fora de 1–4")
    return out


def main():
    sets = json.load(open(PAINEL / "blind_sets.json"))
    if SHARD:
        k, N = map(int, SHARD.split("/"))
        sets = {i: s for n, (i, s) in enumerate(sets.items()) if n % N == k}
    out = json.load(open(OUT)) if OUT.exists() else {}
    for idx, s in sets.items():
        if idx in out:
            continue
        labels = [L for L in "ABCDE" if L in s]
        blocks = "\n\n".join(f"--- Reference list {L} ---\n{s[L]}" for L in labels)
        p = PROMPT.format(pergunta=s["pergunta"], blocks=blocks)
        for tent in range(5):
            try:
                txt, modelo = JUIZES[JUIZ](p)
                out[idx] = parse(txt, labels)
                with open(BRUTO, "a") as f:
                    f.write(json.dumps({"idx": idx, "modelo": modelo, "texto": txt}, ensure_ascii=False) + "\n")
                break
            except Exception as e:
                print(idx, tent, repr(e)[:150], file=sys.stderr, flush=True)
                time.sleep(10 * (tent + 1))
        json.dump(out, open(OUT, "w"), indent=1)
    print(JUIZ, len(out), "de", len(sets))


if __name__ == "__main__":
    main()
