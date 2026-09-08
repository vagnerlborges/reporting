# `backend/quality` - dimensoes RC18, acoplamento e saidas

Gerado por `discovery/scripts/quality.py`.

## As 12 dimensoes

| dimensao | peso | natureza | avaliador(es) | l. | parametros de entrada |
|---|---:|---|---|---:|---|
| `acuracia` | 15 | medida | `evaluate_accuracy` | 20 | `business_errors`, `schema_errors`, `total_records` |
| `completude` | 12 | medida | `evaluate_completeness` | 21 | `filled_fields`, `filled_required`, `required_fields`, `total_fields` |
| `consistencia` | 12 | medida | `evaluate_consistency` | 18 | `cross_validation_errors`, `period_comparison_errors`, `total_checks` |
| `confiabilidade` | 8 | medida | `evaluate_reliability` | 18 | `rejections`, `resubmissions`, `total_submissions` |
| `integridade` | 10 | binaria | `evaluate_integrity` | 14 | `file_hash_valid`, `truncation_detected` |
| `rastreabilidade` | 10 | medida | `evaluate_traceability` | 17 | `has_lineage`, `lineage_coverage` |
| `tempestividade` | 12 | medida | `evaluate_timeliness` | 23 | `deadline`, `pts_por_dia`, `submitted_at` |
| `acessibilidade` | 4 | derivada | `evaluate_accessibility` | 18 | `api_available`, `export_formats` |
| `adaptabilidade` | 4 | derivada | `evaluate_adaptability` | 21 | `normative_changes_handled`, `schema_version_current`, `total_changes` |
| `clareza` | 5 | medida | `evaluate_clarity` | 8 | `dictionary_coverage` |
| `comparabilidade` | 5 | medida | `evaluate_comparability` | 27 | `current_records`, `faixa_pct`, `previous_period_records` |
| `relevancia` | 3 | medida | `evaluate_relevance` | 15 | `required_fields_sent`, `total_required` |

## Acoplamento a informe por modulo (18 de 34 acoplados)

Sinal = import de `flows`/`plugins`/`api`/`worker`/`cadoc_adapters` ou literal de informe.

| modulo | l. | acoplado | sinais |
|---|---:|:-:|---|
| `capabilities.py` | 27 | SIM | `"3040"`x2, `"3044"`x2 |
| `consistency.py` | 96 | SIM | `"3040"`x1, `"3044"`x1 |
| `context/builder_3040.py` | 170 | SIM | `"3040"`x7, `backend.api`x4 |
| `context/builder_3044.py` | 158 | SIM | `"3044"`x7, `backend.api`x4 |
| `correlations/adapters.py` | 122 | SIM | `backend.flows`x1 |
| `correlations/catalog.py` | 90 | SIM | `"3040"`x4, `"3050"`x1, `"3026"`x1 |
| `correlations/evaluators.py` | 120 | SIM | `"3040"`x2 |
| `data_contract_service.py` | 37 | SIM | `backend.flows`x2, `cadoc_registry`x1 |
| `deadlines.py` | 70 | SIM | `"3040"`x1, `"3044"`x1 |
| `dictionary.py` | 74 | SIM | `"3040"`x4, `backend.plugins`x2, `"3044"`x2, `cadoc_3040`x1, `cadoc_3044`x1, `'3040'`x1 |
| `dossie_service.py` | 114 | SIM | `backend.flows`x1, `cadoc_arquivados`x1 |
| `onboarding_service.py` | 19 | SIM | `backend.flows`x1 |
| `reconciliation.py` | 198 | SIM | `cadoc_by_cat`x3 |
| `reconciliation_service.py` | 299 | SIM | `cadoc_rows`x5, `"3040"`x4, `"3044"`x2, `backend.plugins`x2, `cadoc_3050`x1, `cadoc_3026`x1 |
| `report_service.py` | 76 | SIM | `"3040"`x1, `"3044"`x1 |
| `seeding.py` | 71 | SIM | `backend.api`x1, `cadoc_types`x1, `backend.flows`x1, `"3040"`x1 |
| `submissions.py` | 50 | SIM | `backend.api`x1, `backend.worker`x1 |
| `validation_levels.py` | 28 | SIM | `"3040"`x1, `"3044"`x1 |
| `alerts.py` | 98 | nao | - |
| `contabil/rollup.py` | 41 | nao | - |
| `context/base.py` | 13 | nao | - |
| `context/registry.py` | 45 | nao | - |
| `correlations/annotations.py` | 20 | nao | - |
| `correlations/classify.py` | 16 | nao | - |
| `correlations/engine.py` | 66 | nao | - |
| `cosif_amarracoes.py` | 73 | nao | - |
| `coverage.py` | 11 | nao | - |
| `data_contract_report.py` | 57 | nao | - |
| `dimensions.py` | 415 | nao | - |
| `lineage.py` | 60 | nao | - |
| `pdf_hash.py` | 74 | nao | - |
| `periods.py` | 17 | nao | - |
| `report.py` | 414 | nao | - |
| `scorer.py` | 43 | nao | - |

