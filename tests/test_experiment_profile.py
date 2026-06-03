import time

import pytest

from ci_experiment.experiment import load_experiment_config

CONFIG = load_experiment_config()


def test_controlled_failure_flag() -> None:
    assert CONFIG["force_failure"] is False, "controlled failure enabled for this experiment run"


def test_optional_slow_test() -> None:
    delay = CONFIG["slow_test_seconds"]
    if delay > 0:
        time.sleep(delay)
    assert delay >= 0


@pytest.mark.parametrize("index", range(CONFIG["extra_tests"]))
def test_generated_extra_cases(index: int) -> None:
    assert index >= 0
