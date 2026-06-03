from __future__ import annotations

import json
from pathlib import Path

DEFAULT_CONFIG_PATH = Path("ci/experiment_config.json")


def load_experiment_config(config_path: str | Path = DEFAULT_CONFIG_PATH) -> dict:
    path = Path(config_path)
    data = json.loads(path.read_text(encoding="utf-8"))
    return {
        "extra_tests": int(data.get("extra_tests", 0)),
        "slow_test_seconds": int(data.get("slow_test_seconds", 0)),
        "force_failure": bool(data.get("force_failure", False)),
    }
