# V2 partial repair review — PASS bounded corrections, BLOCKED overall

Source reviewed: `956e633d07e0ce401e82a8f89674638f4d75e60b` (`tl/agt-V2-timing-identity-repair-sol-0139`), parent `1a0ea1a40b18084c74f4e40e79b51bef9101acbf`.

## Verdict

- **PASS — bounded correction 1:** `validation.py` treats absent and explicit JSON `null` `from` values as arithmetic zero for source-window and asset-bound checks, while preserving authored JSON `null`; negative, nonnumeric, and out-of-bounds values remain refused.
- **PASS — bounded correction 2:** `_commit_timing_validation.py` carries exact physical child revision/digest pins from the authenticated canonical closure, and `_timing_evaluators.py` keeps repeated shared-image cut intervals local per occurrence. Distinct revisions remain ambiguous even with equal JSON; there is no ambiguity blanket exemption.
- **BLOCKED — overall V2/P1:** the unchanged original P1 corpus is `13 passed, 4 failed`. The four failures now reach the retained timing declaration check and refuse on the inherited unbound word declaration `app.astrid.on="old-anchor"`; no fixture or expectation was changed. Do not call whole V2 qualified.

## Review findings

The changes are limited to the three named production modules and focused regressions. The adapter reuses the existing pure `document_from_bundle` converter only when `_runtime_document` is present; it does not fork the compiler or perform IO. The kernel still rejects genuinely distinct physical revisions with equal serialized content. The added local cut graph preserves occurrence-specific start/end ownership for one verified shared child and retains the original global cut-cycle machinery. No implicit shared fork, guessed source identity, lost ordered effect, or production/test weakening was found.

The overall blocker is the settled Proof-owned issue from escalation `agent-20261023T0151-P1-unbound-anchor.md`: the four original child/merge vectors retain `old-anchor` without an exact transcript binding. A policy/fixture decision is required before those original assertions can pass; this review does not make that decision or alter the fixtures.

## Evidence

All subprocess tests used `ASTRID_RUNTIME_CHECKOUT=/home/user/work/wt/rt-pin-27f0306b`, `PYTHONPATH=.:/home/user/work/wt/rt-pin-27f0306b`, and private temp/cache paths.

```text
/home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider --tb=short \
  tests/editing_conformance/test_commit_timing_validation.py \
  tests/editing_conformance/test_commit_v2_validation.py \
  tests/sdk/test_timing_cycles.py
→ 59 passed in 15.97s

/home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider --tb=short \
  tests/sdk/test_timing_compiler.py \
  tests/sdk/test_timeline_commit_provider_document.py \
  tests/sdk/test_timeline_commit_provider.py
→ 188 passed in 31.03s

/home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider --tb=short \
  tests/sdk/test_p1_doc_patch_provider.py
→ 13 passed, 4 failed in 2.27s (unchanged original P1 assertions; all four fail on missing exact word binding for old-anchor)

/home/user/work/venv-agent/bin/python -m ruff check --no-cache \
  astrid/sdk/timeline/validation.py astrid/sdk/timeline/_commit_timing_validation.py \
  astrid/sdk/timeline/_timing_evaluators.py \
  tests/editing_conformance/test_commit_timing_validation.py \
  tests/editing_conformance/test_commit_v2_validation.py
→ All checks passed!

/tmp/astrid-u2-typecheck/bin/python -m mypy --cache-dir /tmp/w-5744b9561d/mypy-scoped \
  astrid/sdk/timeline/validation.py astrid/sdk/timeline/_commit_timing_validation.py \
  astrid/sdk/timeline/_timing_evaluators.py
→ Success: no issues found in 3 source files

make ruff PY=/home/user/work/venv-agent/bin/python
→ current=2151 baseline=2151

make mypy PY=/tmp/astrid-u2-typecheck/bin/python
→ current=1915 baseline=1915

git diff --check
→ clean
```

## Next step

Proof/orchestrator must resolve whether unchanged unresolved legacy timing declarations are allowed or provide an authentic binding, then rerun the unchanged four P1 assertions. No full/browser/live-socket suite was requested or run.
