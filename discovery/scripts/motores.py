"""Duplicacao entre motores: funcoes por arquivo + similaridade cruzada (difflib sobre corpo normalizado)."""

import ast
import os
import re
import json
import difflib
import collections
import itertools

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
os.chdir(ROOT)

MOTORES = {
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
    "cosif": ["backend/worker/tasks/cosif_tasks.py", "backend/api/routes/cosif.py"],
}

# tokens que so diferem pelo numero do informe / nome do motor
NUM = re.compile(r"\b(3040|3044|3050|3026|cosif|COSIF)\b")


def norm_body(node, src):
    """Corpo normalizado: sem docstring, sem literais de numero de informe, sem espaco."""
    body = list(node.body)
    if (
        body
        and isinstance(body[0], ast.Expr)
        and isinstance(body[0].value, ast.Constant)
        and isinstance(body[0].value.value, str)
    ):
        body = body[1:]
    txt = "\n".join(ast.get_source_segment(src, b) or "" for b in body)
    txt = NUM.sub("N", txt)
    txt = re.sub(r"#.*", "", txt)
    txt = re.sub(r"\s+", " ", txt).strip()
    return txt


def sig(node):
    args = [a.arg for a in node.args.args]
    if node.args.vararg:
        args.append("*" + node.args.vararg.arg)
    args += [a.arg + "=" for a in node.args.kwonlyargs]
    if node.args.kwarg:
        args.append("**" + node.args.kwarg.arg)
    return f"{node.name}({', '.join(args)})"


funcs = []
for informe, paths in MOTORES.items():
    for p in paths:
        if not os.path.isfile(p):
            continue
        src = open(p, encoding="utf-8", errors="ignore").read()
        tree = ast.parse(src)
        for node in tree.body:
            if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                continue
            seg = ast.get_source_segment(src, node) or ""
            decs = [ast.get_source_segment(src, d) or "" for d in node.decorator_list]
            kind = (
                "task"
                if any("task" in d for d in decs)
                else (
                    "rota"
                    if any(
                        re.search(r"\.(get|post|put|patch|delete)\(", d) for d in decs
                    )
                    else "funcao"
                )
            )
            funcs.append(
                {
                    "informe": informe,
                    "file": p,
                    "name": node.name,
                    "sig": sig(node),
                    "kind": kind,
                    "lines": len(seg.splitlines()),
                    "norm": norm_body(node, src),
                    "norm_len": len(norm_body(node, src)),
                }
            )

# --- pares similares entre motores DIFERENTES ---
pairs = []
for a, b in itertools.combinations(funcs, 2):
    if a["informe"] == b["informe"]:
        continue
    if a["norm_len"] < 120 or b["norm_len"] < 120:
        continue  # corpos triviais geram ruido
    if abs(a["norm_len"] - b["norm_len"]) / max(a["norm_len"], b["norm_len"]) > 0.6:
        continue
    r = difflib.SequenceMatcher(None, a["norm"], b["norm"]).ratio()
    if r > 0.70:
        pairs.append({"ratio": round(r, 3), "a": a, "b": b})
pairs.sort(key=lambda x: -x["ratio"])

# --- % de linhas de cada motor com equivalente em outro motor ---
best = collections.defaultdict(float)
for pr in pairs:
    for side, other in (("a", "b"), ("b", "a")):
        k = (pr[side]["file"], pr[side]["name"])
        best[k] = max(best[k], pr["ratio"])

cobertura = collections.defaultdict(
    lambda: {"total": 0, "dup": 0, "nfun": 0, "ndup": 0}
)
for f in funcs:
    c = cobertura[f["informe"]]
    c["total"] += f["lines"]
    c["nfun"] += 1
    if best.get((f["file"], f["name"]), 0) > 0.70:
        c["dup"] += f["lines"]
        c["ndup"] += 1

# --- etapas do pipeline x informe ---
ETAPAS = {
    "process_file": r"^process_\w*file|^_run_process",
    "consolidate": r"^consolidate|^_run_consolidate",
    "sftp_watch": r"^sftp_watch|^_run_sftp",
    "alert_prazo": r"^alert_prazo|^alert_fonte",
    "regenerate/retific": r"^regenerate|^retific",
}
etapa_tab = collections.defaultdict(dict)
for f in funcs:
    for etapa, pat in ETAPAS.items():
        if re.search(pat, f["name"]):
            cur = etapa_tab[etapa].get(f["informe"], [])
            cur.append(f)
            etapa_tab[etapa][f["informe"]] = cur

# --- o que existe em engine/base.py ---
base_src = open("backend/engine/base.py", encoding="utf-8", errors="ignore").read()
base_tree = ast.parse(base_src)
base_names = sorted(
    {
        n.name
        for n in ast.walk(base_tree)
        if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef))
    }
)
base_actions = (
    re.findall(
        r'"(\w+)"', re.search(r"ACTIONS?\s*[:=].*?\n\n", base_src, re.S).group(0)
    )
    if re.search(r"ACTIONS?\s*[:=].*?\n\n", base_src, re.S)
    else []
)

# quais motores instanciam/usam o CadocEngine
usa_base = {}
for informe, paths in MOTORES.items():
    hits = []
    for p in paths:
        if not os.path.isfile(p):
            continue
        s = open(p, encoding="utf-8", errors="ignore").read()
        if re.search(r"CadocEngine|EngineSteps|engine\.base|engine\.cadoc", s):
            hits.append(p)
    # bundle dedicado em backend/engine/cadocNNNN.py
    bundle = ("backend/engine/cosif.py" if informe == "cosif"
              else f"backend/engine/cadoc{informe}.py")
    if os.path.isfile(bundle):
        hits.append(bundle)
    usa_base[informe] = hits

