## D102c report

- Ran the authorized native-seed reproduction using exact sources:
  - App `0244db2c`
  - Agent `bde57850`
  - Composition `635f4de0`
  - Runtime `0c62dfa6` and `689352013`
- Results:
  - Runtime `0c62dfa6`: accepted.
  - Runtime `689352013`: measured `not_ready` / `runtime_unavailable` failure, source-mapped to HTTP 503.
  - Runtime `689352013` private overlay with only `request_id` removed from shared context and retained locally for diagnostics: accepted.
- Source confirms the path:
  - `service.py:2504-2507` adds `request_id` to context.
  - `timeline_commit_execution.py:214-217` propagates it.
  - `timeline_commit_store.py:816-825` strictly validates replay context; `CommitContext` excludes `request_id`.
  - Agent capture retains the full context at `_commit_preview.py:85-86`.

Tests/checks:

- `node --check .../d66-plain-stack.mjs` — PASS
- Targeted Runtime pytest — `32 passed in 5.82s`
- `git diff --check` — PASS
- All exact source checkouts remained clean.
- No product, test, schema, generated, or normal-branch changes.

Unverified: no historical 12031 payload/credential replay and no browser/full journey, as explicitly disallowed. Private evidence remained under 1 MB. Completion marker and commit message were written.