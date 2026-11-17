import random

import pytest

from neurovision.utils.reproducibility import seed_python


def test_python_seed_reproduces_random_sequence() -> None:
    seed_python(42)
    first = [random.random() for _ in range(4)]

    seed_python(42)
    second = [random.random() for _ in range(4)]

    assert first == second


def test_negative_seed_is_rejected() -> None:
    with pytest.raises(ValueError, match="non-negative"):
        seed_python(-1)
