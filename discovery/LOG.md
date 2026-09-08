# LOG do discovery

Registro de esforço por seção: quantos arquivos precisei abrir e quais comandos rodei.
O custo aqui é a métrica — mede o quanto o repositório **não se explica sozinho**.

Scripts reexecutáveis em `discovery/scripts/`. Todos rodam da raiz do repo.

| # | Seção | Arquivos abertos | Comandos/scripts |
|---|---|---:|---|
| 1 | Identidade do repo | 6 (`pyproject.toml`, `pytest.ini`, `frontend/package.json`, `infra/docker-compose.yml`, `CLAUDE.md`, `bitbucket-pipelines.yml`) | `ls`, `git log -1`, `git branch --show-current`. **Não existe `README.md` na raiz** — o "como rodar" só existe dentro do `CLAUDE.md`. |
| 2 | Mapa de módulos | 0 (tudo por script) | `discovery/scripts/modulos.py` |
| 3 | Grafo de dependências | 0 | `discovery/scripts/deps.py` |
| 4 | Contratos e dados | 4 (`backend/api/main.py`, `backend/flows/cadoc_registry.py`, `backend/engine/base.py`, `backend/config/settings.py`) | greps de `CREATE TABLE` em `migrations*/versions/`, `revision/down_revision`, `ls backend/worker/tasks` |
| 5 | Convenções | 5 (`backend/observability.py`, `backend/api/main.py`, `tests/conftest.py`, `backend/api/routes/data_sources.py`, `backend/storage/distribution_store.py`) | `discovery/scripts/convencoes.sh` + greps ad-hoc (SQL cru em rotas, `require_permission`, `print(`, docstring pt/en) |
| 6 | Arquivos exemplares | 4 (os dois acima + `backend/api/routes/engine3040.py` por tamanho, `backend/worker/app.py`) | `wc -l` sobre `routes/`, `storage/`, `worker/tasks/` |
| 7 | Testes | 2 (`tests/conftest.py`, `e2e/playwright.config.ts`) | `pytest -q --durations=15` (2×: sem e com env de DB), `discovery/scripts/cobertura_modulos.py`, script inline de "testes sem assert" |
| 8 | Processo e ferramentas | 5 (`.claude/settings.json`, 2 hooks, `bitbucket-pipelines.yml`, `deploy/deploy.sh`) | `find` por templates de PR/issue (**nenhum**), `ls .claude` |
| 9 | Histórico e pontos quentes | 0 | `discovery/scripts/git_hotspots.sh`, `discovery/scripts/coupling_rework.py` |
| 10–11 | Lacunas e perguntas | — | derivado das seções anteriores |

**Total de arquivos de código/config abertos: ~26.** Tudo o mais saiu de script.

## Perguntas que exigiram abrir mais de 5 arquivos ou script dedicado

1. *"Onde está a fronteira rota → serviço → store, e quantos fluxos a respeitam?"* — não há documento; só um script contando imports e SQL cru por rota resolveu.
2. *"Quantos módulos de produção não têm teste?"* — a convenção `tests/` espelha `backend/`, mas com exceções; precisou do `cobertura_modulos.py` com dois critérios (nome do arquivo + menção do caminho de import).
3. *"A suíte roda?"* — precisou de duas execuções e da leitura do `conftest.py` (linha 461) para descobrir que 726 testes se auto-pulam quando `REGULATORY_DB_PORT` não está setado. Nenhum doc menciona essa variável como gate.
4. *"Qual a cadeia de migrations vigente?"* — o `CLAUDE.md` cita migrations `0004–0007` que **não existem** no disco (a cadeia foi achatada em baselines `0001`). Só o `ls migrations_tenant/versions/` resolveu.
5. *"Que módulo depende de quê?"* — o grafo tem 113 ciclos; nenhuma camada está documentada como acíclica. Só o script mostrou isso.

## Bloqueios encontrados

- Não foi possível rodar os **726 testes dependentes de banco**: o Postgres local (`localhost:5433`, db `regulatory_reports`) está numa cadeia Alembic legada (`admin.alembic_version = '0007_document_dependencies'`) que o `migrations/env.py` recusa com `RuntimeError`. Criar um database descartável foi bloqueado pelo hook `guard_bash.py` e pelo classificador de permissão. Registrado como limitação, não contornado.
