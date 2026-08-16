from __future__ import annotations

from src.config import DatabaseConfig
from src.database import _quote_mysql_identifier


def test_database_config_returns_url_object_without_serializing_password() -> None:
    given_config = DatabaseConfig(
        host="db.example.test",
        port=3307,
        user="stock@user",
        password="",
        database="stockdb",
    )

    when_url = given_config.sqlalchemy_url

    assert when_url.drivername == "mysql+pymysql"
    assert when_url.username == "stock@user"
    assert when_url.host == "db.example.test"
    assert when_url.port == 3307
    assert when_url.database == "stockdb"


def test_quote_mysql_identifier_escapes_closing_backticks() -> None:
    when_identifier = _quote_mysql_identifier("stock`prices")

    assert when_identifier == "`stock``prices`"
