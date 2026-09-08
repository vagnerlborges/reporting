"""2a passagem: confirma os endpoints sem consumidor contra o texto BRUTO do front/e2e.

A 1a passagem (endpoints.py) casa caminhos normalizados; template literals com literal de
informe (`/api/painel/3040/${p}/aprovar`) ou query colada (`events.csv?${qs}`) escapam.
Aqui o path vira regex (`{}` -> segmento livre) e busca no corpus inteiro.
"""

import json
import os
import re

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
os.chdir(ROOT)

ep = json.load(open("discovery/data/endpoints.json"))
dead = [e for e in ep if not e["front"] and not e["e2e"] and not e["backref"]]

corpus = []
for base in ("frontend/app", "frontend/components", "frontend/lib", "e2e/tests"):
    for dp, dn, fn in os.walk(base):
        dn[:] = [d for d in dn if d not in ("node_modules", ".next")]
        for f in fn:
            if f.endswith((".ts", ".tsx")):
                corpus.append(
                    open(os.path.join(dp, f), encoding="utf-8", errors="ignore").read()
                )
blob = "\n".join(corpus)

LIVRE = r"/[^/\"'`\s]*"
conf, falso = [], []
for e in dead:
    pat = "".join(
        LIVRE if s == "{}" else "/" + re.escape(s)
        for s in e["path"].strip("/").split("/")
    )
    (falso if re.search(pat, blob) else conf).append(e)

with open("discovery/data/endpoints-mortos.md", "w", encoding="utf-8") as fh:
    fh.write(
        "# Endpoints sem consumidor - confirmados\n\nGerado por `discovery/scripts/mortos.py`.\n\n"
    )
    fh.write(
        f"Candidatos da 1a passagem: **{len(dead)}**. "
        f"Falsos negativos descartados na 2a: **{len(falso)}**. "
        f"Confirmados: **{len(conf)}**.\n\n"
    )
    fh.write(
        "## Confirmados sem nenhum consumidor\n\n| metodo | path | modulo:funcao | l. |\n|---|---|---|---:|\n"
    )
    for e in conf:
        fh.write(
            f"| {e['method']} | `{e['path']}` | `{e['file']}:{e['func']}` | {e['lines']} |\n"
        )
    fh.write(
        "\n## Descartados (achados na 2a passagem, no texto bruto)\n\n| metodo | path |\n|---|---|\n"
    )
    for e in falso:
        fh.write(f"| {e['method']} | `{e['path']}` |\n")

json.dump(
    [{k: e[k] for k in ("method", "path", "file", "func", "lines")} for e in conf],
    open("discovery/data/endpoints-mortos.json", "w"),
    indent=1,
)
print(
    "candidatos:", len(dead), "falsos negativos:", len(falso), "confirmados:", len(conf)
)
