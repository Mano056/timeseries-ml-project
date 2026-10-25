"""Tests for Average True Range feature engineering."""

from datetime import datetime, timedelta

import pytest

from core import Bar, PriceSeries
from features.atr import calculate_atr


def make_series(
        prices: list[tuple[float, float, float]],
) -> PriceSeries:
    """Create a price series from (high, low, close) tuples."""
    bars =[]

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


def test_calculate_initial_atr() -> None:
    series = make_series(
        [
            (101.0, 99.0, 100.0),
            (104.0, 100.0, 103.0),
            (106.0, 101.0, 105.0),
            (108.0, 105.0, 107.0),
        ]
    )

    atr = calculate_atr(series, period=3)

    assert atr[:3] == [None, None, None]
    assert atr[3] == pytest.approx(4.0)


def test_calculate_next_atr_using_wilder_smoothing() -> None:
    series = make_series(
        [
            (101.0, 99.0, 100.0),
            (104.0, 100.0, 103.0),
            (106.0, 101.0, 105.0),
            (108.0, 105.0, 107.0),
            (110.0, 106.0, 109.0),
        ]
    )

    atr = calculate_atr(series, period=3)

    assert atr[3] == pytest.approx(4.0)
    assert atr[4] == pytest.approx((2 * 4.0 + 4.0) / 3)


def test_output_length_matches_input() -> None:
    series = make_series(
        [
            (101.0, 99.0, 100.0),
            (104.0, 100.0, 103.0),
            (106.0, 101.0, 105.0),
            (108.0, 105.0, 107.0),
        ]
    )

    atr = calculate_atr(series, period=3)

    assert len(atr) == len(series)


def test_insufficient_data_returns_none_value() -> None:
    series = make_series(
        [
            (101.0, 99.0, 100.0),
            (104.0, 100.0, 103.0),
        ]
    )

    atr = calculate_atr(series, period=3)

    assert atr == [None, None]


def test_empty_series_return_empty_list() -> None:
    series = PriceSeries([])

    assert calculate_atr(series, period=3) == []


def test_rejects_zero_period() -> None:
    series = make_series([(101.0, 99.0, 100.0)])

    with pytest.raises(ValueError):
        calculate_atr(series, period=0)


def test_rejects_negative_period() -> None:
    series = make_series([(101.0, 99.0, 100.0)])

    with pytest.raises(ValueError):
        calculate_atr(series, period=-1)