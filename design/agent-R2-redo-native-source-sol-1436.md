# R2 native source correspondence 1436

Ownership: `astrid/sdk/timeline/_commit_patch.py`, inverse-stage projection in
`CommitPatch.after`; only inverse record/binding hunks, focused captured tests.
No compiler, commit service, Runtime, schema, pins, client or publisher changes.

Source cause: accepted native occurrence ownership captures retain a working
shot alias while Runtime's sequential inverse stage starts at the exact physical
canonical shot. The native execution and canonical effect boundaries must be
joined through that occurrence's verified physical source, preserving the
authored execution, original accepted history, stage order and strict guards.

Input: immutable 1404 packet SHA-256
`a29df82beb548306683ab64d738eb776a519587fdb30cad3e997e91468621ef8`;
Agent base `80523b472cc817c2da01bf89c177d5d7dc4c2e10`, Runtime
`cfa0af0d476e6954df041c08d7ef378fd6782932`. PLAN R2 and C0 §§1/2/5
govern this repair. Baseline carrier and all media guards remain intact.

Verification and disposition will be recorded below.

## Disposition: BLOCKED, no product repair qualified

The immutable packet hash was verified before extraction. The worker-retained 444166-byte
fixture is an exact extraction of its retained new-public-05 SQL/document/head/
history, original request, and entire expected forward canonical document.
Fixture SHA-256: `9a47bb934b879efa0f6147d673038cee76299ba4e30ab22b6d5bcb1377ade589`.
The fixture restores the original persisted realm and deterministic original CAS
bytes (both hashes checked against retained media pins); it creates no identities,
credentials, source rows or accepted history. Real RuntimeService admission,
RequestCommitPort, production provider, and strict Runtime acceptance run offline.

The untouched-source positive acceptance probe reproduces RED:
`invalid_records: inverse stage write differs from its sequential input`.
A temporary diagnostic control separately verified that exact rejection and
unchanged complete SQL. It is not a replacement for the required acceptance
behavior. No previously passing test was changed, deleted, skipped or weakened.
The positive exact-canonical-restoration/retry assertions remain in the worker
probe and are RED, not reported as passing. The diagnostic refusal test and its
fixture were retained only in worker evidence, outside the product suites, so
this task does not encode the known missing redo behavior as a passing contract.
No test or product source change remains in the worktree; only this report and
the required immutable packet/manifest are proposed for the harness commit.

A candidate in `CommitPatch.after` joined the working alias to the exact stage
physical input using occurrence identity, native alias, scope, source revision,
internal pin and canonical source image. It changed only the newly generated
ownership-before capture. That candidate clears the original alias refusal but
strict Runtime then rejects:
`inverse stage root differs from its authenticated effect image`.
Actual `_inverse_stage_boundaries` locals are retained in `next-stage.json`.
The native root `shot:selected-shot` creation after value has child clip
`f2-agent-clip.params={"text":"hello"}`. The following native leaf removes
`params.text`; the complete canonical stage after has `params={}`. This is the
same three-write inverse stage: create shot, attach occurrence, clear leaf.
Runtime compares the intermediate native root after capture with the complete
stage-after root. This is concrete additional correspondence evidence; simple
before-alias normalization is insufficient. This report does not claim that
Runtime's guards should be relaxed or that the orchestrator's Agent ownership
decision is disproved. A compatible source representation is still unresolved.

The candidate was removed: normalizing a persisted native operand also needs a
proof that future inverses retain its original source/allocation meaning. No
unproved canonical-row/root replacement, rewritten history, guessed successor,
prepared-byte substitution, private-cache injection, managed-edge injection, or
Runtime change was used. `git diff --exit-code 80523b472 -- astrid` passes.
Compiler baseline carrier, all current 8c/D20 source, R1 capture hunks, client,
schema, pins, dependencies, publishers, emitter and commit service are unchanged.
No G5 product change or unrelated restructure was attempted.

No corrected-provider acceptance GREEN was achieved. Consequently no public
fork/free-edit/undo/redo journey, public retry or new export ran. The requested
negative-control matrix and public receipt/history/SQL idempotency qualification
remain unverified. G5 P1 stays NO-GO. No full/HTTP/browser/original40/281/58/
native14/P1/P4/V4 suite ran. No Git writes, installs, shared-cache writes,
daemon, hand provisioning, deletion, push or classifier denial occurred.

## Commands and evidence

Working directory: `/home/user/work/wt/agt-R2-redo-native-source-sol-1436`.
`E=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-R2-redo-native-source-sol-1436/evidence`.
`TMP=/tmp/w-229b4e3473` is the path stored in the worker's `tmpdir` file.

