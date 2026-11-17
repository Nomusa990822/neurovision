"""Small deterministic helpers; framework-specific seeding is added with model code."""

from __future__ import annotations

import random


def seed_python(seed: int) -> None:
    """Seed Python's built-in pseudo-random generator."""
    if seed < 0:
        raise ValueError("seed must be a non-negative integer")
    random.seed(seed)
