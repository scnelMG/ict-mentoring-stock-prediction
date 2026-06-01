"""Feature engineering for stock price prediction experiments."""

from __future__ import annotations

import pandas as pd
import ta


MOVING_AVERAGE_WINDOWS = (5, 20, 60, 120)


def add_moving_average_features(
    frame: pd.DataFrame,
    windows: tuple[int, ...] = MOVING_AVERAGE_WINDOWS,
) -> pd.DataFrame:
    """Add price and volume moving averages."""

    enriched = frame.copy()
    for window in windows:
        enriched[f"ma_{window}"] = enriched["Close"].rolling(window=window).mean()
        enriched[f"vma_{window}"] = enriched["Volume"].rolling(window=window).mean()
    return enriched


def add_technical_indicators(frame: pd.DataFrame) -> pd.DataFrame:
    """Add representative volume, volatility, trend, and momentum indicators."""

    enriched = frame.copy()
    high = enriched["High"]
    low = enriched["Low"]
    close = enriched["Close"]
    volume = enriched["Volume"]

    enriched["MFI"] = ta.volume.money_flow_index(high, low, close, volume, fillna=True)
    enriched["ADI"] = ta.volume.acc_dist_index(high, low, close, volume, fillna=True)
    enriched["OBV"] = ta.volume.on_balance_volume(close, volume, fillna=True)
    enriched["CMF"] = ta.volume.chaikin_money_flow(high, low, close, volume, fillna=True)
    enriched["FI"] = ta.volume.force_index(close, volume, fillna=True)
    enriched["VPT"] = ta.volume.volume_price_trend(close, volume, fillna=True)
    enriched["NVI"] = ta.volume.negative_volume_index(close, volume, fillna=True)
    enriched["VWAP"] = ta.volume.volume_weighted_average_price(
        high, low, close, volume, fillna=True
    )

    enriched["ATR"] = ta.volatility.average_true_range(high, low, close, fillna=True)
    enriched["BHB"] = ta.volatility.bollinger_hband(close, fillna=True)
    enriched["BLB"] = ta.volatility.bollinger_lband(close, fillna=True)
    enriched["KCH"] = ta.volatility.keltner_channel_hband(high, low, close, fillna=True)
    enriched["KCL"] = ta.volatility.keltner_channel_lband(high, low, close, fillna=True)
    enriched["DCH"] = ta.volatility.donchian_channel_hband(high, low, close, fillna=True)
    enriched["DCL"] = ta.volatility.donchian_channel_lband(high, low, close, fillna=True)
    enriched["UI"] = ta.volatility.ulcer_index(close, fillna=True)

    enriched["SMA"] = ta.trend.sma_indicator(close, fillna=True)
    enriched["EMA"] = ta.trend.ema_indicator(close, fillna=True)
    enriched["WMA"] = ta.trend.wma_indicator(close, fillna=True)
    enriched["MACD"] = ta.trend.macd(close, fillna=True)
    enriched["ADX"] = ta.trend.adx(high, low, close, fillna=True)
    enriched["TRIX"] = ta.trend.trix(close, fillna=True)
    enriched["CCI"] = ta.trend.cci(high, low, close, fillna=True)

    enriched["RSI"] = ta.momentum.rsi(close, fillna=True)
    enriched["SRSI"] = ta.momentum.stochrsi(close, fillna=True)
    enriched["TSI"] = ta.momentum.tsi(close, fillna=True)
    enriched["UO"] = ta.momentum.ultimate_oscillator(high, low, close, fillna=True)
    enriched["WR"] = ta.momentum.williams_r(high, low, close, fillna=True)
    enriched["ROC"] = ta.momentum.roc(close, fillna=True)
    return enriched


def build_model_frame(frame: pd.DataFrame) -> pd.DataFrame:
    """Return a cleaned feature frame ready for scaling/modeling."""

    features = add_moving_average_features(frame)
    features = add_technical_indicators(features)
    return features.dropna()
