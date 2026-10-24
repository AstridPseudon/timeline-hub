## Review report

Scoped security review: **PASS for the standalone historical-image redo case**. No code changes made.

Finding verified:

- Missing root: `internal-revision:authoring-timeline-revision-f910933b73f56ce54527d7f6c40e60bb75e2c7771837f26dd29933e285ca9aed`
- Owner: `occurrence:return-owner/shot`
- Authenticated ranges: native `[0,1]`, effect `[0,3]`
- Parent `36760ee…`: **1 expected failure**
- Reviewed commit `2e96c68ca7f80147a6cd04cde17c574f063846ad`, tree `40eb05d5a51b8d7b31cbfad8a38afeb3318fbd44`

Tests:

```text
ASTRID_CHECKOUT=<archive of Agent 12701589ab...> PYTHONPATH=. \
/home/user/work/venv-agent/bin/python -m pytest tests/test_timeline_inverse_historical_image.py \
-q -o addopts= -p no:cacheprovider
```

**13 passed**

```text
/home/user/work/venv-runtime/bin/python -m pytest -q -p no:cacheprovider \
tests/test_timeline_inverse_occurrence_retirement.py \
tests/test_timeline_inverse_stage_authentication.py \
tests/test_timeline_commit_authentication.py \
tests/test_timeline_history_authenticated_read.py \
tests/test_timeline_source_duplicate_authority.py
```

**243 passed, 74 deselected**

Additional checks:

- Ruff changed files: **passed**
- Scoped Pyright parent/final: **0 errors / 0 errors**
- Artifact manifest: **passed**
- `git diff --check`: **passed**
- 502 protected base files byte-identical; aggregate SHA256:
  `75de7fb81b97ba2320751d61c6b0fa3da9cc8fb6c0a15552fc8e5ea95d26ce3e`

Source archive: Agent `12701589abffd840054515996612d0ed0dd33af0`, tree `efad939c87b5805f2a6f45827ec1a17db3eac5f4`.

The author’s temporary `/tmp/w-3031a908e5` capture directory is gone, and no 61,298-byte capture or 11 manifest artifacts remain available. I therefore could not independently recheck their custody/artifact bytes; the reported capture hash is `2a157e975c3c8f022e119375bf67fe8fbc2153282549c88500c5b8f965379131`. The original 0339 private packet remains uncertified and must not be credited.

No full suite, HTTP, browser, original-family, or benchmark run performed.