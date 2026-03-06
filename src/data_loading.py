"""Reusable data loading helpers for the NovaCred governance audit."""

from __future__ import annotations

import json
from pathlib import Path

import pandas as pd


def load_raw_data(path: str) -> pd.DataFrame:
    """Load the raw NovaCred JSON file into the flat notebook-ready format.

    The current notebooks rely on the column layout produced by
    ``pandas.json_normalize``: top-level fields are preserved, nested objects are
    flattened with dot-notation, and the original ``spending_behavior`` array is
    kept intact for downstream auditing. This helper centralizes that logic so the
    repository has a reusable data-loading module without changing the analysis
    outputs at the last minute.
    """

    dataset_path = Path(path)
    if not dataset_path.exists():
        raise FileNotFoundError(f"Dataset not found: {dataset_path}")

    with dataset_path.open("r", encoding="utf-8") as handle:
        raw_data = json.load(handle)

    if not isinstance(raw_data, list) or len(raw_data) == 0:
        raise ValueError("Expected a non-empty JSON array of application records.")

    return pd.json_normalize(raw_data)
