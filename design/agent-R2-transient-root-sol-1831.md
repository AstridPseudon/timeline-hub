# R2 transient root compiler baseline

Candidate base: `0b735c13710d74600cc51bf55e4963b54163087e`.
Scope: `_root_inverse.py`, one new focused test module, this report. No merge,
commit, pin, Runtime, App, environment file, or frozen interface changes.
Independent Luna review is required next; this report is not acceptance.

Permanent evidence directory:
`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-R2-transient-root-sol-1831/evidence`.

The retained `agt-R2-order-join-sol-1801/evidence/final-neighbors.log` identifies
the original failure at test line 132, redo after accepted undo. Its reported
exception is `_root_inverse.py:190`, `restored root differs from accepted source`.
I inspected the original test, source, retained capture scripts and capture file
names first. I found no retained transient-root capture there. I did not rerun
the unchanged original node for instrumentation.

`source_probe.py` is a bounded deterministic reconstruction of the original
commands and steps using the original DetachedRealm/provider helpers. It is not
the retained execution. Two setup attempts failed before command execution:
the provider imports `apply_inverse` lazily, and the fixture ABI requires a
preloaded Runtime platform. The completed probe reproduced the reported refusal
at 18:29 UTC, before the patch, with no head/history/documents/accepted/prepared
mutation. This is an Agent source bug, consistent with C0 §5's sequential-boundary
rule; no plan or contract decision needs changing.

The actual reconstructed source is publication-2, the accepted whole undo of
publication-1. Its before-root is `new-shot`, name `Edited`, owned by `new-occ`.
Its first native stage changes `occurrence:new-occ/shot` name `Edited` to `New`
at native range `[0, 1]`. Its next stage removes `new-occ` and the complete
`new-shot` root at range `[1, 3]`, effect range `[3, 6]`. Redo reverses the latter
stage first. The resulting complete root correctly has name `New`; comparing
that intermediate root to the whole publication's initial `Edited` is incorrect.
The next stage restores `Edited`. The immutable internal revision is unchanged.
Exact revision IDs, digests, source roots, owners, ranges and full native/effect
records are in `source-classification.json` and `source-probe.json`.

The correction projects accepted native writes into a detached guard State.
It requires the nested source record to match an accepted record and the stage
writes to match its native slice. Every projected native before-value is guarded.
The complete projected final root and its owners must match the authenticated
after-boundary. The live restored root must match the complete projected stage
root, the native removal's complete before-value, and both the initial and stage
owner sets. The compiler retains the exact full accepted before-document through
the existing `_RestoredShot` provenance mechanism. No authored root is copied
into live state; no accepted effect patch is executed. There is no equal-byte
retarget, pin exemption, or exception waiver.

The original current-head guards, physical binding normalization, later-history
ABA scan, selected-step dependencies, surviving-consumer checks and allocation
authentication remain in the unchanged `inverse.py` / `_step_undo.py` paths.
The source loader and compiler still verify source documents/digests and scope.
The new tests cover full authored root preservation, source provenance, changed
payload/internal/owner, foreign source command, altered range/slice, broken native
before/after proof, and a mismatched source after-root. Rejection leaves both
live candidate and source captures unchanged. These tests are additional focused
guards; they do not claim the existing full matrix was rerun.

`original-postpatch.json` captures the one post-patch execution of the unchanged
original node. It records full request contexts, prepared documents/digests,
receipts/replies, records/bindings/effects/dependencies, history and documents
before acceptance. Full inverse sources/native records are saved before inverse
validation, and root state/ranges before root validation. Module hashes are saved
before that validation. `source-probe.json` similarly captures the pre-patch
reconstruction and no-write refusal. Initial command-schema validation and
individual port read calls were not instrumented. These are offline fixture
executions, not live Runtime/CAS evidence. Source inputs are the captured verified
canonical closures/bundles; the source document manifest has no document pins.
The original requests intentionally omit label/merge/group_id defaults; undo
also omits submitted steps. Captures retain those actual requests and provider
normalization rather than inventing explicit fields or new requests.

Exact commands and results are in `evidence/commands.json`. All pytest commands
use `/home/user/work/venv-agent/bin/python`, `PYTHONDONTWRITEBYTECODE=1`, and
`PYTHONPATH=$PWD:/home/user/work/wt/rt-pin-2a9e347f`; the original-node command
also adds the permanent evidence directory for the capture plugin.

| Command after `python -m pytest` | Result |
| --- | --- |
| `-q --tb=short -p no:cacheprovider -p validation_capture tests/editing_conformance/test_provider_step_undo_v2.py::test_create_edit_whole_undo_redo_retains_transient_roots` | 1 passed in 1.96s |
| `-q --tb=short -p no:cacheprovider tests/editing_conformance/test_transient_root_baseline.py tests/editing_conformance/test_captured_redo_media_closure.py -k 'not exact_captured_redo'` | 16 passed, 1 deselected in 4.63s; 8 new cases at that point, 8 existing restoration controls |
| `-q --tb=short -p no:cacheprovider tests/editing_conformance/test_transient_root_baseline.py` | Final 10 passed in 4.58s after adding source-command/range negatives |

The deselected integration node was not run; it needs separate Runtime evidence.
No full suite, sockets, browser, or unrelated 14/110/5 matrix was requested/run.
`/home/user/work/venv-agent/bin/ruff check --no-cache astrid/sdk/timeline/_root_inverse.py tests/editing_conformance/test_transient_root_baseline.py`
passes on the final files. Scoped mypy passes with
`/home/user/work/venv-agent/bin/python -m mypy --cache-dir=<evidence>/mypy-cache astrid/sdk/timeline/_root_inverse.py`.
`git diff --check` passes. No tests were weakened or modified.

Before/after source snapshots and SHA-256 maps are permanent evidence. Root module:
`0d81d995582622367cca770855d7604735d3a707a7e8d6d6d5d6102367c4949a`
→ `6715f34f2f60609d2ed8436f0dde94b475a0966de9d869f4dc3ceade3160b3a1`.
`inverse.py`, `_step_undo.py`, `commit.py`, and `_commit_patch.py` have identical
before/after hashes. `SHA256SUMS` includes this report, changed source/test, and
top-level evidence. `credential-scan.json` records the bounded credential scan.

No blocker. Next: independent Luna source/guard review, then the orchestrator's
serial merge decision. Broader source histories and real Runtime integration
remain unqualified here. Native projection deliberately fails closed when its
accepted source trace cannot be proved by the existing State operations.
