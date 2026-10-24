"""Test for True Range feature engineering."""

from datetime import datetime, timedelta

import pytest

from core import Bar, PriceSeries
from features.true_range import calculate_true_range


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


def test_calculates_true_range() -> None:
    series = make_series(
        [
            (101.0, 98.0, 100.0),
            (104.0, 99.0, 103.0),
            (106.0, 102.0, 105.0),
        ]
    )

    true_range = calculate_true_range(series)

    assert true_range == [None, 5.0, 4.0]


def test_uses_gap_from_previous_close() -> None:
    series = make_series(
        [
            (101.0, 98.0, 100.0),
            (108.0, 103.0, 107.0),
        ]
    )

    true_range = calculate_true_range(series)

    assert true_range[1] == pytest.approx(8.0)


def test_output_length_matches_input() -> None:
    series = make_series(
        [
            (101.0, 98.0, 100.0),
            (104.0, 99.0, 103.0),
            (106.0, 102.0, 105.0),
        ]
    )

    true_range = calculate_true_range(series)

    assert len(true_range) == len(series)


def test_empty_series_returns_empty_list() -> None:
    series = make_series([])

    assert calculate_true_range(series) == []


def test_single_bar_returns_none() -> None:
    series = make_series([(101.0, 98.0, 100.0)])

    assert calculate_true_range(series) == [None]