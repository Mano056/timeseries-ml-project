"""Feature egineering funtions for market data"""

from core import PriceSeries


def calculate_returns(
        price_series: PriceSeries,
        period: int = 1,
) -> list[float | None]:
    """Calculate percentage returns over a specific number of bars..
    
    The first period returns are None because no previous close
    is available for those observations.

    Args: 
        price_series: The price data used to calculate returns.
        period: Number of bars between the current and previous close.
    
    Reeturns:
        A list of percentage returns aligned with the price series.

    Raises:
        ValueError: If period is less than 1.
    """
    if period < 1:
        raise ValueError("period must be at least 1")
    
    closes = price_series.closes
    returns: list[float | None] = [None] * min(period, len(closes))

    for i in range(period, len(closes)):
        previous_close = closes[i - period]
        current_close = closes[i]
        returns.append((current_close / previous_close) - 1)

    return returns