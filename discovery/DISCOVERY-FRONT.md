# Discovery 2 — mapa frontend → API → worker

Continuação do discovery anterior (`discovery/DISCOVERY.md`). Mesmas regras: nada de corpo de código, evidência com caminho/contagem, `[explícito]`/`[inferido]`, scripts reexecutáveis em `discovery/scripts/`, nada de segredo. Registrar esforço em `discovery/LOG2.md`. Saída em `discovery/FRONT.md` (≤ 600 linhas) + tabelas em `discovery/data/`.

Objetivo: decidir por número (não por palpite) qual informe migra primeiro para o pipeline unificado e quais endpoints/tasks estão mortos.

## 1. Página → endpoints
Para cada `frontend/app/**/page.tsx` (e componentes que ela importa de `components/`): rota da página, lista de endpoints chamados (grep por `fetch(`, `/api/`, clientes em `lib/api*`), tipos de `lib/types/*.ts` usados. Salvar em `data/paginas.md`.

## 2. Endpoint → consumidores e dependências
Para cada função de rota em `backend/api/routes/*.py`: método + path, quais páginas o chamam (inverso do item 1), se aparece em `e2e/tests/**`, quais stores importa, quais tasks enfileira (`.delay(`, `.apply_async(`, `send_task`). Salvar em `data/endpoints.md`.

Listar explicitamente: **endpoints sem consumidor** (nem página, nem e2e, nem outro backend) e **páginas que chamam endpoint inexistente**.

## 3. Worker — o que roda e quando
- `beat_schedule` completo de `backend/worker/app.py`: nome, cron/intervalo, task, fila, e último commit que alterou a entrada (`git log -L` ou blame).
- `task_routes` completo: task → fila. Marcar quais vêm de `derive_task_routes` (specs) e quais são manuais.
- Para cada task decorada (55): módulo, fila, quem a enfileira (rota / outra task / beat / ninguém), se tem `acks_late`, `time_limit`, `max_retries` ou `autoretry_for` configurados. Salvar em `data/tasks.md`.
- **Tasks que ninguém enfileira.**

## 4. Duplicação entre motores
Para `engine3040_tasks.py`, `engine3044_tasks.py`, `engine3050`, `engine3026` (tasks e rotas):
- Lista de funções por arquivo com assinatura e nº de linhas.
- Por script (ex.: `difflib` sobre corpo normalizado, ou hash de AST sem nomes), pares de funções com similaridade > 70% entre motores. Percentual de linhas de cada motor que tem equivalente em outro motor.
- Quais dessas funções já têm equivalente em `backend/engine/base.py` (`CadocEngine`/`EngineSteps`). Tabela: informe × etapa do pipeline × (usa base | copiado | não existe).

## 4b. Anatomia dos plugins e do quality
Para cada `backend/plugins/cadoc_*/`: listar módulos e classificar cada função/classe em **parser de entrada**, **regra de negócio/preenchimento**, **gerador de saída**, **validação externa** ou **outro**. Marcar quais são específicas do informe e quais poderiam ser genéricas (mesma lógica aparece em 2+ plugins). Salvar em `data/plugins.md`.

Para `backend/quality/`: listar as 12 dimensões com módulo, o que cada uma verifica e se depende de algo específico de informe (import de `flows`, `plugins`, `api`, `worker`, literal `"3040"` etc.) ou opera sobre dado tabular genérico. Listar os 7 imports de saída do pacote (`quality -> api/flows/plugins/...`) com arquivo e motivo aparente.

Existe hoje algum batimento/conciliação entre datasets ou entre informes (grep por `concilia`, `batimento`, `cruza`, `reconcil`)? Onde, e o que compara.

## 5. Volume e dado massivo
- Para `raw_data`, `account_entries` e as 5 maiores tabelas do schema de tenant: `SELECT count(*)` e `pg_total_relation_size` por tenant no banco local de dev e, **se houver acesso read-only**, no QAS. Se não houver acesso, dizer.
- Tamanho médio e máximo dos arquivos de entrada por informe (bucket ou pasta local de exemplo, se existir).
- Onde no código o dado bruto entra no Postgres (`INSERT INTO raw_data`, `COPY`) e onde é lido para processamento — caminhos e contagem.

## 6. Resumo para decisão
Uma tabela por informe: nº de páginas do front, nº de endpoints, nº de tasks, linhas de motor (rota + task), % copiado de outro motor, % já em `CadocEngine`, volume médio de entrada, último commit de feature. Sem recomendação — só o número.