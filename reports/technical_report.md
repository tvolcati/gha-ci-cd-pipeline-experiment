# Relatorio Tecnico: Analise de Pipeline CI/CD com GitHub Actions

<p align="center">
  <a href="#resumo-executivo"><img alt="Resumo" src="https://img.shields.io/badge/Resumo-1f6feb?style=for-the-badge"></a>
  <a href="#contexto-e-briefing"><img alt="Contexto" src="https://img.shields.io/badge/Contexto-238636?style=for-the-badge"></a>
  <a href="#stack-e-arquitetura"><img alt="Stack" src="https://img.shields.io/badge/Stack-8957e5?style=for-the-badge"></a>
  <a href="#estrutura-do-projeto"><img alt="Estrutura" src="https://img.shields.io/badge/Estrutura-f78166?style=for-the-badge"></a>
  <a href="#evidencias-reais"><img alt="Evidências" src="https://img.shields.io/badge/Evid%C3%AAncias-d29922?style=for-the-badge"></a>
  <a href="#graficos-anexados"><img alt="Gráficos" src="https://img.shields.io/badge/Gr%C3%A1ficos-0969da?style=for-the-badge"></a>
  <a href="#roteiro-de-avaliacao"><img alt="Avaliação" src="https://img.shields.io/badge/Avalia%C3%A7%C3%A3o-57606a?style=for-the-badge"></a>
</p>

## Resumo Executivo

Este projeto instrumenta um pipeline CI/CD real no GitHub Actions para medir tempo total de workflow, duração por job, comportamento dos testes, sucesso/falha, efeito de cache e impacto de paralelismo. O experimento foi executado com 12 variações controladas e consolidado em base estruturada, gráficos e análise crítica.

Indicadores principais:

- 12 execuções reais do GitHub Actions
- média do workflow: `39,42s`
- pior caso: `57s` com jobs sequenciais
- melhor caso: `33s` no run com falha induzida
- média de `tests`: `25,5s`
- média de `lint`: `22,0s`
- taxa de sucesso: `11/12`

## Contexto E Briefing

### O que foi pedido na atividade

A atividade exigia:

- construir ou adaptar um pipeline CI/CD no GitHub Actions
- incluir instalação de dependências, lint ou análise estática, testes automatizados, artefatos e coleta de métricas
- executar o pipeline no mínimo 12 vezes com variações controladas
- gerar base em `CSV` ou `JSON` por meio de script Python próprio
- produzir pelo menos 4 gráficos
- elaborar um relatório técnico com análise crítica

### O que foi entregue neste repositório

- pipeline principal em [`.github/workflows/ci-experiment.yml`](../.github/workflows/ci-experiment.yml)
- projeto Python mínimo com testes em [`src/`](../src/) e [`tests/`](../tests/)
- coletor de métricas em [`scripts/collect_github_actions_metrics.py`](../scripts/collect_github_actions_metrics.py)
- base final em [`data/`](../data/)
- gráficos finais em [`artifacts/graphs/`](../artifacts/graphs/)
- relatório consolidado neste arquivo

## Stack E Arquitetura

### Stack usada

- `Python`
- `pytest`
- `pytest-json-report`
- `ruff`
- `requests`
- `pandas`
- `matplotlib`
- `GitHub Actions`
- `GitHub CLI`
- `CSV`, `JSON`, `JUnit XML`, `Markdown`

### Arquitetura do experimento

1. O código Python é testado localmente e no GitHub Actions.
2. O workflow executa `lint`, `tests` e `summarize`.
3. Os testes geram artefatos estruturados.
4. O coletor consulta a API do GitHub Actions e cruza os dados das execuções com os artefatos.
5. Os CSVs são usados para gerar os gráficos.
6. O relatório interpreta os resultados.

## Estrutura Do Projeto

```text
.
├── .github/workflows/      -> pipeline CI/CD
├── artifacts/graphs/       -> imagens finais dos gráficos
├── ci/                     -> configuração controlada do experimento
├── data/                   -> base consolidada em CSV e JSON
├── reports/                -> documentação final
├── scripts/                -> automação de métricas e gráficos
├── src/ci_experiment/      -> código-fonte da aplicação exemplo
└── tests/                  -> suíte automatizada
```

