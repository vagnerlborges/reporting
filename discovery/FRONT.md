# Discovery 2 — mapa frontend → API → worker

Continuação de [DISCOVERY.md](DISCOVERY.md). Mesmas regras: evidência com caminho e contagem,
`[explícito]` / `[inferido]`, scripts reexecutáveis em `discovery/scripts/`, sem segredo.
Esforço e bloqueios: [LOG2.md](LOG2.md). Tabelas completas em `discovery/data/`.

- Commit base: `898bbea` (2026-09-07).
- Objetivo: decidir **por número** qual informe migra primeiro e o que está morto.

---

## 1. Página → endpoints

Tabela completa das 65 páginas com endpoints e tipos: **[data/paginas.md](data/paginas.md)**
(`data/paginas.json`). Gerado por [`scripts/paginas.py`](scripts/paginas.py), que segue os
imports locais de cada `page.tsx` (componentes e libs de `frontend/`) e normaliza template
literals (`${x}` → `{}`).

| Métrica | Valor |
|---|---:|
| Páginas (`frontend/app/**/page.tsx`) | 65 |
| Endpoints `/api/*` distintos citados pelo front | 224 |
| Páginas sem nenhum endpoint | 6 |
| Arquivos seguidos por página (máximo) | 33 (`/cadoc-3040/[reference_period]`) |

**As 6 páginas sem endpoint não são bugs** `[explícito]`: `/imports/new`, `/imports/new-3044`,
`/calendario` e `/cycle` são stubs de `redirect()` (5–8 linhas, com comentário explicando que a
rota antiga foi mantida para não quebrar link); `/settings` é hub de `<Link>`; `/guia` é conteúdo
estático de onboarding.

### Páginas mais pesadas

| endpoints | rota | arquivos seguidos |
|---:|---|---:|
| 24 | `/admin/tenants/[id]` | 10 |
| 18 | `/cadoc-3040/[reference_period]` | 33 |
| 17 | `/cadoc-3040/[reference_period]/retificacao` | 23 |
| 12 | `/cadoc-3044` | 19 |
| 10 | `/` (Início/Painel) | 23 |
| 10 | `/quality/reconciliation/conciliar` | 7 |
| 9 | `/cadoc-3050` | 16 |

### Endpoints mais compartilhados entre páginas

`/api/setup/reportes` (15 páginas) · `/api/onboarding/status` (8) · `/api/users/me/onboarding` (8)
· `/api/admin/tenants` (5) · `/api/setup/reportes/reference_period` (5).

`[inferido]` `/api/setup/reportes` é o ponto único de "quais informes este tenant tem" — é o
endpoint mais acoplado da aplicação e a dependência transversal de qualquer informe novo.

### Convenção de chamada — **duas coexistem** `[explícito]`

