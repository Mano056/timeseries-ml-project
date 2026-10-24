"""True Range feature engineering."""

from core import PriceSeries


def calculate_true_range(
        price_series: PriceSeries,
) -> list[float | None]:
    """Calculate True Range for each bar.
    
    The first value is None because no previous close is available.
    
    Args:
        price_series: The price data used to calculate True Range.
    
    Returns:
        True Range values aligned with the price series.
    """
    bars = price_series

    if not bars:
        return []

    true_ranges: list[float | None] = [None]

    for previous_bar, current_bar in zip(bars, bars[1:]):
        high_low = current_bar.high - current_bar.low
        high_previous_close = abs(current_bar.high - previous_bar.close)
        low_previous_close = abs(current_bar.low - previous_bar.close)

        true_range = max(
            high_low,
            high_previous_close,
            low_previous_close,
        )

        true_ranges.append(true_range)
    return true_ranges