json.dump(
    {
        "funcs": [{k: v for k, v in f.items() if k != "norm"} for f in funcs],
        "pairs": [
            {
                "ratio": p["ratio"],
                "a": f"{p['a']['informe']}:{p['a']['file'].split('/')[-1]}:{p['a']['name']}",
                "b": f"{p['b']['informe']}:{p['b']['file'].split('/')[-1]}:{p['b']['name']}",
                "lines_a": p["a"]["lines"],
                "lines_b": p["b"]["lines"],
            }
            for p in pairs
        ],
        "cobertura": dict(cobertura),
        "base_names": base_names,
        "base_actions": base_actions,
        "usa_base": usa_base,
    },
    open("discovery/data/motores.json", "w"),
    indent=1,
)

with open("discovery/data/motores.md", "w", encoding="utf-8") as fh:
    fh.write(
        "# Duplicacao entre motores\n\nGerado por `discovery/scripts/motores.py`.\n\n"
    )
    fh.write(
        "Criterio de similaridade: `difflib.SequenceMatcher` sobre o corpo da funcao "
        "normalizado (docstring removida, comentarios removidos, literais `3040|3044|3050|3026|cosif` "
        "trocados por `N`, espaco colapsado). Corpos com menos de 120 caracteres normalizados sao "
        "ignorados (ruido). Pares reportados: ratio > 0.70 entre motores DIFERENTES.\n\n"
    )

    fh.write("## Funcoes por arquivo\n\n")
    for informe, paths in MOTORES.items():
        for p in paths:
            fs = [f for f in funcs if f["file"] == p]
            if not fs:
                continue
            fh.write(
                f"\n### `{p}` ({len(fs)} funcoes de topo, {sum(x['lines'] for x in fs)} linhas)\n\n"
            )
            fh.write(
                "| tipo | assinatura | l. | melhor par em outro motor |\n|---|---|---:|---|\n"
            )
            for f in fs:
                r = best.get((f["file"], f["name"]), 0)
                fh.write(
                    f"| {f['kind']} | `{f['sig']}` | {f['lines']} | {f'{r:.0%}' if r else '-'} |\n"
                )

    fh.write(f"\n## Pares similares entre motores ({len(pairs)})\n\n")
    fh.write("| similaridade | A | l. | B | l. |\n|---:|---|---:|---|---:|\n")
    for p in pairs:
        fh.write(
            f"| {p['ratio']:.0%} | `{p['a']['informe']} :: {p['a']['name']}` | {p['a']['lines']} | "
            f"`{p['b']['informe']} :: {p['b']['name']}` | {p['b']['lines']} |\n"
        )

    fh.write("\n## % de linhas com equivalente em outro motor\n\n")
    fh.write(
        "| informe | funcoes | linhas | funcoes com par | linhas com par | % linhas |\n|---|---:|---:|---:|---:|---:|\n"
    )
    for k, c in sorted(cobertura.items()):
        pct = 100 * c["dup"] / c["total"] if c["total"] else 0
        fh.write(
            f"| {k} | {c['nfun']} | {c['total']} | {c['ndup']} | {c['dup']} | {pct:.0f}% |\n"
        )

    fh.write("\n## Etapa do pipeline x informe\n\n")
    informes = list(MOTORES)
    fh.write(
        "| etapa | "
        + " | ".join(informes)
        + " |\n|---|"
        + "---|" * len(informes)
        + "\n"
    )
    for etapa in ETAPAS:
        cells = []
        for i in informes:
            fs = etapa_tab.get(etapa, {}).get(i)
            if not fs:
                cells.append("nao existe")
            else:
                n = sum(x["lines"] for x in fs)
                cells.append(f"copiado ({n} l.)")
        fh.write(f"| {etapa} | " + " | ".join(cells) + " |\n")

    fh.write(
        f"\n## `backend/engine/base.py`\n\nDefinicoes de topo: {', '.join('`' + n + '`' for n in base_names)}\n\n"
    )
    fh.write("### Bundle CadocEngine por informe + dispatch em runtime" + "\n\n")
    fh.write("| informe | bundle | passos | dispatch() em runtime |" + "\n")
    fh.write("|---|---|---|---|" + "\n")
    DISP = re.compile("get_engine_registry" + re.escape("().") + "dispatch")
    PASSO = "def (process_file|consolidate|sftp_watch|alert_prazo)"
    for k, v in usa_base.items():
        bf = [x for x in v if x.startswith("backend/engine/")]
        bsrc = open(bf[0], encoding="utf-8", errors="ignore").read() if bf else ""
        passos = sorted(set(re.findall(PASSO, bsrc)))
        disp = [x for x in MOTORES[k] if os.path.isfile(x)
                and DISP.search(open(x, encoding="utf-8", errors="ignore").read())]
        nome = ("`" + bf[0] + "`") if bf else "**nenhum**"
        dtxt = ", ".join("`" + x.split("/")[-1] + "`" for x in disp) or "**nao**"
        fh.write("| %s | %s | %s | %s |" % (k, nome, ", ".join(passos) or "-", dtxt) + "\n")

print("funcs:", len(funcs), "pares:", len(pairs))
for k, c in sorted(cobertura.items()):
    print(
        " ",
        k,
        c["nfun"],
        "fn",
        c["total"],
        "l.",
        f"{100 * c['dup'] / max(c['total'], 1):.0f}% dup",
    )
