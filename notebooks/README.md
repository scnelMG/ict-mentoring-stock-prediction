# 노트북 안내

이 폴더에는 포트폴리오에서 빠르게 읽을 수 있는 **경량 대표 노트북**만 둔다. 원본 실험 노트북과 주차별 작업 공간은 당시 Drive·로컬 보관 자료이며, 현재 공개 저장소에는 포함하지 않는다.

## 대표 흐름

1. 데이터 수집: KRX/네이버/키움 기반 가격 데이터 확보
2. 모델링: ARIMA, RNN, LSTM, GRU 실험
3. 피처 엔지니어링: 이동평균, 기술적 지표, PCA
4. 뉴스 분석: 네이버 금융 뉴스 제목 수집과 워드클라우드
5. GUI: PyQt 기반 검색/차트/예측 결과 화면

## 이 저장소의 대표 노트북

- `01_data_collection_overview.ipynb`: 종목 코드·OHLCV 수집과 정규화
- `02_modeling_overview.ipynb`: 기술 지표·PCA·시퀀스 모델 흐름
- `03_news_wordcloud_overview.ipynb`: 뉴스 제목 기반 워드클라우드
- `04_gui_overview.ipynb`: GUI 진입점과 공개 범위

각 노트북은 실행 결과를 재현한다고 주장하지 않는다. 실제 실행 조건과 제외 자료는 [재현성 안내](../docs/reproducibility.md)를 따른다.
