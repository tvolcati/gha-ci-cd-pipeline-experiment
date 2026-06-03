from __future__ import annotations

import argparse
import csv
import io
import json
import os
import zipfile
from datetime import datetime
from pathlib import Path
from typing import Any

import requests

API_ROOT = "https://api.github.com"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Collect GitHub Actions metrics for the experiment."
    )
    parser.add_argument(
        "--repo", required=True, help="GitHub repository in owner/name format."
    )
    parser.add_argument(
        "--workflow",
        default="ci-experiment.yml",
        help="Workflow file name or workflow id. Default: ci-experiment.yml",
    )
    parser.add_argument(
        "--token",
        default=os.getenv("GITHUB_TOKEN"),
        help="GitHub token. Defaults to GITHUB_TOKEN environment variable.",
    )
    parser.add_argument(
        "--output-dir",
        default="data",
        help="Directory for CSV and JSON output files. Default: data",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=100,
        help="Maximum number of workflow runs to collect. Default: 100",
    )
    return parser.parse_args()


def request_json(
    url: str, token: str, params: dict[str, Any] | None = None
) -> dict[str, Any]:
    headers = {
        "Accept": "application/vnd.github+json",
        "Authorization": f"Bearer {token}",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    response = requests.get(url, headers=headers, params=params, timeout=30)
    response.raise_for_status()
    return response.json()


def request_bytes(url: str, token: str) -> bytes:
    headers = {
        "Accept": "application/vnd.github+json",
        "Authorization": f"Bearer {token}",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    response = requests.get(url, headers=headers, timeout=60)
    response.raise_for_status()
    return response.content


def parse_timestamp(value: str | None) -> datetime | None:
    if not value:
        return None
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


def duration_seconds(start: str | None, end: str | None) -> float | None:
    start_ts = parse_timestamp(start)
    end_ts = parse_timestamp(end)
    if not start_ts or not end_ts:
        return None
    return round((end_ts - start_ts).total_seconds(), 3)


def download_test_metrics(repo: str, run_id: int, token: str) -> dict[str, Any]:
    artifacts_url = f"{API_ROOT}/repos/{repo}/actions/runs/{run_id}/artifacts"
    artifacts = request_json(artifacts_url, token)

    for artifact in artifacts.get("artifacts", []):
        if artifact.get("expired"):
            continue
        archive_url = artifact.get("archive_download_url")
        if not archive_url:
            continue

        content = request_bytes(archive_url, token)
        with zipfile.ZipFile(io.BytesIO(content)) as archive:
            for name in archive.namelist():
                if name.endswith("test-metrics.json"):
                    with archive.open(name) as file_obj:
                        return json.load(file_obj)
    return {
        "test_count": None,
        "test_failures": None,
        "test_skipped": None,
        "average_test_duration_seconds": None,
        "total_test_duration_seconds": None,
    }


def collect_runs(
    repo: str, workflow: str, token: str, limit: int
) -> list[dict[str, Any]]:
    runs_url = f"{API_ROOT}/repos/{repo}/actions/workflows/{workflow}/runs"
    payload = request_json(runs_url, token, params={"per_page": min(limit, 100)})
    return payload.get("workflow_runs", [])[:limit]


def collect_jobs(repo: str, run_id: int, token: str) -> list[dict[str, Any]]:
    jobs_url = f"{API_ROOT}/repos/{repo}/actions/runs/{run_id}/jobs"
    payload = request_json(jobs_url, token, params={"per_page": 100})
    return payload.get("jobs", [])


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as file_obj:
        writer = csv.DictWriter(file_obj, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    args = parse_args()
    if not args.token:
        raise SystemExit(
            "A GitHub token is required. Use --token or export GITHUB_TOKEN."
        )

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    runs = collect_runs(args.repo, args.workflow, args.token, args.limit)
    run_rows: list[dict[str, Any]] = []
    job_rows: list[dict[str, Any]] = []
    step_rows: list[dict[str, Any]] = []
    nested_output: list[dict[str, Any]] = []

    for run in runs:
        run_id = run["id"]
        jobs = collect_jobs(args.repo, run_id, args.token)
        test_metrics = download_test_metrics(args.repo, run_id, args.token)
        workflow_duration = duration_seconds(
            run.get("run_started_at"), run.get("updated_at")
        )
        commit_message = (
            (run.get("head_commit") or {}).get("message", "").splitlines()[0]
        )

        run_row = {
            "run_id": run_id,
            "run_number": run.get("run_number"),
            "commit_sha": run.get("head_sha"),
            "commit_message": commit_message,
            "status": run.get("conclusion") or run.get("status"),
            "workflow_duration_seconds": workflow_duration,
            "test_count": test_metrics.get("test_count"),
            "test_failures": test_metrics.get("test_failures"),
            "test_skipped": test_metrics.get("test_skipped"),
            "average_test_duration_seconds": test_metrics.get(
                "average_test_duration_seconds"
            ),
            "total_test_duration_seconds": test_metrics.get(
                "total_test_duration_seconds"
            ),
            "timestamp": run.get("run_started_at") or run.get("created_at"),
            "html_url": run.get("html_url"),
        }
        run_rows.append(run_row)

        nested_jobs: list[dict[str, Any]] = []
        for job in jobs:
            job_duration = duration_seconds(
                job.get("started_at"), job.get("completed_at")
            )
            job_row = {
                "run_id": run_id,
                "job_id": job.get("id"),
                "job_name": job.get("name"),
                "job_status": job.get("conclusion") or job.get("status"),
                "job_duration_seconds": job_duration,
                "started_at": job.get("started_at"),
                "completed_at": job.get("completed_at"),
            }
            job_rows.append(job_row)

            nested_steps: list[dict[str, Any]] = []
            for step in job.get("steps", []):
                step_duration = duration_seconds(
                    step.get("started_at"), step.get("completed_at")
                )
                step_row = {
                    "run_id": run_id,
                    "job_id": job.get("id"),
                    "job_name": job.get("name"),
                    "step_name": step.get("name"),
                    "step_number": step.get("number"),
                    "step_status": step.get("conclusion") or step.get("status"),
                    "step_duration_seconds": step_duration,
                }
                step_rows.append(step_row)
                nested_steps.append(step_row)

            nested_jobs.append({**job_row, "steps": nested_steps})

        nested_output.append({**run_row, "jobs": nested_jobs})

    write_csv(
        output_dir / "run_metrics.csv",
        run_rows,
        [
            "run_id",
            "run_number",
            "commit_sha",
            "commit_message",
            "status",
            "workflow_duration_seconds",
            "test_count",
            "test_failures",
            "test_skipped",
            "average_test_duration_seconds",
            "total_test_duration_seconds",
            "timestamp",
            "html_url",
        ],
    )
    write_csv(
        output_dir / "job_metrics.csv",
        job_rows,
        [
            "run_id",
            "job_id",
            "job_name",
            "job_status",
            "job_duration_seconds",
            "started_at",
            "completed_at",
        ],
    )
    write_csv(
        output_dir / "step_metrics.csv",
        step_rows,
        [
            "run_id",
            "job_id",
            "job_name",
            "step_name",
            "step_number",
            "step_status",
            "step_duration_seconds",
        ],
    )
    (output_dir / "collected_metrics.json").write_text(
        json.dumps(nested_output, indent=2),
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
