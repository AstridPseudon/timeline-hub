## Report

Read-only whole-path investigation complete.

Finding: the line 1192 refusal is caused at the producer seam: `STORE_BUILD` writes raw `pip freeze --all` output (`make-child-venv:702–704`), while `STORE_VERIFY` independently canonicalizes installed distribution inventory (`1177–1192`). No verifier relaxation is indicated.

Evidence written:

- `evidence/wholepath.json`
- `evidence/all-checks.json`
- `evidence/source-manifest.json`
- `evidence/validation.md`

Checks:

- `bash -n`: PASS
- Embedded Python AST checks: PASS, all 7 blocks
- Source/protected hash checks: PASS
- JSON validation: PASS
- `git diff --check`: PASS

Actual retained Farm tree/report was unavailable (`EXACTMISSING`), so no field-level mismatch was invented and no build, install, retry, registration, or product tests were run. Next step is independent review of the sole producer correction, followed by one authorized real Farm request.