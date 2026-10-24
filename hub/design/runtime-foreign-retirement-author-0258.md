Implemented the bounded Runtime fix in [timeline_commit_auth.py](/home/user/work/wt/rt-R2r-foreign-retirement-sol-0258/runtime_protocol/timeline_commit_auth.py:902), plus a new structural/security regression file. No existing assertions, schemas, callers, or generated files changed.

Confirmed the defect:

- All 11 manifest artifacts match their recorded sizes/hashes.
- Auth source at `8ea0766` is byte-identical to base `f3208b26b`.
- Both exact 62,190-byte captures failed parent validation and now pass.
- Native range remains `[0,1]`; effect range remains `[0,3]`. Extra aggregate/canonical native writes remain rejected.

Retirement derives from the exact accepted occurrence creation and full physical images in authenticated history. Surviving occurrence/shot references retain their images and pins.

Validation, with `P=/home/user/work/venv-runtime/bin/python` and `S=/tmp/w-dcf7898e8e`:

```bash
PYTHONPATH=. $P -m pytest -q -p no:cacheprovider tests/test_timeline_inverse_occurrence_retirement.py tests/test_timeline_inverse_stage_authentication.py tests/test_timeline_commit_authentication.py tests/test_timeline_history_authenticated_read.py --basetemp="$S/final-merged-auth-history" --tb=short
```

**230 passed, 74 deselected.** Covers ownership, shared internals, forged source/native/range/count/order/digest claims, accepted/merged replies, preview, retry, and SQLite/CAS/staging no-write refusals.

Additional checks:

- Exact replay: `PYTHONPATH="$S/parent" $P "$S/replay_auth.py"` and `PYTHONPATH=. $P "$S/replay_auth.py"` — expected parent failures and candidate passes.
- Parent structural regression — **2 failed, 1 passed**, reproducing the defect.
- `ruff check --no-cache runtime_protocol/timeline_commit_auth.py tests/test_timeline_inverse_occurrence_retirement.py` — passed.
- Pyright on both changed files, parent and final — **zero diagnostics; zero NEW identities/multiplicities**.
- `$P scripts/artifact_manifest.py --check` and `git diff --check` — passed.

No Runtime blocker. The old parent-owner captures retain their native-input rejection. End-to-end Agent undo/redo and media revalidation remain unverified; request independent Luna security review before merge.

Wrote `commit-msg` and `DONE`. No Git writes or full/browser/HTTP suites ran.