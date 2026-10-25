"""Feature dataset construction."""

import pandas as pd

from core import PriceSeries
from features.atr import calculate_atr
from features.returns import calculate_returns
from features.true_range import calculate_true_range


def build_feature_dataset(
        price_series: PriceSeries,
        return_periods: list[int] | None = None,
        atr_period: int = 14,
) -> pd.DataFrame:
    """Build a DataFrame containing calculated market features.
    
    Rows remain aligned with the original price bars. Initial missing
    feature values are preserved.
    
    Args:
        price_series: The price data used to calculate features.
        return_periods: Periods for percentage-return features.
            Defaults to [1].
        atr_period: Period used to calculate Average True Range.
        
    Returns:
        A DataFrame containing the requested features.
        
    Raises:
        ValueError: If return periods are invalid or duplicated.
    """
    if return_periods is None:
        return_periods = [1]

    if any(period < 1 for period in return_periods):
        raise ValueError("Return periods must be at least 1.")

    if len(return_periods) != len(set(return_periods)):
        raise ValueError("Return periods must be unique.")

    dataset: dict[str, list[float | None]] = {}

    for period in return_periods:
        dataset[f"return_{period}"] = calculate_returns(
            price_series,
            period=period,
        )

    dataset['true_range'] = calculate_true_range(price_series)
    dataset[f'atr_{atr_period}'] = calculate_atr(
        price_series,
        period=atr_period,
    )

    return pd.DataFrame(dataset)