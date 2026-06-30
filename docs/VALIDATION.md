# Validation

The validation flow compares each synthetic scenario against the local oracle.

```powershell
uv run entralab validate
uv run entralab report
uv run entralab demo
```

Generated outputs:

- `artifacts/validation.json`
- `reports/latest/report.md`
- `reports/latest/report.html`
- `reports/latest/validation-matrix.csv`
- `reports/latest/demo.html`

The validation report is reviewer-ready, but it does not claim production detection performance. It proves that the lab logic, fixtures and reporting remain internally consistent.
