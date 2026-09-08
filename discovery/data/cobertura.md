# Modulos de producao sem teste correspondente

Criterio: nao existe `tests/**/test_<stem>.py` E o caminho `backend.<modulo>` nao e mencionado em nenhum arquivo de teste.

- arquivos .py em `backend/` (sem `__init__`): **330**
- sem `test_<stem>.py`: **112**
- sem teste E sem mencao: **31**


## `backend/api` (14)

- `backend/api/middleware/workspace.py`
- `backend/api/routes/bcb.py`
- `backend/api/routes/corrective.py`
- `backend/api/routes/distribution.py`
- `backend/api/routes/document_types.py`
- `backend/api/routes/governance.py`
- `backend/api/routes/manifestacoes.py`
- `backend/api/routes/policy.py`
- `backend/api/routes/public_reports.py`
- `backend/api/routes/reportes.py`
- `backend/api/routes/retification.py`
- `backend/api/routes/schema_versions.py`
- `backend/api/routes/sftp.py`
- `backend/api/routes/telemetry.py`

## `backend/demo` (9)

- `backend/demo/blocks/audit.py`
- `backend/demo/blocks/calendar.py`
- `backend/demo/blocks/communication.py`
- `backend/demo/blocks/governance.py`
- `backend/demo/blocks/quality.py`
- `backend/demo/blocks/sources.py`
- `backend/demo/blocks/treatment.py`
- `backend/demo/blocks/users.py`
- `backend/demo/deadlines.py`

## `backend/services` (3)

- `backend/services/approval_controls.py`
- `backend/services/current_document.py`
- `backend/services/data_source_folders.py`

## `backend/worker` (2)

- `backend/worker/tasks/import_task.py`
- `backend/worker/tasks/sftp_rejection.py`

## `backend/cli` (1)

- `backend/cli/check_drift.py`

## `backend/plugins` (1)

- `backend/plugins/cadoc_3026/anexo11.py`

## `backend/storage` (1)

- `backend/storage/schema_version_gateway.py`
