import pytest

from ci_experiment.calculator import add, divide, normalize_scores


def test_add_returns_sum() -> None:
    assert add(2, 3) == 5


def test_divide_returns_ratio() -> None:
    assert divide(10, 2) == 5


def test_divide_rejects_zero_division() -> None:
    with pytest.raises(ValueError, match="division by zero"):
        divide(10, 0)


def test_normalize_scores_preserves_total() -> None:
    normalized = normalize_scores([2, 3, 5])
    assert pytest.approx(sum(normalized)) == 1.0


def test_normalize_scores_rejects_zero_total() -> None:
    with pytest.raises(ValueError, match="must not be zero"):
        normalize_scores([0, 0, 0])
