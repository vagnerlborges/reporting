# Worker - beat, rotas e tasks

Gerado por `discovery/scripts/tasks.py`.

## beat_schedule (33 entradas)

| entrada | task | agenda | fila | ultimo commit que tocou a linha |
|---|---|---|---|---|
| `check-deadlines` | `backend.worker.tasks.alert_task.check_deadlines` | `3600.0` | `-` | c9c85d0f (2026-06-11) - feat: Celery app with 4 queues (import, validate, generate,  |
| `check-quality-scores` | `backend.worker.tasks.alert_task.check_quality_scores` | `86400.0` | `-` | e8ae8700 (2026-06-11) - feat: proactive alerts â€” deadline, quality, report due via |
| `check-report-due` | `backend.worker.tasks.alert_task.check_report_due` | `86400.0` | `-` | e8ae8700 (2026-06-11) - feat: proactive alerts â€” deadline, quality, report due via |
| `check-manifestacoes` | `backend.worker.tasks.alert_task.check_manifestacoes` | `86400.0` | `-` | 6b3baf2f (2026-07-03) - feat(manifestacoes): alerta diario de prazo (beat) com anti- |
| `check-schema-drift` | `backend.worker.tasks.alert_task.check_schema_drift` | `86400.0` | `-` | 2860960c (2026-06-21) - feat(ops): alerta diÃ¡rio de drift de schema (P1-10, complem |
| `check-stuck-jobs` | `backend.worker.tasks.alert_task.check_stuck_jobs` | `1800.0` | `-` | d07f5882 (2026-06-19) - feat(observabilidade): /ready real + healthcheck worker/beat |
| `sftp-watch-3044` | `backend.worker.tasks.engine3044_tasks.sftp_watch` | `300.0` | `-` | c351653f (2026-06-13) - feat(3044): SFTP watcher (match filename_pattern) + beat sft |
| `alert-fonte-pendente-3044` | `backend.worker.tasks.engine3044_tasks.alert_fonte_pendente` | `1800.0` | `-` | d3412e2e (2026-06-13) - feat(3044): alertas de fonte pendente e prazo 5o dia util (d |
| `alert-prazo-documento-3044` | `backend.worker.tasks.engine3044_tasks.alert_prazo_documento` | `86400.0` | `-` | d3412e2e (2026-06-13) - feat(3044): alertas de fonte pendente e prazo 5o dia util (d |
| `sftp-watch-3040` | `backend.worker.tasks.engine3040_tasks.sftp_watch_3040` | `300.0` | `-` | 3eb99b67 (2026-06-13) - feat(3040): sftp_watch_3040 + alert_prazo_3040 (beat) + deci |
| `alert-prazo-3040` | `backend.worker.tasks.engine3040_tasks.alert_prazo_3040` | `86400.0` | `-` | 3eb99b67 (2026-06-13) - feat(3040): sftp_watch_3040 + alert_prazo_3040 (beat) + deci |
| `sftp-watch-3050` | `backend.worker.tasks.engine3050_tasks.sftp_watch_3050` | `300.0` | `-` | ee3ba52d (2026-06-26) - feat(3050): tasks Celery (process/consolidate/watch/alert) + |
| `alert-prazo-3050` | `backend.worker.tasks.engine3050_tasks.alert_prazo_3050` | `86400.0` | `-` | ee3ba52d (2026-06-26) - feat(3050): tasks Celery (process/consolidate/watch/alert) + |
| `alert-prazo-3026` | `backend.worker.tasks.engine3026_tasks.alert_prazo_3026` | `86400.0` | `-` | 10d42312 (2026-06-26) - feat(3026): tasks process/consolidate + exposiÃ§Ã£o do mov30 |
| `backup-diario` | `backend.worker.tasks.backup_task.run_backup` | `86400.0` | `-` | 41adc8b3 (2026-06-16) - feat(backup): task run_backup + registro no worker + pg_dump |
| `check-backup-stale` | `backend.worker.tasks.backup_task.check_backup_stale` | `21600.0` | `-` | c7d83dd0 (2026-06-22) - feat(backup): run_backup aplica retenÃ§Ã£o + alerta de falha |
| `verify-backup-semanal` | `backend.worker.tasks.backup_task.verify_latest_backup` | `604800.0` | `-` | c7d83dd0 (2026-06-22) - feat(backup): run_backup aplica retenÃ§Ã£o + alerta de falha |
| `backup-validador-semanal` | `backend.worker.tasks.backup_task.backup_validator_artifacts` | `604800.0` | `-` | 6de3fa51 (2026-06-23) - feat(infra): R10 â€” backup semanal do volume do validador B |
| `sweep-tenant-schemas` | `backend.worker.tasks.schema_migration_task.sweep_tenant_schemas` | `900.0` | `-` | 625507f4 (2026-08-30) - feat(REP-56): cadeias Alembic por base (admin/tenant) e base |
| `purge-deleted-tenants` | `backend.worker.tasks.tenant_purge_task.purge_deleted_tenants` | `86400.0` | `-` | ddfbad75 (2026-08-26) - feat(REP-66): criaÃ§Ã£o de tenant no cockpit e exclusÃ£o de  |
| `ops-generate-obligations` | `backend.worker.tasks.ops_task.generate_obligations` | `86400.0` | `-` | fce508ee (2026-06-27) - feat(ops): tasks gerador + monitor de prazo + triagem (loop  |
| `ops-check-deadlines` | `backend.worker.tasks.ops_task.check_obligation_deadlines` | `7200.0` | `-` | fce508ee (2026-06-27) - feat(ops): tasks gerador + monitor de prazo + triagem (loop  |
| `ops-sweep-sftp-processing` | `backend.worker.tasks.ops_task.sweep_sftp_processing` | `21600.0` | `-` | 2e5557d9 (2026-08-24) - feat(REP-36,REP-37): fecha as 4 sugestÃµes do self-review da |
| `ops-check-ingestion` | `backend.worker.tasks.ingestion_task.check_ingestion` | `900.0` | `-` | af34a6f1 (2026-06-27) - feat(ingestao): monitor check_ingestion (projeÃ§Ã£o + incide |
| `radar-check-versions` | `backend.worker.tasks.radar_task.check_regulatory_versions` | `86400.0` | `-` | 52d0e22b (2026-06-27) - feat(radar): detector + agente de impacto consultivo (M3a) |
| `radar-check-web-sources` | `backend.worker.tasks.radar_web_task.check_web_sources` | `86400.0` | `-` | 86e697a0 (2026-06-27) - feat(radar-web): check_web_sources + web_sweep (M3b) |
| `radar-web-sweep` | `backend.worker.tasks.radar_web_task.web_sweep` | `604800.0` | `-` | 86e697a0 (2026-06-27) - feat(radar-web): check_web_sources + web_sweep (M3b) |
| `remediacao-diagnose-pending` | `backend.worker.tasks.remediacao_task.diagnose_pending_incidents` | `1200.0` | `-` | 1839e87f (2026-06-28) - feat(remediacao): contexto + diagnose_incident + cron (M7) |
| `engajar-clientes-diario` | `backend.worker.tasks.customer_engagement_task.engajar_clientes` | `86400.0` | `-` | 3b43143f (2026-06-28) - feat(engajamento): task engajar_clientes (gates+coletor+dedu |
| `harvest-moat-diario` | `backend.worker.tasks.moat_task.harvest_moat` | `86400.0` | `-` | fd392a77 (2026-06-29) - feat(moat): harvester harvest_moat (anonimiza + dedup, atrÃ¡ |
| `auto-semestral-diario` | `backend.worker.tasks.governance_task.auto_gerar_relatorios_semestrais` | `86400.0` | `-` | 0de48083 (2026-06-28) - feat(governanca): cron semestral idempotente + retenÃ§Ã£o CA |
| `arquivar-cadoc-worm-semanal` | `backend.worker.tasks.governance_task.arquivar_cadoc_worm` | `604800.0` | `-` | 0de48083 (2026-06-28) - feat(governanca): cron semestral idempotente + retenÃ§Ã£o CA |
| `check-validador-scr-semanal` | `backend.worker.tasks.validator_update_task.check_scr_validator_update` | `604800.0` | `-` | c596ff8d (2026-07-01) - feat(validador): Fase 3 â€” worker semanal detecta release n |

## task_routes manuais (20)

| padrao | fila |
|---|---|
| `backend.worker.tasks.alert_task.*` | `import.file` |
| `backend.worker.tasks.bacen_ciclo_task.*` | `import.file` |
| `backend.worker.tasks.backup_task.*` | `import.file` |
| `backend.worker.tasks.customer_engagement_task.*` | `import.file` |
| `backend.worker.tasks.distribution_task.*` | `import.file` |
| `backend.worker.tasks.governance_task.*` | `import.file` |
| `backend.worker.tasks.import_task.*` | `import.file` |
| `backend.worker.tasks.ingestion_task.*` | `import.file` |
| `backend.worker.tasks.moat_task.*` | `import.file` |
| `backend.worker.tasks.notification_task.*` | `import.file` |
| `backend.worker.tasks.ops_task.*` | `import.file` |
| `backend.worker.tasks.pecld_tasks.*` | `quality.assess` |
| `backend.worker.tasks.quality_task.*` | `quality.assess` |
| `backend.worker.tasks.radar_task.*` | `import.file` |
| `backend.worker.tasks.radar_web_task.*` | `import.file` |
| `backend.worker.tasks.remediacao_task.*` | `import.file` |
| `backend.worker.tasks.schema_migration_task.*` | `schema.migrate` |
| `backend.worker.tasks.tenant_purge_task.*` | `import.file` |
| `backend.worker.tasks.validate_task.*` | `cadoc.validate` |
| `backend.worker.tasks.validator_update_task.*` | `import.file` |

## task_routes derivadas das flow specs (7)

| task | fila |
|---|---|
| `backend.worker.tasks.cosif_tasks.*` | `import.file` |
| `backend.worker.tasks.engine3026_tasks.*` | `import.file` |
| `backend.worker.tasks.engine3026_tasks.consolidate_3026` | `cadoc.generate` |
| `backend.worker.tasks.engine3040_tasks.*` | `import.file` |
| `backend.worker.tasks.engine3044_tasks.*` | `import.file` |
| `backend.worker.tasks.engine3050_tasks.*` | `import.file` |
| `backend.worker.tasks.engine3050_tasks.consolidate_3050` | `cadoc.generate` |

## Tasks decoradas (55)

| task | modulo | l. | fila | origem da rota | enfileirada por | acks_late | time_limit | max_retries | autoretry_for |
|---|---|---:|---|---|---|:-:|:-:|:-:|:-:|
| `backend.worker.tasks.alert_task.check_deadlines` | `alert_task.py` | 16 | `import.file` | manual(glob) | beat | - | - | - | - |
| `backend.worker.tasks.alert_task.check_manifestacoes` | `alert_task.py` | 17 | `import.file` | manual(glob) | beat | - | - | - | - |
| `backend.worker.tasks.alert_task.check_quality_scores` | `alert_task.py` | 21 | `import.file` | manual(glob) | beat | - | - | - | - |
| `backend.worker.tasks.alert_task.check_report_due` | `alert_task.py` | 20 | `import.file` | manual(glob) | beat | - | - | - | - |
| `backend.worker.tasks.alert_task.check_schema_drift` | `alert_task.py` | 7 | `import.file` | manual(glob) | beat | - | - | - | - |
| `backend.worker.tasks.alert_task.check_stuck_jobs` | `alert_task.py` | 46 | `import.file` | manual(glob) | beat | - | - | - | - |
| `backend.worker.tasks.bacen_ciclo_task.processar_veredito` | `bacen_ciclo_task.py` | 3 | `import.file` | manual(glob) | rota | - | - | - | - |
| `backend.worker.tasks.backup_task.backup_validator_artifacts` | `backup_task.py` | 15 | `import.file` | manual(glob) | beat | - | - | - | - |
| `backend.worker.tasks.backup_task.check_backup_stale` | `backup_task.py` | 4 | `import.file` | manual(glob) | beat | - | - | - | - |
| `backend.worker.tasks.backup_task.run_backup` | `backup_task.py` | 39 | `import.file` | manual(glob) | beat | - | - | - | - |
| `backend.worker.tasks.backup_task.verify_latest_backup` | `backup_task.py` | 18 | `import.file` | manual(glob) | beat | - | - | - | - |
| `backend.worker.tasks.cosif_tasks.process_cosif_file` | `cosif_tasks.py` | 28 | `import.file` | spec(glob) | rota | - | - | - | - |
| `backend.worker.tasks.customer_engagement_task.engajar_clientes` | `customer_engagement_task.py` | 13 | `import.file` | manual(glob) | beat | - | - | - | - |
| `backend.worker.tasks.distribution_task.check_pending_acknowledgments` | `distribution_task.py` | 11 | `import.file` | manual(glob) | **ninguem** | - | - | - | - |
| `backend.worker.tasks.distribution_task.send_report_emails` | `distribution_task.py` | 13 | `import.file` | manual(glob) | rota | - | - | - | - |
| `backend.worker.tasks.engine3026_tasks.alert_prazo_3026` | `engine3026_tasks.py` | 38 | `import.file` | spec(glob) | beat | - | - | - | - |
| `backend.worker.tasks.engine3026_tasks.consolidate_3026` | `engine3026_tasks.py` | 31 | `cadoc.generate` | spec | rota | - | - | - | - |
| `backend.worker.tasks.engine3026_tasks.process_3026_file` | `engine3026_tasks.py` | 17 | `import.file` | spec(glob) | rota | - | - | - | - |
| `backend.worker.tasks.engine3040_tasks.alert_prazo_3040` | `engine3040_tasks.py` | 67 | `import.file` | spec(glob) | beat | - | - | - | - |
| `backend.worker.tasks.engine3040_tasks.consolidate_3040` | `engine3040_tasks.py` | 42 | `import.file` | spec(glob) | rota | - | - | - | - |
| `backend.worker.tasks.engine3040_tasks.process_3040_file` | `engine3040_tasks.py` | 35 | `import.file` | spec(glob) | rota | - | - | - | - |
| `backend.worker.tasks.engine3040_tasks.sftp_watch_3040` | `engine3040_tasks.py` | 93 | `import.file` | spec(glob) | beat | - | - | - | - |
| `backend.worker.tasks.engine3044_tasks.alert_fonte_pendente` | `engine3044_tasks.py` | 37 | `import.file` | spec(glob) | beat | - | - | - | - |
| `backend.worker.tasks.engine3044_tasks.alert_prazo_documento` | `engine3044_tasks.py` | 38 | `import.file` | spec(glob) | beat | - | - | - | - |
| `backend.worker.tasks.engine3044_tasks.consolidate_3044` | `engine3044_tasks.py` | 38 | `import.file` | spec(glob) | rota | - | - | - | - |
| `backend.worker.tasks.engine3044_tasks.process_3044_file` | `engine3044_tasks.py` | 35 | `import.file` | spec(glob) | rota | - | - | - | - |
| `backend.worker.tasks.engine3044_tasks.regenerate_partial_3044` | `engine3044_tasks.py` | 35 | `import.file` | spec(glob) | **ninguem** | - | - | - | - |
| `backend.worker.tasks.engine3044_tasks.sftp_watch` | `engine3044_tasks.py` | 92 | `import.file` | spec(glob) | beat | - | - | - | - |
| `backend.worker.tasks.engine3050_tasks.alert_prazo_3050` | `engine3050_tasks.py` | 57 | `import.file` | spec(glob) | beat | - | - | - | - |
| `backend.worker.tasks.engine3050_tasks.consolidate_3050` | `engine3050_tasks.py` | 34 | `cadoc.generate` | spec | rota | - | - | - | - |
| `backend.worker.tasks.engine3050_tasks.process_3050_file` | `engine3050_tasks.py` | 29 | `import.file` | spec(glob) | rota | - | - | - | - |
| `backend.worker.tasks.engine3050_tasks.sftp_watch_3050` | `engine3050_tasks.py` | 43 | `import.file` | spec(glob) | beat | - | - | - | - |
| `backend.worker.tasks.governance_task.arquivar_cadoc_worm` | `governance_task.py` | 42 | `import.file` | manual(glob) | beat | - | - | - | - |
| `backend.worker.tasks.governance_task.auto_gerar_relatorios_semestrais` | `governance_task.py` | 30 | `import.file` | manual(glob) | beat | - | - | - | - |
| `backend.worker.tasks.import_task.process_import` | `import_task.py` | 3 | `import.file` | manual(glob) | **ninguem** | - | - | - | - |
| `backend.worker.tasks.ingestion_task.check_ingestion` | `ingestion_task.py` | 2 | `import.file` | manual(glob) | beat | - | - | - | - |
| `backend.worker.tasks.moat_task.harvest_moat` | `moat_task.py` | 44 | `import.file` | manual(glob) | beat | - | - | - | - |
| `backend.worker.tasks.notification_task.send_notification` | `notification_task.py` | 12 | `import.file` | manual(glob) | task | - | - | - | - |
| `backend.worker.tasks.ops_task.backfill_sla_assign` | `ops_task.py` | 2 | `import.file` | manual(glob) | **ninguem** | - | - | - | - |
| `backend.worker.tasks.ops_task.check_obligation_deadlines` | `ops_task.py` | 2 | `import.file` | manual(glob) | beat | - | - | - | - |
| `backend.worker.tasks.ops_task.generate_obligations` | `ops_task.py` | 2 | `import.file` | manual(glob) | beat | - | - | - | - |
| `backend.worker.tasks.ops_task.sweep_sftp_processing` | `ops_task.py` | 4 | `import.file` | manual(glob) | beat | - | - | - | - |
| `backend.worker.tasks.pecld_tasks.compute_pecld` | `pecld_tasks.py` | 3 | `quality.assess` | manual(glob) | rota | - | - | - | - |
| `backend.worker.tasks.quality_task.assess_quality` | `quality_task.py` | 14 | `quality.assess` | manual(glob) | outro | - | - | - | - |
| `backend.worker.tasks.radar_task.assess_regulatory_change` | `radar_task.py` | 2 | `import.file` | manual(glob) | rota, task | - | - | - | - |
| `backend.worker.tasks.radar_task.check_regulatory_versions` | `radar_task.py` | 2 | `import.file` | manual(glob) | beat, rota | - | - | - | - |
| `backend.worker.tasks.radar_web_task.check_web_sources` | `radar_web_task.py` | 2 | `import.file` | manual(glob) | beat | - | - | - | - |
| `backend.worker.tasks.radar_web_task.web_sweep` | `radar_web_task.py` | 3 | `import.file` | manual(glob) | beat, rota | - | 960 | - | - |
| `backend.worker.tasks.remediacao_task.diagnose_incident` | `remediacao_task.py` | 2 | `import.file` | manual(glob) | rota | - | - | - | - |
| `backend.worker.tasks.remediacao_task.diagnose_pending_incidents` | `remediacao_task.py` | 2 | `import.file` | manual(glob) | beat | - | - | - | - |
| `backend.worker.tasks.schema_migration_task.migrate_tenant_schema` | `schema_migration_task.py` | 6 | `schema.migrate` | manual(glob) | **ninguem** | - | - | MAX_RETRIES | - |
| `backend.worker.tasks.schema_migration_task.sweep_tenant_schemas` | `schema_migration_task.py` | 22 | `schema.migrate` | manual(glob) | beat | - | - | - | - |
| `backend.worker.tasks.tenant_purge_task.purge_deleted_tenants` | `tenant_purge_task.py` | 2 | `import.file` | manual(glob) | beat | - | - | - | - |
| `backend.worker.tasks.validate_task.validate_submission` | `validate_task.py` | 3 | `cadoc.validate` | manual(glob) | **ninguem** | - | - | - | - |
| `backend.worker.tasks.validator_update_task.check_scr_validator_update` | `validator_update_task.py` | 32 | `import.file` | manual(glob) | beat | - | - | - | - |

## Tasks que ninguem enfileira (6)

- `backend.worker.tasks.distribution_task.check_pending_acknowledgments` - `backend/worker/tasks/distribution_task.py` (11 l., fila `import.file`)
- `backend.worker.tasks.engine3044_tasks.regenerate_partial_3044` - `backend/worker/tasks/engine3044_tasks.py` (35 l., fila `import.file`)
- `backend.worker.tasks.import_task.process_import` - `backend/worker/tasks/import_task.py` (3 l., fila `import.file`)
- `backend.worker.tasks.ops_task.backfill_sla_assign` - `backend/worker/tasks/ops_task.py` (2 l., fila `import.file`)
- `backend.worker.tasks.schema_migration_task.migrate_tenant_schema` - `backend/worker/tasks/schema_migration_task.py` (6 l., fila `schema.migrate`)
- `backend.worker.tasks.validate_task.validate_submission` - `backend/worker/tasks/validate_task.py` (3 l., fila `cadoc.validate`)