### Descrição pasta por pasta

- [`.github/workflows/`](../.github/workflows/)
  Define o workflow `ci-experiment.yml`.

- [`artifacts/graphs/`](../artifacts/graphs/)
  Armazena os gráficos que serão usados na correção e no relatório.

- [`ci/`](../ci/)
  Centraliza a variação experimental via `experiment_config.json`.

- [`data/`](../data/)
  Guarda a saída estruturada do coletor: runs, jobs, steps e JSON consolidado.

- [`reports/`](../reports/)
  Contém o relatório técnico final.

- [`scripts/`](../scripts/)
  Reúne os scripts responsáveis por produzir métricas de teste, coletar dados do GitHub Actions e gerar gráficos.

- [`src/ci_experiment/`](../src/ci_experiment/)
  Contém a aplicação simples usada como base para o pipeline.

- [`tests/`](../tests/)
  Reúne os testes unitários e os testes parametrizados que suportam as variações do experimento.

## Identificacao Do Experimento

- Repositório: <https://github.com/tvolcati/gha-ci-cd-pipeline-experiment>
- Workflow YAML: <https://github.com/tvolcati/gha-ci-cd-pipeline-experiment/blob/main/.github/workflows/ci-experiment.yml>
- Período de coleta: `2026-06-03`
- Quantidade de execuções analisadas: `12`

## Descricao Do Pipeline

O pipeline implementado contém:

- instalação de dependências com `pip install -e .[dev]`
- análise estática com `ruff check .`
- execução de testes com `pytest`
- geração de artefatos com `junit.xml`, `report.json` e `test-metrics.json`
- publicação de resumo da execução no GitHub Actions

Jobs principais:

- `lint`
- `tests`
- `summarize`

## Variacoes Realizadas

| Execucao | Run ID | Commit SHA | Variacao aplicada | Hipotese inicial | Resultado observado |
|---|---:|---|---|---|---|
| 1 | 26888726715 | 76641235834cb33213044382cc91b050aea96cbc | Baseline com cache e jobs paralelos | O pipeline deve concluir abaixo de 1 minuto com sucesso | Sucesso em 36s |
| 2 | 26889087512 | 280791b830907e37249196cd43ef4701bb95e408 | Repetição do baseline após documentação | O tempo deve ficar próximo do baseline | Sucesso em 44s |
| 3 | 26889256053 | 24e1df7e8e4b7af07ef486e72235120099664899 | `extra_tests = 10` | O pipeline deve subir um pouco | 17 testes e tempo final de 36s |
| 4 | 26889258898 | cd16691a7dd19be09d4048c4ecb8a1e4e081041b | `extra_tests = 30` | O pipeline deve subir mais | 37 testes e tempo final de 36s |
| 5 | 26889261056 | a961efb35031d5034b5d3ac9b800ff6d87afc748 | `slow_test_seconds = 2` | O total deve crescer | Sucesso em 35s |
| 6 | 26889268057 | 9a6d644358e38f8f48e74272ced5ce7012463356 | `slow_test_seconds = 5` | O total deve crescer de forma visível | Sucesso em 43s |
| 7 | 26889268378 | b810b77bb038caf306c447fec5d31f41763f8584 | `force_failure = true` | O pipeline deve falhar | Falha em 33s |
| 8 | 26889271482 | c1873e266e0f561d7ecf27187738d9023a954648 | `force_failure = false` | O pipeline deve voltar ao verde | Sucesso em 42s |
| 9 | 26889276148 | e09289ce4a299b84f051443b8ab48c11edf49738 | Workflow sem cache | O tempo deve aumentar | Sucesso em 38s |
| 10 | 26889281225 | f7b1e88866d6d7c67f855b4f6520a8a3432f1ac7 | Workflow com cache restaurado | O tempo deve cair | Sucesso em 34s |
| 11 | 26889284157 | 5a5953d33a42e4f18f63f1a138cc9b06c7ea63a4 | Jobs sequenciais | O tempo deve crescer bastante | Sucesso em 57s |
| 12 | 26889288850 | 0e902f7d59a2113a08f75cfd3d77bed60453afa5 | Jobs paralelos restaurados | O tempo deve cair novamente | Sucesso em 39s |

