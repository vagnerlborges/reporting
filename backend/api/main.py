"""FastAPI application entry point."""

from __future__ import annotations

import logging
import traceback
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from slowapi.middleware import SlowAPIMiddleware

from backend.api.rate_limit import limiter
from backend.config.settings import get_settings
from backend.observability import report_error
from backend.storage.postgres import ensure_admin_schema
from backend.api.middleware.workspace import WorkspaceMiddleware
from backend.api.routes import auth, tenants, users, setup
from backend.api.routes import quality, lineage, dictionary, audit
from backend.api.routes import policy, corrective, bcb, distribution
from backend.api.routes import public_reports
from backend.api.routes import admin
from backend.api.routes import data_sources
from backend.api.routes import validacao
from backend.api.routes import engine3044
from backend.api.routes import engine3040
from backend.api.routes import engine3050
from backend.api.routes import engine3026
from backend.api.routes import painel
from backend.api.routes import reportes
from backend.api.routes import reconciliation
from backend.api.routes import retification
from backend.api.routes import bacen_ciclo
from backend.api.routes import manifestacoes
from backend.api.routes import governance
from backend.api.routes import calendario
from backend.api.routes import lgpd
from backend.api.routes import sftp
from backend.api.routes import onboarding
from backend.api.routes import operations
from backend.api.routes import validator
from backend.api.routes import moat
from backend.api.routes import data_contract
from backend.api.routes import pecld
from backend.api.routes import cosif
from backend.api.routes import correlations
from backend.api.routes import cosif_plano
from backend.api.routes import document_types
from backend.api.routes import schema_versions
from backend.api.routes import telemetry

settings = get_settings()


API_DESCRIPTION = """
API de governança e processamento de **informes legais (CADOCs)** ao Banco Central do Brasil,
multi-tenant, alinhada à **Resolução Conjunta nº 18/2025 (RC 18)**.

## Autenticação
`POST /api/auth/login` com `{email, password}` devolve `access_token` + `refresh_token` (JWT).
Em contas com múltiplos tenants, o login devolve `requires_tenant_selection`; repita o POST com
`tenant_id`. Envie o token em `Authorization: Bearer <access_token>`. Renove em `POST /api/auth/refresh`.

## Autorização
Permissões granulares por papel (`require_permission`): `cadoc:*`, `import:*`, `approval:*`,
`quality:*`, `report:*`, `director:manage`, `datasource:*`, `dictionary:*`, `user:*`, `audit:*`.
Papéis: `dattos_admin`, `tenant_admin`, `manager`, `analyst`, `it_admin`, `auditor`.

## Convenções
- Datas/competência: `AAAA-MM-DD` (data) e `AAAA-MM` (competência). IDs: UUID v4.
- Erros: `HTTPException` com `{detail}` (401 não-autenticado, 403 sem permissão/tenant suspenso,
  404 inexistente, 409 conflito, 422 entrada inválida).
- Limite de requisições: 120/min por IP (Slowapi).

Documentação interativa em **`/docs`** (Swagger) e **`/redoc`**; esquema em **`/openapi.json`**.
"""

TAGS_METADATA = [
    {"name": "auth", "description": "Login, seleção de tenant e refresh de token."},
    {"name": "tenants", "description": "Cadastro e dados do próprio tenant."},
    {"name": "users", "description": "Usuários do tenant e troca da própria senha."},
    {
        "name": "setup",
        "description": "Estado do ciclo de setup do produto (etapas cliente + Dattos).",
    },
    {
        "name": "engine3040",
        "description": "Motor CADOC 3040 (posição mensal da carteira): status, upload, geração e downloads.",
    },
    {
        "name": "engine3044",
        "description": "Motor CADOC 3044 (movimento diário de crédito): status, consolidação, exclusões e downloads.",
    },
    {
        "name": "engine3050",
        "description": "Motor CADOC 3050 (DocTXB semanal, leiaute V11): status, upload, consolidação e download.",
    },
    {
        "name": "engine3026",
        "description": "Motor CADOC 3026 (conglomerados econômicos, anual): status, upload, consolidação e download.",
    },
    {
        "name": "quality",
        "description": "RC 18 — dashboard das 12 dimensões de qualidade, pesos, relatórios e diretor responsável.",
    },
    {
        "name": "data-sources",
        "description": "Fontes de dados de entrada dos CADOCs (incl. cadoc_3040/cadoc_3044).",
    },
    {
        "name": "dictionary",
        "description": "Dicionário de dados por tipo de CADOC (RC 18).",
    },
    {
        "name": "lineage",
        "description": "Linhagem/rastreabilidade das submissões (RC 18).",
    },
    {"name": "audit", "description": "Eventos de auditoria."},
    {
        "name": "policy",
        "description": "Política de Qualidade (PQI): versões e revisões.",
    },
    {
        "name": "corrective",
        "description": "Irregularidades, medidas saneadoras e planos de ação (RC 18).",
    },
    {
        "name": "bcb",
        "description": "Comunicações de impropriedades ao Banco Central (RC 18, Art. 9º).",
    },
    {
        "name": "reports",
        "description": "Distribuição de relatórios (destinatários e envios).",
    },
    {
        "name": "admin",
        "description": "Console Dattos: gestão cross-tenant, impersonação auditada e suspensão.",
    },
]


