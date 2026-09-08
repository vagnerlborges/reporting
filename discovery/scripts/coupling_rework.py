"""Acoplamento por mudanca (arquivos que mudam juntos) + retrabalho + TODO/FIXME."""
import subprocess, collections, itertools, os, re, json
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
os.chdir(ROOT)
raw = subprocess.run(["git","log","--since=6 months ago","--pretty=format:@@%H|%ct|%s","--name-only"],
                     capture_output=True, text=True, errors="ignore").stdout
commits, cur = [], None
for line in raw.splitlines():
    if line.startswith("@@"):
        h, ts, subj = line[2:].split("|", 2)
        cur = {"h": h, "ts": int(ts), "subj": subj, "files": []}
        commits.append(cur)
    elif line.strip() and cur is not None:
        cur["files"].append(line.strip())

pair = collections.Counter(); solo = collections.Counter()
for c in commits:
    fs = sorted(set(f for f in c["files"] if f.endswith((".py", ".tsx", ".ts"))))
    if len(fs) > 25: continue  # commits gigantes distorcem
    for f in fs: solo[f] += 1
    for a, b in itertools.combinations(fs, 2): pair[(a, b)] += 1

# retrabalho: fix/ajuste/corrige em <=2 dias tocando arquivo de um feat anterior
FIX = re.compile(r"^(fix|ajuste|corrige|hotfix)", re.I)
byfile = collections.defaultdict(list)
for c in sorted(commits, key=lambda x: x["ts"]):
    for f in c["files"]: byfile[f].append(c)
rework = {}
for c in commits:
    if not FIX.match(c["subj"]): continue
    for f in c["files"]:
        for prev in byfile[f]:
            if prev["h"] == c["h"]: continue
            if prev["subj"].startswith("feat") and 0 < c["ts"] - prev["ts"] <= 2*86400:
                rework[c["h"]] = (c["subj"], prev["subj"], f); break
        if c["h"] in rework: break

todo = collections.Counter(); samples = []
for dp, dn, fn in os.walk("."):
    dn[:] = [d for d in dn if d not in {".git","node_modules",".next","__pycache__","discovery",".venv","dattos_informes_legais.egg-info",".ruff_cache"}]
    for f in fn:
        if not f.endswith((".py",".ts",".tsx",".js",".sql")): continue
        p = os.path.join(dp, f)
        try: txt = open(p, encoding="utf-8", errors="ignore").read()
        except OSError: continue
        n = len(re.findall(r"\b(TODO|FIXME|HACK|XXX)\b", txt))
        if n:
            todo["/".join(p.split(os.sep)[1:3])] += n
            if len(samples) < 15: samples.append(p.replace(os.sep, "/")[2:])

with open("discovery/data/coupling.md", "w", encoding="utf-8") as fh:
    fh.write("# Acoplamento por mudanca (top 25 pares, 6 meses, commits <=25 arquivos)\n\n")
    fh.write("| juntos | % do menor | arquivo A | arquivo B |\n|---:|---:|---|---|\n")
    for (a,b), n in pair.most_common(25):
        pct = round(100*n/min(solo[a], solo[b]))
        fh.write(f"| {n} | {pct}% | `{a}` | `{b}` |\n")
    fh.write(f"\n# Retrabalho: commits fix/corrige <=2 dias apos feat no mesmo arquivo\n\n")
    fh.write(f"Total: **{len(rework)}** commits (de {sum(1 for c in commits if FIX.match(c['subj']))} commits fix/corrige nos 6 meses).\n\n")
    for h,(s,p,f) in list(rework.items())[:20]:
        fh.write(f"- `{h[:8]}` {s[:90]}\n  - corrige: {p[:90]}  (`{f}`)\n")
    fh.write("\n# TODO/FIXME/HACK/XXX por modulo\n\n| ocorrencias | modulo |\n|---:|---|\n")
    for k,v in todo.most_common(): fh.write(f"| {v} | `{k}` |\n")
    fh.write(f"\nTotal: {sum(todo.values())}\n\nExemplos de arquivos: " + ", ".join(f"`{s}`" for s in samples) + "\n")
print("pairs", len(pair), "rework", len(rework), "todo", sum(todo.values()))
