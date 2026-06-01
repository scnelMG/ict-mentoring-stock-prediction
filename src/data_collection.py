"""Data collection helpers used by the portfolio version of the project."""

from __future__ import annotations

from datetime import date
from pathlib import Path

import pandas as pd
import requests
from bs4 import BeautifulSoup
from pykrx import stock

from .config import STOCK_CODES
from .database import normalize_price_frame


KRX_CORP_LIST_URL = (
    "http://kind.krx.co.kr/corpgeneral/corpList.do"
    "?method=download&searchType=13"
)
NAVER_DAILY_PRICE_URL = "https://finance.naver.com/item/sise_day.naver"


def load_krx_company_codes() -> pd.DataFrame:
    """Download KRX listed company names and six-digit stock codes."""

    frame = pd.read_html(KRX_CORP_LIST_URL, header=0)[0]
    frame["종목코드"] = frame["종목코드"].map("{:06d}".format)
    return frame[["회사명", "종목코드"]].rename(
        columns={"회사명": "name", "종목코드": "code"}
    )


def find_stock_code(item_name: str, code_frame: pd.DataFrame | None = None) -> str:
    """Find a stock code by exact Korean company name."""

    code_frame = code_frame if code_frame is not None else load_krx_company_codes()
    matches = code_frame.loc[code_frame["name"] == item_name, "code"]
    if matches.empty:
        raise ValueError(f"Unknown listed company: {item_name}")
    return str(matches.iloc[0])


def fetch_naver_daily_prices(item_name: str, pages: int = 20) -> pd.DataFrame:
    """Fetch daily price rows from Naver Finance."""

    code = find_stock_code(item_name)
    frames: list[pd.DataFrame] = []
    headers = {"User-agent": "Mozilla/5.0"}
    for page in range(1, pages + 1):
        response = requests.get(
            NAVER_DAILY_PRICE_URL,
            params={"code": code, "page": page},
            headers=headers,
            timeout=10,
        )
        response.raise_for_status()
        frames.append(pd.read_html(response.text, encoding="cp949")[0])
    return pd.concat(frames, ignore_index=True).dropna()


def fetch_pykrx_ohlcv(
    ticker: str,
    start: str | date,
    end: str | date,
) -> pd.DataFrame:
    """Fetch OHLCV data from PyKrx and normalize it for database storage."""

    start_text = _date_to_yyyymmdd(start)
    end_text = _date_to_yyyymmdd(end)
    frame = stock.get_market_ohlcv_by_date(start_text, end_text, ticker)
    frame = frame.reset_index().iloc[:, :-2]
    return normalize_price_frame(frame)


def fetch_portfolio_stocks(start: str, end: str) -> dict[str, pd.DataFrame]:
    """Fetch OHLCV frames for the ten stocks used in the project."""

    return {
        stock_name: fetch_pykrx_ohlcv(ticker, start, end)
        for stock_name, ticker in STOCK_CODES.items()
    }


def save_frames(frames: dict[str, pd.DataFrame], output_dir: Path) -> None:
    """Save fetched frames as CSV files."""

    output_dir.mkdir(parents=True, exist_ok=True)
    for stock_name, frame in frames.items():
        frame.to_csv(output_dir / f"{stock_name}.csv", index=False, encoding="utf-8-sig")


def crawl_naver_finance_titles(target_date: str | None = None) -> list[str]:
    """Collect finance news titles from Naver Finance."""

    params = {"mode": "LSS2D", "section_id": "101", "section_id2": "258"}
    if target_date:
        params["date"] = target_date

    titles: list[str] = []
    page = 1
    while True:
        page_params = {**params, "page": page}
        response = requests.get(
            "https://finance.naver.com/news/news_list.naver",
            params=page_params,
            timeout=10,
        )
        response.raise_for_status()
        soup = BeautifulSoup(response.content, "lxml")
        links = soup.select(".articleSubject > a")
        if not links:
            break
        titles.extend(" ".join(link.get_text(strip=True).split()) for link in links)
        page += 1
    return titles


def _date_to_yyyymmdd(value: str | date) -> str:
    if isinstance(value, date):
        return value.strftime("%Y%m%d")
    return value.replace("-", "")