```bash
PYTHONDONTWRITEBYTECODE=1 ASTRID_RUNTIME_CHECKOUT=/home/user/work/wt/rt-pin-cfa0af0d PYTHONPATH=.:/home/user/work/wt/rt-pin-cfa0af0d /home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider /tmp/w-229b4e3473/test_strict_redo_probe.py::test_retained_native_redo_passes_strict_runtime_acceptance_and_exact_retry --basetemp=/tmp/w-229b4e3473/actual-red
# exit 1: 1 failed, original alias mismatch; actual-red.log.

PYTHONDONTWRITEBYTECODE=1 ASTRID_RUNTIME_CHECKOUT=/home/user/work/wt/rt-pin-cfa0af0d PYTHONPATH=.:/home/user/work/wt/rt-pin-cfa0af0d /home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider tests/editing_conformance/test_captured_redo_native_source.py tests/editing_conformance/test_captured_redo_media_closure.py tests/editing_conformance/test_inverse_stage_images.py tests/sdk/test_timeline_inverse_binding.py tests/timeline/test_authoring_bundle.py::test_timing_is_admitted_but_competing_selected_media_fails_before_publish --basetemp=/tmp/w-229b4e3473/final-hashed
# exit 0: 16 passed in 5.42s. Includes original 10 compiler/selection tests.

PYTHONDONTWRITEBYTECODE=1 ASTRID_RUNTIME_CHECKOUT=/home/user/work/wt/rt-pin-cfa0af0d PYTHONPATH=.:/home/user/work/wt/rt-pin-cfa0af0d /home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -m 'not integration' -p no:cacheprovider tests/editing_conformance/test_occurrence_fork_source_baseline.py tests/editing_conformance/test_inverse_stage_images.py tests/editing_conformance/test_step_undo_v2.py tests/editing_conformance/test_provider_step_undo_v2.py tests/sdk/test_timeline_inverse_binding.py --basetemp=/tmp/w-229b4e3473/guards
# exit 0: 74 passed, 1 existing integration deselected in 9.04s.

/root/.local/bin/ruff check --no-cache tests/editing_conformance/test_captured_redo_native_source.py
# exit 0: all checks passed.
PYTHONDONTWRITEBYTECODE=1 RUFF_CACHE_DIR=/tmp/w-229b4e3473/ruff /home/user/work/venv-agent/bin/python -m scripts.reshape.compare_ruff_baseline
# exit 0: 2149/2149.
PYTHONDONTWRITEBYTECODE=1 MYPY_CACHE_DIR=/tmp/w-229b4e3473/mypy /home/user/work/venv-agent-typecheck-v2/bin/python -m scripts.reshape.compare_mypy_baseline
# exit 0: 1912/1912. Zero added identities: all mypy-scanned product/scripts source is byte-identical to base.
PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-agent/bin/python scripts/vendor_lock.py check runtime.lock.json
# exit 0: ok runtime.lock.json; frozen lock unchanged.
PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-agent/bin/python scripts/artifact_manifest.py --check
# exit 0: artifacts.json is current.
git diff --check
# exit 0.
git diff --exit-code 80523b472 -- astrid runtime.lock.json artifacts.json tests/editing_conformance/test_captured_redo_media_closure.py tests/editing_conformance/test_inverse_stage_images.py tests/sdk/test_timeline_inverse_binding.py
# exit 0: source, pins and original guard files identical.
```

Candidate-only strict test: `strict-cas.log`: 1 failed (root final-image
correspondence), 1 passed (old alias no-write control). `diag.log` and
`next-stage.json` retain the second boundary. `candidate.diff` and
`candidate_commit_patch.py` preserve the exact experimental source. Initial
harness errors were corrected without product changes: worker `tmpdir` is a
path file, not a directory; real acceptance needs real RealmStore transaction
and receipt methods; retained CAS bytes must precede realm admission. An initial
xfail experiment was rejected by the existing test harness, so no xfail remains
and the new positive diagnostic probe is retained outside the main suites.

Recommended next step: independent source/Runtime correspondence review of the
actual grouped creation/descendant stage before another implementation. Preserve
three native source sites, all four canonical effects, exact source history,
all physical bindings, and future inverse allocation semantics. The current
strict validator permits native sites or canonical effect sites but also requires
the native range length to equal the source native-site count; this captured
stage has three native sites and four canonical effects. Merely switching the
recorder to canonical effects does not satisfy those existing checks. Any revised
source representation needs real acceptance and negative controls before the
single authorized public journey. No approval or contract change is inferred.

Final retained-main-suite command (temporary diagnostic file removed):

```bash
PYTHONDONTWRITEBYTECODE=1 ASTRID_RUNTIME_CHECKOUT=/home/user/work/wt/rt-pin-cfa0af0d PYTHONPATH=.:/home/user/work/wt/rt-pin-cfa0af0d /home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider tests/editing_conformance/test_captured_redo_media_closure.py tests/editing_conformance/test_inverse_stage_images.py tests/sdk/test_timeline_inverse_binding.py tests/timeline/test_authoring_bundle.py::test_timing_is_admitted_but_competing_selected_media_fails_before_publish --basetemp=/tmp/w-229b4e3473/retained-final
# exit 0: 15 passed in 3.09s; original guard assertions unchanged.
```

The earlier commands naming the temporary new test file ran while it existed;
its exact contents and fixture are retained in worker evidence. Reproduce the
strict positive RED with the worker `test_strict_redo_probe.py` (fixture path
now points to retained worker evidence). No acceptance expectation was changed
to refusal in the product suite.

Flat source-complete evidence packet: `agent-R2-redo-native-source-1436-b54d2efee42e0934.json`, 2825926 bytes,
SHA-256 `b54d2efee42e093485e7ad6a4c73e7fca2c8318ad0b02cdbcde9330c3750eff3`. File hash manifest: `agent-R2-redo-native-source-1436-manifest.json`.
Credential-pattern matches: 0. Final module origins and pinned Runtime source
are embedded; the candidate is explicitly experimental and removed.