## Evidencias Reais

### Links das execucoes

1. <https://github.com/tvolcati/gha-ci-cd-pipeline-experiment/actions/runs/26888726715>
2. <https://github.com/tvolcati/gha-ci-cd-pipeline-experiment/actions/runs/26889087512>
3. <https://github.com/tvolcati/gha-ci-cd-pipeline-experiment/actions/runs/26889256053>
4. <https://github.com/tvolcati/gha-ci-cd-pipeline-experiment/actions/runs/26889258898>
5. <https://github.com/tvolcati/gha-ci-cd-pipeline-experiment/actions/runs/26889261056>
6. <https://github.com/tvolcati/gha-ci-cd-pipeline-experiment/actions/runs/26889268057>
7. <https://github.com/tvolcati/gha-ci-cd-pipeline-experiment/actions/runs/26889268378>
8. <https://github.com/tvolcati/gha-ci-cd-pipeline-experiment/actions/runs/26889271482>
9. <https://github.com/tvolcati/gha-ci-cd-pipeline-experiment/actions/runs/26889276148>
10. <https://github.com/tvolcati/gha-ci-cd-pipeline-experiment/actions/runs/26889281225>
11. <https://github.com/tvolcati/gha-ci-cd-pipeline-experiment/actions/runs/26889284157>
12. <https://github.com/tvolcati/gha-ci-cd-pipeline-experiment/actions/runs/26889288850>

### Commits reais utilizados

1. `76641235834cb33213044382cc91b050aea96cbc`
2. `280791b830907e37249196cd43ef4701bb95e408`
3. `24e1df7e8e4b7af07ef486e72235120099664899`
4. `cd16691a7dd19be09d4048c4ecb8a1e4e081041b`
5. `a961efb35031d5034b5d3ac9b800ff6d87afc748`
6. `9a6d644358e38f8f48e74272ced5ce7012463356`
7. `b810b77bb038caf306c447fec5d31f41763f8584`
8. `c1873e266e0f561d7ecf27187738d9023a954648`
9. `e09289ce4a299b84f051443b8ab48c11edf49738`
10. `f7b1e88866d6d7c67f855b4f6520a8a3432f1ac7`
11. `5a5953d33a42e4f18f63f1a138cc9b06c7ea63a4`
12. `0e902f7d59a2113a08f75cfd3d77bed60453afa5`

### Base de dados gerada

- [`../data/run_metrics.csv`](../data/run_metrics.csv)
- [`../data/job_metrics.csv`](../data/job_metrics.csv)
- [`../data/step_metrics.csv`](../data/step_metrics.csv)
- [`../data/collected_metrics.json`](../data/collected_metrics.json)

## Graficos Anexados

### Tempo total do pipeline por execução

![Tempo total do pipeline por execução](../artifacts/graphs/pipeline_duration_by_run.png)

### Tempo por job em cada execução

![Tempo por job em cada execução](../artifacts/graphs/job_duration_by_run.png)

### Taxa de sucesso e falha

![Taxa de sucesso e falha](../artifacts/graphs/success_failure_rate.png)

### Relação entre quantidade de testes e duração do pipeline

![Relação entre quantidade de testes e duração do pipeline](../artifacts/graphs/tests_vs_pipeline_duration.png)

## Analise Dos Resultados

### Qual etapa mais contribuiu para o tempo total do pipeline?

O job `tests` foi o maior contribuinte médio, com `25,5s`, seguido por `lint` com `22,0s`. O job `summarize` teve impacto pequeno, com média de `4,9s`.

### Houve diferença significativa entre execuções com e sem cache?

Sim, mas em escala moderada. O run sem cache levou `38s`, enquanto o run com cache restaurado caiu para `34s`. O ganho observado foi de aproximadamente `4s`.

### O paralelismo reduziu o tempo total?

