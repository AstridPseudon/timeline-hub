# OPS-bench-store core projection 1915 — source-only handoff

Implemented a unique continuation of exact final1858 (SHA256 53d90fb3108b24253a29416214ec5fa8f69402f50a515f0399b7464ec39a2e14), not a rewrite. New core SHA256 `88ae9e5af3425639b7eba0b79aa6b84e78a319fe810c0c6a2d3ceece1be8b5f3`. Runtime worktree and integration remain clean at the assigned 2a9 base; no product/generated/client/schema/C0v2/frozen34e changes. Nothing installed, merged, committed, pushed, queued, provisioned, or run through HOST/testservice.

## Changes and decisions

- Optional `report: str`, agreed with creator1912 via early flat interface: strict UTF-8, <=1 MiB, exact verified final-entry `.provision-report` bytes, fixed `tests/provision/<safe-name>.txt` only. Empty/absent report retains original registration shape and unrelated files. Added report text/SHA256 to existing registration hash/journal/projection lifecycle; no generalized path authority.
- Hash/ownership/type/size/collision checks precede report changes. Creation rollback and forward eviction/recovery include exact owned reports; tamper refuses with pending journal. Owned aliases/dependent registrations retire together; foreign files remain exact. Explicit newline-preserving UTF-8 I/O is necessary to preserve unrelated CRLF suites/env bytes.
- Confirmed core1910 and lease1910 caller finding. Genuine existing custom rows conservatively lease all registered managed dependencies without parsing shell or treating path strings as authority. Exact missing/changed/retired managed rows still refuse. Unknown legacy benches remain unadopted and nonevictable.
- Production creator1912 reads verified actual report, passes `report` to ensure, verifies persisted bytes and owns receipts. Production test-run already uses names_for_suite/acquire. Static caller checks pass, and the exact unchanged lease seam is exercised with real inherited flock FDs. No combined creator run was attempted.
- `ensure`, publication rename, `_delete_owned`, payload synchronization, marker/lock checks, `_evict`, acquisition/run and initialization methods are byte-identical to1858. Only report metadata/projection helpers, newline preservation and suite lookup were extended.

## Exact commands and results

All fixtures were writable/private under `/tmp/w-dcb5e29186`. No readonly publication/deletion, chmod, denied-path retry or alternative publication was exercised.

```sh
D=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design
export TMPDIR=/tmp/w-dcb5e29186
python3 -I -B "$D/handoff-runtime-OPS-bench-store-core-projection-1915-test-projection.py"
```
**PASS: 15 tests, 0.765s, exit 0.** Exact actual report bytes (UTF-8/CRLF/literal placeholder), reuse, empty/absent compatibility, invalid type/oversize/source-claim refusal, foreign fixed file/directory symlink/hardlink/type controls, hash tamper before changes, all-and-only owned alias eviction, held retention, creation/eviction recovery, real process crash rollback, pending hash mutation refusal, unchanged suite/env controls; exact lease seam baseline RED and new GREEN with an inherited flock held by a real child.

```sh
python3 -I -B "$D/handoff-runtime-OPS-bench-store-core-projection-1915-test-core.py"
```
**17 PASS / 1 FAIL, 18 tests, 1.384s, exit 1.** Original fixture expectations are unchanged (import basename only). Failure: `test_reclamation_is_real_before_callback_and_failure_preserves_eviction`, line62, assumes the deleted payload inode number cannot be reused anywhere in subsequent staging/metadata. The same assertion also fails against frozen1858:

```sh
python3 -I -B "$D/handoff-runtime-OPS-bench-store-core-precondition-1858-test-core.py" CoreTests.test_reclamation_is_real_before_callback_and_failure_preserves_eviction
```
**FAIL: 1 test, 0.049s, exit 1**, identical assertion. Inode reuse is the likely explanation, not fully diagnosed here. This is retained as RED; no skip, xfail, weakening or combined PASS claim. Previous reviewed1858 evidence of 18 passing private tests and earlier runtime caller positives remains historical evidence, not a pass on this run. The old packet's claimed20 count was already corrected by core1910 to actual18.

```sh
patch --batch --directory="$TMPDIR/projection1915/patch-replay" -p0 < "$D/handoff-runtime-OPS-bench-store-core-projection-1915-core.patch"
cmp "$TMPDIR/projection1915/patch-replay/bench_store.py" "$D/handoff-runtime-OPS-bench-store-core-projection-1915-bench_store.py"
python3 -I -B "$D/handoff-runtime-OPS-bench-store-core-projection-1915-validate.py"
```
**PASS, exit 0:** scoped in-memory compilation, bash syntax of creator1912/runner sources, byte-identical protected lifecycle/lease methods, original18 expectations unchanged, frozen inputs immutable, static caller wiring, patch replay/cmp, Runtime assigned/integration cleanliness, base identity and diff checks. No product tests/typecheck/lint/full suite applies or was run.

Logs: worker `projection-tests.log`, `core-tests.log`, `baseline-inode-test.log`, `validation.log`. Source/interface/tests/unchanged seam/patch/validator/input hashes/report/hashmanifest are flat `handoff-runtime-OPS-bench-store-core-projection-1915-*` exports, under 3 MiB total. No root report or tracked deletion. Worker contains only small logs/report/commit message/markers.

## Limits and next steps

Readonly child publication and rollback EACCES/runtime1905 disposition is still pending. Entire bench store remains **UNQUALIFIED / NO INSTALL**. No readonly algorithm edits or forbidden combined fixture actions. Creator receipt work is creator1912-owned. Independent Luna source review is next; orchestrator must settle permission disposition and the baseline inode assertion before authorizing a combined private caller qualification.

Scratch apparent size is about7.3 MiB (under10 MiB data), but cumulative allocated blocks reached14 MiB because of repeated tiny fixture directories and oversize controls. This exceeds the10 MiB bound if measured by allocated disk. No cleanup/retry on any refused/readonly fixture was attempted; harness owns TMPDIR cleanup. This resource overrun and the RED baseline are explicitly retained as limitations.
