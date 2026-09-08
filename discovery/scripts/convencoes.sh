#!/bin/sh
# Contagens de evidencia para a secao de convencoes.
echo "== rotas: arquivos em backend/api/routes"; ls backend/api/routes/*.py | wc -l
echo "== stores: backend/storage/*_store.py"; ls backend/storage/*_store.py | wc -l
echo "== stores que usam psycopg direto (cursor/execute)"; grep -lE '\.execute\(' backend/storage/*.py | wc -l
echo "== rotas com SQL cru (SELECT/INSERT/UPDATE em string)"; grep -lEi '"""\s*(SELECT|INSERT|UPDATE|DELETE)|\"(SELECT|INSERT|UPDATE|DELETE) ' backend/api/routes/*.py | tee /dev/stderr | wc -l
echo "== rotas que importam algum *_store"; grep -l 'from backend.storage' backend/api/routes/*.py | wc -l
echo "== rotas que importam backend.services"; grep -l 'from backend.services' backend/api/routes/*.py | wc -l
echo "== APIRouter declarados"; grep -h 'APIRouter(' backend/api/routes/*.py | wc -l
echo "== HTTPException usados"; grep -rho 'HTTPException' backend | wc -l
echo "== excecoes custom (class .*Error/Exception) backend"; grep -rhnE '^class \w+(Error|Exception)\(' backend | sort | uniq -c | sort -rn
echo "== logging: import logging"; grep -rl '^import logging\|^from logging' backend --include=*.py | wc -l
echo "== print( em backend"; grep -rn 'print(' backend --include=*.py | wc -l
echo "== structlog/loguru"; grep -rl 'structlog\|loguru' backend --include=*.py | wc -l
echo "== settings usados (get_settings)"; grep -rl 'get_settings\|from backend.config' backend --include=*.py | wc -l
echo "== BaseModel (pydantic) declaracoes"; grep -rhc 'class .*(BaseModel)' backend --include=*.py | paste -sd+ | bc
echo "== BaseModel por modulo"; grep -rlE 'class \w+\(BaseModel\)' backend --include=*.py | cut -d/ -f2 | sort | uniq -c | sort -rn
echo "== Depends( uso"; grep -rho 'Depends(' backend/api | wc -l
echo "== require_role/require_permission"; grep -rho 'require_role\|require_permission' backend/api | sort | uniq -c
echo "== retry/timeout/idempot"; grep -rniE '\bretry\b|\btimeout\b|idempot' backend --include=*.py -l | cut -d/ -f2 | sort | uniq -c | sort -rn
echo "== docstrings (arquivos py com docstring de modulo)"; grep -rl '^"""' backend --include=*.py | wc -l
echo "== total arquivos py backend"; find backend -name '*.py' | wc -l
echo "== safe_schema_name usos"; grep -rn 'safe_schema_name' backend --include=*.py | wc -l
echo "== f-string em SQL (risco)"; grep -rnE '(SELECT|INSERT|UPDATE|DELETE)[^"]*\{' backend --include=*.py | wc -l
