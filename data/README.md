# 데이터 안내

이 폴더는 공개 가능한 샘플 데이터와 데이터 구조 설명을 두기 위한 공간이다.

원본 데이터는 `financial/`, `22_hf352-master/` 아래에 분산되어 있으며, 일부 파일은 크기가 크거나 외부 서비스에서 다시 받을 수 있는 데이터다.

## 주요 데이터

- `financial/dailychart.csv`: 전체 일봉 데이터. 100MB를 넘기 때문에 Git LFS 대상으로 지정했다.
- `financial/10_stocks_data/`: 프로젝트 대표 10개 종목 CSV.
- `financial/stocks_data/`, `financial/leader_stocks_data/`: 추가 종목과 업종 대표 종목 데이터.
- `data/sample/`: GitHub에서 바로 확인할 수 있는 샘플 CSV.

## 공개 주의

DB 파일, 실행 파일, 체크포인트, 개인정보성 자료는 Git 추적 대상에서 제외한다.
