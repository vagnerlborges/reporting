"""Grafo de imports entre subpacotes de backend/ (nivel backend/<x>)."""
import os, re, json, collections
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
BE = os.path.join(ROOT, "backend")
mods = sorted(d for d in os.listdir(BE) if os.path.isdir(os.path.join(BE, d)) and d != "__pycache__")
IMP = re.compile(r"^\s*(?:from\s+backend\.(\w+)|import\s+backend\.(\w+))", re.M)
edges = collections.Counter()
ext = collections.defaultdict(set)
EXTLIBS = ["fastapi","pydantic","psycopg","celery","boto3","httpx","requests","redis","jose","bcrypt","lxml","reportlab","pypdf","fitz","duckdb","alembic","anthropic","slowapi","kombu","pytz"]
for m in mods:
    base = os.path.join(BE, m)
    for dp, dn, fn in os.walk(base):
        dn[:] = [d for d in dn if d != "__pycache__"]
        for f in fn:
            if not f.endswith(".py"): continue
            src = open(os.path.join(dp, f), encoding="utf-8", errors="ignore").read()
            for a, b in IMP.findall(src):
                t = a or b
                if t in mods and t != m: edges[(m, t)] += 1
            for lib in EXTLIBS:
                if re.search(rf"^\s*(?:from|import)\s+{lib}\b", src, re.M):
                    ext[lib].add(m)
g = {m: set() for m in mods}
for (a, b) in edges: g[a].add(b)
rdeps = collections.defaultdict(set)
for a, bs in g.items():
    for b in bs: rdeps[b].add(a)
def reach(start, graph):
    seen, st = set(), [start]
    while st:
        for n in graph.get(st.pop(), ()):
            if n not in seen: seen.add(n); st.append(n)
    return seen
cycles = []
def dfs(n, path, vis):
    for nb in sorted(g[n]):
        if nb in path: cycles.append(path[path.index(nb):] + [nb])
        elif nb not in vis: vis.add(nb); dfs(nb, path + [nb], vis)
for m in mods: dfs(m, [m], {m})
uniq = sorted({" -> ".join(c) for c in cycles})
out = {
 "nodes": [{"id": m, "out_degree": len(g[m]), "in_degree": len(rdeps[m]),
            "impact_radius": len(reach(m, rdeps))} for m in mods],
 "edges": [{"from": a, "to": b, "weight": w} for (a, b), w in sorted(edges.items())],
 "cycles": uniq,
 "external": {k: sorted(v) for k, v in sorted(ext.items())},
}
json.dump(out, open(os.path.join(ROOT, "discovery/data/deps.json"), "w"), indent=1)
with open(os.path.join(ROOT, "discovery/data/deps.md"), "w", encoding="utf-8") as fh:
    fh.write("# Grafo de dependencias backend/*\n\n## Nos\n\n| modulo | depende de (out) | e usado por (in) | raio de impacto |\n|---|---:|---:|---:|\n")
    for n in sorted(out["nodes"], key=lambda x: -x["impact_radius"]):
        fh.write(f"| `{n['id']}` | {n['out_degree']} | {n['in_degree']} | {n['impact_radius']} |\n")
    fh.write("\n## Arestas (peso = nº de arquivos-import)\n\n")
    for e in sorted(out["edges"], key=lambda x: -x["weight"]):
        fh.write(f"- `{e['from']}` -> `{e['to']}` ({e['weight']})\n")
    fh.write(f"\n## Ciclos ({len(uniq)})\n\n")
    for c in uniq: fh.write(f"- {c}\n")
    fh.write("\n## Bibliotecas externas -> modulos que usam\n\n")
    for k, v in out["external"].items(): fh.write(f"- **{k}**: {', '.join('`'+x+'`' for x in v)}\n")
print("nodes", len(mods), "edges", len(edges), "cycles", len(uniq))
