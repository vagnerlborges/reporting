"""Dimensoes RC18: modulo, entradas, acoplamento a informe. + imports de saida do pacote quality."""

import ast
import os
import re
import json
import collections

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
os.chdir(ROOT)
Q = "backend/quality"

src = open(f"{Q}/dimensions.py", encoding="utf-8", errors="ignore").read()
tree = ast.parse(src)
names = []
for node in tree.body:
    if (
        isinstance(node, ast.AnnAssign)
        and getattr(node.target, "id", "") == "DIMENSION_NAMES"
    ):
        names = ast.literal_eval(node.value)
    if (
        isinstance(node, ast.Assign)
        and getattr(node.targets[0], "id", "") == "DIMENSION_NAMES"
    ):
        names = ast.literal_eval(node.value)


def const_dict(var):
    for node in tree.body:
        tgt = getattr(node, "target", None) or (
            node.targets[0] if isinstance(node, ast.Assign) else None
        )
        if tgt is not None and getattr(tgt, "id", "") == var:
            try:
                return ast.literal_eval(node.value)
            except Exception:
                return {}
    return {}


kind = const_dict("DIMENSION_KIND")
weights = const_dict("DIMENSION_WEIGHTS")

# funcao avaliadora de cada dimensao + chaves de entrada que ela le
evald = {}
for node in ast.walk(tree):
    if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
        continue
    if not node.name.startswith('evaluate_') or node.name == 'evaluate_all_dimensions':
        continue
    seg = ast.get_source_segment(src, node) or ''
    m = re.search('"dimension":\\s*"(\\w+)"', seg)
    if not m:
        continue
    d = m.group(1)
    params = [a.arg for a in node.args.args] + [a.arg for a in node.args.kwonlyargs]
    cur = evald.setdefault(d, {'funcs': [], 'entradas': set(), 'lines': 0})
    cur['funcs'].append(node.name)
    cur['entradas'] |= set(params)
    cur['lines'] += len(seg.splitlines())

# acoplamento a informe: por MODULO do pacote quality
ACOPL = re.compile(
    r"backend\.(flows|plugins|api|worker|cadoc_adapters)\b|"
    r'["\'](3040|3042|3044|3050|3026)["\']|cadoc_\w+'
)
mods = []
for dp, dn, fn in os.walk(Q):
    dn[:] = [d for d in dn if d != "__pycache__"]
    for f in sorted(fn):
        if not f.endswith(".py") or f == "__init__.py":
            continue
        p = os.path.join(dp, f).replace(os.sep, "/")
        s = open(p, encoding="utf-8", errors="ignore").read()
        hits = collections.Counter(m.group(0) for m in ACOPL.finditer(s))
        mods.append(
            {
                "file": p,
                "lines": len(s.splitlines()),
                "acoplado": bool(hits),
                "sinais": dict(hits.most_common(6)),
            }
        )

# imports de saida do pacote quality
OUT = re.compile(r"^\s*from\s+backend\.(\w+)([\w.]*)\s+import\s+([^\n#]+)", re.M)
saidas = []
for m in mods:
    s = open(m["file"], encoding="utf-8", errors="ignore").read()
    for pkg, rest, what in OUT.findall(s):
        if pkg == "quality":
            continue
        saidas.append(
            {
                "de": m["file"],
                "para": f"backend.{pkg}{rest}",
                "pkg": pkg,
                "importa": what.strip()[:70],
            }
        )

# batimento / conciliacao no repo
RECON = re.compile(r"concilia|batimento|cruza|reconcil|amarraca|amarração", re.I)
recon = []
for base in ("backend",):
    for dp, dn, fn in os.walk(base):
        dn[:] = [d for d in dn if d != "__pycache__"]
        for f in fn:
            if not f.endswith(".py"):
                continue
            p = os.path.join(dp, f).replace(os.sep, "/")
            s = open(p, encoding="utf-8", errors="ignore").read()
            n = len(RECON.findall(s))
            if n:
                recon.append({"file": p, "hits": n, "lines": len(s.splitlines())})
recon.sort(key=lambda x: -x["hits"])

with open("discovery/data/quality.md", "w", encoding="utf-8") as fh:
    fh.write("# `backend/quality` - dimensoes RC18, acoplamento e saidas\n\n")
    fh.write("Gerado por `discovery/scripts/quality.py`.\n\n")
    fh.write(f"## As {len(names)} dimensoes\n\n")
    fh.write(
        "| dimensao | peso | natureza | avaliador(es) | l. | parametros de entrada |\n"
    )
    fh.write("|---|---:|---|---|---:|---|\n")
    for d in names:
        e = evald.get(d, {"funcs": [], "entradas": set(), "lines": 0})
        ent = ", ".join(f"`{x}`" for x in sorted(e["entradas"])[:8]) or "-"
        fh.write(
            f"| `{d}` | {weights.get(d, '-')} | {kind.get(d, '-')} | "
            f"{', '.join('`' + x + '`' for x in e['funcs']) or '-'} | {e['lines']} | {ent} |\n"
        )

    ac = [m for m in mods if m["acoplado"]]
    fh.write(
        f"\n## Acoplamento a informe por modulo ({len(ac)} de {len(mods)} acoplados)\n\n"
    )
    fh.write(
        "Sinal = import de `flows`/`plugins`/`api`/`worker`/`cadoc_adapters` ou literal de informe.\n\n"
    )
    fh.write("| modulo | l. | acoplado | sinais |\n|---|---:|:-:|---|\n")
    for m in sorted(mods, key=lambda x: (not x["acoplado"], x["file"])):
        sig = ", ".join(f"`{k}`x{v}" for k, v in m["sinais"].items()) or "-"
        fh.write(
            f"| `{m['file'].replace('backend/quality/', '')}` | {m['lines']} | "
            f"{'SIM' if m['acoplado'] else 'nao'} | {sig} |\n"
        )

    fh.write(
        f"\n## Imports de saida do pacote ({len(saidas)})\n\n| de | para | importa |\n|---|---|---|\n"
    )
    for s in sorted(saidas, key=lambda x: (x["pkg"], x["de"])):
        fh.write(
            f"| `{s['de'].replace('backend/quality/', '')}` | `{s['para']}` | `{s['importa']}` |\n"
        )
    dist = collections.Counter(s["pkg"] for s in saidas)
    fh.write(
        "\nPor pacote destino: "
        + ", ".join(f"`{k}` {v}" for k, v in dist.most_common())
        + "\n"
    )

    fh.write(f"\n## Batimento / conciliacao no backend ({len(recon)} arquivos)\n\n")
    fh.write("| arquivo | ocorrencias | l. |\n|---|---:|---:|\n")
    for r in recon[:25]:
        fh.write(f"| `{r['file']}` | {r['hits']} | {r['lines']} |\n")

json.dump(
    {
        "names": names,
        "weights": weights,
        "kind": kind,
        "eval": {
            k: {
                "funcs": v["funcs"],
                "entradas": sorted(v["entradas"]),
                "lines": v["lines"],
            }
            for k, v in evald.items()
        },
        "mods": mods,
        "saidas": saidas,
        "recon": recon,
    },
    open("discovery/data/quality.json", "w"),
    indent=1,
)
print(
    "dimensoes:",
    len(names),
    "modulos:",
    len(mods),
    "acoplados:",
    sum(1 for m in mods if m["acoplado"]),
    "saidas:",
    len(saidas),
    "arquivos com concilia*:",
    len(recon),
)
