"""Configuration helpers for the stock prediction portfolio code.

The original project used local paths and a shared remote database while the
team was developing.  This public version keeps the same intent but reads
runtime values from environment variables so credentials are never committed.
"""

from __future__ import annotations

from dataclasses import dataclass
import os
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_DATA_DIR = PROJECT_ROOT / "data"
DEFAULT_ASSET_DIR = PROJECT_ROOT / "assets"


STOCK_CODES: dict[str, str] = {
    "삼성전자": "005930",
    "삼성바이오로직스": "207940",
    "현대차": "005380",
    "KB금융": "105560",
    "SK": "034730",
    "POSCO홀딩스": "005490",
    "SK이노베이션": "096770",
    "한국전력": "015760",
    "KT": "030200",
    "CJ제일제당": "097950",
}


@dataclass(frozen=True)
class DatabaseConfig:
    """Connection values for the MySQL database used in the original project."""

    host: str
    port: int
    user: str
    password: str
    database: str

    @classmethod
    def from_env(cls) -> "DatabaseConfig":
        return cls(
            host=os.getenv("STOCK_DB_HOST", "localhost"),
            port=int(os.getenv("STOCK_DB_PORT", "3306")),
            user=os.getenv("STOCK_DB_USER", "stock_user"),
            password=os.getenv("STOCK_DB_PASSWORD", ""),
            database=os.getenv("STOCK_DB_NAME", "stockdb"),
        )

    @property
    def sqlalchemy_url(self) -> str:
        return (
            f"mysql+pymysql://{self.user}:{self.password}"
            f"@{self.host}:{self.port}/{self.database}"
        )


def data_dir() -> Path:
    """Return the configured data directory."""

    return Path(os.getenv("STOCK_DATA_DIR", str(DEFAULT_DATA_DIR))).expanduser()


def asset_dir() -> Path:
    """Return the configured asset directory."""

    return Path(os.getenv("NEWS_WORDCLOUD_DIR", str(DEFAULT_ASSET_DIR))).expanduser()
