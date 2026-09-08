# Endpoints -> consumidores, stores, tasks

Gerado por `discovery/scripts/endpoints.py` (AST dos decoradores).

Total de operacoes HTTP: **288** em 42 modulos.

| metodo | path | modulo:funcao | l. | guard | stores | tasks | front | e2e | backref |
|---|---|---|---:|:-:|---|---|---|---|---|
| GET | `/api/admin/audit` | `admin.py:list_audit` | 17 | S | — | — | /admin/audit, /admin/tenants/[id] | — | 1 |
| POST | `/api/admin/impersonate/end` | `admin.py:end_impersonation` | 15 | - | — | — | — | — | 1 |
| POST | `/api/admin/sftp/provision` | `admin.py:sftp_provision` | 93 | S | postgres | — | /admin/sftp | — | — |
| GET | `/api/admin/sftp/status` | `admin.py:sftp_status` | 15 | S | — | — | /admin/sftp, /admin/tenants/[id] | — | — |
| POST | `/api/admin/sftp/tenants/{}/reset-password` | `admin.py:sftp_reset_password` | 51 | S | — | — | /admin/sftp, /admin/tenants/[id] | — | — |
| GET | `/api/admin/tenants` | `admin.py:list_tenants` | 10 | S | — | — | /admin/audit, /admin/gestao, /admin/ingestao, /admin/operations, /admin/tenants/new | — | 1 |
| POST | `/api/admin/tenants` | `admin.py:create_tenant_wizard` | 71 | S | postgres | — | /admin/audit, /admin/gestao, /admin/ingestao, /admin/operations, /admin/tenants/new | — | 1 |
| GET | `/api/admin/tenants/{}` | `admin.py:get_tenant_detail` | 10 | S | — | — | /admin/tenants/[id] | — | 1 |
| PATCH | `/api/admin/tenants/{}` | `admin.py:update_tenant` | 14 | S | — | — | /admin/tenants/[id] | — | 1 |
| POST | `/api/admin/tenants/{}/cancel-deletion` | `admin.py:cancel_tenant_deletion` | 22 | S | — | — | /admin/tenants/[id] | — | — |
| POST | `/api/admin/tenants/{}/delete` | `admin.py:schedule_tenant_deletion` | 43 | S | — | — | /admin/tenants/[id] | — | — |
| POST | `/api/admin/tenants/{}/impersonate` | `admin.py:impersonate_tenant` | 37 | S | — | — | /admin | 49-rep80-versoes-schema.spec.ts | 1 |
| PUT | `/api/admin/tenants/{}/rc18` | `admin.py:set_tenant_rc18` | 23 | S | — | — | /admin/tenants/[id] | — | — |
| POST | `/api/admin/tenants/{}/reactivate` | `admin.py:reactivate_tenant` | 20 | S | — | — | — | — | 1 |
| POST | `/api/admin/tenants/{}/setup-steps/{}` | `admin.py:set_setup_step_override` | 35 | S | — | — | /admin/tenants/[id] | — | 1 |
| POST | `/api/admin/tenants/{}/suspend` | `admin.py:suspend_tenant` | 10 | S | — | — | — | — | 1 |
| GET | `/api/admin/tenants/{}/users` | `admin.py:list_tenant_users` | 7 | S | — | — | /admin/tenants/[id] | — | 1 |
| POST | `/api/admin/tenants/{}/users` | `admin.py:create_tenant_user` | 33 | S | — | — | /admin/tenants/[id] | — | 1 |
| POST | `/api/admin/tenants/{}/users/{}/resend-invite` | `admin.py:resend_invite` | 22 | S | — | — | /admin/tenants/[id] | — | 1 |
| POST | `/api/admin/tenants/{}/users/{}/send-reset-link` | `admin.py:send_reset_link` | 30 | S | — | — | /admin/tenants/[id] | — | — |
| PATCH | `/api/admin/users/{}` | `admin.py:update_any_user` | 22 | S | — | — | /admin/tenants/[id] | — | 1 |
| GET | `/api/audit/actions` | `audit.py:list_audit_actions` | 7 | S | — | — | /audit | 31-regressao-qualidade-pilares.spec.ts | — |
| GET | `/api/audit/events` | `audit.py:list_audit_events` | 14 | S | — | — | /audit | 31-regressao-qualidade-pilares.spec.ts | 2 |
| GET | `/api/audit/events.csv` | `audit.py:export_audit_events_csv` | 19 | S | — | — | — | — | — |
| POST | `/api/auth/forgot-password` | `auth.py:forgot_password` | 14 | - | — | — | /forgot-password | — | 2 |
| POST | `/api/auth/login` | `auth.py:login` | 67 | - | — | — | /login | 49-rep80-versoes-schema.spec.ts | 5 |
| POST | `/api/auth/logout` | `auth.py:logout` | 15 | - | — | — | /, /admin, /admin/audit, /admin/cosif-plano, /admin/gestao, /admin/ingestao, /admin/moat, /admin/operations, /admin/radar, /admin/reportes, /admin/schema-versions, /admin/sftp, /admin/tenants/[id], /admin/tenants/new, /admin/validador, /audit, /bcb, /cadoc-3026, /cadoc-3040, /cadoc-3040/[reference_period], /cadoc-3040/[reference_period]/retificacao, /cadoc-3044, /cadoc-3050, /cadoc-cosif, /change-password, /compliance, /compliance/manifestacoes, /corrective, /distribution, /lgpd, /login, /onboarding, /pecld, /policy, /quality, /quality/dictionary, /quality/indicios, /quality/lineage, /quality/reconciliation, /quality/reconciliation/[id], /quality/reconciliation/conciliar, /quality/reports, /quality/reports/[id], /quality/reports/recipients, /quality/retifications, /rc18, /settings/competencia-inicial, /settings/contrato-dados, /settings/data-sources, /settings/director, /settings/governance, /settings/instituicao, /settings/sftp, /settings/users, /setup | — | 1 |
| POST | `/api/auth/refresh` | `auth.py:refresh_token` | 117 | - | — | — | /, /admin, /admin/audit, /admin/cosif-plano, /admin/gestao, /admin/ingestao, /admin/moat, /admin/operations, /admin/radar, /admin/reportes, /admin/schema-versions, /admin/sftp, /admin/tenants/[id], /admin/tenants/new, /admin/validador, /audit, /bcb, /cadoc-3026, /cadoc-3040, /cadoc-3040/[reference_period], /cadoc-3040/[reference_period]/retificacao, /cadoc-3044, /cadoc-3050, /cadoc-cosif, /change-password, /compliance, /compliance/manifestacoes, /corrective, /distribution, /lgpd, /login, /onboarding, /pecld, /policy, /quality, /quality/dictionary, /quality/indicios, /quality/lineage, /quality/reconciliation, /quality/reconciliation/[id], /quality/reconciliation/conciliar, /quality/reports, /quality/reports/[id], /quality/reports/recipients, /quality/retifications, /rc18, /settings/competencia-inicial, /settings/contrato-dados, /settings/data-sources, /settings/director, /settings/governance, /settings/instituicao, /settings/sftp, /settings/users, /setup | — | 2 |
| POST | `/api/auth/reset-password` | `auth.py:reset_password` | 16 | - | — | — | /reset-password | — | 1 |
| GET | `/api/bacen-ciclo/pendentes` | `bacen_ciclo.py:listar_pendentes` | 8 | S | — | — | /quality/retifications | — | 1 |
| GET | `/api/bacen-ciclo/submissions/{}/ciclo` | `bacen_ciclo.py:ver_ciclo` | 18 | S | — | — | /quality/retifications | — | 1 |
| POST | `/api/bacen-ciclo/submissions/{}/protocolo` | `bacen_ciclo.py:registrar_protocolo` | 50 | S | EventStore | — | /quality/retifications | — | 1 |
| POST | `/api/bacen-ciclo/submissions/{}/retorno` | `bacen_ciclo.py:registrar_retorno` | 72 | S | — | `processar_veredito` | /quality/retifications | — | 1 |
| GET | `/api/bcb/check/{}` | `bcb.py:check_pending_issues` | 6 | S | — | — | — | — | — |
| GET | `/api/bcb/communications` | `bcb.py:list_communications` | 6 | S | — | — | /bcb | 06-mais-fluxos.spec.ts | — |
| POST | `/api/bcb/communications` | `bcb.py:create_communication` | 12 | S | — | — | /bcb | 06-mais-fluxos.spec.ts | — |
| GET | `/api/bcb/communications/{}` | `bcb.py:get_communication` | 9 | S | — | — | — | — | — |
| PUT | `/api/bcb/communications/{}` | `bcb.py:update_communication` | 12 | S | — | — | — | — | — |
| POST | `/api/bcb/communications/{}/approve` | `bcb.py:approve_communication` | 19 | S | — | — | /bcb | — | — |
| POST | `/api/bcb/communications/{}/mark-sent` | `bcb.py:mark_sent` | 21 | S | — | — | /bcb | — | — |
| GET | `/api/bcb/communications/{}/pacote.zip` | `bcb.py:pacote_zip` | 30 | S | — | — | /bcb | — | — |
| GET | `/api/calendario` | `calendario.py:calendario` | 11 | S | — | — | / | — | 3 |
| GET | `/api/calendario/3044/{}` | `calendario.py:calendario_3044_dias` | 17 | S | — | — | / | — | — |
| GET | `/api/corrective/dashboard` | `corrective.py:get_dashboard` | 5 | S | — | — | /corrective | — | — |
| GET | `/api/corrective/issues` | `corrective.py:list_issues` | 7 | S | — | — | /corrective | 05-mutacoes.spec.ts | 1 |
| POST | `/api/corrective/issues` | `corrective.py:create_issue` | 11 | S | — | — | /corrective | 05-mutacoes.spec.ts | 1 |
| GET | `/api/corrective/issues/{}` | `corrective.py:get_issue` | 10 | S | — | — | /corrective | — | 1 |
| PUT | `/api/corrective/issues/{}` | `corrective.py:update_issue` | 12 | S | — | — | /corrective | — | 1 |
| GET | `/api/corrective/issues/{}/plans` | `corrective.py:list_plans` | 6 | S | — | — | /corrective | 05-mutacoes.spec.ts | 1 |
| POST | `/api/corrective/issues/{}/plans` | `corrective.py:create_plan` | 10 | S | — | — | /corrective | 05-mutacoes.spec.ts | 1 |
| POST | `/api/corrective/issues/{}/resolve` | `corrective.py:resolve_issue` | 14 | S | — | — | /corrective | — | — |
| POST | `/api/corrective/plans/{}/approve` | `corrective.py:approve_plan` | 19 | S | — | — | /corrective | 05-mutacoes.spec.ts | 1 |
| POST | `/api/corrective/plans/{}/complete` | `corrective.py:complete_plan` | 12 | S | — | — | /corrective | — | 1 |
| GET | `/api/correlations` | `correlations.py:listar_correlacoes` | 15 | S | CorrelationAnnotationStore, CorrelationStore | — | /quality/indicios | 38-cosif-indicios.spec.ts | 1 |
| POST | `/api/correlations/items/corretiva` | `correlations.py:corretiva_indicio` | 19 | S | CorrelationAnnotationStore | — | /quality/indicios | — | — |
| POST | `/api/correlations/items/justificar` | `correlations.py:justificar_indicio` | 12 | S | CorrelationAnnotationStore | — | /quality/indicios | — | — |
| POST | `/api/correlations/run` | `correlations.py:rodar_correlacoes` | 19 | S | CorrelationStore | — | /quality/indicios | — | 1 |
| GET | `/api/cosif/documents` | `cosif.py:list_cosif_documents` | 32 | S | CosifStore, cosif_store | — | /cadoc-cosif | — | — |
| POST | `/api/cosif/generate` | `cosif.py:generate_cosif` | 76 | S | CosifPlanoStore, cosif_plano_store | `process_cosif_file` | /cadoc-cosif | — | 1 |
| POST | `/api/cosif/upload` | `cosif.py:upload_cosif` | 54 | S | — | `process_cosif_file` | /cadoc-cosif | — | — |
| POST | `/api/admin/cosif-plano` | `cosif_plano.py:upload_oficial` | 19 | S | AdminAuditStore, CosifPlanoStore, admin_store | — | /admin/cosif-plano | — | — |
| POST | `/api/admin/cosif-plano/sync` | `cosif_plano.py:sincronizar_bcb` | 16 | S | AdminAuditStore, CosifPlanoStore, admin_store | — | /admin/cosif-plano | — | — |
| GET | `/api/admin/cosif-plano/versions` | `cosif_plano.py:listar_versoes` | 8 | S | postgres | — | /admin/cosif-plano | — | — |
| POST | `/api/cosif-plano` | `cosif_plano.py:upload_tenant` | 13 | S | CosifPlanoStore | — | — | — | — |
| DELETE | `/api/cosif-plano` | `cosif_plano.py:remover_override` | 7 | S | CosifPlanoStore | — | — | — | — |
| GET | `/api/cosif-plano` | `cosif_plano.py:status_override` | 4 | S | CosifPlanoStore | — | — | — | — |
| GET | `/api/data-contracts` | `data_contract.py:listar` | 3 | S | — | — | /settings/contrato-dados | — | — |
| POST | `/api/data-contracts/emitir` | `data_contract.py:emitir` | 11 | S | — | — | /settings/contrato-dados | — | 1 |
| GET | `/api/data-contracts/preview` | `data_contract.py:preview` | 6 | S | — | — | /settings/contrato-dados | 33-centro-operacoes.spec.ts | 1 |
| GET | `/api/data-contracts/{}/download` | `data_contract.py:download` | 15 | S | — | — | /settings/contrato-dados | — | 1 |
| GET | `/api/data-sources` | `data_sources.py:list_data_sources` | 6 | S | — | — | /settings/data-sources | 07-import-3040.spec.ts, 14-cadoc-3050.spec.ts, 15-cadoc-3026.spec.ts, 23-regressao-setup.spec.ts, 24-regressao-3040.spec.ts, 26-regressao-3050.spec.ts, 28-regressao-conciliacoes.spec.ts, 30-regressao-retificacao-3042.spec.ts, 34-pecld.spec.ts, 35-scr-eventos.spec.ts | 3 |
| POST | `/api/data-sources` | `data_sources.py:create_data_source` | 35 | S | — | — | /settings/data-sources | 07-import-3040.spec.ts, 14-cadoc-3050.spec.ts, 15-cadoc-3026.spec.ts, 23-regressao-setup.spec.ts, 24-regressao-3040.spec.ts, 26-regressao-3050.spec.ts, 28-regressao-conciliacoes.spec.ts, 30-regressao-retificacao-3042.spec.ts, 34-pecld.spec.ts, 35-scr-eventos.spec.ts | 3 |
| GET | `/api/data-sources/layout-catalog/{}` | `data_sources.py:layout_catalog` | 15 | S | — | — | /settings/data-sources | — | — |
| POST | `/api/data-sources/preview-mapping` | `data_sources.py:preview_mapping` | 45 | S | — | — | /settings/data-sources | — | — |
| PATCH | `/api/data-sources/{}` | `data_sources.py:update_data_source` | 37 | S | — | — | /settings/data-sources | — | 1 |
| GET | `/api/dictionary` | `dictionary.py:list_all_entries` | 9 | S | — | — | /quality/dictionary | — | 1 |
| GET | `/api/dictionary/{}` | `dictionary.py:get_entries_by_type` | 7 | S | — | — | /quality/dictionary | — | 1 |
| POST | `/api/dictionary/{}` | `dictionary.py:create_entry` | 14 | S | — | — | /quality/dictionary | — | 1 |
| PUT | `/api/dictionary/{}/{}` | `dictionary.py:update_entry` | 22 | S | — | — | /quality/dictionary | — | — |
| POST | `/api/reports/acknowledgments/{}/confirm` | `distribution.py:confirm_acknowledgment` | 12 | S | — | — | — | — | — |
| GET | `/api/reports/distributions` | `distribution.py:list_distributions` | 6 | S | — | — | /distribution, /quality/reports/[id] | — | — |
| POST | `/api/reports/distributions` | `distribution.py:create_distribution` | 8 | S | — | — | /distribution, /quality/reports/[id] | — | — |
| GET | `/api/reports/distributions/dashboard` | `distribution.py:get_distribution_dashboard` | 5 | S | — | — | /distribution, /quality/reports | — | — |
| GET | `/api/reports/distributions/{}` | `distribution.py:get_distribution` | 12 | S | — | — | /quality/reports/[id] | — | — |
| POST | `/api/reports/distributions/{}/send` | `distribution.py:send_distribution` | 15 | S | — | `send_report_emails` | /quality/reports/[id] | — | — |
| GET | `/api/reports/recipients` | `distribution.py:list_recipients` | 6 | S | — | — | /distribution, /quality/reports/recipients | — | — |
| POST | `/api/reports/recipients` | `distribution.py:create_recipient` | 9 | S | — | — | /distribution, /quality/reports/recipients | — | — |
| PUT | `/api/reports/recipients/{}` | `distribution.py:update_recipient` | 10 | S | — | — | /distribution, /quality/reports/recipients | — | — |
| DELETE | `/api/reports/recipients/{}` | `distribution.py:deactivate_recipient` | 9 | S | — | — | /distribution, /quality/reports/recipients | — | — |
| GET | `/api/reports/semestrais` | `distribution.py:list_reports` | 6 | S | — | — | /quality/reports | 05-mutacoes.spec.ts | — |
| POST | `/api/reports/semestrais/generate` | `distribution.py:generate_report` | 24 | S | — | — | /quality/reports | 05-mutacoes.spec.ts | — |
| GET | `/api/reports/semestrais/{}` | `distribution.py:get_report` | 10 | S | — | — | /quality/reports/[id] | — | — |
| GET | `/api/reports/semestrais/{}/pdf` | `distribution.py:download_report_pdf` | 26 | S | — | — | /quality/reports/[id] | — | — |
| GET | `/api/admin/document-types` | `document_types.py:list_document_types` | 5 | - | — | — | /admin, /admin/reportes, /admin/tenants/[id] | — | 1 |
| POST | `/api/admin/document-types` | `document_types.py:create_document_type` | 27 | - | — | — | /admin, /admin/reportes, /admin/tenants/[id] | — | 1 |
| PATCH | `/api/admin/document-types/{}` | `document_types.py:update_document_type` | 50 | - | — | — | /admin/reportes | — | — |
| POST | `/api/engine3026/consolidate` | `engine3026.py:consolidate_endpoint` | 12 | S | — | `consolidate_3026` | /cadoc-3026 | — | 1 |
| GET | `/api/engine3026/document` | `engine3026.py:document` | 15 | S | — | — | — | — | 1 |
| GET | `/api/engine3026/documents/{}/download` | `engine3026.py:download_document` | 26 | S | — | — | /cadoc-3026 | — | — |
| GET | `/api/engine3026/reconciliation` | `engine3026.py:reconciliation` | 23 | S | — | — | — | 27-regressao-3026.spec.ts, 28-regressao-conciliacoes.spec.ts | 1 |
| GET | `/api/engine3026/source-summary` | `engine3026.py:source_summary` | 19 | S | — | — | — | — | 1 |
| POST | `/api/engine3026/upload` | `engine3026.py:upload_3026` | 44 | S | — | `process_3026_file` | /cadoc-3026 | — | 1 |
| GET | `/api/engine3026/year-status` | `engine3026.py:year_status` | 43 | S | — | — | /cadoc-3026 | 15-cadoc-3026.spec.ts, 27-regressao-3026.spec.ts | 1 |
| GET | `/api/engine3040/competencias` | `engine3040.py:list_competencias` | 205 | S | — | — | /cadoc-3040 | 42-setup-gate.spec.ts, 43-esteira-3040.spec.ts, 44-listagem-3040.spec.ts | — |
| POST | `/api/engine3040/consolidate` | `engine3040.py:consolidate_endpoint` | 61 | S | — | `consolidate_3040` | /cadoc-3040/[reference_period], /cadoc-3040/[reference_period]/retificacao | 30-regressao-retificacao-3042.spec.ts | 1 |
| POST | `/api/engine3040/dev/forcar-homologacao` | `engine3040.py:dev_forcar_homologacao` | 50 | S | — | — | /cadoc-3040/[reference_period], /cadoc-3040/[reference_period]/retificacao | — | — |
| GET | `/api/engine3040/documents/{}/download` | `engine3040.py:download_document` | 35 | S | — | — | /cadoc-3040/[reference_period], /cadoc-3040/[reference_period]/retificacao | 07-import-3040.spec.ts, 24-regressao-3040.spec.ts | 1 |
| GET | `/api/engine3040/historico` | `engine3040.py:historico_competencia` | 80 | S | mov3040_store | — | /cadoc-3040, /cadoc-3040/[reference_period] | — | — |
| POST | `/api/engine3040/imports/delete` | `engine3040.py:delete_imports_3040` | 91 | S | — | `consolidate_3040` | /cadoc-3040/[reference_period], /cadoc-3040/[reference_period]/retificacao | 24-regressao-3040.spec.ts, 28-regressao-conciliacoes.spec.ts, 30-regressao-retificacao-3042.spec.ts | — |
| GET | `/api/engine3040/modelo-extrato` | `engine3040.py:modelo_extrato_3040` | 15 | S | — | — | /cadoc-3040/[reference_period], /cadoc-3040/[reference_period]/retificacao | — | — |
| GET | `/api/engine3040/month-status` | `engine3040.py:month_status` | 158 | S | Rendimento3040Store, rendimento3040_store | — | /cadoc-3040/[reference_period] | 07-import-3040.spec.ts, 16-cadoc-3042.spec.ts, 24-regressao-3040.spec.ts, 28-regressao-conciliacoes.spec.ts, 30-regressao-retificacao-3042.spec.ts, 41-rep19-link-fechamento.spec.ts, 43-esteira-3040.spec.ts, 44-listagem-3040.spec.ts | 1 |
| GET | `/api/engine3040/operacao` | `engine3040.py:operacao_lookup` | 12 | S | — | — | /cadoc-3040/[reference_period], /cadoc-3040/[reference_period]/retificacao | — | — |
| GET | `/api/engine3040/registros` | `engine3040.py:registros` | 34 | S | — | — | /cadoc-3040/[reference_period] | — | — |
| GET | `/api/engine3040/registros/export` | `engine3040.py:registros_export` | 60 | S | — | — | /cadoc-3040/[reference_period] | — | — |
| GET | `/api/engine3040/registros/resumo` | `engine3040.py:registros_resumo` | 12 | S | — | — | /cadoc-3040/[reference_period] | — | — |
| POST | `/api/engine3040/responsavel` | `engine3040.py:set_responsavel_competencia` | 33 | S | — | — | — | — | — |
| GET | `/api/engine3040/source-summary` | `engine3040.py:source_summary` | 12 | S | — | — | /cadoc-3040/[reference_period], /cadoc-3040/[reference_period]/retificacao | 24-regressao-3040.spec.ts | — |
| POST | `/api/engine3040/upload` | `engine3040.py:upload_3040` | 127 | S | DataSourceStore, data_source_store | `process_3040_file` | /cadoc-3040/[reference_period], /cadoc-3040/[reference_period]/retificacao | — | 2 |
| POST | `/api/engine3044/consolidate` | `engine3044.py:consolidate` | 37 | S | — | `consolidate_3044` | /cadoc-3044 | 03-consolida-baixa.spec.ts | 1 |
| GET | `/api/engine3044/day-status` | `engine3044.py:day_status` | 69 | S | — | — | /cadoc-3044 | 03-consolida-baixa.spec.ts, 08-import-react-go.spec.ts, 09-3044-ver-linhas-excluir.spec.ts, 25-regressao-3044.spec.ts, 35-scr-eventos.spec.ts | 1 |
| GET | `/api/engine3044/documents/{}/download` | `engine3044.py:download_document` | 40 | S | — | — | /cadoc-3044 | 03-consolida-baixa.spec.ts, 25-regressao-3044.spec.ts | 1 |
| POST | `/api/engine3044/exclusions` | `engine3044.py:add_exclusions` | 23 | S | — | `consolidate_3044` | /cadoc-3044 | — | 1 |
| GET | `/api/engine3044/exclusions` | `engine3044.py:list_exclusions` | 5 | S | — | — | /cadoc-3044 | — | 1 |
| POST | `/api/engine3044/imports/delete` | `engine3044.py:delete_imports` | 40 | S | — | `consolidate_3044` | /cadoc-3044 | — | — |
| GET | `/api/engine3044/lines` | `engine3044.py:list_lines` | 23 | S | — | — | /cadoc-3044 | 25-regressao-3044.spec.ts | — |
| POST | `/api/engine3044/upload` | `engine3044.py:upload_3044` | 87 | S | DataSourceStore, data_source_store | `process_3044_file` | /cadoc-3044 | — | 1 |
| POST | `/api/engine3050/consolidate` | `engine3050.py:consolidate_endpoint` | 47 | S | — | `consolidate_3050` | /cadoc-3050 | — | 1 |
| GET | `/api/engine3050/document` | `engine3050.py:document` | 15 | S | — | — | — | — | 1 |
| GET | `/api/engine3050/documents/{}/download` | `engine3050.py:download_document` | 15 | S | — | — | /cadoc-3050 | — | — |
| GET | `/api/engine3050/reconciliation` | `engine3050.py:reconciliation` | 23 | S | — | — | /cadoc-3050 | 28-regressao-conciliacoes.spec.ts | 1 |
| GET | `/api/engine3050/source-summary` | `engine3050.py:source_summary` | 15 | S | — | — | — | — | 1 |
| POST | `/api/engine3050/upload` | `engine3050.py:upload_3050` | 45 | S | — | `process_3050_file` | /cadoc-3050 | — | 1 |
| GET | `/api/engine3050/week-status` | `engine3050.py:week_status` | 50 | S | — | — | /cadoc-3050 | 14-cadoc-3050.spec.ts, 26-regressao-3050.spec.ts | 1 |
| GET | `/api/governance/config` | `governance.py:get_config` | 3 | S | — | — | /settings/governance | 05-mutacoes.spec.ts, 31-regressao-qualidade-pilares.spec.ts | — |
| PUT | `/api/governance/config` | `governance.py:put_config` | 9 | S | — | — | /settings/governance | 05-mutacoes.spec.ts, 31-regressao-qualidade-pilares.spec.ts | — |
| POST | `/api/governance/dossie` | `governance.py:gerar_dossie` | 35 | S | CorrelationStore | — | /admin/tenants/[id] | — | 1 |
| GET | `/api/governance/dossie` | `governance.py:listar_dossies` | 6 | S | — | — | /admin/tenants/[id] | — | 1 |
| GET | `/api/governance/dossie/{}/download` | `governance.py:baixar_dossie` | 15 | S | — | — | /admin/tenants/[id] | — | 1 |
| GET | `/api/lgpd/access-log` | `lgpd.py:access_log` | 9 | S | LgpdAccessStore | — | /lgpd | — | — |
| POST | `/api/lgpd/anonimizar` | `lgpd.py:anonimizar` | 18 | S | — | — | /lgpd | — | — |
| GET | `/api/lineage/submission/{}` | `lineage.py:get_submission_lineage` | 14 | S | — | — | /quality/lineage | — | — |
| GET | `/api/lineage/submissions` | `lineage.py:list_submissions` | 10 | S | — | — | /quality/lineage | — | 1 |
| GET | `/api/lineage/{}` | `lineage.py:get_lineage` | 14 | S | — | — | — | — | 1 |
| POST | `/api/manifestacoes` | `manifestacoes.py:registrar` | 20 | S | ManifestacaoStore | — | /compliance/manifestacoes | — | — |
| GET | `/api/manifestacoes` | `manifestacoes.py:listar` | 4 | S | ManifestacaoStore | — | /compliance/manifestacoes | — | — |
| GET | `/api/manifestacoes/export.csv` | `manifestacoes.py:export_csv` | 16 | S | ManifestacaoStore | — | /compliance/manifestacoes | — | — |
| GET | `/api/manifestacoes/{}` | `manifestacoes.py:detalhe` | 10 | S | ManifestacaoStore | — | — | — | — |
| POST | `/api/manifestacoes/{}/transicao` | `manifestacoes.py:transicao` | 46 | S | ManifestacaoStore | — | /compliance/manifestacoes | — | — |
| GET | `/api/moat/fingerprints` | `moat.py:fingerprints` | 4 | - | — | — | /admin/moat | — | 1 |
| GET | `/api/moat/regulatorio` | `moat.py:regulatorio` | 4 | - | — | — | /admin/moat | 33-centro-operacoes.spec.ts | 1 |
| GET | `/api/moat/remediacao` | `moat.py:remediacao` | 4 | - | — | — | /admin/moat | — | 1 |
| POST | `/api/onboarding/depara-aplicar` | `onboarding.py:depara_aplicar` | 25 | S | — | — | /onboarding | — | 1 |
| GET | `/api/onboarding/depara-sugerido` | `onboarding.py:depara_sugerido` | 7 | - | — | — | /onboarding | — | 1 |
| POST | `/api/onboarding/perfis-aplicar` | `onboarding.py:perfis_aplicar` | 58 | S | — | — | /onboarding | — | 1 |
| GET | `/api/onboarding/perfis-sugeridos` | `onboarding.py:perfis_sugeridos_endpoint` | 11 | - | — | — | /onboarding | — | 1 |
| GET | `/api/onboarding/prontidao` | `onboarding.py:prontidao` | 18 | - | — | — | /onboarding | 33-centro-operacoes.spec.ts | 1 |
| GET | `/api/onboarding/status` | `onboarding.py:get_onboarding_status` | 58 | - | — | — | /, /cadoc-3026, /cadoc-3040, /cadoc-3040/[reference_period], /cadoc-3044, /cadoc-3050, /onboarding, /quality | — | — |
| GET | `/api/operations/cockpit` | `operations.py:cockpit` | 47 | - | — | — | /admin | 33-centro-operacoes.spec.ts | 2 |
| GET | `/api/operations/gestao` | `operations.py:gestao_metricas` | 9 | - | — | — | /admin/gestao | 33-centro-operacoes.spec.ts | 1 |
| POST | `/api/operations/gestao/recalcular-abertos` | `operations.py:recalcular_abertos` | 28 | - | EventStore, ops_event_store | — | /admin/gestao | — | 1 |
| GET | `/api/operations/gestao/sla-policies` | `operations.py:listar_sla_policies` | 5 | - | — | — | /admin/gestao | — | 2 |
| PUT | `/api/operations/gestao/sla-policies` | `operations.py:atualizar_sla_policy` | 24 | - | — | — | /admin/gestao | — | 2 |
| GET | `/api/operations/incidents` | `operations.py:list_incidents` | 7 | - | — | — | /admin/operations | 33-centro-operacoes.spec.ts | 1 |
| POST | `/api/operations/incidents/{}/assign` | `operations.py:assign_incident` | 17 | - | — | — | /admin/operations | — | — |
| POST | `/api/operations/incidents/{}/diagnosticar` | `operations.py:diagnosticar_incidente` | 15 | - | — | `diagnose_incident` | /admin/operations, /admin/tenants/[id] | — | — |
| POST | `/api/operations/incidents/{}/resolve` | `operations.py:resolve_incident` | 19 | - | — | — | /admin/operations, /admin/tenants/[id] | — | — |
| GET | `/api/operations/ingestao` | `operations.py:ingestao` | 7 | - | — | — | /admin/ingestao | 33-centro-operacoes.spec.ts | 1 |
| GET | `/api/operations/obligations` | `operations.py:list_obligations` | 14 | - | — | — | /admin/operations | — | — |
| GET | `/api/operations/onboarding` | `operations.py:onboarding_overview_endpoint` | 7 | - | — | — | /admin | 33-centro-operacoes.spec.ts | 1 |
| POST | `/api/operations/portfolios` | `operations.py:assign_carteira` | 20 | - | — | — | /admin/tenants/[id] | — | 1 |
| GET | `/api/operations/portfolios/{}` | `operations.py:list_carteira` | 8 | - | — | — | /admin/tenants/[id] | — | — |
| POST | `/api/operations/profiles` | `operations.py:upsert_profile` | 51 | - | — | — | /admin, /admin/tenants/[id] | 46-reportes-liberados-gate.spec.ts | 2 |
| GET | `/api/operations/profiles/{}` | `operations.py:list_profiles` | 9 | - | — | — | /admin, /admin/tenants/[id] | — | — |
| GET | `/api/operations/radar` | `operations.py:radar` | 5 | - | — | — | /admin/radar | 33-centro-operacoes.spec.ts | 1 |
| GET | `/api/operations/radar/badge` | `operations.py:radar_badge` | 5 | - | — | — | /admin | — | 1 |
| POST | `/api/operations/radar/varredura-web` | `operations.py:radar_varredura_web` | 6 | - | — | `web_sweep` | /admin/radar | — | 1 |
| POST | `/api/operations/radar/verificar` | `operations.py:radar_verificar` | 6 | - | — | `check_regulatory_versions` | /admin/radar | — | — |
| POST | `/api/operations/radar/{}/avaliar` | `operations.py:radar_avaliar` | 8 | - | — | `assess_regulatory_change` | /admin/radar | — | — |
| POST | `/api/operations/radar/{}/review` | `operations.py:radar_review` | 14 | - | — | — | /admin/radar | — | — |
| GET | `/api/operations/tenant/{}` | `operations.py:tenant_ops` | 19 | - | — | — | /admin/tenants/[id] | — | — |
| GET | `/api/operations/tenant/{}/engajamento` | `operations.py:get_engajamento` | 17 | - | — | — | /admin/tenants/[id] | 33-centro-operacoes.spec.ts | — |
| PUT | `/api/operations/tenant/{}/engajamento` | `operations.py:set_engajamento` | 12 | - | — | — | /admin/tenants/[id] | 33-centro-operacoes.spec.ts | — |
| POST | `/api/operations/tenant/{}/engajar` | `operations.py:engajar_agora` | 13 | - | — | — | /admin/tenants/[id] | — | — |
| GET | `/api/painel` | `painel.py:get_painel` | 144 | - | — | — | /, /rc18 | 29-regressao-rc18-fechamento.spec.ts, 41-rep19-link-fechamento.spec.ts | 1 |
| GET | `/api/painel/alertas` | `painel.py:alertas` | 5 | - | — | — | — | — | 1 |
| GET | `/api/painel/saude` | `painel.py:saude` | 26 | - | — | — | /, /compliance | 04-qualidade-cockpit.spec.ts, 31-regressao-qualidade-pilares.spec.ts | 1 |
| GET | `/api/painel/{}/historico` | `painel.py:historico` | 17 | - | — | — | /rc18 | — | 1 |
| POST | `/api/painel/{}/{}/aferir` | `painel.py:aferir` | 33 | S | — | — | — | — | — |
| POST | `/api/painel/{}/{}/aprovar` | `painel.py:aprovar` | 28 | S | — | — | — | — | — |
| GET | `/api/painel/{}/{}/arquivos.zip` | `painel.py:baixar_arquivos` | 23 | S | — | — | /, /rc18 | — | — |
| POST | `/api/painel/{}/{}/concluir` | `painel.py:concluir` | 20 | S | — | — | — | — | — |
| POST | `/api/painel/{}/{}/enviar` | `painel.py:enviar` | 61 | S | — | — | /, /rc18 | — | — |
| POST | `/api/painel/{}/{}/reabrir` | `painel.py:reabrir` | 22 | S | — | — | / | — | — |
| POST | `/api/painel/{}/{}/reprovar` | `painel.py:reprovar` | 14 | S | — | — | /, /rc18 | — | — |
| POST | `/api/pecld/calcular` | `pecld.py:calcular` | 10 | S | — | `compute_pecld` | /pecld | — | — |
| GET | `/api/pecld/conciliacao` | `pecld.py:conciliacao` | 15 | - | PecldResultStore | — | — | 34-pecld.spec.ts | 1 |
| GET | `/api/pecld/parametros` | `pecld.py:get_parametros` | 4 | - | PecldParameterStore | — | — | 34-pecld.spec.ts | 1 |
| PUT | `/api/pecld/parametros` | `pecld.py:put_parametros` | 13 | S | PecldParameterStore | — | — | 34-pecld.spec.ts | 1 |
| GET | `/api/pecld/resultado` | `pecld.py:resultado` | 11 | - | PecldResultStore | — | /pecld | 34-pecld.spec.ts | — |
| GET | `/api/policy/reviews` | `policy.py:list_reviews` | 6 | S | — | — | /policy | — | — |
| POST | `/api/policy/reviews` | `policy.py:create_review` | 8 | S | — | — | /policy | — | — |
| GET | `/api/policy/reviews/status` | `policy.py:get_review_status` | 5 | S | — | — | /policy | — | — |
| GET | `/api/policy/reviews/{}` | `policy.py:get_review` | 9 | S | — | — | — | — | — |
| POST | `/api/policy/reviews/{}/approve` | `policy.py:approve_review` | 17 | S | — | — | /policy | — | — |
| POST | `/api/policy/reviews/{}/reject` | `policy.py:reject_review` | 7 | S | — | — | — | — | — |
| POST | `/api/policy/reviews/{}/submit` | `policy.py:submit_review` | 6 | S | — | — | /policy | — | — |
| GET | `/api/policy/versions` | `policy.py:list_versions` | 6 | S | — | — | /policy | 05-mutacoes.spec.ts | — |
| POST | `/api/policy/versions` | `policy.py:create_version` | 19 | S | policy_store | — | /policy | 05-mutacoes.spec.ts | — |
| GET | `/api/policy/versions/current` | `policy.py:get_current_version` | 8 | S | — | — | /policy | 05-mutacoes.spec.ts, 23-regressao-setup.spec.ts, 31-regressao-qualidade-pilares.spec.ts | — |
| GET | `/api/policy/versions/{}` | `policy.py:get_version` | 9 | S | — | — | — | — | — |
| GET | `/api/public/reports/ack/{}/{}` | `public_reports.py:view_by_token` | 11 | - | — | — | /reports/ack/[tenant_id]/[token] | — | — |
| POST | `/api/public/reports/ack/{}/{}/confirm` | `public_reports.py:confirm_by_token` | 6 | - | — | — | — | — | — |
| POST | `/api/public/reports/ack/{}/{}/confirmar` | `public_reports.py:confirmar_com_codigo` | 49 | - | postgres | — | /reports/ack/[tenant_id]/[token] | — | — |
| POST | `/api/public/reports/ack/{}/{}/enviar-codigo` | `public_reports.py:enviar_codigo` | 20 | - | — | — | /reports/ack/[tenant_id]/[token] | — | — |
| GET | `/api/public/reports/verificar/{}/{}` | `public_reports.py:verificar` | 18 | - | DocumentHashStore, document_hash_store | — | /verificar/[tenant_id]/[sha256] | — | — |
| POST | `/api/quality/assess-now` | `quality.py:assess_now` | 29 | S | — | — | /quality | 29-regressao-rc18-fechamento.spec.ts | — |
| GET | `/api/quality/completude-detail` | `quality.py:completude_detail` | 42 | S | — | — | /quality | — | — |
| GET | `/api/quality/dashboard` | `quality.py:get_dashboard` | 60 | S | GovernanceConfigStore | — | — | 04-qualidade-cockpit.spec.ts, 29-regressao-rc18-fechamento.spec.ts, 31-regressao-qualidade-pilares.spec.ts | 2 |
| GET | `/api/quality/dimensions` | `quality.py:list_dimensions` | 10 | S | — | — | — | 29-regressao-rc18-fechamento.spec.ts, 31-regressao-qualidade-pilares.spec.ts | 1 |
| PUT | `/api/quality/dimensions/{}` | `quality.py:update_dimension` | 17 | S | — | — | — | — | — |
| GET | `/api/quality/director` | `quality.py:get_director` | 10 | S | — | — | /settings/director | 06-mais-fluxos.spec.ts, 31-regressao-qualidade-pilares.spec.ts | — |
| POST | `/api/quality/director` | `quality.py:set_director` | 38 | S | — | — | /settings/director | 06-mais-fluxos.spec.ts, 31-regressao-qualidade-pilares.spec.ts | — |
| GET | `/api/quality/reports` | `quality.py:list_reports` | 15 | S | — | — | /quality | — | 1 |
| POST | `/api/quality/reports/generate` | `quality.py:generate_report` | 11 | S | — | — | — | — | — |
| GET | `/api/reconciliation` | `reconciliation.py:list_reconciliations` | 4 | S | — | — | /quality/reconciliation | 28-regressao-conciliacoes.spec.ts | — |
| POST | `/api/reconciliation/contabil` | `reconciliation.py:run_contabil` | 23 | S | — | — | /quality/reconciliation/conciliar | 06-mais-fluxos.spec.ts | 1 |
| GET | `/api/reconciliation/contabil-config` | `reconciliation.py:contabil_config` | 6 | S | — | — | /quality/reconciliation/conciliar | — | — |
| GET | `/api/reconciliation/contabil-mapping` | `reconciliation.py:get_contabil_mapping` | 5 | S | — | — | /quality/reconciliation/conciliar | — | — |
| PUT | `/api/reconciliation/contabil-mapping` | `reconciliation.py:put_contabil_mapping` | 12 | S | — | — | /quality/reconciliation/conciliar | — | — |
| PUT | `/api/reconciliation/contabil-mapping/csv` | `reconciliation.py:put_contabil_mapping_csv` | 14 | S | — | — | /quality/reconciliation/conciliar | — | — |
| GET | `/api/reconciliation/contabil-mapping/template.csv` | `reconciliation.py:contabil_mapping_template` | 6 | S | — | — | /quality/reconciliation/conciliar | — | — |
| POST | `/api/reconciliation/contabil/dispensa` | `reconciliation.py:dispensa_contabil` | 23 | S | — | — | /quality/reconciliation/conciliar | — | 1 |
| POST | `/api/reconciliation/items/{}/corretiva` | `reconciliation.py:to_corrective` | 14 | S | — | — | /quality/reconciliation/[id], /quality/reconciliation/conciliar | — | — |
| POST | `/api/reconciliation/items/{}/justificar` | `reconciliation.py:justify` | 13 | S | — | — | /quality/reconciliation/[id], /quality/reconciliation/conciliar | — | — |
| POST | `/api/reconciliation/origem` | `reconciliation.py:run_origem` | 13 | S | — | — | /quality/reconciliation/conciliar | 28-regressao-conciliacoes.spec.ts | 1 |
| GET | `/api/reconciliation/scoped` | `reconciliation.py:scoped` | 24 | S | — | — | /quality/reconciliation/conciliar | 28-regressao-conciliacoes.spec.ts | 2 |
| GET | `/api/reconciliation/{}` | `reconciliation.py:get_reconciliation` | 6 | S | — | — | /quality/reconciliation/[id] | — | — |
| GET | `/api/reportes/liberados` | `reportes.py:list_liberados` | 30 | - | — | — | — | seed_regressao.py | 1 |
| POST | `/api/retification` | `retification.py:open_retification` | 11 | S | — | — | /cadoc-3040/[reference_period]/retificacao, /quality/retifications | 06-mais-fluxos.spec.ts, 30-regressao-retificacao-3042.spec.ts | — |
| GET | `/api/retification` | `retification.py:list_retifications` | 18 | S | — | — | /cadoc-3040/[reference_period]/retificacao, /quality/retifications | 06-mais-fluxos.spec.ts, 30-regressao-retificacao-3042.spec.ts | — |
| GET | `/api/retification/context` | `retification.py:retification_context` | 82 | S | — | — | /cadoc-3040/[reference_period]/retificacao | — | — |
| GET | `/api/retification/history` | `retification.py:history` | 4 | S | — | — | — | — | — |
| GET | `/api/retification/{}/3042` | `retification.py:get_3042` | 10 | S | — | — | — | — | — |
| GET | `/api/retification/{}/3042/download` | `retification.py:download_3042` | 19 | S | — | — | /cadoc-3040/[reference_period]/retificacao | 30-regressao-retificacao-3042.spec.ts | — |
| POST | `/api/retification/{}/cancelar` | `retification.py:cancel_retification` | 21 | S | — | — | /cadoc-3040/[reference_period]/retificacao | — | — |
| POST | `/api/retification/{}/consolidate` | `retification.py:consolidate_retification` | 43 | S | — | `consolidate_3040` | /cadoc-3040/[reference_period]/retificacao | — | — |
| POST | `/api/retification/{}/enviar` | `retification.py:send_retification` | 39 | S | — | — | /cadoc-3040/[reference_period]/retificacao | — | — |
| POST | `/api/retification/{}/gerar-3042` | `retification.py:gerar_3042` | 102 | S | — | — | /cadoc-3040/[reference_period]/retificacao | — | — |
| POST | `/api/retification/{}/link-document` | `retification.py:link_document` | 13 | S | — | — | — | — | — |
| POST | `/api/retification/{}/metodo` | `retification.py:set_metodo` | 34 | S | — | — | /cadoc-3040/[reference_period]/retificacao | — | — |
| GET | `/api/admin/schema-versions` | `schema_versions.py:list_schema_versions` | 8 | S | — | — | /admin/schema-versions | 49-rep80-versoes-schema.spec.ts | 1 |
| POST | `/api/admin/schema-versions/migrate` | `schema_versions.py:migrate_tenants` | 40 | S | — | — | /admin/schema-versions | — | 1 |
| GET | `/api/admin/schema-versions/{}/drift` | `schema_versions.py:tenant_drift` | 10 | S | — | — | /admin/schema-versions | — | 1 |
| POST | `/api/admin/schema-versions/{}/migrate` | `schema_versions.py:migrate_tenant` | 19 | S | — | — | /admin/schema-versions | — | 1 |
| GET | `/api/schema-version/me` | `schema_versions.py:my_schema_version` | 25 | - | — | — | /admin/schema-versions | 49-rep80-versoes-schema.spec.ts | 1 |
| GET | `/api/setup/institution` | `setup.py:get_institution` | 16 | - | — | — | /setup | 42-setup-gate.spec.ts | — |
| POST | `/api/setup/institution/confirm` | `setup.py:confirm_institution` | 33 | - | — | — | /setup | 42-setup-gate.spec.ts | 1 |
| GET | `/api/setup/reference_period-inicial` | `setup.py:get_competencia_inicial` | 22 | - | — | — | /settings/competencia-inicial | — | 2 |
| POST | `/api/setup/reference_period-inicial` | `setup.py:set_competencia_inicial` | 26 | S | — | — | /settings/competencia-inicial | — | 2 |
| GET | `/api/setup/reportes` | `setup.py:list_reportes` | 46 | - | — | — | /bcb, /cadoc-3026, /cadoc-3040, /cadoc-3044, /cadoc-3050, /cadoc-cosif, /corrective, /lgpd, /onboarding, /quality/dictionary, /quality/lineage, /quality/retifications, /settings/contrato-dados, /settings/data-sources, /setup | 42-setup-gate.spec.ts, seed_regressao.py | 1 |
| POST | `/api/setup/reportes/inputs` | `setup.py:declare_input` | 50 | S | — | — | /setup | — | 1 |
| DELETE | `/api/setup/reportes/inputs/{}` | `setup.py:remove_input` | 10 | S | — | — | /setup | — | — |
| POST | `/api/setup/reportes/reference_period` | `setup.py:set_reference_period` | 44 | S | — | — | /cadoc-3026, /cadoc-3040, /cadoc-3044, /cadoc-3050, /setup | — | 1 |
| GET | `/api/setup/responsavel-remessa` | `setup.py:get_responsavel_remessa` | 13 | - | — | — | /setup | — | 1 |
| POST | `/api/setup/responsavel-remessa` | `setup.py:set_responsavel_remessa` | 47 | - | — | — | /setup | — | 1 |
| GET | `/api/setup/status` | `setup.py:get_setup_status` | 120 | - | — | — | — | 23-regressao-setup.spec.ts | 3 |
| GET | `/api/sftp/me` | `sftp.py:sftp_me` | 50 | S | — | — | /settings/sftp | — | — |
| POST | `/api/sftp/me/keys` | `sftp.py:add_sftp_key` | 23 | S | — | — | /settings/sftp | — | — |
| DELETE | `/api/sftp/me/keys` | `sftp.py:remove_sftp_key` | 16 | S | — | — | /settings/sftp | — | — |
| POST | `/api/telemetry/error` | `telemetry.py:report_frontend_error` | 11 | - | — | — | — | — | 1 |
| GET | `/api/tenants` | `tenants.py:list_tenants` | 4 | S | — | — | — | — | 1 |
| POST | `/api/tenants` | `tenants.py:create_tenant` | 7 | S | — | — | — | — | 1 |
| GET | `/api/tenants/me` | `tenants.py:get_own_tenant` | 6 | - | — | — | /, /quality/reconciliation, /settings/instituicao | — | 2 |
| PATCH | `/api/tenants/me` | `tenants.py:update_own_tenant` | 26 | S | — | — | /, /quality/reconciliation, /settings/instituicao | — | 2 |
| GET | `/api/tenants/{}` | `tenants.py:get_tenant` | 10 | S | — | — | — | — | 1 |
| PATCH | `/api/tenants/{}` | `tenants.py:update_tenant` | 12 | S | — | — | — | — | 1 |
| GET | `/api/users` | `users.py:list_users` | 4 | S | — | — | /settings/users | — | 1 |
| POST | `/api/users` | `users.py:create_user` | 28 | S | — | — | /settings/users | — | 1 |
| GET | `/api/users/me` | `users.py:get_me` | 4 | - | — | — | — | 13-identidade.spec.ts | 2 |
| PATCH | `/api/users/me/onboarding` | `users.py:patch_me_onboarding` | 8 | - | — | — | /, /cadoc-3026, /cadoc-3040, /cadoc-3040/[reference_period], /cadoc-3044, /cadoc-3050, /onboarding, /quality | — | — |
| POST | `/api/users/me/password` | `users.py:change_my_password` | 16 | - | — | — | /change-password | — | 2 |
| GET | `/api/users/me/tenants` | `users.py:list_my_tenants` | 25 | - | — | — | — | — | — |
| PATCH | `/api/users/{}` | `users.py:update_user` | 46 | S | — | — | /settings/users | — | 1 |
| GET | `/api/validacao/{}/{}` | `validacao.py:validacao` | 6 | S | — | — | /, /rc18 | — | — |
| POST | `/api/admin/validator/apply` | `validator.py:validator_apply` | 15 | S | AdminAuditStore, ValidatorVersionStore, admin_store, validator_version_store | — | /admin/validador | — | — |
| POST | `/api/admin/validator/impact` | `validator.py:validator_impact` | 3 | S | — | — | /admin/validador | — | — |
| GET | `/api/admin/validator/status` | `validator.py:validator_status` | 5 | S | ValidatorVersionStore, validator_version_store | — | /admin/validador | — | — |
| GET | `/api/validator/info` | `validator.py:validator_info` | 10 | - | — | — | /cadoc-3040/[reference_period], /cadoc-3040/[reference_period]/retificacao, /cadoc-3044 | — | — |