- Dominante: `apiFetch<T>("/api/...")` de [frontend/lib/api.ts:61](../frontend/lib/api.ts#L61) —
  74 arquivos em `app/` + `components/`.
- Minoritária: `fetch(`${API_BASE}/api/...`)` direto — 8 arquivos (ex.:
  `frontend/app/(auth)/forgot-password/page.tsx:20`). Foi o que fez a 1ª execução do script
  perder 14 endpoints (ver LOG2).

Tipos: 16 arquivos em `frontend/lib/types/*.ts`, escritos à mão. Exceção:
`frontend/lib/analytics/events.types.ts` é **gerado** (`npm run analytics:codegen`) e tem guarda
de staleness no CI — o único contrato front/back com verificação automática.

---

## 2. Endpoint → consumidores e dependências

Tabela completa das 288 operações HTTP: **[data/endpoints.md](data/endpoints.md)**
(`data/endpoints.json`). Gerado por [`scripts/endpoints.py`](scripts/endpoints.py) via AST dos
decoradores (`@router.get/post/...`), resolvendo o `prefix` do `APIRouter`.

| Métrica | Valor |
|---|---:|
| Operações HTTP | 288 em 40 módulos |
| Com consumidor no front | 242 (84%) |
| Cobertas por spec E2E | **73 (25%)** |
| Com `require_permission`/`require_role` | 218 (76%) |
| Que enfileiram task Celery | 21 (7%) |
| Candidatos a "sem consumidor" (1ª passagem) | 23 |
| **Sem consumidor confirmado (2ª passagem)** | **13** |

Módulos com mais operações: `operations.py` (26), `admin.py` (21), `engine3040.py` (15),
`distribution.py` (14), `reconciliation.py` (13), `retification.py` (12), `painel.py` (11),
`policy.py` (11), `setup.py` (11).

### Páginas que chamam endpoint inexistente: **nenhuma**

Dos 224 endpoints citados pelo front, **202 casam exatamente** com um path do backend e **22
casam por prefixo** (artefatos de query colada ao path ou segmento dinâmico). **Zero sem match.**

### Endpoints sem consumidor — 13 confirmados

Lista completa e os 10 descartados: **[data/endpoints-mortos.md](data/endpoints-mortos.md)**,
gerado por [`scripts/mortos.py`](scripts/mortos.py) (2ª passagem: path vira regex e busca no texto
bruto de `frontend/` + `e2e/tests`, pegando `/api/painel/3040/${p}/aprovar` e `events.csv?${qs}`).

| método | path | módulo:função | l. |
|---|---|---|---:|
| GET | `/api/bcb/check/{}` | `bcb.py:check_pending_issues` | 6 |
| POST | `/api/cosif-plano` | `cosif_plano.py:upload_tenant` | 13 |
| DELETE | `/api/cosif-plano` | `cosif_plano.py:remover_override` | 7 |
| GET | `/api/cosif-plano` | `cosif_plano.py:status_override` | 4 |
| POST | `/api/reports/acknowledgments/{}/confirm` | `distribution.py:confirm_acknowledgment` | 12 |
| POST | `/api/engine3040/responsavel` | `engine3040.py:set_responsavel_competencia` | 33 |
| POST | `/api/painel/{}/{}/aferir` | `painel.py:aferir` | 33 |
| POST | `/api/policy/reviews/{}/reject` | `policy.py:reject_review` | 7 |
| PUT | `/api/quality/dimensions/{}` | `quality.py:update_dimension` | 17 |
| POST | `/api/quality/reports/generate` | `quality.py:generate_report` | 11 |
| GET | `/api/retification/history` | `retification.py:history` | 4 |
| POST | `/api/retification/{}/link-document` | `retification.py:link_document` | 13 |
| GET | `/api/users/me/tenants` | `users.py:list_my_tenants` | 25 |

Total: **198 linhas** de rota sem nenhum chamador. Nenhuma marcada como deprecated no código.
Concentrações notáveis `[inferido]`: os 3 de `cosif-plano` são o CRUD inteiro do override de plano
de contas por tenant (a página `/admin/cosif-plano` existe, mas usa outros endpoints); os 2 de
`retification` e o `painel.py:aferir` são de features recentes onde só parte do fluxo chegou à UI.

### Rotas que enfileiram task (21)

| rota | task |
|---|---|
| `POST /api/engine3040/upload` · `/consolidate` · `/imports/delete` | `process_3040_file`, `consolidate_3040` |
| `POST /api/engine3044/upload` · `/consolidate` · `/imports/delete` · `/exclusions` | `process_3044_file`, `consolidate_3044` |
| `POST /api/engine3050/upload` · `/consolidate` | `process_3050_file`, `consolidate_3050` |
| `POST /api/engine3026/upload` · `/consolidate` | `process_3026_file`, `consolidate_3026` |
| `POST /api/cosif/upload` · `/generate` | `process_cosif_file` |
| `POST /api/retification/{}/consolidate` | `consolidate_3040` |
| `POST /api/bacen-ciclo/submissions/{}/retorno` | `processar_veredito` |
| `POST /api/reports/distributions/{}/send` | `send_report_emails` |
| `POST /api/operations/radar/*` (3) · `/incidents/{}/diagnosticar` | `assess_regulatory_change`, `check_regulatory_versions`, `web_sweep`, `diagnose_incident` |
| `POST /api/pecld/calcular` | `compute_pecld` |

`[explícito]` O contrato "rota que processa arquivo delega para task e responde com job id"
(CLAUDE.md) é respeitado: **todos** os 5 motores só enfileiram, nenhum processa no request path.

---

## 3. Worker — o que roda e quando

Tabelas completas: **[data/tasks.md](data/tasks.md)** (`data/tasks.json`), gerado por
[`scripts/tasks.py`](scripts/tasks.py).

| Métrica | Valor |
|---|---:|
| Entradas em `beat_schedule` | **33** |
| Padrões em `task_routes` manuais | 20 |
| Padrões em `task_routes` derivados das flow specs | 7 |
| Tasks decoradas | 55 |
| Tasks sem rota (cairiam na fila default) | **0** |
| Tasks que ninguém enfileira | **6** |

### `beat_schedule` — 33 entradas, todas com intervalo fixo em segundos

**Não há nenhuma `crontab()`** `[explícito]` — todo agendamento é `float` de segundos, o que
significa "a cada N segundos desde o start do beat", não "às 3h". Distribuição:

| cadência | n | exemplos |
|---|---:|---|
| 300 s (5 min) | 3 | `sftp-watch-3040`, `sftp-watch-3044`, `sftp-watch-3050` |
| 900 s (15 min) | 2 | `sweep-tenant-schemas`, `ops-check-ingestion` |
| 1200–1800 s | 3 | `remediacao-diagnose-pending`, `check-stuck-jobs`, `alert-fonte-pendente-3044` |
| 3600 s (1 h) | 1 | `check-deadlines` |
| 7200 s / 21600 s | 3 | `ops-check-deadlines`, `check-backup-stale`, `ops-sweep-sftp-processing` |
| 86400 s (1 dia) | 16 | alertas, backup diário, radar, moat, engajamento, purge, semestral |
| 604800 s (1 sem.) | 5 | `verify-backup-semanal`, `backup-validador-semanal`, `radar-web-sweep`, `arquivar-cadoc-worm-semanal`, `check-validador-scr-semanal` |

**Nenhuma entrada do beat declara `options.queue`** — todas dependem do `task_routes` para não
cair na fila default. Último commit por entrada está na tabela completa; o mais antigo é
`check-deadlines` (`c9c85d0f`, 2026-06-11) e o mais recente é `sweep-tenant-schemas`
(`625507f4`, 2026-08-30, REP-56).

`[inferido]` Ponto sensível: `sweep-tenant-schemas` roda a cada 900 s no beat, mas o flag
`schema_sweep_enabled` é `False` por default (decisão de produto registrada no CLAUDE.md) — o
agendamento existe e é inerte.

### `task_routes` — 20 manuais + 7 derivados

Filas em uso: `import.file` (17 padrões manuais + wildcards derivados), `quality.assess` (2),
`cadoc.validate` (1), `schema.migrate` (1), `cadoc.generate` (só via override do 3026/3050).

`[explícito]` As 7 derivadas vêm de `derive_task_routes(_engine_registry)`
([backend/worker/app.py:270](../backend/worker/app.py#L270)) — são **padrões wildcard**
(`...engine3040_tasks.*`), mais 2 rotas por ação (`consolidate_3026` e `consolidate_3050` →
`cadoc.generate`). O 3040 e o 3044 são "fila única": tudo em `import.file`, sem `queue_overrides`.

`[inferido]` **`schema.migrate` não está na lista de filas consumidas pelo worker** citada no
CLAUDE.md (`-Q import.file,cadoc.validate,cadoc.generate,quality.assess`). Se o comando de
produção for esse, as duas tasks de `schema_migration_task` ficam sem consumidor — vale conferir
o `values.yaml` do chart.

### Confiabilidade das tasks — o número que importa

De **55 tasks decoradas**:

| opção | quantas declaram |
|---|---:|
| `acks_late` | **0** |
| `max_retries` | **1** (`migrate_tenant_schema`) |
| `autoretry_for` | **0** |
| `time_limit` / `soft_time_limit` próprio | **1** (`web_sweep`, 960 s) |

Todo o resto herda o global de [backend/worker/app.py:29-30](../backend/worker/app.py#L29-L30):
`task_soft_time_limit=300`, `task_time_limit=600`, com `worker_prefetch_multiplier=1`,
`worker_max_memory_per_child=1.5 GiB` e `worker_max_tasks_per_child=100`.

`[inferido]` Consequência medida no próprio código: o comentário em `app.py:34-36` registra pico
de **2,9–4,4 GB no 3040 com 500 mil operações** — acima do `limits.memory` de 2Gi do pod — e o
`worker_max_memory_per_child` "só age DEPOIS que a tarefa termina". Ou seja, uma consolidação
grande estoura o pod **e não tem retry declarado em lugar nenhum**.

### Tasks que ninguém enfileira (6)

| task | módulo | l. | fila |
|---|---|---:|---|
| `distribution_task.check_pending_acknowledgments` | `distribution_task.py` | 11 | `import.file` |
| `engine3044_tasks.regenerate_partial_3044` | `engine3044_tasks.py` | 35 | `import.file` |
| `import_task.process_import` | `import_task.py` | 3 | `import.file` |
| `ops_task.backfill_sla_assign` | `ops_task.py` | 2 | `import.file` |
| `schema_migration_task.migrate_tenant_schema` | `schema_migration_task.py` | 6 | `schema.migrate` |
| `validate_task.validate_submission` | `validate_task.py` | 3 | `cadoc.validate` |

`[inferido]` Três delas são as **únicas** tasks do seu módulo — `import_task`, `validate_task` e
o módulo de migração de schema existem, têm rota manual dedicada em `worker/app.py`, e nunca são
chamados. `validate_task.validate_submission` é a única consumidora da fila `cadoc.validate`.

---

## 4. Duplicação entre motores

Tabelas completas: **[data/motores.md](data/motores.md)** (`data/motores.json`), gerado por
[`scripts/motores.py`](scripts/motores.py).

Método: `difflib.SequenceMatcher` sobre o corpo de cada função de topo, normalizado (docstring e
comentários removidos, literais `3040|3044|3050|3026|cosif` → `N`, espaço colapsado). Corpos com
< 120 caracteres normalizados são descartados. Pares reportados: similaridade > 70% entre motores
**diferentes**. 140 funções de topo analisadas em 10 arquivos.

### % de linhas com equivalente em outro motor

| informe | funções | linhas | funções com par | linhas com par | **% linhas** |
|---|---:|---:|---:|---:|---:|
| 3026 | 18 | 481 | 6 | 129 | **27%** |
| 3050 | 23 | 759 | 7 | 171 | **23%** |
| 3044 | 39 | 1.472 | 5 | 223 | **15%** |
| 3040 | 52 | 2.484 | 4 | 141 | **6%** |
| cosif | 8 | 251 | 0 | 0 | **0%** |

**Isto contradiz a premissa escrita no código.** [backend/engine/base.py:2-4](../backend/engine/base.py#L2-L4)
afirma "a MESMA silhueta ... e ~900 linhas duplicadas por CADOC". A medida diz que a duplicação
textual é de 129–223 linhas por motor, concentrada nos motores **menores**, e que o 3040 — o
maior — é o **menos** duplicado (6%). `[inferido]` A silhueta é a mesma; os corpos divergiram.

### Os 14 pares similares

Os 3 mais fortes são rota HTTP, não núcleo de processamento:

| sim. | A | B |
|---:|---|---|
| 99% | `3050::_fontes_3050` (7 l.) | `3026::_fontes_3026` (7 l.) |
| 97% | `3050::upload_3050` (45 l.) | `3026::upload_3026` (44 l.) |
| 96% | `3050::_validate_week` (6 l.) | `3026::_validate_year` (6 l.) |
| 90% | `3040::download_document` (35 l.) | `3044::download_document` (40 l.) |
| 87% | `3040::_ingest_3040` (64 l.) | `3044::_ingest_3044` (55 l.) |
| 86% | `3040::_maybe_autoconsolidate_3040` (28 l.) | `3044::_maybe_autoconsolidate` (30 l.) |
| 80% | `3050::consolidate_3050` (34 l.) | `3026::consolidate_3026` (31 l.) |
| 76% | `3040::_tem_dados_para_consolidar_3040` | `3044::_tem_dados_para_consolidar_3044` |
| 74–70% | `_ingest_*` (3040×3050, 3044×3050), `upload_3044`×(3050, 3026), `download_document` (3050×3026) | |

`[inferido]` O que de fato se repete: **upload**, **download**, **_ingest** e a thin task
`consolidate_*`. `_ingest_*` aparece em 3 pares — é a função mais replicada do repo.

### Etapa do pipeline × informe

Todas as etapas existentes são **cópia**; nenhuma executa pela base:

| etapa | 3040 | 3044 | 3050 | 3026 | cosif |
|---|---|---|---|---|---|
| `process_file` | copiado (270 l.) | copiado (210 l.) | copiado (106 l.) | copiado (76 l.) | copiado (28 l.) |
| `consolidate` | copiado (223 l.) | copiado (377 l.) | copiado (226 l.) | copiado (162 l.) | **não existe** |
| `sftp_watch` | copiado (93 l.) | copiado (92 l.) | copiado (43 l.) | não existe | não existe |
| `alert_prazo` | copiado (67 l.) | copiado (75 l.) | copiado (57 l.) | copiado (38 l.) | não existe |
| `regenerate/retificação` | não existe | copiado (35 l.) | não existe | não existe | não existe |

### `CadocEngine` — o achado central

`backend/engine/base.py` (160 l.) define `CadocEngine`, `EngineRegistry`, `EngineSteps` e os
passos `process_file`, `consolidate`, `sftp_watch`, `alert_prazo`, mais `queue_for` / `dispatch`.

| informe | bundle | passos declarados | **`dispatch()` em runtime** |
|---|---|---|---|
| 3040 | `backend/engine/cadoc3040.py` (77 l.) | consolidate, process_file, sftp_watch | **não** |
| 3044 | `backend/engine/cadoc3044.py` (80 l.) | consolidate, process_file, sftp_watch | **não** |
| 3050 | `backend/engine/cadoc3050.py` (79 l.) | consolidate, process_file, sftp_watch | **não** |
| 3026 | `backend/engine/cadoc3026.py` (71 l.) | consolidate, process_file | **sim** — `engine3026_tasks.py:171,334` |
| cosif | `backend/engine/cosif.py` (70 l.) | process_file | **não** |

**Os 5 informes têm bundle e os 5 têm rota derivada da spec. Só o 3026 executa pela base.** Para
os outros 4, o `CadocEngine` hoje entrega **roteamento de fila derivado**, não execução: os
bundles delegam de volta às funções `_run_*` das tasks legadas (ver a docstring de
[cadoc3040.py:1-20](../backend/engine/cadoc3040.py#L1-L20), que declara isso explicitamente —
"sem tocar nas tasks Celery reais que rodam em produção").

`[explícito]` Passos ausentes são `NotImplementedError` (1 por bundle), nunca no-op — decisão
documentada. `alert_prazo` não está em nenhum bundle: os 4 beats de prazo apontam direto para a
task.

---

## 4b. Anatomia dos plugins e do `quality`

### Plugins

Tabela por símbolo: **[data/plugins.md](data/plugins.md)**, gerado por
[`scripts/plugins.py`](scripts/plugins.py). 148 símbolos de topo classificados por heurística de
nome `[inferido]`.

| plugin | arquivos | símbolos | linhas | papéis |
|---|---:|---:|---:|---|
| `cadoc_3040` | 13 | 56 | 1.219 | regra 21, gerador 18, validação ext. 8, outro 7, parser 2 |
| `cadoc_3044` | 10 | 47 | 966 | regra 23, **parser 15**, validação ext. 7, outro 2 |
| `cadoc_3050` | 7 | 31 | 759 | parser 11, regra 10, gerador 6, validação ext. 3 |
| `cadoc_3026` | 5 | 6 | 242 | gerador 2, regra 2, validação ext. 1, outro 1 |
| `cadoc_cosif` | 4 | 8 | 138 | parser 3, validação ext. 3, gerador 1, outro 1 |

Perfis distintos `[inferido]`: o **3040 é pesado em geração** (18 símbolos de gerador — inclui o
3042/substituição parcial e o validador XSD próprio); o **3044 é pesado em parsing** (15 —
posicional, portabilidade, layouts); o **3026 é quase só seleção + geração** (6 símbolos no total).

**Candidatos a genérico: apenas 4 pares.** Os plugins são genuinamente divergentes.

| sim. | A | B | papel |
|---:|---|---|---|
| **100%** | `cadoc_3040::validate_3040_xml` | `cadoc_3050::validate_3050_xml` | validação externa |
| 86% | `cadoc_3040::validate_3040_xml` | `cadoc_cosif::validate_cosif_leiaute` | validação externa |
| 86% | `cadoc_3050::validate_3050_xml` | `cadoc_cosif::validate_cosif_leiaute` | validação externa |
| 68% | `cadoc_3040::validate_field` | `cadoc_3044::validate_event` | outro |

`[inferido]` O wrapper de validação XSD é **idêntico** entre 3040 e 3050 e quase idêntico no
COSIF — é a única função de plugin trivialmente promovível a genérica hoje. Símbolos com o mesmo
nome em 2+ plugins: só 4, todos helpers privados (`_dec`, `_err`, `_schema`, `_to_dec`).

### `backend/quality` — as 12 dimensões RC 18

Tabela completa: **[data/quality.md](data/quality.md)**, gerado por
[`scripts/quality.py`](scripts/quality.py).

| dimensão | peso | natureza | avaliador | parâmetros de entrada |
|---|---:|---|---|---|
| `acuracia` | 15 | medida | `evaluate_accuracy` | `business_errors`, `schema_errors`, `total_records` |
| `completude` | 12 | medida | `evaluate_completeness` | `filled_fields`, `filled_required`, `required_fields`, `total_fields` |
| `consistencia` | 12 | medida | `evaluate_consistency` | `cross_validation_errors`, `period_comparison_errors`, `total_checks` |
| `tempestividade` | 12 | medida | `evaluate_timeliness` | `deadline`, `submitted_at`, `pts_por_dia` |
| `rastreabilidade` | 10 | medida | `evaluate_traceability` | `has_lineage`, `lineage_coverage` |
| `integridade` | 10 | **binária** | `evaluate_integrity` | `file_hash_valid`, `truncation_detected` |
| `confiabilidade` | 8 | medida | `evaluate_reliability` | `rejections`, `resubmissions`, `total_submissions` |
| `comparabilidade` | 5 | medida | `evaluate_comparability` | `current_records`, `previous_period_records`, `faixa_pct` |
| `clareza` | 5 | medida | `evaluate_clarity` | `dictionary_coverage` |
| `acessibilidade` | 4 | **derivada** | `evaluate_accessibility` | `api_available`, `export_formats` |
| `adaptabilidade` | 4 | **derivada** | `evaluate_adaptability` | `normative_changes_handled`, `schema_version_current`, `total_changes` |
| `relevancia` | 3 | medida | `evaluate_relevance` | `required_fields_sent`, `total_required` |

**As 12 dimensões operam sobre dado tabular genérico** `[explícito]`: `dimensions.py` (415 l.) é o
maior módulo do pacote, tem **zero** import de `flows`/`plugins`/`api`/`worker` e **zero** literal
de informe. Todas recebem números escalares. `scorer.py` (43 l.) idem. `[explícito]` Os pesos são
fonte única (`DIMENSION_WEIGHTS`, soma 100) e o seed SQL deriva dela.

O acoplamento a informe **não está nas dimensões — está na montagem do contexto**:
**18 de 34 módulos** do pacote são acoplados.

| onde | como |
|---|---|
| `context/builder_3040.py` (170 l.), `context/builder_3044.py` (158 l.) | um builder **por informe**, cada um com 7 literais do seu número e 4 imports de `backend.api.deps` |
| `dictionary.py` | importa `plugins.cadoc_3040.schema` e `plugins.cadoc_3044.schema` |
| `reconciliation_service.py` (299 l.) | `CADOC_FIELDS` hardcoded para 3040/3044; importa `plugins.cadoc_3050.equivalencia` e `plugins.cadoc_3026.engine.selector` |
| `correlations/catalog.py` | literais `"3040"`×4, `"3050"`, `"3026"` |
| `capabilities.py`, `consistency.py`, `deadlines.py`, `report_service.py`, `validation_levels.py` | pares `"3040"`/`"3044"` hardcoded |

**Não existe builder de contexto para 3050, 3026 nem COSIF** — só 3040 e 3044 têm.
`[inferido]` Um informe novo não ganha score RC 18 sem escrever um `builder_<informe>.py`.

### Os 25 imports de saída do pacote `quality`

| destino | n | os mais relevantes |
|---|---:|---|
| `backend.api` | **10** | `api.deps.get_*_store` — os builders e `submissions.py`/`seeding.py` puxam DI da camada HTTP |
| `backend.flows` | 6 | `periods`, `cadoc_registry`, `data_contract`, `dossie`, `onboarding_readiness`, `calendario_bancario` |
| `backend.plugins` | 4 | `cadoc_3040.schema`, `cadoc_3044.schema`, `cadoc_3050.equivalencia`, `cadoc_3026.engine.selector` |
| `backend.storage` | 2 | `postgres.get_connection` (em `deadlines.py`), `DocumentHashStore` |
| `contabil_transforms`, `services`, `worker` | 1 cada | `registry`, `tenant_features`, `quality_task.assess_quality` |

`[inferido]` Os 10 imports de `backend.api.deps` são a causa do ciclo `quality ↔ api` reportado no
Discovery 1. O motivo aparente é **reuso do container de DI**: os builders precisam de stores e o
único lugar onde eles são montados é `api/deps.py`.

### Batimento / conciliação

**46 arquivos** de `backend/` mencionam `concilia|batimento|cruza|reconcil|amarraç`. Dois
mecanismos distintos coexistem `[explícito]`:

**a) Conciliação origem × contábil (por informe)** — `quality/reconciliation_service.py` +
`reconciliation.py` + `api/routes/reconciliation.py` (287 l., 53 ocorrências, o arquivo mais
denso). Compara a soma do movimento do CADOC contra o balancete contábil, agregando por
categoria. Os campos são hardcoded para 2 informes:
`3040 → (codigo_modalidade, valor_contabil)`, `3044 → (carteira, saldo_devedor)`.

**b) Correlação entre informes** — `quality/correlations/catalog.py`, catálogo **declarativo**
com 9 regras, das quais **3 ativas** e **6 desligadas** (`enabled=False`, esqueletos):

| código | o que compara | estado |
|---|---|---|
| `3040x4010` | SCR × Balancete COSIF, por modalidade, tolerância 5% | ativa |
| `3050x3040` | Agregado semanal × detalhe mensal | ativa |
| `3026x3040` | Conglomerado anual × exposição SCR | ativa |
| `CASCATA-COSIF` | cascata dentro do COSIF | ativa |
| `J1`, `H3`, `H4` | (esqueletos, Bloco C) | desligada |
| `DLOxCOSIF`, `DLOxSCR` | DLO 2061 × COSIF / × SCR (contraparte LEC) | desligada |

`[explícito]` Este é o único subsistema do repo desenhado para crescer por dado e não por código:
"o catálogo cresce sem alterar o motor" (docstring). O evaluator e o adapter são resolvidos por
nome via registry (`engine.py`, `adapters.py`, `evaluators.py`).

---

## 5. Volume e dado massivo

Medições do banco: **[data/volume.md](data/volume.md)**, gerado por
[`scripts/volume.py`](scripts/volume.py) (somente `SELECT` e catálogo).

### Banco local de dev — praticamente vazio

2 schemas de tenant, 73 tabelas cada.

| schema | tamanho total | maiores tabelas (count) |
|---|---:|---|
| `tenant_1111...5555` | 3.536 KB | `cadoc3040_mov_operacoes` 120 · `quality_scores` 204 · `audit_events` 82 · `reports` 17 · `cadoc3044_mov_linhas` 10 |
| `tenant_main` | 2.128 KB | todas com 0 linhas exceto `reporting_units` (1) |

**`raw_data` = 0 linhas e `account_entries` = 0 linhas nos dois schemas.**

### QAS: **sem acesso** `[explícito]`

O Postgres do QAS é RDS em VPC privada e nunca foi exposto (registrado no `CLAUDE.md`); não há
credencial nem túnel neste ambiente. **A volumetria de produção não foi medida.**

### Onde o dado bruto entra e sai do Postgres

`[inferido]` **A tabela `raw_data` é efetivamente morta.** Ela existe na baseline de tenant, mas a
única referência em todo o `backend/` é um `SELECT COUNT(*)`
([backend/storage/admin_store.py:231](../backend/storage/admin_store.py#L231)). Não há
`INSERT INTO raw_data` em lugar nenhum. `account_entries` também só aparece em 2 arquivos
(`flows/cadoc_registry.py` e `storage/cosif_store.py`).

O landing real é **uma tabela `mov` por informe**, e o mecanismo **não é uniforme**:

| store | mecanismo | lote |
|---|---|---:|
| `mov3040_store.py` (608 l.) | **`COPY ... FROM STDIN`** via `cur.copy(sql)` (l. 56–61) | streaming |
| `mov3044_store.py` (313 l.) | `cur.executemany` em lotes | 10.000 |
| `mov3050_store.py` (199 l.) | `cur.executemany` em lotes | 10.000 |
| `mov3026_store.py` (187 l.) | `cur.executemany` em lotes | 10.000 |
| `pecld_result_store.py` | `cur.executemany` em lotes | — |

**Só o 3040 usa `COPY`.** Leitura para processamento: 27 `SELECT` em `mov3040_store`, 16 em
`mov3044_store`, 4 em `mov3050_store` e 4 em `mov3026_store`.

Fora do Postgres, `backend/processing/` usa DuckDB com `COPY (...) TO ... (FORMAT PARQUET)`
(`duckdb_stage.py:68`, `ingest_3026.py:160`, `cadoc3026_consolidation.py:85`) — declarado como
"sem carregar tudo em memória". `[inferido]` É o único caminho projetado para volume, e serve
apenas ao 3026.

### Tamanho de entrada

| evidência | valor |
|---|---|
| Limite de upload nas rotas (3040, 3044, 3050, 3026, COSIF) | **100 MB** (`MAX_UPLOAD_BYTES`, HTTP 413) |
| Preview de layout em `data_sources` | 2 MB |
| Como o upload é lido | **`content = await file.read()`** — arquivo inteiro em memória, nas 6 rotas de upload |
| Fixtures versionadas (única amostra no repo) | 23.400 B / 120 linhas (`cadoc3040.txt`); as demais < 2 KB |
| Volumetria real citada no código | "**2,9–4,4 GB** no 3040 com **500 mil operações**" ([worker/app.py:35](../backend/worker/app.py#L35)) |

`[inferido]` Contradição estrutural: o CLAUDE.md diz que "arquivos de cliente chegam na casa das
centenas de MB" e que "solução que só fecha carregando tudo em memória está errada por
construção"; as 6 rotas de upload fazem exatamente isso, com teto de 100 MB.

---

## 6. Resumo para decisão

Tabela gerada por [`scripts/resumo.py`](scripts/resumo.py) →
**[data/resumo-informes.md](data/resumo-informes.md)**. Sem recomendação — só o número.

| informe | páginas | endpoints | tasks | l. motor (task+rota) | l. plugin | % linhas copiadas de outro motor | builder RC 18 | bundle `CadocEngine` | `dispatch()` runtime | volume médio de entrada | último feat no próprio código |
|---|---:|---:|---:|---:|---:|---:|:-:|:-:|:-:|---|---|
| **3040** | 3 | 15 | 4 | **2.870** | 1.743 | **6%** | sim | sim | **não** | 100 MB teto; 2,9–4,4 GB de pico com 500 k operações | `556565f` 2026-09-04 `feat(3040): filtros de retificação e ano` |
| **3044** | 2 | 9 | 6 | 1.744 | 1.382 | 15% | sim | sim | **não** | 100 MB teto; sem medição registrada | `24beaec` 2026-09-04 `feat(ciclo): fim do ponteiro de competência` |
| **3050** | 1 | 7 | 4 | 967 | **1.901** | 23% | **não** | sim | **não** | 100 MB teto; sem medição | `e2d2529` 2026-09-01 `feat(REP-77): e-mails` |
| **3026** | 1 | 7 | 3 | 643 | 404 | **27%** | **não** | sim | **sim** | 100 MB teto; único com pipeline DuckDB/Parquet | `e2d2529` 2026-09-01 `feat(REP-77): e-mails` |
| **cosif** | 2 | 9 | 1 | 436 | 199 | 0% | **não** | sim | **não** | 100 MB teto | `6538625` 2026-08-13 `feat(model): rename tabelas regulatórias` |

Notas de leitura:

- **páginas** = rotas `frontend/app/**` cujo caminho cita o informe. 3040: `/cadoc-3040`,
  `/cadoc-3040/[reference_period]`, `/cadoc-3040/[reference_period]/retificacao`. COSIF:
  `/cadoc-cosif` e `/admin/cosif-plano`.
- **endpoints** = operações cujo módulo de rota ou path cita o informe (inclui
  `cosif_plano.py` na linha do COSIF).
- **% copiadas** mede similaridade **textual** entre motores (§4), não silhueta. A silhueta é
  idêntica nos 5 (§4, tabela de etapas).
- **`dispatch()` runtime** é a única coluna que separa "migrado" de "roteado": 4 dos 5 bundles
  delegam de volta às funções `_run_*` das tasks legadas.
- **último feat** foi apurado com `git log --grep='^feat'` escopado aos diretórios do próprio
  motor (`worker/tasks/*<informe>*`, `api/routes/*<informe>*`, `plugins/*<informe>*`,
  `engine/*<informe>*`). Para 3050 e 3026 o commit mais recente é o REP-77 (e-mails), que tocou
  as tasks de alerta — não é ruído de nome, é a mudança real mais recente nesses motores.
- **volume médio de entrada por informe: não determinável.** Não há amostra de arquivo de cliente
  no repo, nem acesso ao bucket, nem ao QAS (§5). O que existe é o teto de 100 MB, comum aos
  cinco, e uma única medição de pico registrada em comentário, para o 3040.

### Contadores auxiliares

| | 3040 | 3044 | 3050 | 3026 | cosif |
|---|---:|---:|---:|---:|---:|
| entradas no `beat` | 2 | 3 | 2 | 1 | 0 |
| etapas do pipeline implementadas | 4 | 5 | 4 | 3 | 1 |
| passos declarados no bundle | 3 | 3 | 3 | 2 | 1 |
| regras de correlação ativas que o citam | 3 | 0 | 1 | 1 | 2 |
| plugin: símbolos de topo | 56 | 47 | 31 | 6 | 8 |
