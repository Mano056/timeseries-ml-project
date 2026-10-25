"""Tests for feature dataset construction."""

from datetime import datetime, timedelta

import pandas as pd
import pytest

from core import Bar, PriceSeries
from features.dataset import build_feature_dataset


def make_series(
        prices: list[tuple[float, float, float]],
) -> PriceSeries:
    """Create a price series from (high, low, close) tuples."""
    bars = []

    for i, (high, low, close) in enumerate(prices):
        bars.append(
            Bar(
                timestamp=datetime(2024, 1, 1) + timedelta(minutes=i),
                open=close,
                high=high,
                low=low,
                close=close,
                volume=1000,
            )
        )
    return PriceSeries(bars)


def test_builds_dataframe_with_expected_columns() -> None:
    series = make_series(
        [
            (101.0, 99.0, 100.0),
            (104.0, 100.0, 103.0),
            (106.0, 101.0, 105.0),
            (108.0, 105.0, 107.0),
        ]
    )

    dataset = build_feature_dataset(
        series,
        return_periods=[1, 2],
        atr_period=2,
    )

    assert isinstance(dataset, pd.DataFrame)
    assert list(dataset.columns) == [
        'return_1',
        'return_2',
        'true_range',
        'atr_2',
    ]


def test_preserves_one_row_per_price_ar() -> None:
    series = make_series(
        [
            (101.0, 99.0, 100.0),
            (104.0, 100.0, 103.0),
            (106.0, 101.0, 105.0),
        ]
    )

    dataset = build_feature_dataset(series)

    assert len(dataset) == len(series)


def test_calculates_feature_values() -> None:
    series = make_series(
        [
            (101.0, 99.0, 100.0),
            (104.0, 100.0, 103.0),
            (106.0, 101.0, 105.0),
            (108.0, 105.0, 107.0),
        ]
    )

    dataset = build_feature_dataset(
        series,
        return_periods=[1],
        atr_period=2,
    )

    assert dataset['return_1'].iloc[1] == pytest.approx(0.03)
    assert dataset['true_range'].iloc[1] == pytest.approx(4.0)
    assert dataset['atr_2'].iloc[2] == pytest.approx(4.5)


def test_preserves_missing_values_at_start() -> None:
    series = make_series(
        [
            (101.0, 99.0, 100.0),
            (104.0, 100.0, 103.0),
            (106.0, 101.0, 105.0),
        ]
    )

    dataset = build_feature_dataset(
        series,
        return_periods=[2],
        atr_period=2,
    )

    assert pd.isna(dataset['return_2'].iloc[0])
    assert pd.isna(dataset['return_2'].iloc[1])
    assert pd.isna(dataset['true_range'].iloc[0])
    assert pd.isna(dataset['atr_2'].iloc[0])
    assert pd.isna(dataset['atr_2'].iloc[1])


def test_empty_series_returns_empty_dataframe() -> None:
    dataset = build_feature_dataset(PriceSeries([]))

    assert isinstance(dataset, pd.DataFrame)
    assert dataset.empty
    assert list(dataset.columns) == [
        'return_1',
        'true_range',
        'atr_14',
    ]


def test_rejects_invalid_return_period() -> None:
    series = make_series([(101.0, 99.0, 100.0)])

    with pytest.raises(ValueError):
        build_feature_dataset(series, return_periods=[0])


def test_rejects_duplicate_return_periods() -> None:
    series = make_series([(101.0, 99.0, 100.0)])

    with pytest.raises(ValueError):
        build_feature_dataset(series, return_periods=[1, 1])