"""Volumetria por schema de tenant no banco LOCAL de dev (read-only)."""

import os
import sys

import psycopg

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
os.chdir(ROOT)

DSN = os.getenv(
    "DISCOVERY_DSN",
    "host=localhost port=5433 user=postgres dbname=regulatory_reports",  # senha via PGPASSWORD
)
ALVOS = ("raw_data", "account_entries")

out = [
    "# Volumetria - banco LOCAL de dev\n",
    "Gerado por `discovery/scripts/volume.py` (somente SELECT / catalogo).\n",
    f"DSN: `{DSN.split('password=')[0]}...` (banco local de desenvolvimento).\n",
]

try:
    conn = psycopg.connect(DSN, connect_timeout=5)
except Exception as e:
    out.append(
        f"\n**Sem acesso ao banco local:** `{type(e).__name__}: {str(e)[:150]}`\n"
    )
    open("discovery/data/volume.md", "w", encoding="utf-8").write("\n".join(out))
    print("sem acesso")
    sys.exit(0)

with conn:
    schemas = [
        r[0]
        for r in conn.execute(
            "select nspname from pg_namespace where nspname like 'tenant_%' order by 1"
        ).fetchall()
    ]
    out.append(
        f"\nSchemas de tenant encontrados: **{len(schemas)}** -> "
        + ", ".join(f"`{s}`" for s in schemas)
        + "\n"
    )

    for s in schemas:
        out.append(f"\n## `{s}`\n")
        rows = conn.execute(
            """
            select c.relname,
                   pg_total_relation_size(c.oid) as bytes,
                   coalesce(c.reltuples, 0)::bigint as est_rows
            from pg_class c join pg_namespace n on n.oid = c.relnamespace
            where n.nspname = %s and c.relkind = 'r'
            order by pg_total_relation_size(c.oid) desc
        """,
            (s,),
        ).fetchall()
        if not rows:
            out.append("\n(sem tabelas)\n")
            continue
        out.append(
            f"\nTabelas: {len(rows)}. "
            f"Tamanho total do schema: {sum(r[1] for r in rows) / 1024:.0f} KB.\n"
        )
        out.append("\n### 5 maiores tabelas + alvos (`raw_data`, `account_entries`)\n")
        out.append(
            "\n| tabela | count(*) | tamanho total | linhas (estimativa do catalogo) |\n|---|---:|---:|---:|\n"
        )
        alvo_rows = [r for r in rows if r[0] in ALVOS]
        top = rows[:5]
        vistos = set()
        for name, size, est in top + [r for r in alvo_rows if r not in top]:
            if name in vistos:
                continue
            vistos.add(name)
            try:
                n = conn.execute(f'select count(*) from "{s}"."{name}"').fetchone()[0]
            except Exception as e:
                n = f"erro: {type(e).__name__}"
            out.append(f"| `{name}` | {n} | {size / 1024:.0f} KB | {est} |\n")
        faltando = [t for t in ALVOS if t not in {r[0] for r in rows}]
        if faltando:
            out.append(
                f"\nTabelas alvo AUSENTES neste schema: {', '.join('`' + t + '`' for t in faltando)}\n"
            )

open("discovery/data/volume.md", "w", encoding="utf-8").write("".join(out))
print("ok")
