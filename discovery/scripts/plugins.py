"""Anatomia dos plugins: classifica cada funcao/classe por papel no pipeline + similaridade cruzada."""

import ast
import os
import re
import json
import difflib
import itertools
import collections

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
os.chdir(ROOT)
BASE = "backend/plugins"

# Classificacao por papel. Ordem importa: a primeira regra que casar vence.
PAPEIS = [
    (
        "validacao externa",
        r"validator_client|xsd|Xsd|XSD|schema\.py$|own_validator|validator",
    ),
    ("parser de entrada", r"parser|parse|layout|positional|reader|_read|load_"),
    ("gerador de saida", r"generator|builder|render|_xml|to_xml|write_|emit|serial"),
    (
        "regra de negocio",
        r"rules|selector|aggregator|consolidat|completude|equivalencia|"
        r"substituicao|synthetic|anexo|calc|apura|classif",
    ),
]
DEFAULT = "outro"


def papel(modulo, nome):
    alvo = f"{modulo}::{nome}"
    for label, pat in PAPEIS:
        if re.search(pat, alvo):
            return label
    return DEFAULT


NUM = re.compile(r"\b(3040|3042|3044|3050|3026|cosif|COSIF)\b")


def norm_body(node, src):
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
    return re.sub(r"\s+", " ", txt).strip()


items = []
for plug in sorted(os.listdir(BASE)):
    d = os.path.join(BASE, plug)
    if not os.path.isdir(d) or plug == "__pycache__":
        continue
    for dp, dn, fn in os.walk(d):
        dn[:] = [x for x in dn if x != "__pycache__"]
        for f in sorted(fn):
            if not f.endswith(".py") or f == "__init__.py":
                continue
            p = os.path.join(dp, f).replace(os.sep, "/")
            src = open(p, encoding="utf-8", errors="ignore").read()
            try:
                tree = ast.parse(src)
            except SyntaxError:
                continue
            for node in tree.body:
                if not isinstance(
                    node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)
                ):
                    continue
                seg = ast.get_source_segment(src, node) or ""
                nb = "" if isinstance(node, ast.ClassDef) else norm_body(node, src)
                items.append(
                    {
                        "plugin": plug,
                        "file": p,
                        "name": node.name,
                        "tipo": "classe"
                        if isinstance(node, ast.ClassDef)
                        else "funcao",
                        "papel": papel(p, node.name),
                        "lines": len(seg.splitlines()),
                        "norm": nb,
                        "norm_len": len(nb),
                    }
                )

# --- pares entre plugins DIFERENTES (candidatos a generico) ---
pairs = []
for a, b in itertools.combinations([i for i in items if i["tipo"] == "funcao"], 2):
    if a["plugin"] == b["plugin"]:
        continue
    if a["norm_len"] < 100 or b["norm_len"] < 100:
        continue
    if abs(a["norm_len"] - b["norm_len"]) / max(a["norm_len"], b["norm_len"]) > 0.6:
        continue
    r = difflib.SequenceMatcher(None, a["norm"], b["norm"]).ratio()
    if r > 0.65:
        pairs.append((round(r, 3), a, b))
pairs.sort(key=lambda x: -x[0])
generico = {(x[1]["file"], x[1]["name"]) for x in pairs} | {
    (x[2]["file"], x[2]["name"]) for x in pairs
}

# --- nome identico em 2+ plugins (mesmo que o corpo tenha divergido) ---
por_nome = collections.defaultdict(set)
for i in items:
    por_nome[i["name"]].add(i["plugin"])
repetidos = {k: sorted(v) for k, v in por_nome.items() if len(v) > 1}

with open("discovery/data/plugins.md", "w", encoding="utf-8") as fh:
    fh.write("# Anatomia dos plugins\n\nGerado por `discovery/scripts/plugins.py`.\n\n")
    fh.write(
        "Papel atribuido por heuristica de nome de modulo/simbolo `[inferido]` "
        "(ordem: validacao externa > parser > gerador > regra de negocio > outro). "
        "`generico?` = existe funcao com corpo >65% similar em OUTRO plugin.\n\n"
    )

    fh.write(
        "## Resumo por plugin\n\n| plugin | arquivos | simbolos de topo | linhas | papeis |\n|---|---:|---:|---:|---|\n"
    )
    for plug in sorted({i["plugin"] for i in items}):
        sub = [i for i in items if i["plugin"] == plug]
        dist = collections.Counter(i["papel"] for i in sub)
        fh.write(
            f"| `{plug}` | {len({i['file'] for i in sub})} | {len(sub)} | "
            f"{sum(i['lines'] for i in sub)} | "
            + ", ".join(f"{k}: {v}" for k, v in dist.most_common())
            + " |\n"
        )

    fh.write("\n## Simbolos por plugin\n")
    for plug in sorted({i["plugin"] for i in items}):
        fh.write(
            f"\n### `{plug}`\n\n| arquivo | simbolo | tipo | papel | l. | generico? |\n"
            "|---|---|---|---|---:|:-:|\n"
        )
        for i in [x for x in items if x["plugin"] == plug]:
            g = "sim" if (i["file"], i["name"]) in generico else "-"
            fh.write(
                f"| `{i['file'].split('/', 2)[-1]}` | `{i['name']}` | {i['tipo']} | "
                f"{i['papel']} | {i['lines']} | {g} |\n"
            )

    fh.write(
        f"\n## Funcoes com corpo similar entre plugins diferentes ({len(pairs)})\n\n"
    )
    fh.write("| similaridade | A | B | papel |\n|---:|---|---|---|\n")
    for r, a, b in pairs:
        fh.write(
            f"| {r:.0%} | `{a['plugin']}::{a['name']}` | `{b['plugin']}::{b['name']}` | {a['papel']} |\n"
        )

    fh.write(f"\n## Mesmo nome de simbolo em 2+ plugins ({len(repetidos)})\n\n")
    fh.write("| simbolo | plugins |\n|---|---|\n")
    for k, v in sorted(repetidos.items()):
        fh.write(f"| `{k}` | {', '.join(v)} |\n")

json.dump(
    {
        "items": [{k: v for k, v in i.items() if k != "norm"} for i in items],
        "pairs": [
            {
                "ratio": r,
                "a": f"{a['plugin']}::{a['name']}",
                "b": f"{b['plugin']}::{b['name']}",
            }
            for r, a, b in pairs
        ],
        "repetidos": repetidos,
    },
    open("discovery/data/plugins.json", "w"),
    indent=1,
)
print("simbolos:", len(items), "pares:", len(pairs), "nomes repetidos:", len(repetidos))