## Imports de saida do pacote (25)

| de | para | importa |
|---|---|---|
| `context/builder_3040.py` | `backend.api.deps` | `get_document3040_store` |
| `context/builder_3040.py` | `backend.api.deps` | `get_mov3040_store` |
| `context/builder_3040.py` | `backend.api.deps` | `get_quality_store` |
| `context/builder_3040.py` | `backend.api.deps` | `get_submission_store` |
| `context/builder_3044.py` | `backend.api.deps` | `get_document_store` |
| `context/builder_3044.py` | `backend.api.deps` | `get_mov3044_store` |
| `context/builder_3044.py` | `backend.api.deps` | `get_quality_store` |
| `context/builder_3044.py` | `backend.api.deps` | `get_submission_store` |
| `seeding.py` | `backend.api.deps` | `get_quality_store` |
| `submissions.py` | `backend.api.deps` | `get_submission_store` |
| `reconciliation_service.py` | `backend.contabil_transforms` | `registry` |
| `correlations/adapters.py` | `backend.flows.periods` | `business_days_of_month, weeks_of_month` |
| `data_contract_service.py` | `backend.flows.cadoc_registry` | `get_flow_spec` |
| `data_contract_service.py` | `backend.flows.data_contract` | `catalogo_canonico, montar_contrato` |
| `dossie_service.py` | `backend.flows.dossie` | `intervalo_de, montar_manifesto, montar_zip` |
| `onboarding_service.py` | `backend.flows.onboarding_readiness` | `overview_item` |
| `seeding.py` | `backend.flows.calendario_bancario` | `add_dias_uteis` |
| `dictionary.py` | `backend.plugins.cadoc_3040.schema` | `(` |
| `dictionary.py` | `backend.plugins.cadoc_3044.schema` | `EVENT_FIELDS` |
| `reconciliation_service.py` | `backend.plugins.cadoc_3050.equivalencia` | `codigos_3040_para_modalidade` |
| `reconciliation_service.py` | `backend.plugins.cadoc_3026.engine` | `selector` |
| `submissions.py` | `backend.services.tenant_features` | `tenant_features` |
| `deadlines.py` | `backend.storage.postgres` | `get_connection` |
| `pdf_hash.py` | `backend.storage.document_hash_store` | `DocumentHashStore` |
| `submissions.py` | `backend.worker.tasks.quality_task` | `assess_quality` |

Por pacote destino: `api` 10, `flows` 6, `plugins` 4, `storage` 2, `contabil_transforms` 1, `services` 1, `worker` 1

## Batimento / conciliacao no backend (46 arquivos)

| arquivo | ocorrencias | l. |
|---|---:|---:|
| `backend/api/routes/reconciliation.py` | 53 | 287 |
| `backend/flows/resolvers.py` | 44 | 201 |
| `backend/quality/reconciliation_service.py` | 23 | 299 |
| `backend/demo/blocks/communication.py` | 21 | 114 |
| `backend/api/routes/painel.py` | 20 | 956 |
| `backend/quality/correlations/evaluators.py` | 20 | 120 |
| `backend/storage/reconciliation_store.py` | 20 | 131 |
| `backend/worker/tasks/engine3026_tasks.py` | 17 | 391 |
| `backend/flows/data_adapter.py` | 15 | 190 |
| `backend/api/routes/engine3040.py` | 13 | 1421 |
| `backend/api/deps.py` | 12 | 423 |
| `backend/flows/cadoc_registry.py` | 9 | 176 |
| `backend/worker/tasks/engine3040_tasks.py` | 9 | 1449 |
| `backend/api/routes/engine3026.py` | 8 | 252 |
| `backend/api/routes/engine3050.py` | 8 | 278 |
| `backend/worker/tasks/engine3044_tasks.py` | 8 | 1314 |
| `backend/quality/correlations/classify.py` | 7 | 16 |
| `backend/quality/data_contract_service.py` | 5 | 37 |
| `backend/quality/reconciliation.py` | 5 | 198 |
| `backend/api/routes/pecld.py` | 4 | 94 |
| `backend/demo/blocks/sources.py` | 4 | 215 |
| `backend/plugins/cadoc_3050/equivalencia.py` | 4 | 890 |
| `backend/quality/cosif_amarracoes.py` | 4 | 73 |
| `backend/storage/mov3040_store.py` | 4 | 608 |
| `backend/quality/correlations/adapters.py` | 3 | 122 |
