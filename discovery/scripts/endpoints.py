"""Endpoint -> consumidores (front/e2e) + stores + tasks enfileiradas."""
import ast, os, re, json, collections
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
os.chdir(ROOT)
RD = "backend/api/routes"
METHODS = {"get", "post", "put", "patch", "delete", "head", "options"}

def norm(p):
    p = re.sub(r"\{[^}]*\}", "{}", p)
    return p.rstrip("/") or "/"

# --- consumidores ---
pages = json.load(open("discovery/data/paginas.json"))
front = collections.defaultdict(list)
for r in pages:
    for e in r["endpoints"]: front[e].append(r["route"])

API_RE = re.compile(r'["\'`](/api/[^"\'`\s]*)')
def norm_lit(e): return norm(re.sub(r"\$\{[^}]*\}", "{}", e).split("?")[0])
e2e = collections.defaultdict(set)
for dp, dn, fn in os.walk("e2e"):
    dn[:] = [d for d in dn if d != "node_modules"]
    for f in fn:
        if not f.endswith((".ts", ".py")): continue
        p = os.path.join(dp, f)
        for e in API_RE.findall(open(p, encoding="utf-8", errors="ignore").read()):
            e2e[norm_lit(e)].add(f)
# mencao em outro codigo backend/scripts/docs de teste
backref = collections.defaultdict(set)
for base in ("backend", "tests", "scripts"):
    for dp, dn, fn in os.walk(base):
        dn[:] = [d for d in dn if d != "__pycache__"]
        for f in fn:
            if not f.endswith(".py"): continue
            p = os.path.join(dp, f).replace(os.sep, "/")
            if p.startswith(RD): continue
            for e in API_RE.findall(open(p, encoding="utf-8", errors="ignore").read()):
                backref[norm_lit(e)].add(p)

rows = []
for f in sorted(os.listdir(RD)):
    if not f.endswith(".py") or f == "__init__.py": continue
    path = f"{RD}/{f}"
    src = open(path, encoding="utf-8", errors="ignore").read()
    tree = ast.parse(src)
    # prefixos declarados no modulo
    prefixes = {}
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign) and isinstance(node.value, ast.Call) \
           and getattr(node.value.func, "id", "") == "APIRouter":
            name = getattr(node.targets[0], "id", "router")
            pre = ""
            for kw in node.value.keywords:
                if kw.arg == "prefix" and isinstance(kw.value, ast.Constant): pre = kw.value.value
            prefixes[name] = pre
    for node in ast.walk(tree):
        if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)): continue
        for dec in node.decorator_list:
            if not isinstance(dec, ast.Call): continue
            fn = dec.func
            if not isinstance(fn, ast.Attribute) or fn.attr not in METHODS: continue
            rname = getattr(fn.value, "id", "router")
            sub = dec.args[0].value if dec.args and isinstance(dec.args[0], ast.Constant) else ""
            full = norm(prefixes.get(rname, "") + sub)
            body = ast.get_source_segment(src, node) or ""
            stores = sorted(set(re.findall(r"backend\.storage\.(\w+)", body)) |
                            set(re.findall(r"(\w+Store)\(", body)))
            tasks = sorted(set(re.findall(r"(\w+)\.delay\(", body)) |
                           set(re.findall(r"(\w+)\.apply_async\(", body)) |
                           set(re.findall(r'send_task\(\s*["\']([\w.]+)', body)))
            guard = sorted(set(re.findall(r"require_(?:permission|role)\(\s*\"?([\w., \"]*)", body)))
            rows.append({
                "file": f, "method": fn.attr.upper(), "path": full, "func": node.name,
                "lines": len(body.splitlines()),
                "stores": stores, "tasks": tasks, "guard": bool(guard),
                "front": sorted(set(front.get(full, []))),
                "e2e": sorted(e2e.get(full, [])),
                "backref": sorted(backref.get(full, [])),
            })

# endpoints do front que nao existem no backend
known = {r["path"] for r in rows}
orphan_pages = collections.defaultdict(list)
for e, pgs in front.items():
    if e not in known and not any(e.startswith(k) for k in known):
        orphan_pages[e] = sorted(set(pgs))

json.dump(rows, open("discovery/data/endpoints.json", "w"), indent=1)
dead = [r for r in rows if not r["front"] and not r["e2e"] and not r["backref"]]
with open("discovery/data/endpoints.md", "w", encoding="utf-8") as fh:
    fh.write("# Endpoints -> consumidores, stores, tasks\n\nGerado por `discovery/scripts/endpoints.py` (AST dos decoradores).\n\n")
    fh.write(f"Total de operacoes HTTP: **{len(rows)}** em {len({r['file'] for r in rows})} modulos.\n\n")
    fh.write("| metodo | path | modulo:funcao | l. | guard | stores | tasks | front | e2e | backref |\n")
    fh.write("|---|---|---|---:|:-:|---|---|---|---|---|\n")
    for r in sorted(rows, key=lambda x: (x["file"], x["path"])):
        fh.write(f"| {r['method']} | `{r['path']}` | `{r['file']}:{r['func']}` | {r['lines']} | "
                 f"{'S' if r['guard'] else '-'} | {', '.join(r['stores']) or '—'} | {', '.join(f'`{t}`' for t in r['tasks']) or '—'} | "
                 f"{', '.join(r['front']) or '—'} | {', '.join(r['e2e']) or '—'} | {len(r['backref']) or '—'} |\n")
    fh.write(f"\n## Endpoints SEM consumidor (nem front, nem e2e, nem outro codigo): {len(dead)}\n\n")
    by = collections.defaultdict(list)
    for r in dead: by[r["file"]].append(r)
    for k in sorted(by, key=lambda x: -len(by[x])):
        fh.write(f"\n### `{k}` ({len(by[k])})\n\n")
        for r in by[k]: fh.write(f"- `{r['method']} {r['path']}` — `{r['func']}` ({r['lines']} l.)\n")
    fh.write(f"\n## Endpoints chamados pelo front que NAO existem no backend: {len(orphan_pages)}\n\n")
    for e, pgs in sorted(orphan_pages.items()):
        fh.write(f"- `{e}` — chamado por: {', '.join(pgs)}\n")
print("ops:", len(rows), "sem consumidor:", len(dead), "orfaos do front:", len(orphan_pages))
