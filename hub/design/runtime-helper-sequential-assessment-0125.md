# R2r-helper-sequential report

- **Owner:** Agent core, specifically sequential rebase/materialization binding in `astrid/sdk/timeline/_commit_patch.py`; not Runtime auth and not the fixture for this case.
- **Exact invariant:** Runtime requires `replay_bindings` to be a unique, complete one-to-one map of every moved-head patch/read input. `timeline_commit_auth.py:2196` correctly rejects duplicate or omitted map keys. Equal bytes do not establish equivalence.
- **Evidence:** Later bounded Agent capture reports show command 2 losing the staged internal physical read and corresponding patch binding after peer rebase. Agent’s reviewed `851439d`/`67ba416` changes specifically add staged materialization retention and `replay_ref`; Runtime was unchanged.
- **Failure tuple:** Runtime `8ea0766f5`, tree `6047ac3033c3594b8f83db3afd8bb2c47cafa6d6`; Agent `3b0dc9e80f`, tree `b0dd975805d47056d7272c057832aef91374d929`.
- **Production boundary:** Agent `commit.py:1122–1153` → `_commit_preview.capture_sequential_execution` (`:25–80`) → Runtime `RequestCommitPort.capture_sequential_execution` (`timeline_commit_port.py:177–204`) → store validation (`timeline_commit_store.py:836–883`) → `validate_sequential_capture` (`timeline_commit_auth.py:1983–2290`).
- **Interface decision:** Keep the existing private six-field capture carrier unchanged. The Agent must emit complete source-bound staged read/patch lineage. No Runtime schema, public DTO, guard waiver, alias retargeting, or byte-equality shortcut is justified.
- **Separate fixture owners:** The `"second"` case fails earlier on missing typed word binding; the process persistence case reaches a fake `_remote` transport. Neither explains `[True]`.

## Evidence limitation

The referenced `commands.txt`, `numeric-capture.json.gz`, and G5 boundary captures were not present in accessible `/tmp` or `/home/user` paths. Manager should request these exact retained members if available:

- worker0048 `commands.txt` and `numeric-capture.json.gz`;
- G5 `boundary-001-execute.json` through `boundary-005-execute-error.json`, plus `sequential-cut.log`.

They must include the complete original/landing envelopes, records, request/context, prepared digest, replay map, base/landing heads, and intervening history—not a new replay.

## Verification

Read-only source/hash/callsite inspection completed. `git status` clean; `git diff --check` passed.

Tests, typecheck, lint, full suites, the known failed test, and public original9 were **not run**, as required.

Bounded eventual acceptance:

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.:/home/user/work/wt/rt-pin-3b926efa \
ASTRID_RUNTIME_CHECKOUT=/home/user/work/wt/rt-pin-3b926efa \
/home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider \
'tests/sdk/test_timeline_helper_capture.py::test_contiguous_helpers_keep_sequential_steps[True]'
```

Then run the Agent private sequential tests and Runtime’s `test_timeline_commit_sequential_verifier.py` plus authentication/port neighbors. No tracked edits were made.