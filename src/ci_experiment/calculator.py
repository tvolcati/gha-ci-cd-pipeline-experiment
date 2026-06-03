def add(a: int | float, b: int | float) -> int | float:
    return a + b


def divide(a: int | float, b: int | float) -> float:
    if b == 0:
        raise ValueError("division by zero is not allowed")
    return a / b


def normalize_scores(values: list[float]) -> list[float]:
    if not values:
        return []
    total = sum(values)
    if total == 0:
        raise ValueError("sum of values must not be zero")
    return [value / total for value in values]
