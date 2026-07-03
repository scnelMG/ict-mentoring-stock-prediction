# Publication Checklist

Run this checklist before committing or pushing the portfolio version.

## Required Safety Checks

- [ ] Confirm `git status --short` and preserve unrelated dirty files.
- [ ] Confirm `.env` is ignored and only `.env.example` is tracked.
- [ ] Scan for credentials with `rg -i "api_key=|secret|password|token|begin private key" . --glob "!.git/**"`.
- [ ] Classify environment variable names such as `STOCK_DB_PASSWORD` as safe placeholders only when no real value is present.
- [ ] Scan for personal/team material such as KakaoTalk captures, HWP reports, application forms, phone numbers, emails, and private screenshots.
- [ ] Scan for archives, executables, notebook checkpoints, database dumps, and files larger than 50 MB.
- [ ] Confirm `financial/dailychart.csv` is intentionally Git LFS-managed and is not part of a docs-only change.
- [ ] Review every README/docs link and image path.
- [ ] Run `python -m compileall src` when Python is available.
- [ ] Review `git diff -- README.md docs .env.example` before publication.

## Publish Blockers

Block publication until reviewed or removed:

- Real database hostnames, passwords, tokens, API keys, cookies, or credential files.
- HWP reports or screenshots containing names, teammate details, chats, forms, grades, emails, or phone numbers.
- Raw financial/private data not explicitly approved for public GitHub.
- Drive folders copied wholesale into the repo.
- Unsupported model-performance, ranking, or investment claims.
