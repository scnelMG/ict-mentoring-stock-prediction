from __future__ import annotations

from src.config import DatabaseConfig
from src.database import _quote_mysql_identifier


def test_database_config_encodes_reserved_characters_in_sqlalchemy_url() -> None:
    given_config = DatabaseConfig(
        host="db.example.test",
        port=3307,
        user="stock@user",
        password="p@ss/word",
        database="stockdb",
    )

    when_url = given_config.sqlalchemy_url

    assert when_url == "mysql+pymysql://stock%40user:p%40ss%2Fword@db.example.test:3307/stockdb"


def test_quote_mysql_identifier_escapes_closing_backticks() -> None:
    when_identifier = _quote_mysql_identifier("stock`prices")

    assert when_identifier == "`stock``prices`"
