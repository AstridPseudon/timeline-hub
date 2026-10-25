# D137 independent source/security and install-readiness review

## Verdict

`FAIL` for the requested final stderr-retention gate. The source captures each
stage's stderr privately while the maker is running, but the ordinary production
dispatcher path loses that log during Store rollback. The fixture E2E gate is
honestly `WITHDRAWN`; its result remains `NOTRUN`. No fixture body, Store,
production child, live target, network acquisition, or production request was
run.

## Exact source identity

- Review commit: `4932c0f8e2e02ce6a203bf41fe014f9c3a7db5fa`
- Review tree: `2416d249840c7ca94cb4f1666ec3e435f5599c58`
- Maker: `ops-child-custody/make-child-venv`, SHA-256
  `7a065c078972d9fe91041bcd895ec8be151a034ef66539fed59aa884950119f8`,
  70,119 bytes, mode `0755`
- Installed preimage: SHA-256
  `0857a5e0d9faeceb585b371f1f82cbf4b574ff20350974fd3c95f852e57b6d39`,
  68,351 bytes, mode `0755`
- Protected `bench_store.py`: `123bb93c1f2e3d6bd23c21e50cc8445afc8853e5e659759cd30dcaa53b7adfe2`
- Protected `verify_dependency_seed.py`: `116b4e6bcb791d08e6c3c548f7fb52c52e9225b9428d7e201c09b02160d7bfe2`
- Embedded `STORE_PY`: `0889b24010e67bd31f28f5efbaec37fed43adf1a0d5ebe8c4fcd57a8248ca50c`
- Embedded `STORE_VERIFY`: `f7c7ebcc26221958ce24e36025faad167c6015a2889202752d267e03d5eda209`

The `STORE_PY` and `STORE_VERIFY` blocks compare byte-for-byte with the parent
candidate. The unchanged protected helper hashes match the recorded kit.

## Whole-path finding

`run_stage` creates `.provision-stderr/<stage>.stderr` under the maker staging
root, truncates it with mode `0600`, redirects child stderr there, and calls
`failure` with the original exit status. The public marker and summary contain
only the allowlisted stage, status, timing, source identities, lock identity and
fixed diagnostic. This satisfies the in-process capture and bounded-output
checks.

The actual handoff then fails the D137 requirement. The dispatcher runs the
maker through `prov`; the maker's normal path calls `store.ensure`. On a failed
build, `Store.ensure` invokes `_roll(journal, False)` before `_record_failure`.
`_roll` calls `_delete_owned` for the new staging directory, recursively deleting
the `.provision-stderr` directory and its first-error log. The later failure
record preserves only the bounded marker fields and no path/digest/raw stderr.
Thus a normal failed Store request cannot provide the exact first error after
cleanup, including a timeout failure. The existing diagnostic-retention mode
does not close this finding because the production dispatcher does not select
that mode.

Minimum exact fix: preserve a private, bounded, mode-`0600` stage-log copy (with
stage identity and digest) at the existing Store failure/cleanup boundary before
`_roll`, or retain the authorized staging evidence through cleanup, while keeping
the public marker bounded and the verifier unchanged. This is a Store/STORE_PY
handoff change, not another fixture or investigator. The current candidate's
protected Store helper/hash contract means it needs a separately reviewed
source change and requalification.

## Installer source review

The private installer route accepts the exact decision shape:

```json
{
  "authorization": "D137",
  "fixture_e2e_gate": "WITHDRAWN",
  "e2e_result": "NOTRUN",
  "e2e_pass": false,
  "install_route": "CAS_MANAGER_ONLY",
  "production_install": false,
  "candidate_sha256": "7a065c078972d9fe91041bcd895ec8be151a034ef66539fed59aa884950119f8",
  "candidate_bytes": 70119,
  "source_commit": "4932c0f8e2e02ce6a203bf41fe014f9c3a7db5fa",
  "reviewed_installer": "installer1826",
  "decision_path": "<absolute private decision path>"
}
```

The private run replaced only a private target. It passed exact candidate hash,
source archive extraction, installed preimage CAS, protected-helper hashes,
descriptor-bound no-follow/no-clobber backup, receiving lock, target identity
check, atomic rename, and post-commit `cmp`/readback. It returned:
`PASS: candidate installed with CAS preimage, no-clobber backup, atomic
replacement, and helper readback`. No live target was touched.

## Commands and results

All commands were run against this worktree after the final source was present.

- `bash -n ops-child-custody/make-child-venv` — PASS.
- `bash -n ops-child-custody/install-prep/apply-reviewed-maker.sh` — PASS.
- `PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-runtime/bin/python -m unittest discover -s ops-child-custody/tests -v` — **42/42 PASS**, 5.577s.
- `PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-runtime/bin/python -B ops-child-custody/install-prep/dry_run_controls.py` — PASS for candidate, preimage, no-clobber, descriptor-race, identity-CAS, helper, symlink and hardlink controls.
- `/home/user/work/venv-agent/bin/ruff check --no-cache ops-child-custody/tests ops-child-custody/install-prep/dry_run_controls.py ops-child-custody/install-prep/install_atomic.py ops-child-custody/install-prep/verify_gate_artifacts.py` — PASS.
- Embedded Python compile plus all `ops-child-custody/**/*.py` via `ast.parse` with the Runtime interpreter — PASS (6 embedded Python blocks plus all Python files).
- Embedded `STORE_PY` and `STORE_VERIFY` byte comparison against the parent candidate — PASS.
- `git diff --check` — PASS.
- Private `ORCH=... SOURCE_CHECKOUT=<this checkout> TMPDIR=... D137_DECISION=... bash ops-child-custody/install-prep/apply-reviewed-maker.sh` — PASS; private target and backup hashes matched expected values.

No full suite, browser, localhost, socket, fixture E2E, live installer, Store
initialization or child request was run.
