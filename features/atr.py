"""Average True Range feature engineering."""

from core import PriceSeries
from features.true_range import calculate_true_range


def calculate_atr(
        price_series: PriceSeries,
        period: int = 14,
) -> list[float | None]:
    """Calculate Average True Range using Wilder's smoothing.
    
    The first ATR appears after period valid True Range values.
    
    Args:
        price_series: The price data used to calculate ATR.
        period: Number of True Range values used for initialization.
        
    Returns:
        ATR values aligned with the price series.
        
    Raises:
        ValueError: If period is less than 1.
    """
    if period < 1:
        raise ValueError("period must be at least 1")

    true_ranges = calculate_true_range(price_series)
    atr_values: list[float | None] = [None] * len(true_ranges)

    if len(true_ranges) <= period:
        return atr_values

    initial_ranges = true_ranges[1 : period + 1]
    previous_atr = sum(initial_ranges) / period
    atr_values[period] = previous_atr

    for i in range(period + 1, len(true_ranges)):
        current_true_range = true_ranges[i]

        previous_atr = (
            ((period - 1) * previous_atr + current_true_range) / period
        )
        atr_values[i] = previous_atr

    return atr_values