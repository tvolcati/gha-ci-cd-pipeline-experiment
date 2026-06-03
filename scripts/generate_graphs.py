from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate charts for the CI/CD experiment."
    )
    parser.add_argument("--run-metrics", required=True, help="Path to run_metrics.csv")
    parser.add_argument("--job-metrics", required=True, help="Path to job_metrics.csv")
    parser.add_argument(
        "--output-dir", default="artifacts/graphs", help="Output directory for PNGs"
    )
    return parser.parse_args()


def save_pipeline_duration_chart(run_df: pd.DataFrame, output_dir: Path) -> None:
    ordered = run_df.sort_values("run_number")
    plt.figure(figsize=(10, 5))
    plt.plot(ordered["run_number"], ordered["workflow_duration_seconds"], marker="o")
    plt.title("Tempo total do pipeline por execucao")
    plt.xlabel("Numero da execucao")
    plt.ylabel("Duracao do workflow (s)")
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(output_dir / "pipeline_duration_by_run.png", dpi=200)
    plt.close()


def save_job_duration_chart(job_df: pd.DataFrame, output_dir: Path) -> None:
    pivot = (
        job_df.pivot_table(
            index="run_id",
            columns="job_name",
            values="job_duration_seconds",
            aggfunc="sum",
        )
        .fillna(0)
        .sort_index()
    )
    plt.figure(figsize=(11, 6))
    pivot.plot(kind="bar", stacked=True)
    plt.title("Tempo por job em cada execucao")
    plt.xlabel("Run ID")
    plt.ylabel("Duracao do job (s)")
    plt.tight_layout()
    plt.savefig(output_dir / "job_duration_by_run.png", dpi=200)
    plt.close()


def save_status_chart(run_df: pd.DataFrame, output_dir: Path) -> None:
    counts = run_df["status"].fillna("unknown").value_counts()
    plt.figure(figsize=(7, 5))
    counts.plot(kind="bar", color=["#2e7d32", "#c62828", "#1565c0", "#6a1b9a"])
    plt.title("Taxa de sucesso e falha")
    plt.xlabel("Status")
    plt.ylabel("Quantidade de execucoes")
    plt.tight_layout()
    plt.savefig(output_dir / "success_failure_rate.png", dpi=200)
    plt.close()


def save_tests_vs_duration_chart(run_df: pd.DataFrame, output_dir: Path) -> None:
    valid = run_df.dropna(subset=["test_count", "workflow_duration_seconds"])
    plt.figure(figsize=(8, 5))
    plt.scatter(valid["test_count"], valid["workflow_duration_seconds"])
    plt.title("Relacao entre quantidade de testes e duracao do pipeline")
    plt.xlabel("Quantidade de testes")
    plt.ylabel("Duracao do workflow (s)")
    plt.tight_layout()
    plt.savefig(output_dir / "tests_vs_pipeline_duration.png", dpi=200)
    plt.close()


def main() -> None:
    args = parse_args()
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    run_df = pd.read_csv(args.run_metrics)
    job_df = pd.read_csv(args.job_metrics)

    save_pipeline_duration_chart(run_df, output_dir)
    save_job_duration_chart(job_df, output_dir)
    save_status_chart(run_df, output_dir)
    save_tests_vs_duration_chart(run_df, output_dir)


if __name__ == "__main__":
    main()
