## U1d integrated qualification

- Verified `HEAD=e68cf2316` tree equals `60e7838d8` exactly: `a2cbedd1`.
- Verified genuine `d4f496ec4` ancestry.
- Runtime worktree remains clean; no product changes or commit made.
- Agent:
  - `HEAD=47b744dfe9`, tree `68a73004`
  - `origin/main=9244377167`
  - pinned source `1a407fef`

Targeted union command completed with raw exit `1`:

- `448 passed`
- `9 skipped` — all named Windows-native platform tests
- `2 xfailed` — the two pre-existing strict retired-route tests
- XML: `459 tests`, `0 failures`, `0 errors`, `11 skipped`
- No actual source failures.

Static checks all passed:

- `generators/generate.py --check`
- `scripts/artifact_manifest.py --check` — manifest current
- Scoped Ruff
- Python compile
- `git diff --check`

Reused prior normalized Pyright evidence: both relevant source blobs match the reviewed candidate; prior result was 142 existing diagnostics. No broad typing rerun.

Evidence retained under the worker evidence directory. No full suite, browser, or security/source review was repeated. DONE marker created.