# Duplicacao entre motores

Gerado por `discovery/scripts/motores.py`.

Criterio de similaridade: `difflib.SequenceMatcher` sobre o corpo da funcao normalizado (docstring removida, comentarios removidos, literais `3040|3044|3050|3026|cosif` trocados por `N`, espaco colapsado). Corpos com menos de 120 caracteres normalizados sao ignorados (ruido). Pares reportados: ratio > 0.70 entre motores DIFERENTES.

## Funcoes por arquivo


### `backend/worker/tasks/engine3040_tasks.py` (22 funcoes de topo, 1267 linhas)

| tipo | assinatura | l. | melhor par em outro motor |
|---|---|---:|---|
| funcao | `_cnpj_if(cnpj)` | 3 | - |
| funcao | `classificar_linha_3040(rec)` | 16 | - |
| funcao | `filtrar_operacoes_3040(operacoes)` | 8 | - |
| funcao | `pares_com_linha_fisica(adapter, raw, meta)` | 10 | - |
| funcao | `filtrar_operacoes_3040_enumeradas(pares)` | 16 | - |
| funcao | `_build_validate_emit_3040(tenant_id, schema, reference_period, operacoes, tipo_envio, cnpj_if, tenant, stores=, storage=, jobs=, import_job_id=, validator=, trig=, source_ids=, retification_id=)` | 400 | - |
| funcao | `_list_period_jobs_3040(schema, reference_period)` | 37 | - |
| funcao | `find_duplicate_operations(operacoes)` | 9 | - |
| funcao | `_run_consolidate_3040(tenant_id, reference_period, stores=, storage=, jobs=, validator=, forcar=, retification_id=)` | 120 | - |
| task | `consolidate_3040(tenant_id, reference_period, forcar, retification_id)` | 42 | - |
| funcao | `_run_process_3040_file(tenant_id, import_job_id, stores=, storage=, jobs=, validator=, connect=)` | 235 | - |
| funcao | `_fontes_status_3040(schema, reference_period)` | 4 | - |
| funcao | `_maybe_autoconsolidate_3040(tenant_id, import_job_id, result, jobs=)` | 28 | 86% |
| task | `process_3040_file(tenant_id, import_job_id)` | 35 | - |
| funcao | `match_source_3040(filename, sources)` | 5 | - |
| funcao | `prazo_mensal_proximo(hoje, deadline_day, limite_dias)` | 10 | - |
| funcao | `_competencia_concluida_3040(schema, period)` | 20 | - |
| funcao | `_rejeitar_ingestao_concluida(schema, tenant, src, inbox, rel, period, dests)` | 10 | - |
| funcao | `_ingest_3040(schema, tenant, src, inbox, rel, period, dests)` | 64 | 87% |
| task | `sftp_watch_3040()` | 93 | - |
| funcao | `alertas_competencias_vencidas(tenant=, schema=, hoje=, comp_store=, regra=, claim=, enviar=)` | 35 | - |
| task | `alert_prazo_3040()` | 67 | - |

### `backend/api/routes/engine3040.py` (30 funcoes de topo, 1217 linhas)

| tipo | assinatura | l. | melhor par em outro motor |
|---|---|---:|---|
| funcao | `_validate_period(value)` | 12 | - |
| funcao | `_extract_file_data_base(content)` | 17 | - |
| funcao | `fechamento_status(schema, period)` | 17 | - |
| funcao | `_aviso_competencia_concluida(schema, period, acao)` | 17 | - |
| funcao | `_responsavel_da_competencia(registrada, padrao)` | 8 | - |
| funcao | `_dias_uteis_com_sinal(inicio, fim)` | 11 | - |
| funcao | `_nomes_de_usuarios(user_ids)` | 11 | - |
| funcao | `_descricao_regra_prazo(regra)` | 30 | - |
| funcao | `_prazo_regra_payload(regra)` | 4 | - |
| rota | `list_competencias(cursor, limit, ano, situacao, retificacao, user)` | 205 | - |
| rota | `set_responsavel_competencia(req, user)` | 33 | - |
| rota | `dev_forcar_homologacao(req, user)` | 50 | - |
| rota | `historico_competencia(period, user)` | 80 | - |
| rota | `month_status(period, user)` | 158 | - |
| rota | `source_summary(period, source_id, user)` | 12 | - |
| rota | `registros(period, view, q, modalidade, page, page_size, user)` | 34 | - |
| rota | `registros_resumo(period, user)` | 12 | - |
| rota | `registros_export(period, view, user)` | 60 | - |
| rota | `operacao_lookup(period, source_id, numero, user)` | 12 | - |
| rota | `modelo_extrato_3040(user)` | 15 | - |
| rota | `upload_3040(data_source_id, reference_period, file, confirmar, user)` | 127 | - |
| funcao | `_competencia_travada(schema, period)` | 11 | - |
| funcao | `_retificacao_aberta(schema, period)` | 14 | - |
| funcao | `_retificacao_parcial_aberta(schema, period)` | 14 | - |
| funcao | `_bloquear_se_retificacao_parcial(schema, period)` | 24 | - |
| rota | `delete_imports_3040(req, user)` | 91 | - |
| funcao | `_tem_dados_para_consolidar_3040(schema, period)` | 14 | 76% |
| rota | `consolidate_endpoint(req, user)` | 61 | - |
| rota | `download_document(id, kind, user)` | 35 | 90% |
| funcao | `_csv_from_document(schema, doc)` | 28 | - |

