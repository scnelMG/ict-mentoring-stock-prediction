# 공개 전 체크리스트

- [ ] `rg -i "password|secret|token|api[_-]?key|aws|rds|email|전화" .`로 민감정보를 확인한다.
- [ ] 개인정보성 파일이 `.gitignore`로 제외되는지 확인한다.
- [ ] `financial/dailychart.csv`가 Git LFS 대상으로 잡혔는지 확인한다.
- [ ] README 링크가 실제 파일과 맞는지 확인한다.
- [ ] `src/` Python 파일이 문법 오류 없이 컴파일되는지 확인한다.
- [ ] 커밋 전 `git diff --cached --stat`와 `git diff --cached`를 검토한다.
