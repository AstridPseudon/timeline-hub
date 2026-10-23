# PASS — independent G2 exact current-pair reader review

Reviewed `tl/agt-G2-restore-reader-sol-1804` at `75fde1b96259ab3bc29923229e3b01e668a61bc6` against PLAN §3 G2/G5/C0.

## Verdict

**PASS for the assigned G2 exact current-pair reader change.** The product diff is limited to `astrid/sdk/timeline/store.py` and the new `tests/editing_conformance/test_current_pair_reader.py`. No product or test-oracle edits were made by this review. The existing G5 retained-body failure/qualification remains unverified; this review does not claim that lost run was captured or repaired.

## Source and authority review

The current read path now:

1. opens the normal public bundle;
2. uses the bundle’s canonical project/timeline scope for `history(..., cursor=None, limit=1)`;
3. requires a non-empty Runtime head containing both revision and publication IDs;
4. requires the history head revision to equal the opened bundle’s revision; and
5. reopens through the existing exact `revision_id` + `publication_id` hydration path.

Explicit revision-only and explicit revision/publication reads remain separate and unchanged. The existing hydration path continues to enforce exact scope, revision, digest, internal owner, canonical closure, publication receipt, future/unknown publication refusal, and strict fail-closed behavior. No row-order or old-revision ambiguity guessing, equal-byte retargeting, private cache, new API, or alternate authority was introduced. `Checkout._reset_base()` still calls `store.fetch_bundle()` for the current read.

The new authentic fixture exercises the reused content revision under a fresh publication and checks full authored/canonical source readback, consumed draft history, and undo/redo refusal. Negative controls cover missing/changed head proof, denied history, missing or mismatched publication history evidence, wrong project/timeline/revision/digest/internal owner, and explicit wrong-publication refusal. Future/ABA behavior was not newly claimed as a separate dynamic scenario; the existing exact-pair historical guards and fail-closed source path are preserved.

The retained G5 test file is outside the product diff and its prior source/body equality packet reports unchanged bytes across d32, base079, and this worktree. No G5 ancestry or G5 test body was added by `75fde1b96`.

## Evidence

The prior author packet was audited rather than accepted as sole authority. Its permanent evidence files exist at:

`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-G2-restore-reader-sol-1804/evidence/`

Verified independently:

- Runtime source-fidelity: commit `2a9e347ff0e1df1dedff5ab7b59ddb27dfe3129d`, 476 files, 0 missing, 0 mismatched.
- Authentic archive SHA-256: `2915bd4ac0d46954d19c30f87a517b82074218699978e650fab03fcba81b72d3`.
- Evidence SHA manifest: 434 files, 0 bad; manifest SHA-256 `4b1a6df06ef158e433b6194e0d2a92ec50a683146e1ae9cb84fdaac82a39081a`.
- Credential-shaped scan: 433 files, 0 findings.
- Changed paths: exactly the two assigned paths; worktree clean after testing.

The packet includes the complete exact-command/results log, product diff, early-cause note, observer, source-fidelity output, SHA outputs, and retained-test equality output. No SQL/direct-store mutation, alternate authority, live HTTP, browser, daemon, Git, Runtime/schema/pin, environment, or merge operation was used by this review.

## Commands and results

The first attempted pytest invocation did not enter any test body because the harness-provided `tmpdir` path was a file; pytest reported 16 setup errors (`NotADirectoryError`). It was rerun with a private run directory and passed:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.:/home/user/work/runtime:<runtime-2a9e-source> ASTRID_RUNTIME_CHECKOUT=<runtime-2a9e-source> ASTRID_AUTHENTIC_LEGACY_ARCHIVE=<archive> TMPDIR=<private-run-tmp> /home/user/work/venv-agent/bin/python -m pytest -q --tb=short -o addopts= -p no:cacheprovider -m integration tests/editing_conformance/test_current_pair_reader.py --basetemp=<private-run-tmp>/pytest
16 passed in 3.48s
```

Directly needed existing reader controls:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.:/home/user/work/runtime /home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider tests/sdk/test_remote_timeline_owner_scope.py
6 passed in 0.39s
```

Static and integrity checks:

- Ruff on the new test: `All checks passed!`.
- Mypy on the new test: `Success: no issues found in 1 source file`.
- Full Ruff ratchet: `current=2149 baseline=2149`.
- Full private Mypy ratchet: `current=1912 baseline=1912`.
- `scripts/vendor_lock.py check runtime.lock.json`: `ok`.
- `scripts/artifact_manifest.py --check`: `artifacts.json is current`.
- `git diff --check`: passed.
- No full suite was requested or run.

The author’s scoped `store.py` Ruff E731 and Mypy arg-type findings are unchanged pre-existing diagnostics and are disclosed in its exact-results packet; the new test’s scoped Ruff/Mypy checks are clean.

## Disposition

G2 exact current-pair reader: **PASS**. The next step is manager-controlled merge/review. Keep the original G5 retained test unchanged and arrange a faithful independent oracle/support port before making any G5 qualification claim.