### `backend/worker/tasks/engine3044_tasks.py` (28 funcoes de topo, 1126 linhas)

| tipo | assinatura | l. | melhor par em outro motor |
|---|---|---:|---|
| funcao | `_dec_default(o)` | 5 | - |
| funcao | `_dec_number_default(o)` | 7 | - |
| funcao | `_cnpj_if(cnpj)` | 3 | - |
| funcao | `_parse_rows_3044(raw, meta)` | 11 | - |
| funcao | `_build_and_persist_partial(schema, meta, rows, import_job_id, stores=, storage=, jobs=)` | 46 | - |
| funcao | `_run_process_3044_file(tenant_id, import_job_id, stores=, storage=, jobs=, connect=)` | 175 | - |
| funcao | `_run_generate_partial_3044(tenant_id, import_job_id, stores=, storage=, jobs=)` | 31 | - |
| funcao | `_fontes_status_3044(schema, reference_date)` | 5 | - |
| funcao | `_maybe_autoconsolidate(tenant_id, import_job_id, result, jobs=)` | 30 | 86% |
| task | `process_3044_file(tenant_id, import_job_id)` | 35 | - |
| task | `regenerate_partial_3044(tenant_id, import_job_id)` | 35 | - |
| funcao | `_advisory_lock(schema, reference_date)` | 11 | - |
| funcao | `_run_consolidate_3044(tenant_id, reference_date, stores=, storage=, jobs=, validator=, forcar=)` | 302 | - |
| funcao | `_to_date(s)` | 5 | - |
| funcao | `_dec(x)` | 9 | - |
| funcao | `_to_dec_str(x)` | 8 | - |
| funcao | `_datas_ok(data_saldo, remessa)` | 14 | - |
| funcao | `_valores_ok(saldo_devedor)` | 8 | - |
| funcao | `flatten_csv(doc, source_file_name)` | 88 | - |
| funcao | `dias_uteis_ate(d_from, n)` | 5 | - |
| funcao | `is_past_cutoff(now_hm, cutoff)` | 2 | - |
| funcao | `sources_sem_arquivo(sources, received_source_ids, now_hm)` | 12 | - |
| funcao | `docs_proximos_do_prazo(docs, hoje, limite_dias)` | 19 | - |
| task | `alert_fonte_pendente()` | 37 | - |
| task | `alert_prazo_documento()` | 38 | - |
| funcao | `_ingest_3044(schema, tenant, src, inbox, rel, ref, dests)` | 55 | 87% |
| task | `sftp_watch()` | 92 | - |
| task | `consolidate_3044(tenant_id, reference_date, forcar)` | 38 | - |

### `backend/api/routes/engine3044.py` (11 funcoes de topo, 346 linhas)

| tipo | assinatura | l. | melhor par em outro motor |
|---|---|---:|---|
| funcao | `_validate_iso_date(value)` | 9 | - |
| rota | `day_status(date, user)` | 69 | - |
| funcao | `_serialize_line(line)` | 2 | - |
| rota | `list_lines(date, source_id, offset, limit, q, user)` | 23 | - |
| funcao | `_tem_dados_para_consolidar_3044(schema, reference_date)` | 11 | 76% |
| rota | `consolidate(req, user)` | 37 | - |
| rota | `delete_imports(req, user)` | 40 | - |
| rota | `download_document(id, kind, user)` | 40 | 90% |
| rota | `add_exclusions(req, user)` | 23 | - |
| rota | `list_exclusions(user)` | 5 | - |
| rota | `upload_3044(data_source_id, reference_date, file, user)` | 87 | 71% |

