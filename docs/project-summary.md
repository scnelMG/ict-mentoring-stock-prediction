# Project Summary

## Purpose

This repository documents a 2022 Hanium ICT Mentoring project that explored a stock-price prediction workflow for Korean listed companies. The public version focuses on engineering clarity: how data enters the system, how features and sequence datasets are prepared, how recurrent models were structured, and how news keywords and GUI artifacts fit around the modeling work.

## Problem

The original project asked whether market OHLCV data, technical indicators, and finance-news headlines could be combined into a practical inspection workflow for stock-price prediction experiments. The project output was a prototype system, not a deployable trading service.

## Contribution Boundary

The public repository represents these contribution areas:

- Data collection and normalization paths for KRX/PyKrx/Naver Finance data.
- MySQL-oriented storage utilities with credentials moved to environment variables.
- Feature engineering for moving averages and technical indicators.
- PCA-based feature reduction and LSTM/GRU sequence-model helpers.
- Finance-news title collection and Korean noun wordcloud generation.
- PyQt GUI entry-point documentation and safe screenshot curation.
- Publication cleanup that excludes credentials, personal/team files, and raw workspace material.

Because the project came from a mentoring/team context, the repo describes the inspectable implementation surface and does not overclaim sole ownership of all historical deliverables.

## System Flow

1. Collect stock codes, OHLCV rows, and finance-news titles from external sources.
2. Normalize OHLCV columns and optionally persist them to MySQL.
3. Build technical indicators across moving-average, volume, volatility, trend, and momentum families.
4. Scale features, reduce non-target features with PCA, and construct fixed-window sequence datasets.
5. Train compact recurrent models such as LSTM or GRU with early stopping.
6. Generate wordcloud images from recent Naver Finance titles.
7. Load the historical Qt Designer UI when local GUI files are present.

## Public Artifacts

- `src/`: cleaned, readable implementation surface.
- `notebooks/README.md`: notebook review guide for the historical experiment flow.
- `data/sample/`: small CSV samples for schema inspection.
- `assets/gui/` and `assets/wordclouds/`: curated, public-safe images.
- `docs/reproducibility.md`: setup commands, environment variables, and run limits.
- `docs/architecture.md`: component map and data-flow notes.

## Public-Safety Notes

The repository intentionally excludes or quarantines personal screenshots, KakaoTalk captures, HWP reports, application forms, real `.env` files, database credentials, executables, IDE settings, and unreviewed raw workspace files. Drive materials are treated as reference-only unless an asset is separately reviewed as public-safe.

## Reproducibility Level

The project is partially reproducible. Source files can be compiled and inspected from a clean checkout, and selected scripts can run when their external dependencies are available. End-to-end recreation of the original mentoring results is limited by private/local database state, external service dependencies, Windows-specific GUI/OpenAPI requirements, and excluded raw data.

## Limitations

- The repo is for portfolio inspection and engineering review, not investment decision support.
- No publishable, independently verified final trading metric is claimed.
- External crawling and market-data APIs may change behavior over time.
- Historical notebooks may assume local paths from the original 2022 workspace.
