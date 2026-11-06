# Judge prompt — reference-quality panel

Exact prompt sent to each judge (`judge_panel.py`); `{pergunta}` and `{blocks}` are filled per question (lists from `build_panel_lists_detailed.py`). Double braces are literal braces.

Sensitivity analysis (coarse types, `build_panel_lists.py`): same prompt except `title — year, type, source` and `(1 old .. 4 current)` without the sentence on the current year.

```
You are a senior physician judging the QUALITY OF THE REFERENCE LIST each tool returned for a real clinical question (judge the references, not any answer). Below are up to five anonymised reference lists (A-E). "(no references provided)" means the tool cited nothing.
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

Return ONLY JSON: {{"A":{{"relevance":N,"evidence_level":N,"recency":N,"sufficiency":N}},"B":{{...}},"C":{{...}},"D":{{...}},"E":{{...}}}}
```
