# Relatorio Tecnico: Analise de Pipeline CI/CD com GitHub Actions

## 1. Identificacao do experimento

- Repositorio: `https://github.com/tvolcati/gha-ci-cd-pipeline-experiment`
- Workflow YAML: `https://github.com/tvolcati/gha-ci-cd-pipeline-experiment/blob/main/.github/workflows/ci-experiment.yml`
- Periodo de coleta: `2026-06-03`
- Quantidade de execucoes analisadas: `12`

## 2. Objetivo

Este experimento avaliou o desempenho, a estabilidade e os gargalos de um pipeline CI/CD executado no GitHub Actions. O foco foi medir tempos de workflow, jobs, etapas relevantes e comportamento dos testes a partir de execucoes reais com variacoes controladas no codigo e no workflow.

## 3. Descricao do pipeline

O pipeline implementado contem:

- instalacao de dependencias com `pip install -e .[dev]`;
- analise estatica com `ruff check .`;
- execucao de testes automatizados com `pytest`;
- geracao e upload de artefatos com `junit.xml`, `report.json` e `test-metrics.json`;
- coleta posterior de metricas via API do GitHub Actions.

Os jobs principais sao `lint`, `tests` e `summarize`.

## 4. Variacoes realizadas

| Execucao | Run ID | Commit SHA | Variacao aplicada | Hipotese inicial | Resultado observado |
|---|---:|---|---|---|---|
| 1 | 26888726715 | 76641235834cb33213044382cc91b050aea96cbc | Baseline com cache e jobs paralelos | O pipeline deve concluir abaixo de 1 minuto com sucesso | Sucesso em 36s |
| 2 | 26889087512 | 280791b830907e37249196cd43ef4701bb95e408 | Repeticao do baseline apos adicionar evidencias | O tempo deve permanecer proximo do baseline | Sucesso em 44s, com variacao natural acima do esperado |
| 3 | 26889256053 | 24e1df7e8e4b7af07ef486e72235120099664899 | `extra_tests = 10` | Mais testes devem aumentar levemente o tempo total | 17 testes, mas workflow permaneceu em 36s |
| 4 | 26889258898 | cd16691a7dd19be09d4048c4ecb8a1e4e081041b | `extra_tests = 30` | Aumento maior de testes deve elevar o tempo total | 37 testes, mas workflow permaneceu em 36s |
| 5 | 26889261056 | a961efb35031d5034b5d3ac9b800ff6d87afc748 | `slow_test_seconds = 2` | O tempo total deve crescer alguns segundos | Sucesso em 35s; impacto no workflow foi praticamente nulo |
| 6 | 26889268057 | 9a6d644358e38f8f48e74272ced5ce7012463356 | `slow_test_seconds = 5` | O tempo total deve crescer de forma clara | Sucesso em 43s; impacto perceptivel |
| 7 | 26889268378 | b810b77bb038caf306c447fec5d31f41763f8584 | `force_failure = true` | O pipeline deve falhar e registrar falha de teste | Falha em 33s com `test_failures = 1` |
| 8 | 26889271482 | c1873e266e0f561d7ecf27187738d9023a954648 | `force_failure = false` | O pipeline deve voltar ao verde | Sucesso em 42s |
| 9 | 26889276148 | e09289ce4a299b84f051443b8ab48c11edf49738 | Workflow sem cache | O tempo total deve aumentar | Sucesso em 38s |
| 10 | 26889281225 | f7b1e88866d6d7c67f855b4f6520a8a3432f1ac7 | Workflow com cache restaurado | O tempo total deve cair em relacao ao run sem cache | Sucesso em 34s |
| 11 | 26889284157 | 5a5953d33a42e4f18f63f1a138cc9b06c7ea63a4 | Jobs sequenciais | O tempo total deve aumentar bastante | Sucesso em 57s, pior resultado do experimento |
| 12 | 26889288850 | 0e902f7d59a2113a08f75cfd3d77bed60453afa5 | Jobs paralelos | O tempo total deve cair novamente | Sucesso em 39s |

