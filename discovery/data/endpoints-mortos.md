# Endpoints sem consumidor - confirmados

Gerado por `discovery/scripts/mortos.py`.

Candidatos da 1a passagem: **23**. Falsos negativos descartados na 2a: **10**. Confirmados: **13**.

## Confirmados sem nenhum consumidor

| metodo | path | modulo:funcao | l. |
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

## Descartados (achados na 2a passagem, no texto bruto)

| metodo | path |
|---|---|
| GET | `/api/audit/events.csv` |
| GET | `/api/bcb/communications/{}` |
| PUT | `/api/bcb/communications/{}` |
| GET | `/api/manifestacoes/{}` |
| POST | `/api/painel/{}/{}/aprovar` |
| POST | `/api/painel/{}/{}/concluir` |
| GET | `/api/policy/versions/{}` |
| GET | `/api/policy/reviews/{}` |
| POST | `/api/public/reports/ack/{}/{}/confirm` |
| GET | `/api/retification/{}/3042` |
