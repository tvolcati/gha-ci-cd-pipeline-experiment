# Relatorio Tecnico: Analise de Pipeline CI/CD com GitHub Actions

## 1. Identificacao do experimento

- Repositorio: `https://github.com/tvolcati/gha-ci-cd-pipeline-experiment`
- Workflow YAML: `https://github.com/tvolcati/gha-ci-cd-pipeline-experiment/blob/main/.github/workflows/ci-experiment.yml`
- Periodo de coleta: `2026-06-03`
- Quantidade de execucoes analisadas: `1`

## 2. Objetivo

Este experimento avalia o desempenho, a estabilidade e os gargalos de um pipeline CI/CD executado no GitHub Actions. O foco foi medir tempos de workflow, jobs, etapas relevantes e comportamento dos testes a partir de execucoes reais.

## 3. Descricao do pipeline

O pipeline implementado contem:

- instalacao de dependencias;
- analise estatica com `ruff`;
- execucao de testes automatizados com `pytest`;
- geracao e upload de artefatos com resultados de teste;
- coleta posterior de metricas via script Python e API do GitHub Actions.

## 4. Variacoes realizadas

Preencha a tabela abaixo com os commits e as mudancas reais usadas no experimento.

| Execucao | Run ID | Commit SHA | Variacao aplicada | Hipotese inicial | Resultado observado |
|---|---:|---|---|---|---|
| 1 | 26888726715 | 76641235834cb33213044382cc91b050aea96cbc | Baseline com cache e jobs paralelos | O pipeline deve concluir abaixo de 1 minuto com sucesso | Concluiu com sucesso em 36s; lint e tests dominaram o tempo total |
| 2 | TODO | TODO | Repeticao do baseline | TODO | TODO |
| 3 | TODO | TODO | `extra_tests = 10` | TODO | TODO |
| 4 | TODO | TODO | `extra_tests = 30` | TODO | TODO |
| 5 | TODO | TODO | `slow_test_seconds = 2` | TODO | TODO |
| 6 | TODO | TODO | `slow_test_seconds = 5` | TODO | TODO |
| 7 | TODO | TODO | `force_failure = true` | TODO | TODO |
| 8 | TODO | TODO | `force_failure = false` | TODO | TODO |
| 9 | TODO | TODO | Workflow sem cache | TODO | TODO |
| 10 | TODO | TODO | Workflow com cache restaurado | TODO | TODO |
| 11 | TODO | TODO | Jobs sequenciais | TODO | TODO |
| 12 | TODO | TODO | Jobs paralelos | TODO | TODO |

## 5. Evidencias reais de execucao

Inclua obrigatoriamente:

- prints ou links das execucoes reais do GitHub Actions;
- IDs reais dos workflows executados;
- commits reais usados no experimento.

### Links das execucoes

1. `https://github.com/tvolcati/gha-ci-cd-pipeline-experiment/actions/runs/26888726715`
2. `Aguardando proximas execucoes reais`
3. `Aguardando proximas execucoes reais`

### Prints

Adicione as imagens nesta pasta ou faça referencia a elas:

- `Adicionar prints das runs em reports/images/`

## 6. Base de dados coletada

Arquivos gerados pelo experimento:

- `data/run_metrics.csv`
- `data/job_metrics.csv`
- `data/step_metrics.csv`
- `data/collected_metrics.json`

Explique brevemente como a coleta foi feita:

```bash
export GITHUB_TOKEN=seu_token
python scripts/collect_github_actions_metrics.py \
  --repo tvolcati/gha-ci-cd-pipeline-experiment \
  --workflow ci-experiment.yml \
  --output-dir data
```

## 7. Graficos

Inclua os quatro graficos obrigatorios:

1. Tempo total do pipeline por execucao
2. Tempo por job ou etapa
3. Taxa de sucesso e falha
4. Relacao entre quantidade de testes e duracao do pipeline

Comando usado:

```bash
python scripts/generate_graphs.py \
  --run-metrics data/run_metrics.csv \
  --job-metrics data/job_metrics.csv \
  --output-dir artifacts/graphs
```

## 8. Analise dos resultados

### 8.1 Qual etapa mais contribuiu para o tempo total do pipeline?

`TODO`

### 8.2 Houve diferenca significativa entre execucoes com e sem cache?

`TODO`

### 8.3 O paralelismo reduziu o tempo total? Em que condicoes?

`TODO`

### 8.4 Quais falhas foram mais frequentes?

`TODO`

### 8.5 O pipeline fornece feedback rapido o suficiente para o desenvolvedor?

`TODO`

### 8.6 Que melhorias poderiam ser feitas no pipeline?

`TODO`

### 8.7 Quais limitacoes existem nos dados coletados?

`TODO`

### 8.8 Como essa analise pode apoiar decisoes de engenharia?

`TODO`

## 9. Resultados inesperados

Descreva pelo menos dois resultados inesperados.

### Resultado inesperado 1

- Hipotese inicial: `TODO`
- Resultado observado: `TODO`
- Possivel explicacao: `TODO`

### Resultado inesperado 2

- Hipotese inicial: `TODO`
- Resultado observado: `TODO`
- Possivel explicacao: `TODO`

## 10. Comparacao entre hipotese e resultado observado

`TODO`

## 11. Limitacoes do experimento

`TODO`

## 12. Reproducao

1. Clonar o repositorio.
2. Instalar dependencias com `pip install -e .[dev]`.
3. Executar `pytest` e `ruff check .`.
4. Enviar os commits com as variacoes definidas.
5. Aguardar as execucoes no GitHub Actions.
6. Coletar as metricas com o script Python.
7. Gerar os graficos.
8. Atualizar este relatorio com evidencias reais.
