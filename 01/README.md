# sweep

파일을 확장자별 폴더로 정리하는 작은 CLI입니다.

기본 실행은 미리보기만 합니다.

```bash
uv run python main.py
```

특정 폴더를 보려면:

```bash
uv run python main.py ~/Downloads
```

실제로 이동하려면:

```bash
uv run python main.py ~/Downloads --apply
```
