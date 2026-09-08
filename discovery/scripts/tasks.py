"""Inventario de tasks Celery: fila, opcoes, quem enfileira; beat_schedule; task_routes."""

import ast
import os
import re
import json
import collections
import subprocess
import datetime
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
os.chdir(ROOT)
sys.path.insert(0, ROOT)
APP = "backend/worker/app.py"
src = open(APP, encoding="utf-8", errors="ignore").read()
tree = ast.parse(src)


def const(n):
    try:
        return ast.literal_eval(n)
    except Exception:
        return ast.get_source_segment(src, n)


routes_manual, beat = {}, {}
for node in ast.walk(tree):
    if isinstance(node, ast.Call):
        for kw in node.keywords:
            if kw.arg == "task_routes":
                routes_manual = {
                    const(k): const(v) for k, v in zip(kw.value.keys, kw.value.values)
                }
            if kw.arg == "beat_schedule":
                for k, v in zip(kw.value.keys, kw.value.values):
                    beat[const(k)] = const(v)

# beat: ultimo commit que tocou a linha da entrada
lines = src.splitlines()


def line_of(name):
    pat = re.compile(r'["\']' + re.escape(name) + r'["\']\s*:')
    for i, ln_txt in enumerate(lines, 1):
        if pat.search(ln_txt):
            return i
    return None


blame = {}
try:
    out = subprocess.run(
        ["git", "blame", "--line-porcelain", APP],
        capture_output=True,
        text=True,
        errors="ignore",
    ).stdout
    cur = {}
    for row in out.splitlines():
        if re.match(r"^[0-9a-f]{40} ", row):
            cur = {"sha": row[:8], "ln": int(row.split()[2])}
        elif row.startswith("author-time"):
            cur["t"] = int(row.split()[1])
        elif row.startswith("summary"):
            cur["s"] = row[8:]
        elif row.startswith("\t") and cur:
            blame[cur["ln"]] = cur.copy()
except Exception:
    pass


def blame_of(name):
    ln = line_of(name)
    b = blame.get(ln) if ln else None
    if not b:
        return "-", "-"
    d = datetime.datetime.utcfromtimestamp(b["t"]).strftime("%Y-%m-%d")
    return f"{b['sha']} ({d})", b.get("s", "")[:60]


# --- tasks decoradas ---
tasks = []
for dp, dn, fn in os.walk("backend/worker"):
    dn[:] = [d for d in dn if d != "__pycache__"]
    for f in sorted(fn):
        if not f.endswith(".py"):
            continue
        p = os.path.join(dp, f).replace(os.sep, "/")
        s = open(p, encoding="utf-8", errors="ignore").read()
        t = ast.parse(s)
        for node in ast.walk(t):
            if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                continue
            for dec in node.decorator_list:
                dsrc = ast.get_source_segment(s, dec) or ""
                if not re.search(r"(shared_task|celery_app\.task|app\.task)", dsrc):
                    continue
                opts = {}
                if isinstance(dec, ast.Call):
                    for kw in dec.keywords:
                        try:
                            opts[kw.arg] = ast.literal_eval(kw.value)
                        except Exception:
                            opts[kw.arg] = ast.get_source_segment(s, kw.value)
                name = opts.get("name") or f"{p[:-3].replace('/', '.')}.{node.name}"
                body = ast.get_source_segment(s, node) or ""
                tasks.append(
                    {
                        "name": name,
                        "func": node.name,
                        "module": p,
                        "lines": len(body.splitlines()),
                        "opts": {k: str(v) for k, v in opts.items()},
                    }
                )
                break

# --- rotas derivadas das flow specs ---
derived = {}
derived_err = None
try:
    from backend.engine.discovery import derive_task_routes
    from backend.worker.app import _engine_registry

    derived = derive_task_routes(_engine_registry)
except Exception as e:
    derived_err = f"{type(e).__name__}: {e}"[:160]

# --- quem enfileira ---
enq = collections.defaultdict(set)
CALL = re.compile(r"(\w+)\.(?:delay|apply_async)\(|send_task\(\s*[\"']([\w.]+)")
for base in ("backend", "scripts"):
    for dp, dn, fn in os.walk(base):
        dn[:] = [d for d in dn if d != "__pycache__"]
        for f in fn:
            if not f.endswith(".py"):
                continue
            p = os.path.join(dp, f).replace(os.sep, "/")
            s = open(p, encoding="utf-8", errors="ignore").read()
            for a, b in CALL.findall(s):
                enq[a or b].add(p)

beat_tasks = {(v or {}).get("task") for v in beat.values() if isinstance(v, dict)}
beat_short = {str(x).split(".")[-1] for x in beat_tasks if x}


