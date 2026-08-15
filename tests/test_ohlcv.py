from __future__ import annotations

import pandas as pd
import pytest

from src.ohlcv import normalize_price_frame


def test_normalize_price_frame_maps_krx_columns_when_change_rate_is_present() -> None:
    given_frame = pd.DataFrame(
        {
            "날짜": ["2022-05-31", "2022-05-30"],
            "시가": [67500, 67500],
            "고가": [67500, 67800],
            "저가": [66700, 66900],
            "종가": [67400, 67700],
            "거래량": [24365002, 14255484],
            "등락률": [-0.44, 2.73],
        }
    )

    when_normalized = normalize_price_frame(given_frame)

    assert when_normalized.columns.tolist() == [
        "date",
        "open",
        "high",
        "low",
        "close",
        "volume",
    ]
    assert when_normalized.iloc[-1].tolist() == [20220531, 67500, 67500, 66700, 67400, 24365002]


def test_normalize_price_frame_rejects_missing_ohlcv_column() -> None:
    given_frame = pd.DataFrame(
        {
            "date": [20220531],
            "open": [67500],
            "high": [67500],
            "low": [66700],
            "close": [67400],
        }
    )

    with pytest.raises(KeyError, match="volume"):
        _ = normalize_price_frame(given_frame)