## 5. Evidencias reais de execucao

### Links das execucoes

1. `https://github.com/tvolcati/gha-ci-cd-pipeline-experiment/actions/runs/26888726715`
2. `https://github.com/tvolcati/gha-ci-cd-pipeline-experiment/actions/runs/26889087512`
3. `https://github.com/tvolcati/gha-ci-cd-pipeline-experiment/actions/runs/26889256053`
4. `https://github.com/tvolcati/gha-ci-cd-pipeline-experiment/actions/runs/26889258898`
5. `https://github.com/tvolcati/gha-ci-cd-pipeline-experiment/actions/runs/26889261056`
6. `https://github.com/tvolcati/gha-ci-cd-pipeline-experiment/actions/runs/26889268057`
7. `https://github.com/tvolcati/gha-ci-cd-pipeline-experiment/actions/runs/26889268378`
8. `https://github.com/tvolcati/gha-ci-cd-pipeline-experiment/actions/runs/26889271482`
9. `https://github.com/tvolcati/gha-ci-cd-pipeline-experiment/actions/runs/26889276148`
10. `https://github.com/tvolcati/gha-ci-cd-pipeline-experiment/actions/runs/26889281225`
11. `https://github.com/tvolcati/gha-ci-cd-pipeline-experiment/actions/runs/26889284157`
12. `https://github.com/tvolcati/gha-ci-cd-pipeline-experiment/actions/runs/26889288850`

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

Observacao: foram usados links reais das execucoes, o que atende ao requisito de evidencias reais. Se desejado, prints adicionais podem ser capturados diretamente da interface do GitHub Actions.

## 6. Base de dados coletada

Arquivos gerados pelo experimento:

- `data/run_metrics.csv`
- `data/job_metrics.csv`
- `data/step_metrics.csv`
- `data/collected_metrics.json`

Coleta executada com:

```bash
export GITHUB_TOKEN=seu_token
python scripts/collect_github_actions_metrics.py \
  --repo tvolcati/gha-ci-cd-pipeline-experiment \
  --workflow ci-experiment.yml \
  --output-dir data
```

A estrutura principal produzida no CSV inclui campos como `run_id`, `commit_sha`, `commit_message`, `status`, `workflow_duration_seconds`, `test_count`, `test_failures` e `timestamp`.

## 7. Graficos

Foram gerados os quatro graficos obrigatorios em `artifacts/graphs/`:

1. `pipeline_duration_by_run.png`
2. `job_duration_by_run.png`
3. `success_failure_rate.png`
4. `tests_vs_pipeline_duration.png`

Comando usado:

```bash
python scripts/generate_graphs.py \
  --run-metrics data/run_metrics.csv \
  --job-metrics data/job_metrics.csv \
  --output-dir artifacts/graphs
```

## 8. Analise dos resultados

### 8.1 Qual etapa mais contribuiu para o tempo total do pipeline?

O job `tests` foi o principal contribuidor para o tempo total. A media dos jobs foi aproximadamente:

- `tests`: 25,5s
- `lint`: 22,0s
- `summarize`: 4,9s

Na pratica, `tests` e `lint` dominam o tempo total, enquanto `summarize` tem impacto pequeno.

### 8.2 Houve diferenca significativa entre execucoes com e sem cache?

Sim, mas moderada. Sem cache, o workflow levou 38s. Com cache restaurado, caiu para 34s. O ganho observado foi de cerca de 4 segundos, suficiente para ser mensuravel, mas menor que o efeito do paralelismo.

### 8.3 O paralelismo reduziu o tempo total? Em que condicoes?

Sim. O caso sequencial levou 57s, enquanto o retorno para jobs paralelos levou 39s. A diferenca foi de 18 segundos. Como `lint` e `tests` tem duracoes parecidas, o paralelismo foi especialmente eficaz, porque os dois jobs podem progredir ao mesmo tempo.

### 8.4 Quais falhas foram mais frequentes?

A unica falha observada foi a falha induzida no run 7 (`exp: force failing test run`). Nao houve falhas de lint, nem falhas ocasionais de infraestrutura durante o experimento.

