"""Resumo por informe: paginas, endpoints, tasks, linhas de motor, % copiado, ultimo feat."""

import json
import os
import re
import datetime
import subprocess

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
os.chdir(ROOT)

INFORMES = ["3040", "3044", "3050", "3026", "cosif"]
ARQ = {
    "3040": [
        "backend/worker/tasks/engine3040_tasks.py",
        "backend/api/routes/engine3040.py",
    ],
    "3044": [
        "backend/worker/tasks/engine3044_tasks.py",
        "backend/api/routes/engine3044.py",
    ],
    "3050": [
        "backend/worker/tasks/engine3050_tasks.py",
        "backend/api/routes/engine3050.py",
    ],
    "3026": [
        "backend/worker/tasks/engine3026_tasks.py",
        "backend/api/routes/engine3026.py",
    ],
    "cosif": [
        "backend/worker/tasks/cosif_tasks.py",
        "backend/api/routes/cosif.py",
        "backend/api/routes/cosif_plano.py",
    ],
}
PLUGIN = {i: f"backend/plugins/cadoc_{i}" for i in INFORMES}

paginas = json.load(open("discovery/data/paginas.json"))
endpoints = json.load(open("discovery/data/endpoints.json"))
tasks = json.load(open("discovery/data/tasks.json"))["tasks"]
mot = json.load(open("discovery/data/motores.json"))


def marca(txt, inf):
    return re.search(inf if inf != "cosif" else "cosif", txt, re.I) is not None


linhas = subprocess.run(
    ["git", "log", "--pretty=format:%h|%ct|%s", "--name-only", "-n", "800"],
    capture_output=True,
    text=True,
    errors="ignore",
).stdout.splitlines()
commits, cur = [], None
for row in linhas:
    if (
        "|" in row
        and row.count("|") >= 2
        and not row.startswith(
            ("backend", "frontend", "tests", "e2e", "docs", "deploy")
        )
    ):
        h, t, s = row.split("|", 2)
        cur = {"h": h, "t": int(t), "s": s, "f": []}
        commits.append(cur)
    elif row.strip() and cur:
        cur["f"].append(row.strip())


res = []
for inf in INFORMES:
    pg = [p for p in paginas if marca(p["route"], inf) or marca(p["page"], inf)]
    eps = [
        e
        for e in endpoints
        if e["file"].replace(".py", "").endswith(inf) or marca(e["path"], inf)
    ]
    tk = [t for t in tasks if marca(t["module"], inf)]
    arqs = [a for a in ARQ[inf] if os.path.isfile(a)]
    lin = sum(len(open(a, encoding="utf-8", errors="ignore").readlines()) for a in arqs)
    plug = PLUGIN[inf]
    plin = 0
    if os.path.isdir(plug):
        for dp, dn, fn in os.walk(plug):
            dn[:] = [d for d in dn if d != "__pycache__"]
            plin += sum(
                len(
                    open(
                        os.path.join(dp, f), encoding="utf-8", errors="ignore"
                    ).readlines()
                )
                for f in fn
                if f.endswith(".py")
            )
    cob = mot["cobertura"].get(inf, {"total": 0, "dup": 0})
    pct = 100 * cob["dup"] / cob["total"] if cob["total"] else 0
    bundle = (
        "backend/engine/cosif.py" if inf == "cosif" else f"backend/engine/cadoc{inf}.py"
    )
    tem_bundle = os.path.isfile(bundle)
    dispatch = any(
        re.search(
            r"get_engine_registry\(\)\.dispatch",
            open(a, encoding="utf-8", errors="ignore").read(),
        )
        for a in arqs
    )
    feat = next(
        (
            c
            for c in commits
            if c["s"].startswith("feat")
            and any(marca(f, inf) and f.startswith(("backend/", "frontend/")) for f in c["f"])
        ),
        None,
    )
    res.append(
        {
            "informe": inf,
            "paginas": len(pg),
            "endpoints": len(eps),
            "tasks": len(tk),
            "linhas_motor": lin,
            "linhas_plugin": plin,
            "pct_copiado": round(pct),
            "bundle": tem_bundle,
            "dispatch": dispatch,
            "ultimo_feat": (
                f"{feat['h']} {datetime.datetime.utcfromtimestamp(feat['t']).date()} "
                f"{feat['s'][:55]}"
            )
            if feat
            else "-",
            "rotas_pag": sorted(p["route"] for p in pg),
        }
    )

with open("discovery/data/resumo-informes.md", "w", encoding="utf-8") as fh:
    fh.write("# Resumo por informe\n\nGerado por `discovery/scripts/resumo.py`.\n\n")
    fh.write(
        "| informe | paginas | endpoints | tasks | l. motor (task+rota) | l. plugin | "
        "% linhas copiadas de outro motor | bundle CadocEngine | dispatch em runtime | ultimo feat |\n"
    )
    fh.write("|---|---:|---:|---:|---:|---:|---:|:-:|:-:|---|\n")
    for r in res:
        fh.write(
            f"| **{r['informe']}** | {r['paginas']} | {r['endpoints']} | {r['tasks']} | "
            f"{r['linhas_motor']} | {r['linhas_plugin']} | {r['pct_copiado']}% | "
            f"{'sim' if r['bundle'] else 'nao'} | {'sim' if r['dispatch'] else 'NAO'} | "
            f"{r['ultimo_feat']} |\n"
        )
    fh.write("\n## Paginas por informe\n\n| informe | rotas |\n|---|---|\n")
    for r in res:
        fh.write(
            f"| {r['informe']} | {', '.join('`' + x + '`' for x in r['rotas_pag']) or '-'} |\n"
        )

json.dump(res, open("discovery/data/resumo-informes.json", "w"), indent=1)
for r in res:
    print(
        r["informe"],
        r["paginas"],
        "pg",
        r["endpoints"],
        "ep",
        r["tasks"],
        "tk",
        r["linhas_motor"],
        "l",
        r["pct_copiado"],
        "%",
    )
