# Release checklist

Do not create `v0.1.0` until these checks pass.

## Local

```powershell
uv sync --extra dev --locked
uv run ruff check .
uv run pytest --cov=entralab --cov-report=term-missing
uv run entralab all
uv run entralab demo
git diff --ignore-space-at-eol --exit-code -- reports/latest
uv run detect-secrets-hook --baseline .secrets.baseline $(git ls-files)
uv run pip-audit --skip-editable
```

## Public

- GitHub Actions validation is green.
- GitHub Pages is enabled with GitHub Actions as the source.
- Public demo returns `200`.
- GitBook documentation returns `200`.
- Playbook links in the demo point to the published GitBook space.

## Release

```powershell
git tag -a v0.1.0 -m "v0.1.0"
git push origin v0.1.0
```
