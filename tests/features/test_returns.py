"""Tests for feature engineering returns."""

from datetime import datetime, timedelta

import pytest

from core import Bar, PriceSeries
from features.returns import calculate_returns


def make_series(closes: list[float]) -> PriceSeries:
    """Create a price series with the supplied closing prices."""
    bars = []

    for i, close in enumerate(closes):
        bars.append(
            Bar(
                timestamp=datetime(2024, 1, 1) + timedelta(minutes=i),
                open=close,
                high=close + 1,
                low=close - 1, 
                close=close,
                volume=1000,
            )
        )
    return PriceSeries(bars)


def test_calculates_one_bar_return() -> None:
    series = make_series([100.0, 102.0, 101.0])

    returns = calculate_returns(series)

    assert returns[0] is None
    assert returns[1] == pytest.approx(0.02)
    assert returns[2] == pytest.approx((101.0 / 102.0) - 1)


def test_output_length_mathes_input() -> None:
    series = make_series([100.0, 102.0, 101.0, 104.0])

    returns = calculate_returns(series)

    assert len(returns) == len(series)


def test_empty_series_returns_empty_list() -> None:
    series = PriceSeries([])

    assert calculate_returns(series) == []


def test_single_bar_returns_none() -> None:
    series = make_series([100.0])

    assert calculate_returns(series) == [None]


def test_calculation_does_not_modify_price_series() -> None:
    series = make_series([100.0, 102.0, 101.0])
    original_closes = series.closes
    original_timestamps = series.timestamps

    calculate_returns(series)

    assert series.closes == original_closes
    assert series.timestamps == original_timestamps


def test_calculates_five_bar_return() -> None:
    series = make_series([100.0, 102.0, 101.0, 103.0, 104.0, 105.0, 107.0])

    returns = calculate_returns(series, period=5)

    assert returns[:5] == [None, None, None, None, None]
    assert returns[5] == pytest.approx(0.05)
    assert returns[6] == pytest.approx((107.0 / 102.0) - 1)


def test_rejects_zero_period() -> None:
    series = make_series([100.0, 102.0, 105.0])

    with pytest.raises(ValueError):
        calculate_returns(series, period=0)


def test_rejects_negative_period() -> None:
    series = make_series([100.0, 102.0, 105.0])

    with pytest.raises(ValueError):
        calculate_returns(series, period=-1)