@asynccontextmanager
async def lifespan(app: FastAPI):
    ensure_admin_schema()
    yield


log = logging.getLogger(__name__)

# Seg #10: em produção, não expor o mapa de endpoints (Swagger/ReDoc/OpenAPI).
# Em dev/test/local/ci mantém a documentação interativa.
_docs_kwargs = (
    {}
    if settings.is_dev_environment
    else {"docs_url": None, "redoc_url": None, "openapi_url": None}
)

app = FastAPI(
    title="Dattos Reportes Regulatórios",
    description=API_DESCRIPTION,
    version="0.1.0",
    contact={"name": "Dattos", "url": "https://reporting.dattos.solutions"},
    openapi_tags=TAGS_METADATA,
    lifespan=lifespan,
    **_docs_kwargs,
)
app.state.limiter = limiter
app.add_middleware(SlowAPIMiddleware)
app.add_middleware(WorkspaceMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins.split(","),
    allow_credentials=True,
    # P2-6: com credentials, "*" é não-conforme (o browser rejeita) e amplo demais.
    # Restringe aos métodos/headers realmente usados pela API.
    allow_methods=["GET", "POST", "PATCH", "PUT", "DELETE", "OPTIONS"],
    # x-workspace-id é lido pelo WorkspaceMiddleware → precisa estar no allowlist.
    allow_headers=["Authorization", "Content-Type", "x-workspace-id"],
)

# REP-34: exceção não tratada vira erro funcional no Loki (source=API). O handler
# preserva a resposta 500 padrão — telemetria não muda contrato de API.
@app.exception_handler(Exception)
async def _report_unhandled(request: Request, exc: Exception):
    try:
        report_error(
            source="API",
            message=str(exc),
            path=request.url.path,
            exception=type(exc).__name__,
            traceback="".join(traceback.format_exception(exc))[:8000],
            request_id=request.headers.get("x-request-id"),
        )
    except Exception:  # nunca mascarar o erro original
        logging.getLogger(__name__).warning("falha ao reportar erro ao Loki", exc_info=True)
    return JSONResponse(status_code=500, content={"detail": "Internal Server Error"})


app.include_router(telemetry.router)
app.include_router(auth.router)
app.include_router(tenants.router)
app.include_router(users.router)
app.include_router(setup.router)
app.include_router(reportes.router)
app.include_router(quality.router)
app.include_router(lineage.router)
app.include_router(dictionary.router)
app.include_router(audit.router)
app.include_router(policy.router)
app.include_router(corrective.router)
app.include_router(bcb.router)
app.include_router(distribution.router)
app.include_router(public_reports.router)
app.include_router(admin.router)
app.include_router(data_sources.router)
app.include_router(validacao.router)
app.include_router(engine3044.router)
app.include_router(engine3040.router)
app.include_router(engine3050.router)
app.include_router(engine3026.router)
app.include_router(validator.router)
app.include_router(validator.admin_router)
app.include_router(painel.router)
app.include_router(reconciliation.router)
app.include_router(retification.router)
app.include_router(bacen_ciclo.router)
app.include_router(manifestacoes.router)
app.include_router(governance.router)
app.include_router(calendario.router)
app.include_router(lgpd.router)
app.include_router(sftp.router)
app.include_router(onboarding.router)
app.include_router(operations.router)
app.include_router(moat.router)
app.include_router(data_contract.router)
app.include_router(pecld.router)
app.include_router(cosif.router)
app.include_router(correlations.router)
app.include_router(cosif_plano.router)
app.include_router(cosif_plano.admin_router)
app.include_router(document_types.router)
app.include_router(schema_versions.router)
app.include_router(schema_versions.support_router)


@app.get("/health")
async def health() -> dict:
    """Liveness: a aplicação está de pé (não checa dependências)."""
    return {"status": "ok"}


@app.get("/ready")
async def ready():
    """Readiness: checa as dependências reais (DB, Redis, broker). 503 se alguma falha."""
    from fastapi.responses import JSONResponse

    checks: dict[str, str] = {}
    ok = True

    try:
        from backend.storage.postgres import get_connection

        with get_connection() as conn:
            conn.execute("SELECT 1")
        checks["database"] = "ok"
    except Exception:  # noqa: BLE001
        log.exception("readiness: database check failed")
        checks["database"] = "error"
        ok = False

    try:
        import redis

        redis.Redis.from_url(settings.redis_url, socket_connect_timeout=2).ping()
        checks["redis"] = "ok"
    except Exception:  # noqa: BLE001
        log.exception("readiness: redis check failed")
        checks["redis"] = "error"
        ok = False

    try:
        from backend.worker.app import celery_app

        conn = celery_app.connection()
        conn.ensure_connection(max_retries=1, timeout=2)
        conn.release()
        checks["broker"] = "ok"
    except Exception:  # noqa: BLE001
        log.exception("readiness: broker check failed")
        checks["broker"] = "error"
        ok = False

    return JSONResponse(
        status_code=200 if ok else 503,
        content={"status": "ready" if ok else "degraded", "checks": checks},
    )
