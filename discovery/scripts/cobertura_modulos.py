"""Mapa teste -> modulo de producao, por espelhamento de caminho tests/<x> ~ backend/<x>."""
import os, json
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
os.chdir(ROOT)
def files(base, pref=""):
    out = set()
    for dp, dn, fn in os.walk(base):
        dn[:] = [d for d in dn if d != "__pycache__"]
        for f in fn:
            if f.endswith(".py") and f != "__init__.py":
                out.add(os.path.relpath(os.path.join(dp, f), base).replace(os.sep, "/"))
    return out
prod = files("backend")
tests = files("tests")
tnames = {os.path.basename(t)[5:] for t in tests}  # sem 'test_'
tstems = {os.path.basename(t)[5:-3] for t in tests}
sem = []
for p in sorted(prod):
    stem = os.path.basename(p)[:-3]
    if stem in tstems: continue
    # heuristica secundaria: algum teste menciona o caminho do modulo
    sem.append(p)
# refina: procura mencao ao modulo importado nos testes
import re
mentions = set()
for dp, dn, fn in os.walk("tests"):
    dn[:] = [d for d in dn if d != "__pycache__"]
    for f in fn:
        if not f.endswith(".py"): continue
        src = open(os.path.join(dp, f), encoding="utf-8", errors="ignore").read()
        for m in re.findall(r"backend\.([\w.]+)", src):
            mentions.add(m.replace(".", "/") + ".py")
sem2 = [p for p in sem if p not in mentions]
by = {}
for p in sem2: by.setdefault(p.split("/")[0], []).append(p)
with open("discovery/data/cobertura.md", "w", encoding="utf-8") as fh:
    fh.write(f"# Modulos de producao sem teste correspondente\n\nCriterio: nao existe `tests/**/test_<stem>.py` E o caminho `backend.<modulo>` nao e mencionado em nenhum arquivo de teste.\n\n")
    fh.write(f"- arquivos .py em `backend/` (sem `__init__`): **{len(prod)}**\n")
    fh.write(f"- sem `test_<stem>.py`: **{len(sem)}**\n")
    fh.write(f"- sem teste E sem mencao: **{len(sem2)}**\n\n")
    for k in sorted(by, key=lambda x: -len(by[x])):
        fh.write(f"\n## `backend/{k}` ({len(by[k])})\n\n")
        for p in sorted(by[k]): fh.write(f"- `backend/{p}`\n")
print(len(prod), len(sem), len(sem2))
