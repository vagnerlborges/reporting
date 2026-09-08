"""Cliente Firecrawl fino e injetável (busca+scrape → markdown enxuto). Degrada sem chave.

Usa a API REST /v2/search via requests (sem SDK extra). Trunca o markdown por resultado
para controlar o orçamento de tokens da varredura.
"""

from __future__ import annotations

import logging
from typing import Optional, Protocol

logger = logging.getLogger(__name__)

_ENDPOINT = "https://api.firecrawl.dev/v2/search"


class WebSearcher(Protocol):
    def search(self, query: str, limit: int = 5,
               max_chars: int = 1500) -> list[dict]:
        ...


class FirecrawlClient:
    """Busca web com conteúdo em markdown. Retorna [] se sem chave/erro."""

    def __init__(self, api_key: str) -> None:
        self._api_key = api_key

    def search(self, query: str, limit: int = 5, max_chars: int = 1500) -> list[dict]:
        """Retorna [{'url','title','markdown'}] (markdown truncado em max_chars). [] sem chave/erro."""
        if not self._api_key:
            return []
        try:
            import requests
            resp = requests.post(
                _ENDPOINT,
                headers={"Authorization": f"Bearer {self._api_key}",
                         "Content-Type": "application/json"},
                json={"query": query[:500], "limit": limit,
                      "scrapeOptions": {"formats": [{"type": "markdown"}]}},
                timeout=(5, 60),
            )
            resp.raise_for_status()
            data = (resp.json() or {}).get("data") or {}
            web = data.get("web") or []
            out = []
            for r in web[:limit]:
                md = (r.get("markdown") or r.get("description") or "")[:max_chars]
                out.append({"url": r.get("url", ""), "title": r.get("title", ""),
                            "markdown": md})
            return out
        except Exception as exc:  # noqa: BLE001 — firecrawl nunca derruba a varredura
            logger.warning("firecrawl.search falhou: %s", exc)
            return []
