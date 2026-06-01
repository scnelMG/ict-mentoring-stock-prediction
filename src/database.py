"""Database utilities for loading and storing stock market data."""

from __future__ import annotations

from collections.abc import Iterable

import pandas as pd
import pymysql
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine

from .config import DatabaseConfig


PRICE_COLUMNS = ["date", "open", "high", "low", "close", "volume"]


def create_mysql_connection(config: DatabaseConfig | None = None):
    """Create a PyMySQL connection from environment-backed config."""

    config = config or DatabaseConfig.from_env()
    return pymysql.connect(
        host=config.host,
        user=config.user,
        password=config.password,
        db=config.database,
        port=config.port,
        use_unicode=True,
        charset="utf8",
    )


def create_sqlalchemy_engine(config: DatabaseConfig | None = None) -> Engine:
    """Create a SQLAlchemy engine from environment-backed config."""

    config = config or DatabaseConfig.from_env()
    return create_engine(config.sqlalchemy_url)


def create_price_table(table_name: str, config: DatabaseConfig | None = None) -> None:
    """Create a stock price table if it does not exist."""

    sql = f"""
    CREATE TABLE IF NOT EXISTS `{table_name}` (
        date INT NOT NULL PRIMARY KEY,
        open INT,
        high INT,
        low INT,
        close INT,
        volume BIGINT
    )
    """
    with create_mysql_connection(config) as connection:
        with connection.cursor() as cursor:
            cursor.execute(sql)
        connection.commit()


def save_price_frame(
    frame: pd.DataFrame,
    table_name: str,
    config: DatabaseConfig | None = None,
    if_exists: str = "append",
) -> None:
    """Save a normalized OHLCV frame into MySQL."""

    normalized = normalize_price_frame(frame)
    engine = create_sqlalchemy_engine(config)
    with engine.begin() as connection:
        normalized.to_sql(table_name, con=connection, if_exists=if_exists, index=False)


def load_price_frame(table_name: str, config: DatabaseConfig | None = None) -> pd.DataFrame:
    """Load stock prices from MySQL and return a date-indexed frame."""

    engine = create_sqlalchemy_engine(config)
    with engine.begin() as connection:
        frame = pd.read_sql_table(table_name, connection)
    return prepare_price_index(frame)


def normalize_price_frame(frame: pd.DataFrame) -> pd.DataFrame:
    """Normalize Korean/English OHLCV columns into the schema used by the DB."""

    normalized = frame.copy()
    if len(normalized.columns) >= len(PRICE_COLUMNS):
        normalized = normalized.iloc[:, : len(PRICE_COLUMNS)]
        normalized.columns = PRICE_COLUMNS
    normalized["date"] = normalized["date"].astype(str).str.replace("-", "", regex=False)
    normalized["date"] = normalized["date"].astype(int)
    return normalized.sort_values("date")


def prepare_price_index(frame: pd.DataFrame) -> pd.DataFrame:
    """Return a frame indexed by datetime with English OHLCV column names."""

    prepared = frame.copy()
    prepared.columns = ["Date", "Open", "High", "Low", "Close", "Volume"]
    prepared["Date"] = pd.to_datetime(prepared["Date"].astype(str))
    prepared = prepared.sort_values("Date")
    return prepared.set_index("Date")


def initialize_tables_from_csv(
    csv_paths: Iterable[tuple[str, str]],
    config: DatabaseConfig | None = None,
) -> None:
    """Create tables and load CSV files.

    Args:
        csv_paths: Iterable of ``(table_name, csv_path)`` pairs.
    """

    for table_name, csv_path in csv_paths:
        create_price_table(table_name, config)
        save_price_frame(pd.read_csv(csv_path), table_name, config)
