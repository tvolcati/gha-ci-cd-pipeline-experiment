# Experimento de Pipeline CI/CD com GitHub Actions

Este repositório foi preparado para a atividade de instrumentação de pipeline no GitHub Actions. Ele inclui:

- projeto Python mínimo com testes automatizados;
- workflow com lint, testes, artefatos e coleta de métricas;
- script de coleta via API do GitHub Actions;
- script de geração de gráficos;
- relatório técnico base em Markdown.

## Estrutura

- `.github/workflows/ci-experiment.yml`: pipeline principal
- `ci/experiment_config.json`: configura variações controladas do experimento
- `scripts/build_test_metrics.py`: resume métricas dos testes
- `scripts/collect_github_actions_metrics.py`: coleta dados reais do GitHub Actions
- `scripts/generate_graphs.py`: gera os gráficos exigidos
- `reports/technical_report.md`: relatório técnico base

## Setup local

```bash
python -m venv .venv
source .venv/bin/activate
pip install -U pip
pip install -e .[dev]
pytest
ruff check .
```

## Como executar o experimento

1. Crie um repositório no GitHub e envie este conteúdo.
2. Garanta que a branch padrão seja `main` ou ajuste o workflow.
3. Faça pelo menos 12 execuções com variações controladas.
4. Colete os dados reais:

```bash
export GITHUB_TOKEN=seu_token
python scripts/collect_github_actions_metrics.py \
  --repo tvolcati/gha-ci-cd-pipeline-experiment \
  --workflow ci-experiment.yml \
  --output-dir data
```

5. Gere os gráficos:

```bash
python scripts/generate_graphs.py \
  --run-metrics data/run_metrics.csv \
  --job-metrics data/job_metrics.csv \
  --output-dir artifacts/graphs
```

## Roteiro sugerido para 12 execuções

Use commits reais e registre cada alteração no relatório:

1. baseline com cache habilitado e testes normais
2. novo commit sem mudanças funcionais para medir variabilidade
3. `extra_tests = 10`
4. `extra_tests = 30`
5. `slow_test_seconds = 2`
6. `slow_test_seconds = 5`
7. `force_failure = true`
8. volta `force_failure = false`
9. desabilitar cache no workflow
10. reabilitar cache
11. tornar jobs sequenciais no workflow
12. voltar para jobs paralelos

## Observação

Os arquivos em `data/` e as evidências finais do relatório devem ser gerados a partir de execuções reais no GitHub Actions.