def caller_kind(t):
    short, full = t["func"], t["name"]
    srcs = (
        enq.get(short, set())
        | enq.get(full, set())
        | enq.get(full.split(".")[-1], set())
    )
    srcs = {s for s in srcs if s != t["module"]}
    kinds = set()
    if full in beat_tasks or short in beat_short:
        kinds.add("beat")
    for s in srcs:
        if s.startswith("backend/api/"):
            kinds.add("rota")
        elif s.startswith("backend/worker/"):
            kinds.add("task")
        elif s.startswith("backend/cli/"):
            kinds.add("cli")
        else:
            kinds.add("outro")
    return kinds, sorted(srcs)


def queue_of(name):
    if name in derived:
        d = derived[name]
        return (d.get("queue") if isinstance(d, dict) else d), "spec"
    if name in routes_manual:
        d = routes_manual[name]
        return (d.get("queue") if isinstance(d, dict) else d), "manual"
    for src_name, table in (("spec", derived), ("manual", routes_manual)):
        for pat, cfg in table.items():
            if str(pat).endswith("*") and name.startswith(str(pat)[:-1]):
                q = cfg.get("queue") if isinstance(cfg, dict) else cfg
                return q, f"{src_name}(glob)"
    return None, "SEM ROTA"


for t in tasks:
    k, s = caller_kind(t)
    t["callers"], t["caller_src"] = sorted(k), s
    t["queue"], t["route_origin"] = queue_of(t["name"])

orphan = [t for t in tasks if not t["callers"]]
json.dump(
    {
        "tasks": tasks,
        "beat": beat,
        "routes_manual": routes_manual,
        "derived": derived,
        "derived_err": derived_err,
    },
    open("discovery/data/tasks.json", "w"),
    indent=1,
    default=str,
)

with open("discovery/data/tasks.md", "w", encoding="utf-8") as fh:
    fh.write(
        "# Worker - beat, rotas e tasks\n\nGerado por `discovery/scripts/tasks.py`.\n\n"
    )
    fh.write(f"## beat_schedule ({len(beat)} entradas)\n\n")
    fh.write(
        "| entrada | task | agenda | fila | ultimo commit que tocou a linha |\n|---|---|---|---|---|\n"
    )
    for k, v in beat.items():
        v = v if isinstance(v, dict) else {}
        q = (v.get("options") or {}).get("queue", "-")
        sha, sub = blame_of(k)
        fh.write(
            f"| `{k}` | `{v.get('task', '-')}` | `{v.get('schedule')}` | `{q}` | {sha} - {sub} |\n"
        )
    fh.write(
        f"\n## task_routes manuais ({len(routes_manual)})\n\n| padrao | fila |\n|---|---|\n"
    )
    for k, v in sorted(routes_manual.items(), key=str):
        q = v.get("queue") if isinstance(v, dict) else v
        fh.write(f"| `{k}` | `{q}` |\n")
    fh.write(f"\n## task_routes derivadas das flow specs ({len(derived)})\n\n")
    if derived_err:
        fh.write(f"**Nao foi possivel derivar em processo:** `{derived_err}`\n\n")
    fh.write("| task | fila |\n|---|---|\n")
    for k, v in sorted(derived.items(), key=str):
        q = v.get("queue") if isinstance(v, dict) else v
        fh.write(f"| `{k}` | `{q}` |\n")
    fh.write(f"\n## Tasks decoradas ({len(tasks)})\n\n")
    fh.write(
        "| task | modulo | l. | fila | origem da rota | enfileirada por | acks_late | time_limit | max_retries | autoretry_for |\n"
    )
    fh.write("|---|---|---:|---|---|---|:-:|:-:|:-:|:-:|\n")
    for t in sorted(tasks, key=lambda x: (x["module"], x["name"])):
        o = t["opts"]
        fh.write(
            f"| `{t['name']}` | `{t['module'].split('/')[-1]}` | {t['lines']} | `{t['queue'] or '-'}` | "
            f"{t['route_origin']} | {', '.join(t['callers']) or '**ninguem**'} | "
            f"{o.get('acks_late', '-')} | {o.get('time_limit', o.get('soft_time_limit', '-'))} | "
            f"{o.get('max_retries', '-')} | {'sim' if 'autoretry_for' in o else '-'} |\n"
        )
    fh.write(f"\n## Tasks que ninguem enfileira ({len(orphan)})\n\n")
    for t in orphan:
        fh.write(
            f"- `{t['name']}` - `{t['module']}` ({t['lines']} l., fila `{t['queue']}`)\n"
        )

print(
    "tasks:",
    len(tasks),
    "beat:",
    len(beat),
    "manuais:",
    len(routes_manual),
    "derivadas:",
    len(derived),
    "err:",
    derived_err,
    "orfas:",
    len(orphan),
)
