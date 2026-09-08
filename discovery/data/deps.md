# Grafo de dependencias backend/*

## Nos

| modulo | depende de (out) | e usado por (in) | raio de impacto |
|---|---:|---:|---:|
| `config` | 0 | 10 | 18 |
| `ai` | 1 | 2 | 17 |
| `api` | 16 | 6 | 17 |
| `audit` | 1 | 2 | 17 |
| `auth` | 2 | 1 | 17 |
| `cadoc_adapters` | 1 | 4 | 17 |
| `cli` | 5 | 1 | 17 |
| `contabil_transforms` | 1 | 2 | 17 |
| `demo` | 7 | 1 | 17 |
| `engine` | 3 | 1 | 17 |
| `flows` | 4 | 8 | 17 |
| `governance` | 0 | 1 | 17 |
| `pecld` | 1 | 3 | 17 |
| `plugins` | 4 | 8 | 17 |
| `quality` | 7 | 6 | 17 |
| `services` | 4 | 6 | 17 |
| `storage` | 5 | 11 | 17 |
| `worker` | 13 | 4 | 17 |
| `workflow` | 3 | 2 | 17 |
| `integrations` | 0 | 0 | 0 |
| `processing` | 1 | 0 | 0 |

## Arestas (peso = nº de arquivos-import)

- `worker` -> `storage` (144)
- `api` -> `storage` (130)
- `api` -> `flows` (66)
- `worker` -> `workflow` (54)
- `api` -> `auth` (43)
- `worker` -> `api` (41)
- `api` -> `audit` (38)
- `worker` -> `flows` (33)
- `api` -> `services` (28)
- `demo` -> `storage` (27)
- `worker` -> `plugins` (27)
- `api` -> `worker` (26)
- `worker` -> `services` (21)
- `api` -> `quality` (20)
- `api` -> `plugins` (19)
- `worker` -> `cadoc_adapters` (18)
- `worker` -> `config` (17)
- `worker` -> `quality` (16)
- `api` -> `config` (14)
- `cli` -> `storage` (14)
- `engine` -> `worker` (12)
- `cadoc_adapters` -> `plugins` (10)
- `quality` -> `api` (10)
- `engine` -> `flows` (7)
- `services` -> `storage` (7)
- `engine` -> `plugins` (6)
- `quality` -> `flows` (6)
- `storage` -> `config` (6)
- `workflow` -> `storage` (6)
- `api` -> `governance` (5)
- `demo` -> `flows` (5)
- `worker` -> `engine` (5)
- `cli` -> `demo` (4)
- `flows` -> `storage` (4)
- `quality` -> `plugins` (4)
- `services` -> `config` (4)
- `storage` -> `quality` (4)
- `worker` -> `audit` (4)
- `workflow` -> `worker` (4)
- `api` -> `workflow` (3)
- `demo` -> `quality` (3)
- `pecld` -> `storage` (3)
- `services` -> `flows` (3)
- `api` -> `ai` (2)
- `api` -> `cadoc_adapters` (2)
- `api` -> `cli` (2)
- `api` -> `contabil_transforms` (2)
- `auth` -> `api` (2)
- `demo` -> `cadoc_adapters` (2)
- `flows` -> `plugins` (2)
- `flows` -> `quality` (2)
- `plugins` -> `storage` (2)
- `quality` -> `contabil_transforms` (2)
- `quality` -> `storage` (2)
- `services` -> `api` (2)
- `storage` -> `flows` (2)
- `workflow` -> `config` (2)
- `ai` -> `config` (1)
- `api` -> `pecld` (1)
- `audit` -> `storage` (1)
- `auth` -> `config` (1)
- `cli` -> `api` (1)
- `cli` -> `config` (1)
- `cli` -> `services` (1)
- `contabil_transforms` -> `quality` (1)
- `demo` -> `config` (1)
- `demo` -> `plugins` (1)
- `demo` -> `services` (1)
- `flows` -> `services` (1)
- `plugins` -> `cadoc_adapters` (1)
- `plugins` -> `config` (1)
- `plugins` -> `flows` (1)
- `processing` -> `plugins` (1)
- `quality` -> `services` (1)
- `quality` -> `worker` (1)
- `storage` -> `api` (1)
- `storage` -> `pecld` (1)
- `worker` -> `ai` (1)
- `worker` -> `pecld` (1)

