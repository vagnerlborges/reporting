# Discovery — `dattos-regulatory-reporting`

Levantamento factual do repositório para servir de insumo a CLAUDE.md, política de testes e
comandos customizados. **Não contém recomendações de implementação.**

- Commit base: `898bbea` (2026-09-07), branch `analise-poc-ebanx`.
- Marcações: `[explícito]` = está escrito no repo; `[inferido]` = deduzido de evidência.
- Tabelas grandes e listas de caminhos: `discovery/data/`. Scripts: `discovery/scripts/`.
- Esforço de leitura e bloqueios: `discovery/LOG.md`.

---

## 1. Identidade do repo

### Stack

| Camada | Tecnologia | Versão declarada | Evidência |
|---|---|---|---|
| Backend | Python + FastAPI + Pydantic v2 | `requires-python = ">=3.12"`, `fastapi>=0.110`, `pydantic>=2.6` | [pyproject.toml:9-13](../pyproject.toml#L9-L13) |
| Banco | PostgreSQL 16, acesso via **psycopg3 sem ORM** | `psycopg[binary]>=3.1`, `psycopg-pool>=3.2` | [pyproject.toml:19-20](../pyproject.toml#L19-L20); `postgres:16` em [bitbucket-pipelines.yml:16](../bitbucket-pipelines.yml#L16) |
| Async/jobs | Celery + RabbitMQ (broker) + Redis (backend) | `celery[redis]>=5.4` | [pyproject.toml:21](../pyproject.toml#L21) |
| Migrations | Alembic — **duas cadeias** (admin e tenant) | `alembic.ini` + `alembic_tenant.ini` | raiz do repo |
| Frontend | Next.js 16 + React 19 + Tailwind 4 | `next ^16.2.0`, `react ^19.2.0` | [frontend/package.json:16-20](../frontend/package.json#L16-L20) |
| Testes backend | pytest + pytest-asyncio + **pytest-xdist obrigatório** | `--dist loadfile` fixo em addopts | [pytest.ini:5](../pytest.ini#L5) |
| Testes frontend | vitest | `"test": "vitest run"` | [frontend/package.json:10](../frontend/package.json#L10) |
| E2E | Playwright, projeto separado com `package.json` próprio | `e2e/playwright.config.ts` | [e2e/playwright.config.ts](../e2e/playwright.config.ts) |
| Extras notáveis | `duckdb>=1.1.0` (declarado como "Fase 0 = spike"), `anthropic>=0.40`, `langsmith>=0.2` | | [pyproject.toml:35-40](../pyproject.toml#L35-L40) |

**Não é monorepo formal** `[inferido]`: um único pacote Python (`packages.find include = ["backend*"]`),
mas dois projetos JS independentes sem workspace (`frontend/`, `e2e/`), cada um com seu
`package.json` e `node_modules`.

### Gerenciadores de pacote
- Python: `setuptools` + `pip install -e ".[dev]"` `[explícito]` ([bitbucket-pipelines.yml:31](../bitbucket-pipelines.yml#L31)). Sem lockfile Python.
- JS: `npm` (`package-lock.json` presente em `frontend/` e `e2e/`).

### Pontos de entrada

| Tipo | Caminho | Nota |
|---|---|---|
| API HTTP | [backend/api/main.py](../backend/api/main.py) | `FastAPI` + 45 `include_router` |
| Worker Celery | [backend/worker/app.py](../backend/worker/app.py) | `task_routes` (l.39) + `imports` (l.230) + `beat_schedule` (l.86) |
| Scheduler | mesmo `celery_app`, serviço `beat` no compose | [infra/docker-compose.yml](../infra/docker-compose.yml) |
| CLI | `backend/cli/` (8 arquivos): `seed.py`, `seed_demo.py`, `check_drift.py` | `python -m backend.cli.seed` |
| Frontend | `frontend/app/` (Next app router) | rotas `(auth)`, `(dashboard)`, `admin`, `reports`, `setup`, `verificar` |
| Motor de documentos | [backend/engine/base.py](../backend/engine/base.py) + [backend/flows/cadoc_registry.py](../backend/flows/cadoc_registry.py) | rotas e imports Celery são **derivados** das flow specs por `backend/engine/discovery.py` |

### Como rodar / testar / buildar

**Não existe `README.md` na raiz** `[explícito]`. A documentação operacional está no
[CLAUDE.md](../CLAUDE.md); há READMEs só em `deploy/` (`README.md`, `README-dev.md`, `k8s/README.md`,
`k8s/prod-bootstrap.md`, `k8s/secrets-e-config.md`).

```bash
# ambiente local completo
docker compose -f infra/docker-compose.yml up -d --build
# app http://localhost:8081 | API http://localhost:8004/docs | front http://localhost:3006
# postgres localhost:5433 (postgres/postgres, db regulatory_reports)

python -m backend.cli.seed          # tenant + admin
pip install -e ".[dev]" && pytest   # backend
cd frontend && npm run build|lint|test
cd e2e && npx playwright test       # contra https://reporting.qas.dattos.solutions
```

**Divergências entre documentação e realidade** (todas verificadas):

| # | O que a doc diz | O que o repo mostra |
|---|---|---|
| D1 | `CLAUDE.md`: "Pré-requisito: umbrella da plataforma no ar (postgres/redis/minio/mailpit **compartilhados**)" | O cabeçalho de [infra/docker-compose.yml:1-5](../infra/docker-compose.yml#L1-L5) diz "**AUTO-CONTIDO** — não depende de nenhum outro repo. Sobe TUDO"; o arquivo declara `postgres`, `redis`, `rabbitmq`, `minio`, `mailpit`, `sftpgo` localmente. |
| D2 | `CLAUDE.md`: "a cadeia Alembic ... migrations 0004–0007 do REP-51/52/53" | `migrations_tenant/versions/` tem **3** arquivos: `0001_baseline_tenant`, `0002_cadoc3040_retification_lane`, `0003_drop_opcomp_pointer`. As `0004–0007` não existem (foram achatadas em baseline). |
| D3 | `CLAUDE.md`: "`TENANT_TABLES_DDL` foi removido no REP-56 Fase B" | O identificador ainda aparece **3×** em `backend/**/*.py`. |
| D4 | `CLAUDE.md` já anota o bug | [deploy/deploy.sh:19](../deploy/deploy.sh#L19) ainda tem `APP_SERVICES=(api worker beat web)`; o serviço chama-se `frontend` no compose. Continua quebrado. |
| D5 | `pyproject.toml` ainda se chama `dattos-informes-legais`, description "envio de CADOCs ao Banco Central" | O `CLAUDE.md` afirma que **nós não enviamos** (limite de responsabilidade) e que o escopo não é só CADOC/BACEN. |

---

## 2. Mapa de módulos

Tabela completa (93 linhas, todos os módulos de topo e um nível abaixo, com contagem de arquivos e
linhas): **[data/modulos.md](data/modulos.md)** / `data/modulos.json`.
Gerado por [`scripts/modulos.py`](scripts/modulos.py).

Resumo de topo:

| Caminho | Arquivos | Linhas | Classificação `[inferido]` |
|---|---:|---:|---|
| `backend/` | 377 | 51.349 | aplicação |
| `deploy/` | 672 | 70.737 | infraestrutura (641 arquivos são `terraform/`, majoritariamente providers/lock) |
| `docs/` | 328 | 110.342 | documentação (**216 arquivos / 97k linhas em `docs/superpowers/`**) |
| `frontend/` | 200 | 33.837 | entrada (UI) |
| `tests/` | 572 | 53.807 | testes |
| `e2e/` | 65 | 10.259 | testes |
| `migrations/` + `migrations_tenant/` | 12 | 2.948 | infraestrutura |
| `scripts/` | 3 | 72 | operacional pontual |
| `valx/`, `backend/integrations/` | 0 | 0 | **vazios** |

### `backend/` por subpacote

| Caminho | Arq. | Linhas | Responsabilidade (1 linha) | Classe `[inferido]` |
|---|---:|---:|---|---|
| `backend/api` | 49 | 12.089 | FastAPI: `main.py`, `deps.py`, 43 módulos em `routes/`, middleware | entrada |
| `backend/storage` | 66 | 9.362 | 57 `*_store.py` + `postgres.py` (pool, schema, `safe_schema_name`) | infraestrutura |
| `backend/worker` | 31 | 7.237 | Celery app + 28 módulos de task | entrada (jobs) |
| `backend/plugins` | 56 | 7.698 | parsers/validators/generators por informe (`cadoc_3040`, `cadoc_3044`, `cadoc_3050`, `cadoc_3026`, `cadoc_cosif`) | domínio |
| `backend/flows` | 35 | 3.397 | registry declarativo de documentos, períodos, prazos, resolvers, painel | domínio |
| `backend/quality` | 38 | 3.283 | 12 dimensões RC 18, scorer, dicionário, linhagem, correlações | domínio |
| `backend/demo` | 16 | 1.541 | seeder de ambiente de demonstração (blocos por área) | compartilhado/tooling |
| `backend/workflow` | 6 | 1.542 | notificações / e-mail | infraestrutura |
| `backend/services` | 15 | 1.287 | serviços de aplicação — 11 dos 15 são SFTP/SFTPGo | domínio/infra |
| `backend/cadoc_adapters` | 18 | 884 | adapters posicionais/delimitados por layout de cliente | domínio |
| `backend/engine` | 8 | 848 | `CadocEngine` base, registry, `discovery.py` | domínio |
| `backend/cli` | 8 | 493 | seeds e checagem de drift | entrada (CLI) |
| `backend/pecld` | 7 | 337 | cálculo de PECLD | domínio |
| `backend/processing` | 4 | 357 | consolidação analítica (DuckDB) | domínio |
| `backend/auth` | 4 | 252 | JWT, middleware, roles | compartilhado |
| `backend/ai` | 3 | 194 | cliente Anthropic + Firecrawl (radar regulatório) | infraestrutura |
| `backend/config` | 2 | 185 | `Settings` Pydantic, prefixo `REGULATORY_` | compartilhado |
| `backend/contabil_transforms` | 4 | 107 | transformações contábeis | domínio |
| `backend/audit` | 2 | 44 | gravador de eventos de auditoria | compartilhado |
| `backend/governance` | 2 | 8 | ~vazio (8 linhas) | domínio |
| `backend/integrations` | 1 | 0 | **pacote vazio** | — |

---

## 3. Grafo de dependências

Gerado por [`scripts/deps.py`](scripts/deps.py) →
**[data/deps.json](data/deps.json)** (21 nós, 79 arestas) e **[data/deps.md](data/deps.md)**.
Escopo: imports `backend.<x>` entre subpacotes de `backend/`, peso = nº de arquivos que importam.

### Hubs (mais dependentes)

| Módulo | é importado por | importa | Leitura |
|---|---:|---:|---|
| `storage` | 11 | 5 | hub de dados; toda escrita passa aqui |
| `config` | 10 | **0** | única **folha limpa** do grafo |
| `flows` | 8 | 4 | hub de domínio (registry de documentos) |
| `plugins` | 8 | 4 | hub de domínio (motores por informe) |
| `api` | 6 | **16** | maior fan-out do repo |
| `quality`, `services` | 6 | 7 / 4 | |

Arestas mais pesadas: `worker→storage` (144), `api→storage` (130), `api→flows` (66),
`worker→workflow` (54), `api→auth` (43), **`worker→api` (41)**, `api→audit` (38).

### Folhas
- `config` — 0 imports internos. É a única dependência verdadeiramente terminal.
- `governance` (8 linhas) e `integrations` (vazio) são folhas por serem inertes.
- `processing` (DuckDB) e `integrations` são as únicas com **in-degree 0** — ninguém os usa.
  `processing` só é referenciado por `tests/processing`.

### Ciclos — o achado estrutural principal

**113 ciclos distintos** entre subpacotes de `backend/`. Consequência direta:
**o raio de impacto transitivo é 17 para 19 dos 21 módulos** — mudar praticamente qualquer módulo
alcança praticamente todos os outros. Não existe camada acíclica.

Ciclos curtos, que são os que definem o problema:
- `api ↔ auth` — `auth/middleware.py` importa de `backend.api` (2 arquivos).
- `api ↔ worker` — a rota enfileira a task (26) **e** a task importa a rota (41).
- `api ↔ cli`, `api ↔ storage`, `api ↔ quality`, `api ↔ services`.
- `storage ↔ flows`, `storage ↔ pecld`, `plugins ↔ flows`, `plugins ↔ cadoc_adapters`,
  `quality ↔ contabil_transforms`, `quality ↔ worker`, `worker ↔ engine`, `worker ↔ workflow`.

`[inferido]` Boa parte deve ser import diferido dentro de função (o processo importa sem erro),
mas o script conta o texto do import — o acoplamento existe de qualquer forma.

### Dependências externas e onde são usadas

| Lib | Módulos que a usam |
|---|---|
| `psycopg` | **só `storage`** — o isolamento de acesso a dados é real |
| `celery` | **só `worker`** |
| `fastapi` | `api`, `auth` |
| `pydantic` | `api`, `config` |
| `jose` (JWT) | **só `auth`** |
| `bcrypt` | `services`, `storage` |
| `boto3` (S3) | `storage`, `worker` |
| `requests` | `ai`, `api`, `plugins`, `storage`, `worker` — **5 módulos, o mais espalhado** |
| `httpx` | `services` |
| `lxml` | `plugins` |
| `reportlab` / `pypdf` / `fitz` | `api`+`quality` / `quality` / `storage` |
| `duckdb` | `processing` (módulo sem consumidor) |
| `alembic` | `storage` |
| `anthropic` | `ai` |
| `slowapi` (rate limit) | `api` |
| `redis` | `api` |

Divergência de convenção `[inferido]`: cliente HTTP não é único — `requests` em 5 módulos,
`httpx` em 1, e `httpx` está declarado tanto em `dependencies` quanto em `dev`.

---

## 4. Contratos e dados

### Onde vivem schemas / DTOs / tipos

| Artefato | Caminho | Contagem |
|---|---|---|
| DTOs de request/response | `class X(BaseModel)` — **89 declarações, 100% dentro de `backend/api/`** | 89 |
| Spec declarativa de documento | [backend/flows/cadoc_registry.py](../backend/flows/cadoc_registry.py) — `@dataclass(frozen=True) CadocFlowSpec` (13 campos) | 1 dataclass, N specs |
| Contrato de plugin | `backend/plugins/base.py` — `CadocPlugin` | |
| Contrato de motor | [backend/engine/base.py](../backend/engine/base.py) — `CadocEngine` + `EngineSteps` (`Protocol`, duck-typed) | |
| Layout de arquivo de cliente | `backend/cadoc_adapters/layout_spec.py` (`field_catalog`, `validate_layout_spec`) | 18 arquivos no pacote |
| Config | [backend/config/settings.py](../backend/config/settings.py) — `Settings(BaseSettings)`, prefixo `REGULATORY_` | 1 |
| Tipos do frontend | `frontend/lib/types/*.ts` | **16 arquivos** |
| XSDs oficiais | `backend/plugins/cadoc_3040/schemas/*.xsd` (declarados em `package-data`) | |

`[inferido]` Não há um pacote de "modelos de domínio" compartilhado: o modelo canônico é a
**tabela** (SQL cru) e os `BaseModel` existem só na borda HTTP. Os tipos do frontend são escritos
à mão, sem geração a partir do OpenAPI — exceto `lib/analytics/events.types.ts`, que **é** gerado
(`npm run analytics:codegen`) e tem guarda de staleness no CI.

### Modelos de dado centrais `[inferido]`

Critério: tabelas que aparecem em mais de um módulo (rota + store + task) e nas duas cadeias de
migration. Os recorrentes são `tenants` e `users` (schema `admin`, globais),
`reports` / `report_steps` / `report_artifacts` / `report_transmissions` (funil do documento),
`operational_competencies` + `regulatory_deadlines` (série de competências),
`data_sources` + `import_jobs` + `raw_data` (ingestão),
`quality_assessments` / `quality_scores` / `quality_dimensions` (RC 18),
`account_entries` (COSIF/contábil) e `audit_events`.

### Migrações

| Cadeia | Ferramenta | Config | Revisões | Head atual |
|---|---|---|---:|---|
| Schema admin | Alembic | `alembic.ini` / `migrations/` | 3 | `0003_alert_log_global` (2026-09-01) |
| Schema de tenant (`tenant_<slug>`) | Alembic | `alembic_tenant.ini` / `migrations_tenant/` | 3 | `0003_drop_opcomp_pointer` (2026-09-03) |

Última migração: **2026-09-03**. Ambas as cadeias são lineares (cada `down_revision` aponta para a
anterior); o CI tem um **guard explícito de head única** ([bitbucket-pipelines.yml:56-65](../bitbucket-pipelines.yml#L56-L65)).

Superfície de dados: **64 `CREATE TABLE`** na baseline de tenant (54 nomes distintos) e
**25 tabelas** no schema `admin` (`tenants`, `users`, `obligations`, `refresh_tokens`, `moat_*`,
`regulatory_*`, `backups`, `incidents`, `tenant_migration_runs`, …).

`[explícito]` A migration de tenant é aplicada a todos os tenants iterando schemas `tenant_%`, e o
`ensure_tenant_schema(tenant_id)` ([backend/storage/postgres.py:245](../backend/storage/postgres.py#L245))
roda `upgrade head` de forma idempotente.

### Contratos externos

| Tipo | Onde |
|---|---|
| API HTTP exposta | 43 módulos em `backend/api/routes/`, 45 `APIRouter`, prefixo `/api/*`; OpenAPI em `/docs` |
| Fila | Celery: 55 tasks decoradas, 28 módulos em `backend/worker/tasks/`. Filas consumidas: `import.file`, `cadoc.validate`, `cadoc.generate`, `quality.assess` |
| Rotas de task | **derivadas** das flow specs por `backend/engine/discovery.py` (`derive_task_routes`/`derive_imports`, com `assert_routing_covered`); as demais são manuais em `worker/app.py:39` |
| Ingestão de arquivo | SFTP por tenant (SFTPGo) — `backend/services/sftp_*.py` (11 arquivos), pasta `entrada/` e `entrada/<fonte>/` |
| Artefato gerado | `.zip`/XML do informe, `document_outputs` / `report_artifacts` |
| Validador BACEN SCR2 | serviço Java externo `cadoc-validator`; cliente em `backend/plugins/cadoc_3044/engine/validator_client.py`; wrapper em `deploy/cadoc-validator/wrapper.py` (**classes/lib fora do repo em runtime**) |
| Telemetria de erro | Loki central — [backend/observability.py](../backend/observability.py) |
| Serviços externos | S3/MinIO (boto3), SES/Mailpit (SMTP), Anthropic + Firecrawl (radar regulatório), Amplitude (frontend) |

---

## 5. Convenções observadas

Contagens por [`scripts/convencoes.sh`](scripts/convencoes.sh).

### Estrutura de camadas: `route → (service) → store`

| Evidência | Valor |
|---|---|
| Módulos em `backend/api/routes/` | 43 |
| Rotas que importam algum `backend.storage.*` | **37 / 43** |
| Rotas que importam `backend.services.*` | 12 / 43 |
| Rotas que **não** importam nem storage nem services | 6 (`auth.py`, `tenants.py`, `document_types.py`, `moat.py`, `telemetry.py`, `__init__.py`) |
| Stores em `backend/storage/*_store.py` | 57 |
| Arquivos em `storage/` que executam SQL | 59 |

**Violação medida da regra "rotas não falam SQL direto"** (`CLAUDE.md`): **14 das 43 rotas** contêm
SQL literal. Concentração nos motores:
`engine3040.py` (7), `engine3050.py` (7), `engine3026.py` (5), `engine3044.py` (5), `painel.py` (5),
`cosif.py` (3), `quality.py` (3), e 1 em cada de `cosif_plano`, `data_sources`, `dictionary`,
`onboarding`, `public_reports`, `users`, `validator`.

A camada `services/` **não é uma camada geral**: 11 dos 15 arquivos são SFTP/SFTPGo. O padrão
dominante real é `route → store` direto `[inferido]`.

### SQL e multi-tenancy
- **358 usos** de `safe_schema_name` em `backend/`.
- **409 linhas** com f-string dentro de SQL; **330 (81%)** interpolam apenas `{schema}`/`{table}` —
  o padrão sancionado. As demais são majoritariamente `{ctx.schema}` no seeder de demo
  (`backend/demo/blocks/*.py`).
- Único caso encontrado de interpolação de **lista de colunas** vinda de request:
  [backend/api/routes/quality.py:137](../backend/api/routes/quality.py#L137) —
  `f"SELECT numero_operacao, codigo_cliente, {', '.join(campos)} "`. Vale conferir a origem de `campos`.
- Valores sempre por `%s` `[explícito]` (regra do CLAUDE.md; não encontrei contraexemplo).
- Armadilha documentada: `safe_schema_name` **não é idempotente** — passe sempre `tenant_id` cru.

### Nomenclatura

| Item | Padrão | Evidência |
|---|---|---|
| Store | `<Dominio>Store` em `backend/storage/<dominio>_store.py`, herdando `BaseStore` | 57 arquivos |
| Rota | `backend/api/routes/<area>.py`, `router = APIRouter(prefix="/api/<area>", tags=[...])` | 45 `APIRouter` |
| Task | `backend/worker/tasks/<area>_task.py` ou `<area>_tasks.py` (**plural só nos motores**) | 28 arquivos |
| Teste | `tests/<subpacote>/test_<stem>.py` espelhando `backend/<subpacote>/<stem>.py` | 540 arquivos |
| Migration | `migrations*/versions/AAAAMMDD_HHMM_NNNN_<slug>.py`, `revision = "NNNN_<slug>"` | 6 arquivos |
| Env var | `REGULATORY_<CAMPO>` — mapeado por prefixo do `BaseSettings` | `settings.py` |
| Legado convivendo | prefixo `cadoc_`, literais `"3040"`/`"3044"`, `informes_*` no localStorage, `dattos-informes-*` nos buckets default | `settings.py:36-40` |
| Idioma | identificadores em inglês; **docstrings mistas: 85 módulos em pt-BR vs 130 en/indefinido** | script inline |

### Tratamento de erro
- **Praticamente só `HTTPException`**: 424 ocorrências em `backend/`.
- **Apenas 4 exceções próprias** no repo inteiro: `DemoGuardError`, `SourceFileMissingError`,
  `SftpGoError` (todas `RuntimeError`) e `FrontendError` (que é um `BaseModel`, não exceção).
- Um único handler global: `@app.exception_handler(Exception)` em
  [backend/api/main.py:184](../backend/api/main.py#L184), que chama `report_error` (Loki).
- `[inferido]` Não existe formato de resposta de erro padronizado além do `{"detail": ...}` do FastAPI.

### Logging
- `logging` da stdlib em **46 arquivos**; **zero** `structlog`/`loguru`.
- Flag `log_json: bool = False` em `settings.py`.
- **43 `print(`** remanescentes em `backend/` `[inferido]` — em CLIs/seeders na maioria.
- Telemetria funcional: [backend/observability.py](../backend/observability.py) — fila não-bloqueante,
  `source` de cardinalidade fechada (`API`/`Worker`/`Report`/`Front`), **mascaramento LGPD de
  CPF/CNPJ/e-mail antes do envio**, descarta em vez de bloquear a request.

### Configuração
- Entrada única: `Settings(BaseSettings)` + `get_settings()` (`lru_cache`), usado em 41 arquivos.
- Validação **fail-closed** `[explícito]`: defaults inseguros (`change-me-in-production`,
  senha `informes`) só são tolerados em `{development, test, local, ci}`; qualquer outro valor —
  inclusive vazio ou com typo — exige segredos fortes ([backend/config/settings.py:7-11](../backend/config/settings.py#L7-L11)).

### Validação de input
- Na borda HTTP, por Pydantic (89 `BaseModel`) + `Depends(` (366 usos em `backend/api`).
- Autorização por dependência: **213 `require_permission`** e **44 `require_role`**.
- Layout de arquivo de cliente: `validate_layout_spec` em `cadoc_adapters/layout_spec.py`.

### Integração externa: retry / timeout / idempotência
`[inferido]` **Não há padrão único.** Grep por `retry|timeout|idempot` acha arquivos em 13 módulos,
concentrados em `storage` (24) e `worker` (13) — ou seja, a política vive espalhada em cada
chamador, não numa camada de cliente. Não existe wrapper/decorator comum de retry no repo.
Idempotência é explícita e documentada apenas nos stores de ponte (`SubmissionStore`, `QualityStore`)
e no `ensure_tenant_schema`.

### Comentários e docstrings
- **337 de 373** arquivos `.py` de `backend/` começam com docstring de módulo (90%).
- As docstrings são longas e **explicam o porquê e a alternativa descartada** — ver
  `backend/engine/base.py:1-19`, `tests/conftest.py:445-458`, `backend/observability.py:1-16`.
  Esse é o traço estilístico mais forte do repo.
- Idioma **misto**: 85 módulos com docstring em pt-BR, 130 em inglês/indefinido.
- Comentários inline referenciam ticket/spec (`REP-35`, `R7`, `Gap 5`, `docs/superpowers/specs/...`).
- **Apenas 15 TODO/FIXME/HACK/XXX** no repo inteiro — o débito não é sinalizado por marcador.

---

## 6. Arquivos exemplares

| Tipo | Modelo a copiar | Por quê | Contraexemplo | O que difere |
|---|---|---|---|---|
| **Endpoint/rota** | [backend/api/routes/data_sources.py](../backend/api/routes/data_sources.py) | Docstring de módulo; `APIRouter(prefix=..., tags=...)`; imports separados por camada (`api.deps`, `auth.middleware`, `services`, `storage`); `require_permission`; zero SQL; constantes de domínio comentadas; delega nomeação de pasta ao serviço ("o /setup usa os MESMOS") | [backend/api/routes/engine3040.py](../backend/api/routes/engine3040.py) | 1.421 linhas (3× o 2º maior), 7 blocos de SQL literal na rota, mistura orquestração de motor com HTTP |
| **Service** | [backend/services/data_source_folders.py](../backend/services/data_source_folders.py) | Funções puras (`assign_folder`, `cadoc_of`, `folder_slug`) reusadas por 2 rotas — a razão de existir da camada | `backend/services/sftp_provision.py` + `sftp_provisioning.py` + `sftpgo_provisioning.py` | três arquivos de nome quase idêntico para o mesmo assunto; a fronteira entre eles não é legível pelo nome |
| **Repository/store** | [backend/storage/distribution_store.py](../backend/storage/distribution_store.py) | Herda `BaseStore`; colunas declaradas como constantes de classe (`_recipient_columns`…), o que dá projeção explícita; `_serialize_dates`; seções demarcadas por comentário; usa `get_connection()` | [backend/storage/tenant_migrations.py](../backend/storage/tenant_migrations.py) (640 linhas) | não é um `*_store.py`, não herda `BaseStore`, e é o maior arquivo de `storage/` |
| **Job/worker** | [backend/worker/tasks/ops_task.py](../backend/worker/tasks/ops_task.py) (445 l.) | Tamanho tratável, task registrada e roteada, coberto por `tests/worker/test_sftp_watch_s3.py` (mudam juntos em 9 commits) | [backend/worker/tasks/engine3040_tasks.py](../backend/worker/tasks/engine3040_tasks.py) (1.449 l.) | é o motor copiado que o `engine/base.py` existe para substituir; `engine3040_tasks` e `engine3044_tasks` mudam juntos em 12 commits — duplicação viva |
| **Cliente de integração** | [backend/plugins/cadoc_3044/engine/validator_client.py](../backend/plugins/cadoc_3044/engine/validator_client.py) | Cliente isolado do serviço externo, com teste de contrato pareado (`tests/deploy/test_validator_wrapper.py`) | [backend/observability.py](../backend/observability.py) | também é integração externa (Loki), mas mora na raiz de `backend/`, não em `services/` nem num pacote de clientes |
| **Migração** | `migrations_tenant/versions/20260901_0000_0002_cadoc3040_retification_lane.py` | Revisão incremental, nomeada por assunto, na cadeia de tenant | `migrations/versions/20260828_0100_0002_limpa_obrigacoes_fantasma.py` | migration de **limpeza de dado**, não de schema, e é uma das 15 ocorrências de TODO do repo |
| **Config/fundação** | [backend/config/settings.py](../backend/config/settings.py) | Único módulo com out-degree 0; guard fail-closed explicado no topo | — | — |
| **Registry declarativo** | [backend/flows/cadoc_registry.py](../backend/flows/cadoc_registry.py) | Docstring diz o invariante ("adicionar um CADOC novo = uma entrada aqui"); cada campo do dataclass comentado com o porquê | — | — |
| **Teste unitário** | `tests/flows/test_periods.py` / `tests/flows/test_resolvers.py` | Acoplamento de mudança de **100%** e **92%** com o módulo que cobrem — teste que anda junto com o código | ver §7 (18 testes sem assert) | |
| **Teste de integração** | `tests/worker/test_engine3044_consolidate.py` | 92% de co-mudança com `engine3044_tasks.py` | `tests/storage/test_tenant_fixture_isolamento.py` | é o único arquivo cujos 5 testes **erram** (não pulam) sem banco — a fixture `_public()` chama `ensure_admin_schema()` fora do gate de skip |
| **E2E** | `e2e/tests/44-listagem-3040.spec.ts` | 85% de co-mudança com a página que testa | — | — |
| **Seeder** | [backend/cli/seed.py](../backend/cli/seed.py) | Ponto de entrada documentado no CLAUDE.md | `backend/demo/blocks/*` (9 dos 16 sem teste) | ver §7 |

---

## 7. Testes

### Estrutura

| Item | Valor |
|---|---|
| Framework backend | pytest, `asyncio_mode = auto`, `testpaths = tests` |
| Descoberta | `python_files = test_*.py`, `python_functions = test_*` ([pytest.ini](../pytest.ini)) |
| Paralelismo | **`--dist loadfile` fixo em `addopts`** — `pytest-xdist` é dependência obrigatória; sem ele *qualquer* `pytest` morre com "unrecognized arguments" (comentado em `pyproject.toml:47-49`) |
| conftest | 3: `tests/conftest.py` (539 l.), `tests/api/conftest.py`, `tests/demo/conftest.py` |
| Fixture central | `tenant` — schema estável por cenário, reset de **dado** (~60 ms) em vez de recriar schema (~1,5 s). O invariante de isolamento é fixado por `tests/storage/test_tenant_fixture_isolamento.py` |
| Marcadores | 1 (`slug_literal`) |
| Mocks | 137 arquivos usam `monkeypatch`/`unittest.mock`/`MagicMock` |
| Frontend | vitest, 19 arquivos de teste (`frontend/lib/__tests__`, analytics) |
| E2E | Playwright, 52 specs em `e2e/tests/`, `workers: 1`, `fullyParallel: false`, `retries: 1` |

### Contagem por tipo `[inferido]`

Critério usado: **unit** = não referencia pool/schema/psycopg; **integração** = usa a fixture
`tenant`/`db_pool`/`psycopg` (gated por `REGULATORY_DB_PORT`); **e2e** = spec Playwright em `e2e/`.

| Tipo | Contagem |
|---|---:|
| Arquivos `test_*.py` | 540 |
| Funções `test_*` (backend) | 2.911 |
| Arquivos que tocam banco (integração) | 48 |
| Specs E2E (Playwright) | 52 |
| Testes frontend (vitest) | 19 arquivos |

### Execução da suíte

```
python -m pytest -q --durations=15
2497 passed, 726 skipped, 2 xfailed, 6 warnings, 5 errors in 49.49s   (exit 1)
```

- **726 skips (22%) são o gate de banco**: `tests/conftest.py:461` faz
  `pytest.skip("precisa do DB de teste")` quando `REGULATORY_DB_PORT` não está no ambiente.
  Nada no repo documenta essa variável como pré-requisito da suíte.
- **5 errors pré-existentes**, todos em `tests/storage/test_tenant_fixture_isolamento.py`: a fixture
  `autouse` `_public()` chama `ensure_admin_schema()` **antes** do gate de skip, então sem banco ela
  não pula — erra. Sai com exit 1 mesmo sem falha real de teste.
- **Não foi possível rodar os 726 testes de banco neste ambiente**: o Postgres local
  (`localhost:5433`, db `regulatory_reports`) está numa cadeia Alembic legada
  (`admin.alembic_version = '0007_document_dependencies'`) e `migrations/env.py:94` recusa aplicar
  ("Este ambiente ficou entre as duas cadeias"). Criar um database descartável foi bloqueado pelo
  hook `guard_bash.py` do próprio repo. → **A cobertura real de integração não foi verificada.**

### 15 testes mais lentos (sem banco)

| s | Teste |
|---:|---|
| 4,39 | `tests/processing/test_cadoc3026_consolidation_decimal.py::test_exposicao_no_limiar_...` |
| 4,12 | `tests/api/test_auth.py::test_ready_check` |
| 4,01 | `tests/api/test_rate_limit_auth.py::test_limiter_usa_storage_redis` (setup) |
| 1,09–1,04 | 7 testes de `tests/worker/test_notification_mailpit.py` (SMTP real contra Mailpit) |
| 1,02 | `tests/workflow/test_email_contract_estrutural.py` |
| 0,83 / 0,61 | `tests/services/test_sftp_provisioning.py` (bcrypt real) |
| 0,54 / 0,53 | `tests/workflow/test_email_guards.py`, `tests/api/test_admin_sftp.py` |

A suíte é **rápida** (49 s), mas os 3 mais lentos e 7 dos 15 dependem de serviço externo
(Redis, Mailpit) — ou seja, os testes "lentos" são justamente os de integração que ainda passam.

### Teste → módulo de produção

Gerado por [`scripts/cobertura_modulos.py`](scripts/cobertura_modulos.py) →
**[data/cobertura.md](data/cobertura.md)**.

- Arquivos `.py` em `backend/` (fora `__init__`): **330**
- Sem `tests/**/test_<stem>.py` correspondente: **112**
- Sem teste **e** sem nenhuma menção a `backend.<caminho>` em teste algum: **31**

Concentração dos 31 sem cobertura:

| Módulo | Qtd | Destaques |
|---|---:|---|
| `backend/api` | 14 | `routes/retification.py` (547 l.), `routes/schema_versions.py`, `routes/sftp.py`, `routes/public_reports.py`, `routes/policy.py`, `middleware/workspace.py` |
| `backend/demo` | 9 | quase todo o seeder de demo (`blocks/users.py`, `calendar.py`, `communication.py`, `sources.py`, …) |
| `backend/services` | 3 | `approval_controls.py`, `current_document.py`, `data_source_folders.py` |
| `backend/worker` | 2 | `tasks/import_task.py`, `tasks/sftp_rejection.py` |
| outros | 3 | `cli/check_drift.py`, `plugins/cadoc_3026/anexo11.py`, `storage/schema_version_gateway.py` |

Notas: `retification.py` (547 linhas, feature recente) e `import_task.py` (ingestão) sem teste
próprio é o par mais exposto `[inferido]`. `backend/demo/` sem teste alinha-se ao histórico:
**7 dos 20 commits de retrabalho amostrados são correções no seeder de demo** (§9).

**Módulos com teste que só passam por dependência externa**: os 48 arquivos gated por
`REGULATORY_DB_PORT`, mais `tests/worker/test_notification_mailpit.py` (SMTP/Mailpit) e
`tests/api/test_rate_limit_auth.py` (Redis).

### Sinais de teste fraco

| Sinal | Contagem | Exemplos |
|---|---:|---|
| Funções `test_*` sem `assert` e sem `pytest.raises` | **18 de 2.911 (0,6%)** | `tests/api/test_data_source_schedule.py::test_schedule_diaria_valido`, `tests/auth/test_middleware_suspension.py::test_active_tenant_passes`, `tests/config/test_settings.py::test_dev_aceita_defaults_inseguros` |
| Testes cujo nome declara "não levanta" (smoke puro) | ≥3 | `test_nunca_propaga_erro`, `test_justificar_ok_nao_levanta`, `test_move_by_job_outcome_arquivo_ja_movido_nao_levanta` |
| Só `pytest.raises`, sem asserção sobre a mensagem/estado | 103 | — |
| Testes que testam mock | não quantificado — 137 arquivos usam mock; a distinção exigiria leitura caso a caso |
| Testes duplicados | não quantificado |

`[inferido]` 0,6% de testes sem assert é baixo. O sinal mais relevante não é teste vazio, é
**ausência de teste** nos 31 módulos acima.

### Cobertura e "só o afetado"

- **Nenhuma ferramenta de cobertura configurada** (`coverage`/`pytest-cov` não estão em
  `pyproject.toml`, `pytest.ini` nem no CI). Não configurei.
- **Não existe execução "só o afetado" formal** (`pytest-testmon` ausente, `--lf` não usado no CI).
  O que existe é o hook `Stop` do Claude Code
  ([.claude/hooks/run_tests.py](../.claude/hooks/run_tests.py)): roda "um subconjunto rápido de testes
  para o que mudou" com base no caminho editado (`backend/**` ou `tests/**` → `pytest` na raiz), e
  **pula silenciosamente se o Postgres não estiver acessível**.
- O CI roda `pytest -q` inteiro, sempre.

---

## 8. Processo e ferramentas existentes

### Instruções para agentes

| Arquivo | Existe | Conteúdo |
|---|---|---|
| `CLAUDE.md` (raiz) | sim, 190 linhas | O documento mais denso do repo: identidade do produto, limite de responsabilidade, invariantes de domínio, princípios de arquitetura, stack, estrutura de pastas, convenções, ambiente/AWS, quirks de push, e uma seção "Armadilhas conhecidas" |
| `.cursorrules`, `AGENTS.md`, `.github/copilot-instructions.md` | **não existem** | |
| `.claude/` | sim | `agents/` (3), `commands/` (1), `hooks/` (3), `skills/` (13), `settings.json`, `launch.json` |
| `.superpowers/sdd/` | sim | 43 arquivos / 5.562 linhas |

**Desatualizações do `CLAUDE.md` verificadas**: D1–D4 na §1 (compose auto-contido vs umbrella;
migrations 0004–0007 inexistentes; `TENANT_TABLES_DDL` ainda presente 3×; `deploy.sh` com serviço
`web`). O `CLAUDE.md` foi alterado **28 vezes em 6 meses** — está entre os 20 arquivos mais mexidos
do repo, o que indica que é mantido, mas por acréscimo.

### CI — Bitbucket Pipelines

[bitbucket-pipelines.yml](../bitbucket-pipelines.yml), image `python:3.12`, serviço `postgres:16`.

| Step | O que faz | Bloqueia merge? |
|---|---|---|
| `tests` | `pip install -e ".[dev]"` + `pytest -q` com envs `REGULATORY_DB_*` apontando para o Postgres do serviço | **sim** |
| `migrations` | guard de **head única** (`alembic heads` deve dar 1) → `upgrade head` → `downgrade base` (reversibilidade) → `upgrade head` (idempotência) | **sim** |
| `security` | `bandit -r backend --severity-level high --confidence-level high` | **sim** (hoje 0 achados; ~362 de severidade média conhecidos e não triados `[explícito]`) |
| | `pip-audit \|\| true` | **não** — informativo por decisão declarada |
| `npm-audit` | `npm audit --audit-level=high \|\| true`; `npm run test`; `npm run analytics:codegen && git diff --exit-code lib/analytics/events.types.ts` | o audit não bloqueia; **o teste vitest e a guarda de staleness dos tipos gerados bloqueiam** |
| `build-deploy` | branch `qas` → tag `qas-<build#>` no ECR da conta QAS; branch `main` → `prd-<build#>` no ECR da conta **PROD apartada**; `sed` no `values-<env>.yaml` e force-push da branch `regulatory-report-<env>-live` → ArgoCD (QAS auto-sync, PROD sync manual) | — |

**Tempo médio de pipeline: não determinável a partir do repo** — exigiria a API do Bitbucket.
Referência local: `pytest` sem banco = 49 s.

**Ausências**: nenhum step de lint Python (`ruff`) ou de type check (`mypy`/`pyright`) no CI; não há
`npm run lint` nem `npm run build` no pipeline (só `test` e `audit`); os E2E do Playwright **não
rodam no CI**.

### Hooks locais, linters, formatters, type checkers

| Ferramenta | Existe | Ativo onde |
|---|---|---|
| `.pre-commit-config.yaml`, `.husky/` | **não existem** | — |
| `ruff` | usado, mas **sem seção `[tool.ruff]`** em `pyproject.toml` e sem `ruff.toml` — roda com defaults | hook `PostToolUse` do Claude Code |
| `eslint` (`eslint-config-next`) | sim, `npm run lint` | não roda no CI |
| `tsc` / type check Python | **nenhum type checker configurado** | — |
| `bandit`, `pip-audit`, `npm audit` | sim | CI |

Hooks do Claude Code ([.claude/settings.json](../.claude/settings.json)) — são o gate real do dia a dia:
- **`PostToolUse`** em `Edit|Write|MultiEdit`: `format_lint.py` (`ruff format` + `ruff check --fix`
  em `.py`; `npx eslint --fix` em `frontend/**`; falha de lint sai 2) e `check-dead-code.sh`.
- **`PreToolUse`** em `Bash`: `guard_bash.py` — bloqueia comandos destrutivos de banco
  (`DROP DATABASE`/`dropdb`/`TRUNCATE`). *(Confirmado na prática: bloqueou meu próprio probe.)*
- **`Stop`**: `run_tests.py` — subconjunto de testes, não-bloqueante, pula sem Postgres.
- `permissions`: allow/deny/ask com deny em `git push --force`, `git reset --hard`, `rm -rf /`, `DROP DATABASE`.

**O código passa nessas ferramentas hoje?** `bandit` no nível alto: sim (0 achados, declarado no
pipeline). `ruff`/`eslint`: não verificável sem executar — não estão no CI, então não há gate.

### Scripts de automação

| Local | Conteúdo |
|---|---|
| `Makefile` | **não existe** |
| `pyproject.toml` | sem `[project.scripts]`; entrypoints são `python -m backend.cli.<x>` |
| `frontend/package.json` | `dev`, `build`, `start`, `lint`, `test`, `analytics:codegen` |
| `e2e/package.json` | projeto Playwright separado |
| `scripts/` | 3 scripts pontuais de migração/seed (72 linhas no total) |
| `deploy/` | `deploy.sh` (tag por SHA, health-gate, rollback automático — **com o bug do serviço `web`**), `rollback.sh`, `docker-compose.prod.yml`, `k8s/chart` (Helm), `terraform/` (4 camadas) |
| `.claude/skills/` | 13 arquivos — automação de implantação/suporte/QA embutida no repo |

### Templates de PR/issue
**Não existem** — nenhum `pull_request_template`, `PULL_REQUEST_TEMPLATE` ou `ISSUE_TEMPLATE` no repo.

---

## 9. Histórico e pontos quentes

Gerado por [`scripts/git_hotspots.sh`](scripts/git_hotspots.sh) e
[`scripts/coupling_rework.py`](scripts/coupling_rework.py) →
**[data/git-hotspots.md](data/git-hotspots.md)**, **[data/coupling.md](data/coupling.md)**.
Janela: últimos 6 meses. **1.931 commits**, 6 autores
(Guilherme Pessoa 1.295, Vagner Borges 520, Denis Azevedo 86+22, `merge-check` 83, Claude 4, CI 2).

> Ressalva de leitura: o repo passou por **duas renomeações de pasta** —
> `dattos_informes/` → `backend/` e `web/` → `frontend/`. O `git log --name-only` sem `--follow`
> conta os dois caminhos separadamente, então cada arquivo quente aparece "duas vezes".

### Top arquivos alterados (somando os dois nomes)

| commits | arquivo |
|---:|---|
| **125** | `storage/postgres.py` (71 legado + 54 atual) |
| **68** | página `cadoc-3040/page.tsx` (30 + 38) |
| **61** | `worker/tasks/engine3040_tasks.py` (35 + 26) |
| 44 | `worker/tasks/engine3044_tasks.py` |
| 43 | `api/routes/painel.py` |
| 41 | `api/main.py` / `api/deps.py` |
| 40 | `worker/app.py` |
| 39 | `deploy/docker-compose.prod.yml` |
| 36 | `api/routes/engine3040.py` |
| **28** | **`CLAUDE.md`** |
| 24 | `bitbucket-pipelines.yml` |

`storage/postgres.py` (283 linhas hoje) é de longe o arquivo mais volátil do repo — é onde vivem o
pool, `safe_schema_name` e `ensure_tenant_schema`.

### Módulos com mais commits (arquivos tocados)

`tests/api` (646) > `docs/superpowers` (584) > `tests/storage` (533) > `api` (376+254) >
`frontend/app` (375+325) > `tests/worker` (345) > `storage` (271+247).

`[inferido]` Os três primeiros lugares são **teste e documentação**, não código de produção — a
proporção teste/produção nas mudanças é alta.

### Acoplamento por mudança (top pares)

Dois grupos distintos:

**a) Teste anda com o código (saudável)** — `flows/periods.py` ↔ `tests/flows/test_periods.py`
(**100%**), `flows/resolvers.py` ↔ seu teste (92%), `engine3044_tasks.py` ↔
`test_engine3044_consolidate.py` (92%), `services/sftp_inbox.py` ↔ `test_sftp_inbox.py` (100%),
`deploy/cadoc-validator/wrapper.py` ↔ `tests/deploy/test_validator_wrapper.py` (100%).

**b) Fronteira que vaza (atrito)**:
- `api/routes/engine3040.py` ↔ `cadoc-3040/[reference_period]/page.tsx` (12 commits, 50%) e ↔
  `cadoc-3040/page.tsx` (11, 33%) — **backend e frontend mudam juntos**, consistente com tipos TS
  escritos à mão.
- `api/routes/painel.py` ↔ `lib/types/painel.ts` (7) ↔ `components/flow-card.tsx` (7);
  `flow-card.tsx` ↔ `lib/types/painel.ts` (13, **72%**).
- **`engine3040_tasks.py` ↔ `engine3044_tasks.py` (12 commits, 34%)** — a duplicação entre motores
  que o `backend/engine/base.py` foi escrito para eliminar, ainda ativa.
- `api/deps.py` ↔ `storage/postgres.py` (9).
- `plugins/cadoc_3044/engine/validator_client.py` ↔ `deploy/cadoc-validator/wrapper.py` (7, 88%) —
  contrato com um componente cujo código-fonte **não está versionado neste repo**.

### Convenção de mensagem de commit

Conventional Commits, com escopo `[explícito]` (`tipo(escopo): descrição`):

| tipo | n | | tipo | n |
|---|---:|---|---|---:|
| `feat` | 744 | | `chore` | 41 |
| `fix` | 305 | | `merge` | 22 |
| `docs` | 290 | | `style`/`perf` | 7 / 7 |
| `test` | 98 | | `ci` | 5 |
| `refactor` | 63 | | sem prefixo | 12 |

Escopos observados: ora o ticket (`fix(REP-83)`), ora a área (`fix(3040)`, `fix(demo)`,
`fix(front)`, `fix(local)`) — **as duas convenções convivem**.

**Referência a ticket: 234 de 1.931 commits (12%)** citam `REP-nnn`. A rastreabilidade
commit→Jira é minoritária.

Rodapé `Co-Authored-By: Claude` é a convenção declarada no `CLAUDE.md`.

### Retrabalho

Critério: commit `fix|ajuste|corrige|hotfix` que toca um arquivo mexido por um commit `feat` **nas
48 h anteriores**.

**238 de 305 commits `fix` (78%) se encaixam.** O critério é generoso (basta co-ocorrência de
arquivo, não causalidade provada), mas a magnitude e a **concentração** são o sinal:

| Área | Exemplos de retrabalho |
|---|---|
| **Seeder de demo** (`backend/demo/`, `backend/cli/seed_demo.py`) | 7 dos 20 amostrados — `fix(REP-83): seeder recupera admin ausente`, `fix(REP-83): rebuild no longer deletes the admin`, `fix(demo): 3044 usa data cheia na competência (GET /api/painel 500ava)`, `fix(demo): onda final de correções da revisão de branch (10 achados)` |
| **Frontend 3040/topbar** | `fix(front): topbar alinhado por construção`, `fix(front): avatar no tamanho dos ícones (22px)`, `fix(3040): troca de filtro em voo não é mais engolida` |
| **Compose local** | `fix(local): cria o bucket de backups no compose local`, `fix(local): bucket de backup segue o nome do produto` |
| **Review de PR** | `fix(REP-80): corrige os 8 achados do review desta PR` |

`[inferido]` O padrão é: as áreas com retrabalho são exatamente as **sem teste automatizado**
(`backend/demo/` tem 9 dos 31 módulos sem cobertura; frontend visual e compose local não têm gate).

### TODO/FIXME/HACK/XXX

**15 no repo inteiro.** Distribuição: `e2e/tests` 3, `backend/flows` 2, `e2e/seed` 2, e 1 em cada de
`backend/api`, `backend/cli`, `backend/plugins`, `backend/storage`, `migrations/versions`,
`tests/flows`, `tests/storage`, `tests/workflow`. **Nenhuma concentração.**

---

## 10. O que faltou para o repo se explicar

Derivado de [LOG.md](LOG.md). ~26 arquivos de código/config abertos; o resto por script.

**Perguntas que exigiram abrir >5 arquivos ou escrever script dedicado**

1. Qual é a camada canônica (`route → service → store`)? Não há documento; foi preciso contar
   imports e SQL por rota para descobrir que o padrão real é `route → store` e que `services/` é
   quase só SFTP.
2. Como rodar a suíte de verdade? Só lendo `tests/conftest.py:461` se descobre que
   `REGULATORY_DB_PORT` é o gate de 22% dos testes.
3. Qual a cadeia de migrations vigente? O `CLAUDE.md` cita revisões inexistentes.
4. Quem depende de quem? 113 ciclos — nenhuma camada documentada como acíclica.
5. O que é `backend/processing/` (DuckDB)? Nenhum módulo o importa; só o `pyproject.toml` diz
   "Fase 0 = spike".

**Convenções que só apareceram por contagem**

- `route → store` direto é o padrão (37/43), não `route → service → store`.
- 14 rotas com SQL literal — contradiz a regra escrita.
- `HTTPException` é praticamente a única exceção (424×); só 4 exceções próprias no repo.
- Docstrings em idioma misto (85 pt / 130 en) — a regra escrita diz "identificadores em inglês",
  mas não decide o idioma da prosa.
- Nenhum padrão comum de retry/timeout para integração externa.
- `requests` (5 módulos) vs `httpx` (1) — dois clientes HTTP sem regra.
- Escopo do commit ora é ticket, ora é área.
- 12% de rastreabilidade commit→Jira.

**Decisões de arquitetura sem documentação em lugar nenhum**

- Por que `backend/observability.py` mora na raiz de `backend/` e não em `services/` ou `integrations/`.
- Por que `backend/integrations/` existe vazio e `valx/` existe vazio.
- Por que `services/` tem `sftp_provision.py`, `sftp_provisioning.py` **e** `sftpgo_provisioning.py`.
- Qual o estado do `CadocEngine` — o `base.py` diz que é "fundação conservadora" que "coexiste com
  os motores legados", mas nada diz quais motores já migraram e quais faltam.
- Por que `duckdb` é dependência de runtime para um módulo sem consumidor.
- Se `--dist loadfile` é permanente ou dívida das 3 fixtures de escopo de módulo citadas no `pytest.ini`.
- Por que não há `ruff`/`mypy` no CI, se o hook local já roda `ruff`.
- Por que `tests/storage/test_tenant_fixture_isolamento.py` não respeita o gate de skip (5 erros
  permanentes fazem a suíte sair com exit 1 fora do CI).
- Onde vive o versionamento do `cadoc-validator` (Java), com quem o repo tem contrato de 88% de
  co-mudança mas que não está versionado aqui.

---

## 11. Perguntas para o time

1. `services/` deve ser uma camada obrigatória entre rota e store, ou o padrão `route → store` direto é o desejado?
2. As 14 rotas com SQL literal (concentradas nos motores) são dívida a pagar ou exceção aceita para motores?
3. Qual é a fronteira entre `sftp_provision.py`, `sftp_provisioning.py` e `sftpgo_provisioning.py`?
4. Os 113 ciclos entre subpacotes são consequência de imports diferidos intencionais ou dívida a quebrar? Existe alguma camada que deveria ser acíclica por regra?
5. `worker` importa `api` em 41 arquivos — isso é intencional (reuso de schema/deps) ou inversão a corrigir?
6. Qual o estado da migração dos motores para o `CadocEngine`? Quais informes já usam a base e quais ainda são motor copiado?
7. `engine3040_tasks.py` e `engine3044_tasks.py` mudam juntos em 34% dos commits — há plano ativo de unificação ou isso é status quo aceito?
8. `backend/processing/` (DuckDB) tem consumidor previsto, ou o spike terminou e a dependência deve sair do `pyproject`?
9. `backend/integrations/` e `valx/` estão vazios — devem existir?
10. Qual é a política de retry/timeout para chamadas externas (validador BACEN, SFTPGo, Loki, Firecrawl, Anthropic)? Existe uma, ou é decisão de cada chamador?
11. `requests` ou `httpx` — qual é o cliente HTTP canônico?
12. Docstring de módulo deve ser em português ou inglês?
13. Deve existir formato padronizado de resposta de erro além do `{"detail": ...}` do FastAPI?
14. Por que não há `ruff` nem type checker no pipeline, se o hook local já os roda? É decisão ou lacuna?
15. Cobertura de código deve ser medida? Há meta?
16. `--dist loadfile` é permanente, ou as 3 fixtures de escopo de módulo devem ser corrigidas para liberar `--dist load`?
17. Os 5 erros permanentes de `test_tenant_fixture_isolamento.py` sem banco são conhecidos e aceitos?
18. Qual é a receita suportada para levantar um banco de teste local do zero, dado que o `regulatory_reports` local pode ficar preso entre cadeias Alembic?
19. Os E2E do Playwright devem entrar no CI, ou permanecem execução manual contra QAS?
20. `retification.py` (547 linhas) e `worker/tasks/import_task.py` não têm teste próprio — é lacuna ou estão cobertos por outro caminho?
21. `backend/demo/` (seeder) concentra retrabalho e não tem teste — deve ganhar gate automatizado ou é código descartável?
22. Rastreabilidade commit→Jira está em 12%. Referenciar `REP-nnn` deveria ser obrigatório?
23. Escopo do commit deve ser o ticket (`fix(REP-83)`) ou a área (`fix(3040)`)?
24. Deve haver template de PR? Hoje não existe.
25. O `pyproject.toml` ainda se chama `dattos-informes-legais` e diz "envio de CADOCs ao Banco Central" — renomear o pacote é aceitável, ou o nome de distribuição é contrato?
26. O compose local é auto-contido (como diz o próprio arquivo) ou depende da umbrella da plataforma (como diz o `CLAUDE.md`)?
27. `deploy/deploy.sh` continua com `APP_SERVICES=(api worker beat web)`, serviço que não existe mais. O script ainda é usado, ou está morto desde a migração para EKS?
28. Onde vive o código do `cadoc-validator` (Java) e qual o processo para mudá-lo em conjunto com `validator_client.py`?
29. Os ~362 achados `bandit` de severidade média serão triados, e há prazo para subir o gate?
30. `pip-audit` e `npm audit` são `|| true` hoje — quando viram gate?
31. `campos` em `backend/api/routes/quality.py:137` é interpolado numa cláusula SELECT — a origem é lista fechada validada?
32. O `CLAUDE.md` é atualizado por acréscimo (28 commits em 6 meses) e já tem 4 divergências verificadas com o código. Quem é dono dele e com que cadência é auditado?
