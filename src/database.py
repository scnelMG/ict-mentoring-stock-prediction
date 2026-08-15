"""Database utilities for loading and storing stock market data."""

from __future__ import annotations

from collections.abc import Iterable
from typing import Literal

import pandas as pd
import pymysql
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine

from .config import DatabaseConfig
from .ohlcv import normalize_price_frame


def create_mysql_connection(config: DatabaseConfig | None = None):
    """Create a PyMySQL connection from environment-backed config."""

    config = config or DatabaseConfig.from_env()
    return pymysql.connect(
        host=config.host,
        user=config.user,
        password=config.password,
        database=config.database,
        port=config.port,
        use_unicode=True,
        charset="utf8",
    )


def create_sqlalchemy_engine(config: DatabaseConfig | None = None) -> Engine:
    """Create a SQLAlchemy engine from environment-backed config."""

    config = config or DatabaseConfig.from_env()
    return create_engine(config.sqlalchemy_url)


def _quote_mysql_identifier(identifier: str) -> str:
    return f"`{identifier.replace('`', '``')}`"


def create_price_table(table_name: str, config: DatabaseConfig | None = None) -> None:
    """Create a stock price table if it does not exist."""

    quoted_table_name = _quote_mysql_identifier(table_name)
    sql = f"""
    CREATE TABLE IF NOT EXISTS {quoted_table_name} (
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
    if_exists: Literal["fail", "replace", "append", "delete_rows"] = "append",
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
