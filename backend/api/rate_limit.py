"""Limiter slowapi compartilhado — extraído de main.py para evitar ciclo de import
(routes importam o limiter; main importa routes).

Storage no Redis para que o limite valha entre os múltiplos workers da API (uvicorn
``--workers N`` usa um processo por worker; um storage em memória contaria por worker e
tornaria o limite ineficaz). ``in_memory_fallback_enabled`` garante que, se o Redis estiver
indisponível, o limiter degrada para memória em vez de derrubar rotas críticas como o login."""

from slowapi import Limiter
from slowapi.util import get_remote_address

from backend.config.settings import get_settings

limiter = Limiter(
    key_func=get_remote_address,
    default_limits=["120/minute"],
    storage_uri=get_settings().redis_url,
    in_memory_fallback_enabled=True,
)