## Endpoints SEM consumidor (nem front, nem e2e, nem outro codigo): 23


### `bcb.py` (3)

- `GET /api/bcb/communications/{}` — `get_communication` (9 l.)
- `PUT /api/bcb/communications/{}` — `update_communication` (12 l.)
- `GET /api/bcb/check/{}` — `check_pending_issues` (6 l.)

### `cosif_plano.py` (3)

- `POST /api/cosif-plano` — `upload_tenant` (13 l.)
- `DELETE /api/cosif-plano` — `remover_override` (7 l.)
- `GET /api/cosif-plano` — `status_override` (4 l.)

### `painel.py` (3)

- `POST /api/painel/{}/{}/aprovar` — `aprovar` (28 l.)
- `POST /api/painel/{}/{}/aferir` — `aferir` (33 l.)
- `POST /api/painel/{}/{}/concluir` — `concluir` (20 l.)

### `policy.py` (3)

- `GET /api/policy/versions/{}` — `get_version` (9 l.)
- `GET /api/policy/reviews/{}` — `get_review` (9 l.)
- `POST /api/policy/reviews/{}/reject` — `reject_review` (7 l.)

### `retification.py` (3)

- `GET /api/retification/history` — `history` (4 l.)
- `POST /api/retification/{}/link-document` — `link_document` (13 l.)
- `GET /api/retification/{}/3042` — `get_3042` (10 l.)

### `quality.py` (2)

- `PUT /api/quality/dimensions/{}` — `update_dimension` (17 l.)
- `POST /api/quality/reports/generate` — `generate_report` (11 l.)

### `audit.py` (1)

- `GET /api/audit/events.csv` — `export_audit_events_csv` (19 l.)

### `distribution.py` (1)

- `POST /api/reports/acknowledgments/{}/confirm` — `confirm_acknowledgment` (12 l.)

### `engine3040.py` (1)

- `POST /api/engine3040/responsavel` — `set_responsavel_competencia` (33 l.)

### `manifestacoes.py` (1)

- `GET /api/manifestacoes/{}` — `detalhe` (10 l.)

### `public_reports.py` (1)

- `POST /api/public/reports/ack/{}/{}/confirm` — `confirm_by_token` (6 l.)

### `users.py` (1)

- `GET /api/users/me/tenants` — `list_my_tenants` (25 l.)

## Endpoints chamados pelo front que NAO existem no backend: 0

