# Acoplamento por mudanca (top 25 pares, 6 meses, commits <=25 arquivos)

| juntos | % do menor | arquivo A | arquivo B |
|---:|---:|---|---|
| 13 | 59% | `dattos_informes/api/routes/painel.py` | `tests/api/test_painel.py` |
| 13 | 72% | `web/components/flow-card.tsx` | `web/lib/types/painel.ts` |
| 12 | 50% | `backend/api/routes/engine3040.py` | `frontend/app/(dashboard)/cadoc-3040/[reference_period]/page.tsx` |
| 12 | 34% | `dattos_informes/worker/tasks/engine3040_tasks.py` | `dattos_informes/worker/tasks/engine3044_tasks.py` |
| 11 | 33% | `backend/api/routes/engine3040.py` | `frontend/app/(dashboard)/cadoc-3040/page.tsx` |
| 11 | 85% | `e2e/tests/44-listagem-3040.spec.ts` | `frontend/app/(dashboard)/cadoc-3040/page.tsx` |
| 11 | 100% | `dattos_informes/flows/periods.py` | `tests/flows/test_periods.py` |
| 11 | 92% | `dattos_informes/worker/tasks/engine3044_tasks.py` | `tests/worker/test_engine3044_consolidate.py` |
| 11 | 92% | `dattos_informes/flows/resolvers.py` | `tests/flows/test_resolvers.py` |
| 9 | 38% | `frontend/app/(dashboard)/cadoc-3040/[reference_period]/page.tsx` | `frontend/app/(dashboard)/cadoc-3040/page.tsx` |
| 9 | 75% | `frontend/app/(dashboard)/cadoc-3040/[reference_period]/page.tsx` | `frontend/components/cadoc-3040/SecaoFontes.tsx` |
| 9 | 75% | `backend/worker/tasks/ops_task.py` | `tests/worker/test_sftp_watch_s3.py` |
| 9 | 22% | `dattos_informes/api/deps.py` | `dattos_informes/storage/postgres.py` |
| 8 | 80% | `backend/services/sftp_inbox.py` | `tests/worker/test_sftp_watch_s3.py` |
| 8 | 100% | `frontend/app/admin/operations/page.tsx` | `frontend/app/admin/tenants/[id]/page.tsx` |
| 8 | 80% | `dattos_informes/api/routes/painel.py` | `dattos_informes/flows/painel_service.py` |
| 7 | 100% | `backend/services/sftp_inbox.py` | `tests/services/test_sftp_inbox.py` |
| 7 | 78% | `backend/storage/s3.py` | `tests/worker/test_sftp_watch_s3.py` |
| 7 | 37% | `dattos_informes/api/routes/engine3040.py` | `dattos_informes/api/routes/engine3044.py` |
| 7 | 88% | `dattos_informes/plugins/cadoc_3044/engine/validator_client.py` | `deploy/cadoc-validator/wrapper.py` |
| 7 | 100% | `deploy/cadoc-validator/wrapper.py` | `tests/deploy/test_validator_wrapper.py` |
| 7 | 39% | `dattos_informes/api/routes/painel.py` | `web/lib/types/painel.ts` |
| 7 | 33% | `dattos_informes/api/routes/painel.py` | `web/components/flow-card.tsx` |
| 6 | 75% | `frontend/components/cadoc-3040/SecaoFontes.tsx` | `frontend/components/cadoc-3040/types.ts` |
| 6 | 33% | `backend/api/routes/engine3040.py` | `backend/worker/tasks/engine3040_tasks.py` |

# Retrabalho: commits fix/corrige <=2 dias apos feat no mesmo arquivo

Total: **238** commits (de 325 commits fix/corrige nos 6 meses).

- `bac179a7` fix(REP-83): seeder recupera admin ausente sem abortar o seeding
  - corrige: feat(demo-seeder): perfis de obrigacao (gate REP-65) e usuario admin condicional  (`backend/demo/blocks/users.py`)
- `822c4d7b` fix(REP-83): derivaÃ§Ã£o da competÃªncia e do code falham alto em vez de degradar
  - corrige: feat(demo): bloco de documentos com funil por motor e criticas do validador  (`backend/demo/blocks/documents.py`)
- `b7746999` fix(3040): listagem sem os badges "Em andamento" e "Prazo vencido"
  - corrige: feat(3040): quick wins â€” filtro de ano, badge prazo vencido, tooltip do ciclo, autoria v  (`docs/superpowers/specs/2026-09-02-ciclo-competencias-fisicas-design.md`)
- `20bd3a3b` fix(REP-83): demo seeder derives 3050 reference_period from its weekly cadence
  - corrige: feat(demo): bloco de documentos com funil por motor e criticas do validador  (`backend/demo/blocks/documents.py`)
- `5c5038ca` fix(REP-83): demo seeder uses the catalog's real deadline_rule per engine
  - corrige: feat(demo-seeder): perfis de obrigacao (gate REP-65) e usuario admin condicional  (`backend/demo/blocks/obligations.py`)
