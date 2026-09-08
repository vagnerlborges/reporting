# LOG do Discovery 2 (frontend → API → worker)

Registro de esforço por seção. Como no `LOG.md`, o custo é a métrica: quanto o repo
**não se explica sozinho**. Scripts em `discovery/scripts/`, todos rodam da raiz.

| # | Seção | Arquivos abertos à mão | Comandos / scripts |
|---|---|---:|---|
| 1 | Página → endpoints | 5 (`frontend/lib/api.ts` + 4 páginas para conferir falso negativo) | `scripts/paginas.py` (2 execuções — a 1ª perdeu chamadas com `${API_BASE}/api/...`) |
| 2 | Endpoint → consumidores | 0 | `scripts/endpoints.py` (AST dos decoradores) + `scripts/mortos.py` (2ª passagem sobre texto bruto) |
| 3 | Worker | 2 (`backend/worker/app.py` trechos) | `scripts/tasks.py` (4 execuções — ver "retrabalho do script" abaixo) |
| 4 | Duplicação entre motores | 2 (`backend/engine/base.py`, `backend/engine/cadoc3040.py`) | `scripts/motores.py` + greps de `dispatch`, `queue_overrides`, `NotImplementedError` |
| 4b | Plugins e quality | 2 (`backend/quality/dimensions.py`, um evaluator) | `scripts/plugins.py`, `scripts/quality.py` |
| 5 | Volume e dado massivo | 0 | `scripts/volume.py` (psycopg direto no Postgres local) + greps de `COPY`/`executemany`/`MAX_UPLOAD_BYTES` |
| 6 | Resumo por informe | 0 | `scripts/resumo.py` + `git log` escopado por diretório de motor |

**Total de arquivos abertos à mão: ~11.** O resto saiu de script.

## Retrabalho do próprio levantamento (o que o repo escondeu)

Cada item abaixo custou uma re-execução de script porque a estrutura real diverge da esperada:

1. **`paginas.py` (1ª vs 2ª execução).** A regex `["'\`](/api/...)` perdia 14 endpoints porque
   parte do front chama `` `${API_BASE}/api/auth/forgot-password` `` — o path não começa na
   aspa. Convivem dois estilos de chamada: `apiFetch("/api/...")` (dominante) e
   `fetch(`${API_BASE}/api/...`)`. 210 → 224 endpoints distintos após corrigir.
2. **`tasks.py` (4 execuções).** `task_routes` e `beat_schedule` **não** são kwargs do
   construtor `Celery(...)` — vêm em `celery_app.conf.update(...)`. Enquanto a detecção assumia
   o construtor, o beat vinha vazio e 37 tasks apareciam como órfãs. Número real: **6**.
3. **`tasks.py`, rotas derivadas.** `derive_task_routes` devolve **padrões wildcard**
   (`...engine3040_tasks.*`), não nomes de task. Sem aplicar glob também à tabela derivada,
   16 tasks de motor apareciam como "SEM ROTA" — falso.
4. **`endpoints.py` → `mortos.py`.** Dos 23 endpoints "sem consumidor" da 1ª passagem,
   **10 eram falso negativo**: o front monta o path com literal de informe embutido
   (`/api/painel/3040/${p}/aprovar`) ou cola a query no path (`events.csv?${qs}`). Só uma 2ª
   passagem com o path virando regex sobre o texto bruto fechou o número em **13**.
5. **`quality.py`.** As 12 dimensões não se identificam pelo nome da função: as funções são
   `evaluate_completeness` (inglês) e a dimensão é `"completude"` (português). O vínculo real é o
   literal `"dimension": "<nome>"` **dentro** do corpo. Nenhum índice liga os dois.
6. **`motores.py`.** O bundle do COSIF é `backend/engine/cosif.py`, não
   `backend/engine/cadoccosif.py` — o padrão `cadoc<informe>` vale para 4 dos 5.

## Perguntas que exigiram script dedicado (não davam para responder lendo)

- "Qual informe está mais migrado para o `CadocEngine`?" — todos os 5 têm bundle e todos os 5
  têm rota derivada, mas **só o 3026 chama `dispatch()` em runtime**. Ler os bundles sugere
  "migrado"; só o grep de `get_engine_registry().dispatch` mostra que 4 deles são fachada de
  roteamento.
- "Quanto de um motor é cópia de outro?" — a percepção (e o `CLAUDE.md`) diz "~900 linhas
  duplicadas por CADOC"; a medida por `difflib` dá **6% a 27%**, e a maior parte da
  similaridade está em rota de upload/download, não no núcleo.
- "O que está morto?" — 13 endpoints e 6 tasks, nenhum marcado como deprecated no código.
- "Onde o dado bruto entra?" — a tabela `raw_data` existe no baseline mas só é lida por um
  `COUNT(*)`; o landing real é `cadocNNNN_mov_*`.

## Bloqueios

- **Sem acesso read-only ao QAS.** O Postgres do QAS é RDS em VPC privada (o `CLAUDE.md`
  registra que o banco nunca foi exposto publicamente); não há credencial nem túnel neste
  ambiente. A volumetria de produção **não foi medida** — só o banco local de dev, que está
  praticamente vazio (3,5 MB no maior schema de tenant).
- **Sem amostra real de arquivo de cliente** no repo. As únicas entradas versionadas são as
  fixtures de e2e (23 KB no maior). O tamanho real de entrada só aparece indiretamente:
  `MAX_UPLOAD_BYTES = 100 MB` nas rotas e o comentário de medição em `worker/app.py`
  ("2,9–4,4 GB no 3040 com 500 mil operações").
