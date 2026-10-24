"""Feature egineering funtions for market data"""

from core import PriceSeries

def calculate_returns(
        price_series: PriceSeries,
) -> list[float | None]:
    """Calculate one-bar percentage returns.
    
    The first return is None because no previous close is available.
    The original price series is not modified.
    """
    closes = price_series.closes

    if not closes:
        return []

    returns: list[float | None] = [None]

    for previous_close, current_close in zip(closes, closes[1:]):
        returns.append((current_close / previous_close) - 1)

    return returns