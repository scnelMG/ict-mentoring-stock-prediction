# 재현 및 실행 안내

## 환경 준비

```powershell
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
Copy-Item .env.example .env
```

`.env`에 로컬 DB 정보를 입력한다.

```text
STOCK_DB_HOST=localhost
STOCK_DB_PORT=3306
STOCK_DB_USER=stock_user
STOCK_DB_PASSWORD=your-password
STOCK_DB_NAME=stockdb
```

## 제한사항

- Kiwoom OpenAPI 코드는 Windows, 증권사 로그인, OCX 환경에 의존한다.
- 원본 MySQL RDS 접속정보는 공개 저장소에서 제거했다.
- 일부 원본 노트북은 과거 로컬 경로와 데이터 파일을 전제로 작성되었다.
- KoNLPy/Okt는 Java 환경 설정이 필요할 수 있다.
- PyQt 화면은 `financial/qt_design/*.ui` 원본 UI 파일이 있어야 실행된다.

## 대표 코드 실행 예시

```powershell
python -m src.news_wordcloud
python -m src.app_main
```

데이터 수집과 모델 학습은 네트워크, DB, 외부 API 상태에 따라 결과가 달라질 수 있다.
