# Reproducibility Guide

## Scope

This guide defines what a public reviewer can run or inspect without private credentials or the original team workspace. The repository supports partial reproduction and inspection, not full recreation of every 2022 mentoring experiment.

## Environment Setup

```powershell
uv venv
.\.venv\Scripts\Activate.ps1
uv pip install -r requirements.txt
Copy-Item .env.example .env
```

Edit `.env` only on the local machine. Do not commit `.env`.

```text
STOCK_DB_HOST=localhost
STOCK_DB_PORT=3306
STOCK_DB_USER=stock_user
STOCK_DB_PASSWORD=__SET_LOCALLY_NOT_COMMITTED__
STOCK_DB_NAME=stockdb
STOCK_DATA_DIR=data/sample
NEWS_WORDCLOUD_DIR=assets
```

`STOCK_DB_PASSWORD` is an environment variable name, not a published credential. The value shown above is a dummy placeholder.

## Verification Commands

These commands verify the public source surface without requiring private data:

```powershell
python -m compileall src
Test-Path .env.example
uv run --with pytest --with numpy --with pandas --with scikit-learn pytest tests -q
```

Optional runtime checks:

```powershell
python -m src.news_wordcloud
python -m src.app_main
```

The optional commands depend on external services and local desktop/runtime setup.

## Component Reproduction Notes

| Component | Public reproduction status | Notes |
| --- | --- | --- |
| Configuration | Inspectable | `.env.example` contains safe placeholders only. |
| Data collection | Partial | PyKrx/Naver requests require network access and may vary by date or website behavior. |
| Database storage | Local-only | MySQL must be created locally; original remote credentials are excluded. |
| Feature engineering | Inspectable/reusable | Requires a DataFrame with normalized OHLCV columns. |
| Modeling | Inspectable/partial | Requires prepared data; recurrent models preserve chronological train/test ordering, fit preprocessing on the training period only, and use the tail of that period for early stopping. Final historical model metrics are not republished. |
| News wordcloud | Optional run | Requires network access, KoNLPy/Okt, Java, and Korean font support. |
| PyQt GUI | Local inspection only | Requires PyQt5, a desktop session, and the historical `.ui` file path. |

## Data Boundary

Public data is limited to `data/sample/` and curated artifacts in `assets/`.

The following are not required for public reproduction and must not be treated as publishable evidence without separate review:

- Private `.env` files or database dumps.
- HWP reports, personal/team screenshots, KakaoTalk captures, application forms, and Drive-only raw materials.
- Unreviewed historical workspace files under local-only folders.
- Raw market or private data beyond the curated public samples.

## Known Limits

- Kiwoom OpenAPI workflows depend on Windows, account login, and OCX setup.
- KoNLPy may require local Java configuration.
- External website markup can change, causing crawlers to fail.
- 대표 노트북은 코드 진입점을 설명하는 경량 안내 자료이며, 당시 전체 실험 노트북·로컬 경로는 공개하지 않는다.
- Published docs do not include a final independently reproducible model metric.
