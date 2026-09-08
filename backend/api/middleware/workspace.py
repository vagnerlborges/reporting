"""Workspace middleware — injects workspace_id from request header into state."""

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request


class WorkspaceMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        ws_id = request.headers.get("x-workspace-id", "").strip() or None
        request.state.workspace_id = ws_id
        return await call_next(request)
