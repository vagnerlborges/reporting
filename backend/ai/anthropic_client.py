"""Cliente Anthropic fino e injetável. Degrada graciosamente sem chave.

O import do SDK `anthropic` é PREGUIÇOSO: o caminho sem-chave não importa nada,
então testes locais não precisam do pacote instalado.
"""

from __future__ import annotations

import json
import logging
import os
from functools import lru_cache
from typing import Optional, Protocol

from backend.config.settings import get_settings

logger = logging.getLogger(__name__)


@lru_cache(maxsize=8)
def _criar_cliente(api_key: str):
    """Cria (uma vez por chave) o cliente Anthropic, com tracing LangSmith se configurado (REP-2).

    Tracing nunca pode derrubar uma chamada de IA: sem chave ou sem o pacote
    `langsmith`, retorna o cliente puro. O lru_cache garante que a exportação
    das envs LANGSMITH_* e o wrap acontecem uma única vez por processo.
    """
    import anthropic

    client = anthropic.Anthropic(api_key=api_key)
    s = get_settings()
    if not s.langsmith_api_key:
        return client
    try:
        os.environ["LANGSMITH_TRACING"] = "true"
        os.environ["LANGSMITH_API_KEY"] = s.langsmith_api_key
        if s.langsmith_project:
            os.environ["LANGSMITH_PROJECT"] = s.langsmith_project
        from langsmith.wrappers import wrap_anthropic

        return wrap_anthropic(client)
    except Exception as exc:  # noqa: BLE001 — tracing é opcional
        logger.warning("LangSmith indisponível, seguindo sem tracing: %s", exc)
        return client


def _extrair_json(texto: str) -> Optional[dict]:
    """Extrai o primeiro objeto JSON balanceado do texto (tolerante a prosa ao redor)."""
    inicio = texto.find("{")
    if inicio < 0:
        return None
    profundidade = 0
    for i in range(inicio, len(texto)):
        if texto[i] == "{":
            profundidade += 1
        elif texto[i] == "}":
            profundidade -= 1
            if profundidade == 0:
                try:
                    return json.loads(texto[inicio : i + 1])
                except ValueError:
                    return None
    return None


class LLMClient(Protocol):
    def structured_call(
        self, system: str, user: str, schema: dict
    ) -> Optional[dict]: ...


class AnthropicClient:
    """Chamada estruturada (JSON schema) ao modelo Anthropic. Retorna None se sem chave/erro."""

    def __init__(self, api_key: str, model: str) -> None:
        self._api_key = api_key
        self._model = model

    def structured_call(self, system: str, user: str, schema: dict) -> Optional[dict]:
        if not self._api_key:
            return None
        try:
            client = _criar_cliente(self._api_key)
            resp = client.messages.create(
                model=self._model,
                max_tokens=16000,
                system=system,
                messages=[{"role": "user", "content": user}],
                output_config={"format": {"type": "json_schema", "schema": schema}},
            )
            for block in resp.content:
                if getattr(block, "type", None) == "text":
                    return json.loads(block.text)
            return None
        except Exception as exc:  # noqa: BLE001 — LLM nunca pode derrubar o detector
            logger.warning("structured_call falhou: %s", exc)
            return None

    def research_call(
        self, system: str, user: str, schema: dict, max_rounds: int = 3
    ) -> Optional[dict]:
        """Pesquisa web agêntica (web_search/web_fetch) com saída JSON. None sem chave/erro.

        `max_uses` limita as buscas/leituras para caber no time-limit do worker.
        """
        if not self._api_key:
            return None
        try:
            client = _criar_cliente(self._api_key)
            tools = [
                {"type": "web_search_20260209", "name": "web_search", "max_uses": 5},
                {"type": "web_fetch_20260209", "name": "web_fetch", "max_uses": 5},
            ]
            user_full = (
                user + "\n\nResponda APENAS com um objeto JSON conforme o schema "
                "fornecido (sem texto fora do JSON)."
            )
            messages = [{"role": "user", "content": user_full}]
            for _ in range(max_rounds):
                resp = client.messages.create(
                    model=self._model,
                    max_tokens=16000,
                    system=system,
                    messages=messages,
                    tools=tools,
                )
                if getattr(resp, "stop_reason", None) == "pause_turn":
                    messages = [
                        {"role": "user", "content": user_full},
                        {"role": "assistant", "content": resp.content},
                    ]
                    continue
                for block in resp.content:
                    if getattr(block, "type", None) == "text":
                        return _extrair_json(block.text)
                return None
            return None
        except Exception as exc:  # noqa: BLE001 — LLM nunca derruba o detector
            logger.warning("research_call falhou: %s", exc)
            return None
