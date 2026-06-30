# Contributing

Contributions should keep the lab defensive, synthetic and reproducible.

Before opening a pull request, run:

```powershell
uv run ruff check .
uv run pytest --cov=entralab --cov-report=term-missing
uv run entralab all
uv run entralab demo
uv run detect-secrets-hook --baseline .secrets.baseline $(git ls-files)
uv run pip-audit --skip-editable
```

Do not add real tenant data, credentials, tokens, malware, payloads, uploads, backend services or host-changing actions.
