# ICT Mentoring Stock Prediction System

Portfolio reconstruction of a 2022 Hanium ICT Mentoring project for stock-price data collection, feature engineering, recurrent model experiments, news keyword visualization, and a PyQt inspection GUI.

This repository is meant to show the engineering shape of the system without requiring private credentials, the original team workspace, or raw financial datasets.

## Review Path

1. Start with this README for the system map, data policy, and reproduction limits.
2. Read [docs/project-summary.md](docs/project-summary.md) for the project brief and contribution boundary.
3. Read [docs/architecture.md](docs/architecture.md) for the data flow and component responsibilities.
4. Read [docs/reproducibility.md](docs/reproducibility.md) before trying to run any command locally.
5. Inspect `src/` for the public, cleaned implementation entry points.

## Problem

The project explored how Korean stock OHLCV data, technical indicators, and finance-news signals can be organized into a price-prediction workflow. The original mentoring deliverable combined data acquisition, database storage, model experimentation, keyword visualization, and a desktop GUI so a reviewer could inspect stock trends and prediction outputs.

This public repo does not present the system as investment advice and does not claim production trading performance.

## Role and Contribution

The publishable work represented here covers:

- Curating the original mentoring project into a reviewer-readable portfolio repository.
- Refactoring representative implementation paths into `src/` instead of publishing the full historical workspace.
- Documenting the data pipeline, environment variables, modeling approach, GUI boundary, and public/private data split.
- Preserving safe sample data and screenshots while excluding personal, credential, and raw workspace material.

The 2022 project was a mentoring/team project. This repository documents the implementation areas and artifacts available for public inspection, not sole authorship of every original file.

## Tech Stack

| Area | Tools |
| --- | --- |
| Data collection | Python, pandas, requests, BeautifulSoup, pykrx, Kiwoom OpenAPI context |
| Storage | MySQL, SQLite, SQLAlchemy, PyMySQL |
| Feature engineering | moving averages, volume/volatility/trend/momentum indicators, `ta` |
| Modeling | NumPy, scikit-learn, PCA, TensorFlow/Keras, LSTM, GRU, historical ARIMA/RNN experiments |
| News analysis | Naver Finance titles, KoNLPy/Okt, wordcloud |
| GUI | PyQt5, Qt Designer `.ui` files from the original local project |

## Architecture and Pipeline

```text
External market/news sources
  -> data collection (`src/data_collection.py`)
  -> normalized OHLCV storage (`src/database.py`)
  -> technical indicators (`src/features.py`)
  -> PCA + sequence dataset (`src/modeling.py`)
  -> LSTM/GRU training experiments
  -> news keyword counts + wordcloud (`src/news_wordcloud.py`)
  -> PyQt inspection shell (`src/app_main.py`)
```

Important source entry points:

- `src/config.py`: stock-code map, safe path helpers, and environment-variable based database settings.
- `src/data_collection.py`: KRX, PyKrx, Naver daily price, and Naver Finance news-title collection helpers.
- `src/database.py`: MySQL connection, OHLCV normalization, table creation, storage, and loading utilities.
- `src/features.py`: moving average and technical-indicator generation for model inputs.
- `src/modeling.py`: deterministic seed setup, PCA reduction, sequence dataset construction, and compact LSTM/GRU models.
- `src/news_wordcloud.py`: Korean noun extraction and wordcloud generation from recent finance-news titles.
- `src/app_main.py`: minimal PyQt entry point that loads the historical Qt Designer UI file when it exists locally.

## Setup and Environment

The safe local setup path is:

```powershell
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
Copy-Item .env.example .env
```

The `.env.example` file intentionally contains variable names and dummy placeholders only. Real database values must stay in `.env`, which is ignored by Git.

Key variables:

| Variable | Purpose | Public value policy |
| --- | --- | --- |
| `STOCK_DB_HOST` | Local or private MySQL host | use `localhost` in examples |
| `STOCK_DB_PORT` | MySQL port | safe numeric placeholder |
| `STOCK_DB_USER` | MySQL user | dummy local username only |
| `STOCK_DB_PASSWORD` | MySQL password | placeholder only, never a real secret |
| `STOCK_DB_NAME` | MySQL database | dummy database name |
| `STOCK_DATA_DIR` | CSV/sample data root | defaults to `data/sample` for public inspection |
| `NEWS_WORDCLOUD_DIR` | output directory for generated wordclouds | defaults to `assets` |

## Data and Public-Safety Policy

Publicly inspectable data is limited to small sample CSVs under `data/sample/` and curated images under `assets/`.

Excluded from the portfolio surface:

- Real `.env` files, database passwords, remote database hosts, API keys, and credential material.
- Personal/team screenshots, KakaoTalk captures, application forms, HWP reports, IDE settings, executables, and duplicate archives.
- Raw local workspace folders and unrestricted financial datasets that are unnecessary for a public reviewer.
- Any Drive report contents that contain names, teammate information, personal screenshots, or redistribution-sensitive material.

`financial/dailychart.csv` is tracked through Git LFS because it is large historical market data. It is not required for the README review path and should not be modified during documentation-only portfolio cleanup.

## Reproduce or Inspect

Recommended public inspection path:

```powershell
python -m compileall src
python -m src.news_wordcloud
```

`python -m src.news_wordcloud` requires network access to Naver Finance plus a working KoNLPy/Java environment. The generated output path is printed by the script.

`python -m src.app_main` is an inspection path for the GUI shell, but it requires the historical `financial/qt_design/main_window.ui` file and a desktop environment with PyQt5 installed.

Full end-to-end model reproduction is intentionally limited because the original MySQL database, Kiwoom/OpenAPI setup, local UI files, and parts of the historical experiment workspace are not public-safe or not portable.

## Evidence and Results

Inspectable artifacts in this repo:

- Cleaned representative source code under `src/`.
- Notebook review guide under `notebooks/README.md`.
- Safe sample data under `data/sample/`.
- GUI and wordcloud screenshots under `assets/`.
- Project and reproducibility documentation under `docs/`.

The repository does not publish a final verified trading metric. Historical ARIMA/RNN/LSTM/GRU experiments are documented as project work, but public reproduction is constrained by data and environment limits.

## Limitations

- This is a portfolio reconstruction of a 2022 mentoring project, not a maintained trading product.
- Stock prices are volatile and the models here must not be used for financial advice.
- Network crawlers can break when external websites change markup or access rules.
- Kiwoom OpenAPI and some PyQt UI paths are Windows/local-environment dependent.
- KoNLPy/Okt can require local Java and Korean font setup.
- Full model results are not independently reproducible from a clean public checkout without the excluded original data and database environment.
