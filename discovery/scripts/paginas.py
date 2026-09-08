"""Pagina -> endpoints /api/* (seguindo imports locais) + tipos de lib/types."""
import os, re, json, collections
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
os.chdir(ROOT)
FE = "frontend"
IMPORT = re.compile(r'^\s*import\s+(?:type\s+)?(?:\{([^}]*)\}|[\w*\s,]+)\s+from\s+["\']([^"\']+)["\']', re.M)
API = re.compile(r"(/api/[^\"'`\s)]*)")

def resolve(spec, frm):
    if spec.startswith("@/"): cand = os.path.join(FE, spec[2:])
    elif spec.startswith("."): cand = os.path.normpath(os.path.join(os.path.dirname(frm), spec))
    else: return None
    for ext in (".tsx", ".ts", "/index.tsx", "/index.ts"):
        if os.path.isfile(cand + ext): return (cand + ext).replace(os.sep, "/")
    return cand.replace(os.sep, "/") if os.path.isfile(cand) else None

cache = {}
def read(p):
    if p not in cache:
        try: cache[p] = open(p, encoding="utf-8", errors="ignore").read()
        except OSError: cache[p] = ""
    return cache[p]

def norm(ep):
    """Normaliza template literals: /api/x/${id}/y -> /api/x/{}/y"""
    ep = re.sub(r"\$\{[^}]*\}", "{}", ep)
    return ep.split("?")[0].rstrip("/") or ep

def collect(path, seen):
    """Retorna (endpoints, tipos, arquivos_visitados)."""
    if path in seen: return set(), set(), set()
    seen.add(path)
    src = read(path)
    eps = {norm(e) for e in API.findall(src)}
    types, files = set(), {path}
    for names, spec in IMPORT.findall(src):
        tgt = resolve(spec, path)
        if not tgt: continue
        if "/lib/types/" in tgt:
            types.add(tgt)
            continue
        if not tgt.startswith(FE + "/"): continue
        # segue componentes e libs locais (nao segue node_modules)
        e2, t2, f2 = collect(tgt, seen)
        eps |= e2; types |= t2; files |= f2
    return eps, types, files

pages = []
for dp, dn, fn in os.walk(os.path.join(FE, "app")):
    dn[:] = [d for d in dn if d not in ("node_modules", ".next")]
    for f in fn:
        if f == "page.tsx": pages.append(os.path.join(dp, f).replace(os.sep, "/"))

rows = []
for p in sorted(pages):
    route = p[len(FE) + len("/app"):-len("/page.tsx")]
    route = re.sub(r"/\([^)]*\)", "", route) or "/"
    eps, types, files = collect(p, set())
    rows.append({"page": p, "route": route, "endpoints": sorted(eps),
                 "types": sorted(t.split("/")[-1] for t in types), "files_walked": len(files)})

json.dump(rows, open("discovery/data/paginas.json", "w"), indent=1)
with open("discovery/data/paginas.md", "w", encoding="utf-8") as fh:
    fh.write("# Pagina -> endpoints -> tipos\n\n")
    fh.write("Endpoints coletados seguindo os imports locais da pagina (componentes e libs de `frontend/`), ")
    fh.write("com template literals normalizados (`${x}` -> `{}`). Gerado por `discovery/scripts/paginas.py`.\n\n")
    fh.write(f"Total de paginas: **{len(rows)}**. Paginas sem nenhum endpoint: **{sum(1 for r in rows if not r['endpoints'])}**.\n\n")
    fh.write("| rota | page.tsx | arquivos seguidos | endpoints | tipos |\n|---|---|---:|---|---|\n")
    for r in rows:
        eps = "<br>".join(f"`{e}`" for e in r["endpoints"]) or "—"
        ts = ", ".join(f"`{t}`" for t in r["types"]) or "—"
        fh.write(f"| `{r['route']}` | `{r['page']}` | {r['files_walked']} | {eps} | {ts} |\n")
print("paginas:", len(rows), "endpoints distintos:", len({e for r in rows for e in r["endpoints"]}))
