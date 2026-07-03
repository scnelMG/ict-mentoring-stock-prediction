# Architecture Notes

## System Design

The public architecture is a modular stock-analysis pipeline rather than a single runnable production app. Each source file in `src/` isolates one responsibility so a reviewer can inspect the system without opening the full historical workspace.

```text
KRX/PyKrx/Naver Finance
  -> collection helpers
  -> normalized OHLCV frames
  -> optional MySQL persistence
  -> technical indicators
  -> PCA and fixed-window sequence arrays
  -> LSTM/GRU experiments
  -> news keyword wordclouds
  -> PyQt GUI inspection shell
```

## Components

| Component | File | Responsibility |
| --- | --- | --- |
| Configuration | `src/config.py` | Central stock-code list, project paths, data paths, and safe environment-variable based DB configuration. |
| Collection | `src/data_collection.py` | KRX company-code lookup, PyKrx OHLCV collection, Naver daily price scraping, and Naver Finance title crawling. |
| Storage | `src/database.py` | MySQL engine creation, OHLCV schema normalization, table creation, insert, and load helpers. |
| Features | `src/features.py` | Moving averages plus volume, volatility, trend, and momentum indicators using `ta`. |
| Modeling | `src/modeling.py` | Reproducible seed setup, PCA feature reduction, sequence dataset construction, and LSTM/GRU model helpers. |
| News visualization | `src/news_wordcloud.py` | Title cleaning, Korean noun extraction, keyword counts, and wordcloud image generation. |
| GUI | `src/app_main.py` | Minimal PyQt entry point that loads the historical Qt Designer UI file when present locally. |

## Data Flow

1. `fetch_portfolio_stocks()` collects OHLCV frames for the ten representative stock codes.
2. `normalize_price_frame()` standardizes Korean source columns into Date/Open/High/Low/Close/Volume style fields.
3. `save_price_frame()` can persist each normalized frame to MySQL for local experiments.
4. `build_model_frame()` enriches price rows with moving averages and technical indicators.
5. `make_sequence_dataset()` scales/reduces features and creates train/test windows without shuffling time order.
6. `train_model()` builds and trains a compact LSTM or GRU regression model with early stopping.
7. `collect_recent_titles()` and `generate_wordcloud()` provide a separate news-keyword visualization path.

## Reproducibility Controls

- Database configuration is read from environment variables, not hardcoded credentials.
- `set_reproducible_seed()` sets Python, NumPy, and TensorFlow seeds for model experiments.
- Public sample data lives under `data/sample/`; full historical reproduction needs excluded local data and database state.
- External-source calls are intentionally not mocked in the public docs because their outputs change over time.

## Inspection Boundaries

- The GUI entry point is inspectable, but a full desktop run needs the historical `.ui` file and PyQt environment.
- Kiwoom/OpenAPI behavior is documented as original project context and is not a clean public dependency.
- This architecture is for portfolio review and reproducibility explanation, not a production deployment design.