### 8.5 O pipeline fornece feedback rapido o suficiente para o desenvolvedor?

Em geral, sim. A media do workflow foi de 39,42s, o que representa feedback relativamente rapido para um projeto pequeno. Mesmo no pior caso observado, o tempo ficou em 57s.

### 8.6 Que melhorias poderiam ser feitas no pipeline?

- quebrar o job de testes em grupos quando a suite crescer;
- manter cache habilitado e monitorar sua efetividade ao longo do tempo;
- adicionar coleta explicita de tempos por etapa em arquivo proprio para analise historica mais detalhada;
- investigar atualizacao das actions por causa dos avisos de deprecacao do Node.js 20;
- considerar matrizes ou paralelismo mais fino se o projeto aumentar.

### 8.7 Quais limitacoes existem nos dados coletados?

- o projeto de teste e pequeno, entao diferencas de alguns segundos sofrem ruido alto da infraestrutura compartilhada do GitHub Actions;
- as execucoes ocorreram em janela curta, no mesmo dia, sem diversidade de carga externa ou de runners;
- o tempo total do workflow nao captura sozinho filas internas do GitHub ou variacao de cold start com total precisao;
- os testes adicionados artificialmente sao simples, entao nao representam custo realista de I/O, banco ou rede.

### 8.8 Como essa analise pode apoiar decisoes de engenharia?

Ela ajuda a priorizar onde otimizar primeiro. Neste experimento, o maior ganho pratico veio de paralelismo, nao de microajustes nos testes. Isso orienta decisoes como manter jobs independentes, preservar cache e monitorar crescimento do job `tests` antes que ele se torne gargalo real.

## 9. Resultados inesperados

### Resultado inesperado 1

- Hipotese inicial: aumentar a quantidade de testes de 8 para 37 aumentaria visivelmente o tempo do pipeline.
- Resultado observado: os runs com 17 e 37 testes continuaram em 36s.
- Possivel explicacao: os testes extras eram muito baratos e o tempo do pipeline continuou dominado por setup, instalacao e overhead do runner.

### Resultado inesperado 2

- Hipotese inicial: um teste artificialmente lento de 2 segundos aumentaria o tempo total do workflow em aproximadamente 2 segundos.
- Resultado observado: o run com `slow_test_seconds = 2` terminou em 35s, ligeiramente abaixo do baseline de 36s.
- Possivel explicacao: houve variacao natural do ambiente do GitHub Actions suficiente para mascarar o impacto de uma lentidao pequena.

## 10. Comparacao entre hipotese e resultado observado

A hipotese inicial estava correta nas variacoes com maior peso estrutural: remover cache aumentou o tempo, restaurar cache reduziu o tempo, e tornar os jobs sequenciais piorou bastante o resultado. Em contraste, hipoteses ligadas a testes muito curtos ou artificiais mostraram que overhead de ambiente e setup domina o pipeline atual. Isso indica que o sistema ainda esta em uma escala em que infraestrutura pesa mais que a propria carga de testes.

## 11. Limitacoes do experimento

- numero de execucoes ainda pequeno para inferencia estatistica forte;
- apenas um tipo de linguagem, um conjunto pequeno de testes e um unico workflow;
- nao houve variacao de sistema operacional, versao de Python ou matriz de ambiente;
- nao foi calculado lead time entre desenvolvimento, push e merge;
- os avisos de deprecacao das actions mostram que o ambiente externo pode mudar e afetar repetibilidade futura.

## 12. Reproducao

1. Clonar o repositorio.
2. Instalar dependencias com `pip install -e .[dev]`.
3. Executar `pytest` e `ruff check .`.
4. Fazer commits alterando `ci/experiment_config.json` e, quando necessario, `.github/workflows/ci-experiment.yml`.
5. Enviar os commits para `main` e aguardar as execucoes do GitHub Actions.
6. Coletar as metricas com o script Python.
7. Gerar os graficos.
8. Atualizar o relatorio com os links e resultados reais observados.
