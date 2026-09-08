# Volumetria - banco LOCAL de dev
Gerado por `discovery/scripts/volume.py` (somente SELECT / catalogo).
DSN: `host=localhost port=5433 user=postgres dbname=regulatory_reports...` (banco local de desenvolvimento).

Schemas de tenant encontrados: **2** -> `tenant_11111111_2222_4333_8444_555555555555`, `tenant_main`

## `tenant_11111111_2222_4333_8444_555555555555`

Tabelas: 73. Tamanho total do schema: 3536 KB.

### 5 maiores tabelas + alvos (`raw_data`, `account_entries`)

| tabela | count(*) | tamanho total | linhas (estimativa do catalogo) |
|---|---:|---:|---:|
| `cadoc3040_mov_operacoes` | 120 | 216 KB | 120 |
| `audit_events` | 82 | 184 KB | 53 |
| `quality_scores` | 204 | 144 KB | 156 |
| `reports` | 17 | 128 KB | 17 |
| `cadoc3044_mov_linhas` | 10 | 128 KB | -1 |
| `account_entries` | 0 | 32 KB | -1 |
| `raw_data` | 0 | 24 KB | -1 |

## `tenant_main`

Tabelas: 73. Tamanho total do schema: 2128 KB.

### 5 maiores tabelas + alvos (`raw_data`, `account_entries`)

| tabela | count(*) | tamanho total | linhas (estimativa do catalogo) |
|---|---:|---:|---:|
| `cadoc3044_mov_linhas` | 0 | 64 KB | -1 |
| `reporting_obligations` | 0 | 48 KB | -1 |
| `cadoc3040_mov_operacoes` | 0 | 48 KB | -1 |
| `reports` | 0 | 48 KB | -1 |
| `reporting_units` | 1 | 48 KB | -1 |
| `account_entries` | 0 | 32 KB | -1 |
| `raw_data` | 0 | 24 KB | -1 |