Sim. O caso sequencial levou `57s`, enquanto o caso com jobs paralelos levou `39s`. O ganho foi de `18s`, o maior efeito observável do experimento.

### Quais falhas foram mais frequentes?

Houve apenas uma falha, e ela foi intencional: o run com `force_failure = true`, que registrou `test_failures = 1`.

### O pipeline fornece feedback rápido o suficiente?

Para um projeto pequeno, sim. A média geral foi `39,42s`, o que caracteriza feedback relativamente rápido. Mesmo o pior caso ficou abaixo de 1 minuto.

### Que melhorias poderiam ser feitas?

- quebrar a suíte de testes em grupos quando ela crescer
- manter o cache e monitorar sua efetividade
- medir tempo por etapa com maior granularidade histórica
- atualizar actions devido aos avisos de depreciação de Node.js 20
- explorar paralelismo mais fino se a base de testes aumentar

### Quais limitações existem nos dados?

- projeto pequeno e suscetível a ruído do runner
- amostra concentrada no mesmo dia
- testes artificiais baratos, com baixa representatividade de cenários reais
- ausência de matriz de ambientes e múltiplos sistemas operacionais

### Como essa análise apoia decisões de engenharia?

Ela mostra que, neste cenário, o maior ganho não veio de reduzir tempo de teste individual, mas de manter jobs independentes e paralelos. Isso ajuda a priorizar arquitetura do pipeline em vez de micro-otimizações prematuras.

## Resultados Inesperados

### Resultado inesperado 1

- Hipótese inicial: aumentar de 8 para 37 testes elevaria claramente o tempo total.
- Resultado observado: os runs com 17 e 37 testes continuaram em `36s`.
- Interpretação: o custo dominante ainda é setup, instalação e overhead de runner, não a execução de testes triviais.

### Resultado inesperado 2

- Hipótese inicial: um teste artificialmente lento de 2 segundos aumentaria o workflow em cerca de 2 segundos.
- Resultado observado: o run com `slow_test_seconds = 2` terminou em `35s`, abaixo do baseline.
- Interpretação: a variabilidade do ambiente mascarou o efeito de uma lentidão pequena.

## Comparacao Entre Hipotese E Resultado Observado

As hipóteses estruturais se confirmaram: remover cache piorou o tempo, restaurar cache ajudou, e tornar jobs sequenciais foi o pior cenário. Já as hipóteses ligadas a pequenas mudanças em testes curtos não produziram impacto proporcional. Isso indica que o pipeline ainda está em uma escala onde overhead de infraestrutura pesa mais do que a carga da suíte.

## Roteiro De Avaliacao

### Checklist do avaliador

- [x] Repositório GitHub entregue
- [x] YAML do GitHub Actions entregue
- [x] Script Python de coleta entregue
- [x] Base de dados em CSV e JSON entregue
- [x] Quatro gráficos entregues
- [x] Relatório técnico entregue
- [x] 12 execuções reais com `run IDs`
- [x] Commits reais listados
- [x] Variações controladas documentadas
- [x] Análise de resultados inesperados
- [x] Comparação entre hipótese e resultado
- [x] Discussão sobre limitações

### Passo a passo de correção

1. Abrir o repositório e confirmar o workflow em `.github/workflows/ci-experiment.yml`.
2. Conferir as 12 execuções listadas na seção de evidências.
3. Verificar a base em `data/`.
4. Verificar os gráficos anexados.
5. Conferir se a análise textual reflete os números dos CSVs.

## Reproducao

### Validacao local

```bash
python3 -m pip install --user --break-system-packages -e '.[dev]'
python3 -m pytest
python3 -m ruff check .
```

### Coleta de métricas

```bash
export GITHUB_TOKEN=seu_token
python3 scripts/collect_github_actions_metrics.py \
  --repo tvolcati/gha-ci-cd-pipeline-experiment \
  --workflow ci-experiment.yml \
  --output-dir data
```

### Geração de gráficos

```bash
python3 scripts/generate_graphs.py \
  --run-metrics data/run_metrics.csv \
  --job-metrics data/job_metrics.csv \
  --output-dir artifacts/graphs
```