### `backend/worker/tasks/engine3050_tasks.py` (14 funcoes de topo, 536 linhas)

| tipo | assinatura | l. | melhor par em outro motor |
|---|---|---:|---|
| funcao | `_cnpj_if(cnpj)` | 3 | - |
| funcao | `_aggregated_to_rows(aggregated, reference_period)` | 20 | - |
| funcao | `_rows_to_aggregated(rows)` | 32 | - |
| funcao | `_run_process_3050_file(tenant_id, import_job_id, stores=, storage=, jobs=, validator=, connect=)` | 77 | - |
| task | `process_3050_file(tenant_id, import_job_id)` | 29 | - |
| funcao | `_contato_tenant(tenant)` | 12 | - |
| funcao | `_run_consolidate_3050(tenant_id, reference_period, stores=, storage=, jobs=, validator=, forcar=)` | 145 | - |
| task | `consolidate_3050(tenant_id, reference_period, forcar)` | 34 | 80% |
| funcao | `match_source_3050(filename, sources)` | 5 | - |
| funcao | `semana_alvo_alerta(hoje)` | 4 | - |
| funcao | `_ingest_3050(schema, tenant, src, inbox, rel, period, dests)` | 49 | 74% |
| task | `sftp_watch_3050()` | 43 | - |
| funcao | `fechamento_sem_mensal(schema, week, doc_store)` | 26 | - |
| task | `alert_prazo_3050()` | 57 | - |

### `backend/api/routes/engine3050.py` (9 funcoes de topo, 223 linhas)

| tipo | assinatura | l. | melhor par em outro motor |
|---|---|---:|---|
| funcao | `_validate_week(value)` | 6 | 96% |
| funcao | `_fontes_3050(schema)` | 7 | 99% |
| rota | `week_status(week, user)` | 50 | - |
| rota | `source_summary(week, source_id, user)` | 15 | - |
| rota | `upload_3050(data_source_id, reference_period, file, user)` | 45 | 97% |
| rota | `reconciliation(week, user)` | 23 | - |
| rota | `consolidate_endpoint(week, forcar, user)` | 47 | - |
| rota | `document(week, user)` | 15 | 84% |
| rota | `download_document(id, kind, user)` | 15 | 70% |

### `backend/worker/tasks/engine3026_tasks.py` (9 funcoes de topo, 286 linhas)

| tipo | assinatura | l. | melhor par em outro motor |
|---|---|---:|---|
| funcao | `_cnpj_if(cnpj)` | 3 | - |
| funcao | `_cnpj_3026(tenant)` | 6 | - |
| funcao | `_run_process_3026_file(tenant_id, import_job_id, stores=, storage=, jobs=, validator=, connect=)` | 59 | - |
| task | `process_3026_file(tenant_id, import_job_id)` | 17 | - |
| funcao | `_periodo_3040_dezembro(reference_period)` | 3 | - |
| funcao | `_conciliacao_serializavel(res)` | 10 | - |
| funcao | `_run_consolidate_3026(tenant_id, reference_period, stores=, storage=, jobs=, validator=, forcar=)` | 119 | - |
| task | `consolidate_3026(tenant_id, reference_period, forcar)` | 31 | 80% |
| task | `alert_prazo_3026()` | 38 | - |

### `backend/api/routes/engine3026.py` (9 funcoes de topo, 195 linhas)

| tipo | assinatura | l. | melhor par em outro motor |
|---|---|---:|---|
| funcao | `_validate_year(value)` | 6 | 96% |
| funcao | `_fontes_3026(schema)` | 7 | 99% |
| rota | `year_status(year, user)` | 43 | - |
| rota | `source_summary(year, source_id, user)` | 19 | - |
| rota | `upload_3026(data_source_id, reference_period, file, user)` | 44 | 97% |
| rota | `reconciliation(year, user)` | 23 | - |
| rota | `consolidate_endpoint(year, user)` | 12 | - |
| rota | `document(year, user)` | 15 | 84% |
| rota | `download_document(id, kind, user)` | 26 | 70% |

### `backend/worker/tasks/cosif_tasks.py` (3 funcoes de topo, 59 linhas)

| tipo | assinatura | l. | melhor par em outro motor |
|---|---|---:|---|
| funcao | `_serializar_amarracoes(amarracoes)` | 11 | - |
| funcao | `_process_cosif(schema=, import_job_id=, meta=, content=, store=)` | 20 | - |
| task | `process_cosif_file(tenant_id, job_id)` | 28 | - |

### `backend/api/routes/cosif.py` (5 funcoes de topo, 192 linhas)

