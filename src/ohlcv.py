from __future__ import annotations

import re

import pandas as pd

OHLCV_COLUMNS = ("date", "open", "high", "low", "close", "volume")
COLUMN_ALIASES = {
    "date": ("date", "Date", "날짜", "Unnamed: 0", "index"),
    "open": ("open", "Open", "시가"),
    "high": ("high", "High", "고가"),
    "low": ("low", "Low", "저가"),
    "close": ("close", "Close", "종가"),
    "volume": ("volume", "Volume", "거래량"),
}
EIGHT_DIGIT_DATE = re.compile(r"\d{8}")


def normalize_price_frame(frame: pd.DataFrame) -> pd.DataFrame:
    materialized = _materialize_date_index(frame)
    renamed = materialized.rename(columns=_column_rename_map(materialized))
    normalized = renamed.loc[:, OHLCV_COLUMNS].copy()
    normalized["date"] = _normalize_date_column(normalized["date"])
    for column in OHLCV_COLUMNS[1:]:
        normalized[column] = pd.to_numeric(normalized[column], errors="raise")
    return normalized.set_index("date").sort_index().reset_index()


def _materialize_date_index(frame: pd.DataFrame) -> pd.DataFrame:
    date_aliases = COLUMN_ALIASES["date"]
    if any(alias in frame.columns for alias in date_aliases):
        return frame.copy()
    return frame.reset_index()


def _column_rename_map(frame: pd.DataFrame) -> dict[str, str]:
    rename_map: dict[str, str] = {}
    for canonical_name, aliases in COLUMN_ALIASES.items():
        source_name = next((alias for alias in aliases if alias in frame.columns), None)
        if source_name is None:
            raise KeyError(f"Missing OHLCV column: {canonical_name}")
        rename_map[source_name] = canonical_name
    return rename_map


def _normalize_date_column(values: pd.Series) -> pd.Series:
    text_values = values.astype(str).str.strip()
    eight_digit_values = text_values.str.fullmatch(EIGHT_DIGIT_DATE.pattern)
    parsed_values = pd.to_datetime(text_values.where(~eight_digit_values), errors="raise")
    formatted_values = text_values.where(eight_digit_values, parsed_values.dt.strftime("%Y%m%d"))
    return formatted_values.astype(int)
