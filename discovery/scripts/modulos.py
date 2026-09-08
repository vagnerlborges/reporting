"""Conta arquivos e linhas por modulo de topo (e 1 nivel abaixo) dos pacotes principais."""
import os, json, sys
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
SKIP = {".git", "node_modules", ".next", "__pycache__", ".venv", "venv", "dattos_informes_legais.egg-info", "discovery", ".pytest_cache"}
EXT = {".py", ".ts", ".tsx", ".js", ".jsx", ".sql", ".yaml", ".yml", ".tf", ".md", ".json", ".xsd"}

def walk(base):
    n = l = 0
    for dp, dn, fn in os.walk(base):
        dn[:] = [d for d in dn if d not in SKIP]
        for f in fn:
            if os.path.splitext(f)[1] not in EXT: continue
            p = os.path.join(dp, f)
            n += 1
            try: l += sum(1 for _ in open(p, encoding="utf-8", errors="ignore"))
            except OSError: pass
    return n, l

rows = []
for top in sorted(os.listdir(ROOT)):
    tp = os.path.join(ROOT, top)
    if top in SKIP or not os.path.isdir(tp): continue
    n, l = walk(tp)
    rows.append({"path": top, "files": n, "lines": l, "level": 0})
    for sub in sorted(os.listdir(tp)):
        sp = os.path.join(tp, sub)
        if sub in SKIP or not os.path.isdir(sp): continue
        sn, sl = walk(sp)
        if sn: rows.append({"path": f"{top}/{sub}", "files": sn, "lines": sl, "level": 1})
json.dump(rows, open(os.path.join(ROOT, "discovery/data/modulos.json"), "w"), indent=1)
with open(os.path.join(ROOT, "discovery/data/modulos.md"), "w", encoding="utf-8") as fh:
    fh.write("| caminho | arquivos | linhas |\n|---|---:|---:|\n")
    for r in rows:
        pad = "&nbsp;&nbsp;" if r["level"] else ""
        fh.write(f"| {pad}`{r['path']}` | {r['files']} | {r['lines']} |\n")
print(len(rows), "linhas")