- `af4ed100` fix(REP-83): demo seeder rebuild no longer deletes the admin without recreating it
  - corrige: feat(demo-seeder): perfis de obrigacao (gate REP-65) e usuario admin condicional  (`backend/demo/blocks/users.py`)
- `bc82fa99` fix(demo-seeder): fontes cobrem os quatro motores, nao so o 3044
  - corrige: feat(demo): bloco de fontes de dados com importacoes concluidas  (`backend/demo/blocks/sources.py`)
- `3c5fbc01` fix(demo): conciliacao do seeder usa kind e periodo do vocabulario do produto
  - corrige: feat(demo): bloco de comunicacao BCB e conciliacao  (`backend/demo/blocks/communication.py`)
- `da9e521a` fix(demo): 3044 usa data cheia na competencia, nao o mes cru (GET /api/painel 500ava)
  - corrige: feat(demo): bloco de calendario com historico concluido e competencia corrente  (`backend/demo/blocks/calendar.py`)
- `7b6fbb33` fix(3040): tour nÃ£o destaca mais o slot vazio do indicador de retificaÃ§Ã£o
  - corrige: feat(cadoc-3040): listagem sem abas, indicador de retificacao e Tooltip global  (`frontend/app/(dashboard)/cadoc-3040/page.tsx`)
- `da51f031` fix(3040): troca de filtro em voo nÃ£o Ã© mais engolida; falha de load-more nÃ£o apaga a t
  - corrige: feat(cadoc-3040): listagem sem abas, indicador de retificacao e Tooltip global  (`frontend/app/(dashboard)/cadoc-3040/page.tsx`)
- `92ead0c2` fix(front): topbar alinhado por construÃ§Ã£o â€” caixas de 32px nos trÃªs controles, disco
  - corrige: feat(3040): quick wins â€” filtro de ano, badge prazo vencido, tooltip do ciclo, autoria v  (`frontend/components/topbar.tsx`)
- `c2e52b69` fix(front): avatar do topbar no tamanho dos Ã­cones vizinhos (22px)
  - corrige: feat(3040): quick wins â€” filtro de ano, badge prazo vencido, tooltip do ciclo, autoria v  (`frontend/components/topbar.tsx`)
- `ab3da42c` fix(demo): falha alto em cadence sem flow spec e corrige docstring do reset
  - corrige: feat(demo-seeder): perfis de obrigacao (gate REP-65) e usuario admin condicional  (`backend/demo/blocks/obligations.py`)
- `e2355b4b` fix(REP-80): corrige os 8 achados do review desta PR
  - corrige: feat(REP-80): acoes por situacao, cards que filtram e aviso de schema em impersonate  (`backend/api/routes/schema_versions.py`)
- `65e1aeaf` fix(local): bucket de backup segue o nome do produto, nao o legado
  - corrige: feat(REP-77): identidade, template HTML, links e consolidacao dos e-mails  (`infra/docker-compose.yml`)
- `c067ea96` fix(REP-80): tabela rola dentro de si, e a referencia abre a lista em cinza
  - corrige: feat(REP-80): acoes por situacao, cards que filtram e aviso de schema em impersonate  (`frontend/app/admin/schema-versions/page.tsx`)
- `3366fc1f` fix(demo): onda final de correcoes da revisao de branch (10 achados)
  - corrige: feat(demo): esqueleto do seeder â€” contexto, perfil e guarda do tenant  (`backend/cli/seed_demo.py`)
- `31d41b72` fix(local): cria o bucket de backups no compose local
  - corrige: feat(REP-77): identidade, template HTML, links e consolidacao dos e-mails  (`infra/docker-compose.yml`)
- `c5a9caa9` fix(REP-79): migracao por tenant nao depende mais de importar migrations_tenant
  - corrige: feat(retificacao): ciclo isolado em carril proprio, sem reabrir a competencia  (`backend/storage/postgres.py`)

# TODO/FIXME/HACK/XXX por modulo

| ocorrencias | modulo |
|---:|---|
| 3 | `e2e/tests` |
| 2 | `backend/flows` |
| 2 | `e2e/seed` |
| 1 | `backend/api` |
| 1 | `backend/cli` |
| 1 | `backend/plugins` |
| 1 | `backend/storage` |
| 1 | `migrations/versions` |
| 1 | `tests/flows` |
| 1 | `tests/storage` |
| 1 | `tests/workflow` |

Total: 15

Exemplos de arquivos: `backend/api/routes/reconciliation.py`, `backend/cli/seed.py`, `backend/flows/obligations.py`, `backend/plugins/cadoc_3050/engine/builder.py`, `backend/storage/contabil_mapping_store.py`, `e2e/seed/seed_regressao.py`, `e2e/tests/26-regressao-3050.spec.ts`, `e2e/tests/31-regressao-qualidade-pilares.spec.ts`, `e2e/tests/41-rep67-operations-ui.spec.ts`, `migrations/versions/20260828_0100_0002_limpa_obrigacoes_fantasma.py`, `tests/flows/test_resolvers.py`, `tests/storage/test_manifestacao_store.py`, `tests/workflow/test_notifications_contract.py`