## Ciclos (113)

- api -> audit -> storage -> api
- api -> audit -> storage -> flows -> quality -> api
- api -> audit -> storage -> flows -> quality -> services -> api
- api -> audit -> storage -> flows -> quality -> worker -> api
- api -> audit -> storage -> flows -> services -> api
- api -> auth -> api
- api -> cadoc_adapters -> plugins -> flows -> quality -> api
- api -> cadoc_adapters -> plugins -> flows -> quality -> services -> api
- api -> cadoc_adapters -> plugins -> flows -> quality -> worker -> api
- api -> cli -> api
- api -> cli -> demo -> quality -> api
- api -> cli -> demo -> quality -> services -> api
- api -> cli -> demo -> quality -> worker -> api
- api -> cli -> demo -> services -> api
- api -> cli -> services -> api
- api -> worker -> api
- audit -> storage -> api -> audit
- audit -> storage -> api -> cadoc_adapters -> plugins -> flows -> quality -> worker -> audit
- audit -> storage -> flows -> quality -> worker -> audit
- auth -> api -> auth
- cadoc_adapters -> plugins -> cadoc_adapters
- cadoc_adapters -> plugins -> flows -> quality -> api -> cadoc_adapters
- cadoc_adapters -> plugins -> flows -> quality -> api -> cli -> demo -> cadoc_adapters
- cadoc_adapters -> plugins -> flows -> quality -> api -> worker -> cadoc_adapters
- cadoc_adapters -> plugins -> flows -> quality -> worker -> cadoc_adapters
- cli -> api -> cli
- contabil_transforms -> quality -> api -> contabil_transforms
- contabil_transforms -> quality -> contabil_transforms
- demo -> cadoc_adapters -> plugins -> flows -> quality -> api -> cli -> demo
- engine -> flows -> plugins -> storage -> api -> cli -> demo -> quality -> worker -> engine
- flows -> plugins -> flows
- flows -> plugins -> storage -> api -> cli -> demo -> flows
- flows -> plugins -> storage -> api -> cli -> demo -> quality -> flows
- flows -> plugins -> storage -> api -> cli -> demo -> quality -> services -> flows
- flows -> plugins -> storage -> api -> cli -> demo -> quality -> worker -> engine -> flows
- flows -> plugins -> storage -> api -> cli -> demo -> quality -> worker -> flows
- flows -> plugins -> storage -> api -> flows
- flows -> plugins -> storage -> flows
- flows -> quality -> api -> audit -> storage -> flows
- flows -> quality -> api -> cli -> demo -> flows
- flows -> quality -> api -> cli -> demo -> services -> flows
- flows -> quality -> api -> cli -> services -> flows
- flows -> quality -> api -> flows
- flows -> quality -> api -> worker -> engine -> flows
- flows -> quality -> api -> worker -> flows
- flows -> quality -> flows
- flows -> quality -> services -> flows
- flows -> quality -> worker -> engine -> flows
- flows -> quality -> worker -> flows
- flows -> services -> flows
- pecld -> storage -> api -> cadoc_adapters -> plugins -> flows -> quality -> worker -> pecld
- pecld -> storage -> api -> pecld
- pecld -> storage -> pecld
- plugins -> cadoc_adapters -> plugins
- plugins -> flows -> plugins
- plugins -> flows -> quality -> api -> cli -> demo -> plugins
- plugins -> flows -> quality -> api -> plugins
- plugins -> flows -> quality -> api -> worker -> engine -> plugins
- plugins -> flows -> quality -> api -> worker -> plugins
- plugins -> flows -> quality -> plugins
- plugins -> flows -> quality -> worker -> engine -> plugins
- plugins -> flows -> quality -> worker -> plugins
- plugins -> storage -> api -> cli -> demo -> plugins
- plugins -> storage -> api -> cli -> demo -> quality -> plugins
- plugins -> storage -> api -> cli -> demo -> quality -> worker -> engine -> plugins
- plugins -> storage -> api -> cli -> demo -> quality -> worker -> plugins
- plugins -> storage -> api -> plugins
- quality -> api -> audit -> storage -> flows -> quality
- quality -> api -> audit -> storage -> quality
- quality -> api -> cli -> demo -> quality
- quality -> api -> contabil_transforms -> quality
- quality -> api -> quality
- quality -> api -> worker -> quality
- quality -> contabil_transforms -> quality
- quality -> worker -> quality
- services -> api -> audit -> storage -> flows -> quality -> services
- services -> api -> audit -> storage -> flows -> quality -> worker -> services
- services -> api -> audit -> storage -> flows -> services
- services -> api -> cli -> demo -> services
- services -> api -> cli -> services
- services -> api -> services
- storage -> api -> audit -> storage
- storage -> api -> cadoc_adapters -> plugins -> flows -> quality -> services -> storage
- storage -> api -> cadoc_adapters -> plugins -> flows -> quality -> storage
- storage -> api -> cadoc_adapters -> plugins -> flows -> quality -> worker -> pecld -> storage
- storage -> api -> cadoc_adapters -> plugins -> flows -> quality -> worker -> storage
- storage -> api -> cadoc_adapters -> plugins -> flows -> quality -> worker -> workflow -> storage
- storage -> api -> cadoc_adapters -> plugins -> flows -> storage
- storage -> api -> cadoc_adapters -> plugins -> storage
- storage -> api -> cli -> demo -> quality -> services -> storage
- storage -> api -> cli -> demo -> quality -> storage
- storage -> api -> cli -> demo -> quality -> worker -> pecld -> storage
- storage -> api -> cli -> demo -> quality -> worker -> storage
- storage -> api -> cli -> demo -> quality -> worker -> workflow -> storage
- storage -> api -> cli -> demo -> storage
- storage -> api -> cli -> storage
- storage -> api -> storage
- storage -> flows -> plugins -> storage
- storage -> flows -> quality -> services -> storage
- storage -> flows -> quality -> storage
- storage -> flows -> quality -> worker -> pecld -> storage
- storage -> flows -> quality -> worker -> storage
- storage -> flows -> quality -> worker -> workflow -> storage
- storage -> flows -> services -> storage
- storage -> flows -> storage
- storage -> pecld -> storage
- worker -> api -> audit -> storage -> flows -> quality -> worker
- worker -> api -> worker
- worker -> api -> workflow -> worker
- worker -> engine -> worker
- worker -> workflow -> worker
- workflow -> storage -> api -> cadoc_adapters -> plugins -> flows -> quality -> worker -> workflow
- workflow -> storage -> api -> workflow

## Bibliotecas externas -> modulos que usam

- **alembic**: `storage`
- **anthropic**: `ai`
- **bcrypt**: `services`, `storage`
- **boto3**: `storage`, `worker`
- **celery**: `worker`
- **duckdb**: `processing`
- **fastapi**: `api`, `auth`
- **fitz**: `storage`
- **httpx**: `services`
- **jose**: `auth`
- **lxml**: `plugins`
- **psycopg**: `storage`
- **pydantic**: `api`, `config`
- **pypdf**: `quality`
- **redis**: `api`
- **reportlab**: `api`, `quality`
- **requests**: `ai`, `api`, `plugins`, `storage`, `worker`
- **slowapi**: `api`