| tipo | assinatura | l. | melhor par em outro motor |
|---|---|---:|---|
| rota | `upload_cosif(document_type, reference_period, file, user)` | 54 | - |
| funcao | `_gerar_bytes(saldos_folhas, plano, document_type=, reference_period=)` | 18 | - |
| rota | `generate_cosif(document_type, reference_period, file, transform, delimiter, encoding, user)` | 76 | - |
| funcao | `_ultimo_resumo(jobs, document_type, reference_period)` | 12 | - |
| rota | `list_cosif_documents(document_type, reference_period, user)` | 32 | - |

## Pares similares entre motores (14)

| similaridade | A | l. | B | l. |
|---:|---|---:|---|---:|
| 99% | `3050 :: _fontes_3050` | 7 | `3026 :: _fontes_3026` | 7 |
| 97% | `3050 :: upload_3050` | 45 | `3026 :: upload_3026` | 44 |
| 96% | `3050 :: _validate_week` | 6 | `3026 :: _validate_year` | 6 |
| 90% | `3040 :: download_document` | 35 | `3044 :: download_document` | 40 |
| 87% | `3040 :: _ingest_3040` | 64 | `3044 :: _ingest_3044` | 55 |
| 86% | `3040 :: _maybe_autoconsolidate_3040` | 28 | `3044 :: _maybe_autoconsolidate` | 30 |
| 84% | `3050 :: document` | 15 | `3026 :: document` | 15 |
| 80% | `3050 :: consolidate_3050` | 34 | `3026 :: consolidate_3026` | 31 |
| 76% | `3040 :: _tem_dados_para_consolidar_3040` | 14 | `3044 :: _tem_dados_para_consolidar_3044` | 11 |
| 74% | `3040 :: _ingest_3040` | 64 | `3050 :: _ingest_3050` | 49 |
| 72% | `3044 :: _ingest_3044` | 55 | `3050 :: _ingest_3050` | 49 |
| 71% | `3044 :: upload_3044` | 87 | `3050 :: upload_3050` | 45 |
| 71% | `3044 :: upload_3044` | 87 | `3026 :: upload_3026` | 44 |
| 70% | `3050 :: download_document` | 15 | `3026 :: download_document` | 26 |

## % de linhas com equivalente em outro motor

| informe | funcoes | linhas | funcoes com par | linhas com par | % linhas |
|---|---:|---:|---:|---:|---:|
| 3026 | 18 | 481 | 6 | 129 | 27% |
| 3040 | 52 | 2484 | 4 | 141 | 6% |
| 3044 | 39 | 1472 | 5 | 223 | 15% |
| 3050 | 23 | 759 | 7 | 171 | 23% |
| cosif | 8 | 251 | 0 | 0 | 0% |

## Etapa do pipeline x informe

| etapa | 3040 | 3044 | 3050 | 3026 | cosif |
|---|---|---|---|---|---|
| process_file | copiado (270 l.) | copiado (210 l.) | copiado (106 l.) | copiado (76 l.) | copiado (28 l.) |
| consolidate | copiado (223 l.) | copiado (377 l.) | copiado (226 l.) | copiado (162 l.) | nao existe |
| sftp_watch | copiado (93 l.) | copiado (92 l.) | copiado (43 l.) | nao existe | nao existe |
| alert_prazo | copiado (67 l.) | copiado (75 l.) | copiado (57 l.) | copiado (38 l.) | nao existe |
| regenerate/retific | nao existe | copiado (35 l.) | nao existe | nao existe | nao existe |

## `backend/engine/base.py`

Definicoes de topo: `CadocEngine`, `EngineRegistry`, `EngineSteps`, `__init__`, `_run`, `alert_prazo`, `consolidate`, `dispatch`, `document_type`, `get`, `list_types`, `prazo_proximo`, `process_file`, `queue_for`, `register`, `sftp_watch`

### Bundle CadocEngine por informe + dispatch em runtime

| informe | bundle | passos | dispatch() em runtime |
|---|---|---|---|
| 3040 | `backend/engine/cadoc3040.py` | consolidate, process_file, sftp_watch | **nao** |
| 3044 | `backend/engine/cadoc3044.py` | consolidate, process_file, sftp_watch | **nao** |
| 3050 | `backend/engine/cadoc3050.py` | consolidate, process_file, sftp_watch | **nao** |
| 3026 | `backend/engine/cadoc3026.py` | consolidate, process_file | `engine3026_tasks.py` |
| cosif | `backend/engine/cosif.py` | process_file | **nao** |
