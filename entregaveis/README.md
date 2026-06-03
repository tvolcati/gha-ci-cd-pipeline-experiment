# Entregaveis

Esta pasta concentra objetivamente os itens pedidos no enunciado para facilitar a correção.

## Itens exigidos

### 1. Link do repositório GitHub

- Repositório: <https://github.com/tvolcati/gha-ci-cd-pipeline-experiment>

### 2. Link do arquivo YAML do GitHub Actions

- Workflow no GitHub: <https://github.com/tvolcati/gha-ci-cd-pipeline-experiment/blob/main/.github/workflows/ci-experiment.yml>
- Workflow local: [`.github/workflows/ci-experiment.yml`](../.github/workflows/ci-experiment.yml)

### 3. Script de coleta das métricas

- Script principal: [`scripts/collect_github_actions_metrics.py`](../scripts/collect_github_actions_metrics.py)

### 4. Base de dados gerada em CSV ou JSON

- Runs: [`data/run_metrics.csv`](../data/run_metrics.csv)
- Jobs: [`data/job_metrics.csv`](../data/job_metrics.csv)
- Steps: [`data/step_metrics.csv`](../data/step_metrics.csv)
- Consolidado JSON: [`data/collected_metrics.json`](../data/collected_metrics.json)

### 5. Graficos produzidos

- Tempo total do pipeline: [`artifacts/graphs/pipeline_duration_by_run.png`](../artifacts/graphs/pipeline_duration_by_run.png)
- Tempo por job: [`artifacts/graphs/job_duration_by_run.png`](../artifacts/graphs/job_duration_by_run.png)
- Taxa de sucesso e falha: [`artifacts/graphs/success_failure_rate.png`](../artifacts/graphs/success_failure_rate.png)
- Testes x duração: [`artifacts/graphs/tests_vs_pipeline_duration.png`](../artifacts/graphs/tests_vs_pipeline_duration.png)

### 6. Relatorio tecnico em Markdown

- Relatório final: [`reports/technical_report.md`](../reports/technical_report.md)

### 7. Breve explicação sobre como reproduzir o experimento

1. Instalar dependências:

```bash
python3 -m pip install --user --break-system-packages -e '.[dev]'
```

2. Validar localmente:

```bash
python3 -m pytest
python3 -m ruff check .
```

3. Coletar métricas reais do GitHub Actions:

```bash
export GITHUB_TOKEN=seu_token
python3 scripts/collect_github_actions_metrics.py \
  --repo tvolcati/gha-ci-cd-pipeline-experiment \
  --workflow ci-experiment.yml \
  --output-dir data
```

4. Gerar os gráficos:

```bash
python3 scripts/generate_graphs.py \
  --run-metrics data/run_metrics.csv \
  --job-metrics data/job_metrics.csv \
  --output-dir artifacts/graphs
```

## Atalho para correção

- Página principal: [`README.md`](../README.md)
- Relatório completo: [`reports/technical_report.md`](../reports/technical_report.md)
- Evidências reais e análise: [`reports/technical_report.md`](../reports/technical_report.md)
