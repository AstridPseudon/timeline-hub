# P4 canonical-path correction — ap2-P4-rerun-path-resume-sol-0824

Disposition: bounded path correction complete; offline checks PASS. Live P4 remains
unverified. A separate downstream request-versus-recorded-command assertion issue
is proven offline and needs the Proof/orchestrator's judgment before expecting a
green original-node run. No product defect was established and no product was edited.

## Exact source and contract identity

- Resumed exact `tl/ap2-P4-rerun-path-sol-0817`, also exact
  `tl/ap2-P4-rerun-base-keys-0810`: source HEAD
  `d3696bbf84e88705fdf825f2b51d74cabe4d316d`.
- Source tree: `ecb4e61423cc87a68359c86546fe51c3f7537041`.
- Candidate source tree, computed from HEAD entries plus the single edited blob
  without writing Git objects: `f35ff9cbebb6b0e00543ee56d7cf052e8d74f4c9`.
- Only edited file: `tests/editing_conformance/test_p4_note_rerun_v2_runtime.py`;
  4 insertions, 2 deletions. Before blob
  `244d6569747824ba77e52645dc8845066b79335e`; candidate blob
  `7e63a8e6bdb55b5a9bf4d4b30ee997ebe1837b24`; candidate file SHA-256
  `7525e6d5a435e4cad1014d0c87ca2e01d5898854c508b4a42aa3c57b05458359`.
- Neighboring ten-note file unchanged, blob
  `b8876628d100897a9dcda6750fc5395a3b5b41f3`.
- No final commit SHA exists yet: committing is reserved for the harness.
- Runtime checkout `/home/user/work/wt/rt-pin-a5d42583`: clean at
  `a5d4258312c979024865ee704da2d632ca5b2730`, tree
  `f74b016ea837f8148db4a602c972073a226ed177`.
- Normal vendored source remains `34eac0041b0891e9011966b39bcbd26053fde5bc`;
  unchanged `runtime.lock.json` SHA-256
  `320d278366bc344aad35f3564845d9b62d9cc5f2e000a8a4cc6b6fea508d6cd2`.
- Agent and Runtime schema digests match:
  `sha256:35c2d9c5e0b51ab8d8b7a4f4dbafbdfcb13d232d7bd22fff21cf73e250398d4c`.
- Read PLAN first, including §3 P4. Read C0 §§2,3,4,5,7 in
  `$ORCH/design/commit-v2.md`, 210581 bytes, SHA-256
  `4581ea85aada0af405b1b1b9284e9938a6dba3ca4f6980b7c3c0be8f135f9bb7`.

## Cause, decision and smallest correction

Read the full `log.txt`, request, summary and source identity for service
`ap2-P4-rerun-base-keys-0810-p4-v2-http-nodes-1023081628-21187`.
It ran the original named node against the exact source tree above, failed with
1 failure in 5.70s (service exit 1), and reached all original request, key,
base/current and `atomic_scope_changed` checks before failing at the path.
The real sequence was `[200, 409, 200]`, with two callback evaluations,
absent-to-peer note transition and the retry's peer-value before guard. The
earlier 3610 evidence and independent 0813 keys review remain historical evidence,
not passing evidence for this candidate.

The submitted operand is exactly:
`["clips", "id:clip-a", "app", "org.example", "p4_note", "note-04"]`.
The diagnostic/effect path is exactly:
`["config", "clips", "id:clip-a", "app", "org.example", "p4_note", "note-04"]`.
These are distinct serialized addresses of the SAME authenticated parent note,
not separate clip/note identities. C0 §2 explicitly makes parent `clips` and
`config.clips` one logical identity and requires normalization for conflicts,
history and undo. §4 requires normalized conflict addresses; §§2/7 require
authoritative effect patches. The actual parent closure authenticates both copies:
`commit._verify_document` rejects disagreeing parent/config clips, `Closure`
binds `parent` to its verified image, and `Closure.native_sites` resolves either
id-addressed mirror to `parent/clip:clip-a`.

Source trace:

- `_doc_patch.normalized_path("parent", ...)` adds only the `config` prefix to
  `clips` operands; `_commit_patch.canonical_site` uses that normalization.
- `_commit_patch` replay guards retain the exact note path in generated bindings
  and raise `CommandError(..., kind="atomic_scope_changed", path=guard["path"])`.
  `commit.py` passes that path to `_failure`; `_commit_errors` preserves the tokens
  in `details.path`, with original structured code/hint/command/head diagnostics.
- `_commit_patch.CommitPatch.finish` normalizes the authoritative parent
  `steps[].patch` path as well, retaining ref, op, before and value.

Added one explicit `CANONICAL_NOTE_PATH` constant with all seven literal tokens.
Changed the diagnostic assertion to exact equality against it. The downstream
accepted step-effect assertion had the identical mirror boundary, so it now
compares the entire change against `{**retry_change, "path": CANONICAL_NOTE_PATH}`.
No product normalizer is called to generate either expected value. No contains,
suffix comparison, alternate-path set, fixture rewrite or expectation of refusal
was introduced. Every original NOTE_PATH request operand remains unchanged.

## Entire downstream oracle trace and owner finding

Preserved request checks: api_version 1, project/timeline scope, exact revision /
publication base pair, commands and guarded changes, label, step id/label/intent/
tags/command_ordinals/patch/reads, merge, omitted request reads, dry_run, source,
original/retry keys. Preserved callback count and exact heads/notes, nine untouched
notes, conflict code/reason/path/hint/suggested-command keys and no receipt.

Preserved accepted result assertions: canonical closure, document and payload
digests, head/receipt, commands/steps, accepted status/rebased_onto, previous pins,
receipt/result equality, publisher/provider/compiler. Preserved history cardinality,
stored label/publisher/merge/steps/records, writes/reads/selections/bindings/created/
dependencies/derived_writes, exact authoritative effect and scope dependency.
Preserved restart, public reopen, private-cache absence from the public bundle,
authenticated exact-head canonical readback, non-note/full-closure metadata and
empty pending/flight. The unchanged neighboring P4 oracle retains CLI show/history,
ten notes in one commit and guarded per-step undo/redo. Existing conflict/invalid
structured diagnostic coverage elsewhere is untouched; this file is a conflict /
rerun scenario and does not independently prove invalid or merged outcomes.

**Separate existing oracle issue, owner Proof/app2 + orchestrator:**
`_assert_success` line 120 still asserts `data["commands"] == body["commands"]`.
Runtime `timeline_commit_store.py:804` returns
`[r["command"] for r in records["commands"]]`, which includes authoritative
captures, whereas public `Timeline._append` deliberately sends raw caller commands.
The real offline provider execution in this task proves the lists differ by
`authorship`, `bindings`, `created`, `expect`, `intent`, `reads`, `resolved`,
`selections`. Executing that exact existing AST assertion against the real plan's
recorded commands fails. This is an assertion-boundary issue, not evidence of a
product failure. It occurs before the corrected downstream step-patch assertion.
The sibling ten-records review already documents the analogous correction on its
separate branch; it is not in this resumed base. I did not broaden this path-only
task into that correction or alter/trim any returned capture metadata.

The unchanged sibling `_assert_step_patch` also expects the unnormalized clips
operand; it warrants its own exact-path review in its owning task. No other
physical-path comparisons were found in the remaining rerun oracle. Remaining
downstream Runtime behavior is unverified because the original live node stopped
at its diagnostic assertion. No genuine product issue was discovered to repair.

## Exact verification commands and results

All commands below ran in
`/home/user/work/wt/ap2-P4-rerun-path-resume-sol-0824`. `tmpdir` is an existing
pointer file containing `/tmp/w-1c6439af9a`; scratch scripts and caches use that
private directory. No shared cache/install was written.

```bash
timeout 45s env PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD:/home/user/work/wt/rt-pin-a5d42583" ASTRID_RUNTIME_CHECKOUT=/home/user/work/wt/rt-pin-a5d42583 /home/user/work/venv-app2-native/bin/python -m pytest -q --collect-only -m integration -o cache_dir=/tmp/w-1c6439af9a/pytest-cache tests/editing_conformance/test_p4_note_rerun_v2_runtime.py::test_http_note_conflict_reruns_public_function_from_verified_peer_document
```

PASS, exit 0: 1 test collected in 0.57s. Existing unknown `timeout` config warning.
Collection only; no fixture or body execution.

```bash
timeout 45s /root/.local/bin/ruff check --config pyproject.toml --no-cache tests/editing_conformance/test_p4_ten_note_v2_runtime.py tests/editing_conformance/test_p4_note_rerun_v2_runtime.py
```

PASS, exit 0: All checks passed.

```bash
timeout 45s env PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD:/home/user/work/wt/rt-pin-a5d42583" ASTRID_RUNTIME_CHECKOUT=/home/user/work/wt/rt-pin-a5d42583 /root/.local/bin/mypy --config-file pyproject.toml --platform linux --no-incremental --cache-dir /tmp/w-1c6439af9a/mypy-cache tests/editing_conformance/test_p4_ten_note_v2_runtime.py tests/editing_conformance/test_p4_note_rerun_v2_runtime.py
```

PASS, exit 0: no issues in 2 source files. Existing notes say the untyped test
function's body is not checked under the repository configuration.

```bash
timeout 45s env PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD:/home/user/work/wt/rt-pin-a5d42583" ASTRID_RUNTIME_CHECKOUT=/home/user/work/wt/rt-pin-a5d42583 /home/user/work/venv-app2-native/bin/python /tmp/w-1c6439af9a/offline_controls.py
```

PASS, exit 0 (ran twice; second includes downstream inspection): the existing
pure provider `execute` on the shared real document fixture preserves the raw
NOTE_PATH operand, lands `PEER_VALUE + SUFFIX` in both mirrors and emits the exact
canonical step patch. The actual edited AST assertions accept the literal
canonical path and reject unrelated path, wrong clip, wrong note, different root
and original unnormalized operand at BOTH diagnostic/effect boundaries: 10
negative checks. The entire effect comparison additionally rejects another
physical ref, a lost peer value and an absent before guard: 3 negative checks.
The separately reported pre-existing raw/enriched-command assertion is confirmed
to fail; this expected diagnostic finding does not become a passing behavior test.
These are auxiliary offline controls, not live or main-suite acceptance evidence.

```bash
timeout 45s env PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-app2-native/bin/python scripts/vendor_lock.py check runtime.lock.json
timeout 45s env PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD:/home/user/work/wt/rt-pin-a5d42583" ASTRID_RUNTIME_CHECKOUT=/home/user/work/wt/rt-pin-a5d42583 /home/user/work/venv-app2-native/bin/python /tmp/w-1c6439af9a/preflight.py | tee /tmp/w-1c6439af9a/preflight.log
git diff --check
git status --short
git diff --stat
git diff -- tests/editing_conformance/test_p4_note_rerun_v2_runtime.py
```

PASS: vendor lock prints `ok runtime.lock.json`; preflight completes with
`PASS: source/delta, lock/schema, pinned clean runtime, origins and unchanged service row`.
Runtime modules `runtime_protocol`, `.service`, `.store`,
`.timeline_commit_provider`, `astrid_runtime` all resolve inside the pinned a5d
checkout; Agent generated/client/metadata modules resolve inside this worktree.
The preflight proves the exact three-substitution delta and absence of any
untracked worktree files. Diff check is clean; status contains only the one file.

Existing `agent p4-v2-http-nodes` row: exactly one, 1379 bytes; SHA-256
`fafc5fa04275856881cb8188f782f00b73caf9492640a34369799738bd0af948`.
Whole suites.conf SHA-256
`c4e4e6f03a3cf79258de2393ce0017009f702238d0a57a4688bbf5a0e5ca1cf8`;
outside-row SHA-256
`8d532ead4341ec9f89f311c50ee43ba428e6b4db5879031d145176306bef0468`.
All are unchanged from the independent 0813 preflight.

Read-only investigation also used `git rev-parse`, `git show`, `rg`, `sed`,
`cat`, `ls`, and `pwd` for the files/branches cited above. No Git mutation ran.

## Limits and handoff

No live HTTP/body/socket/browser/daemon/service/full/build/test-service request
ran. No new transport/executor/private canonical cache, fixture, product,
generated, pin, lock, package, ops, shared install, suite row or tracked report
was changed; no deletes, commits, checkouts, merges, rebases, pushes or refs ran.
Authoring was confined to the assigned one-file test change and named handoff /
worker artifacts. No plan or contract decision was changed.

Independent Luna review follows this candidate before ONE changed-evidence
original-node run by the authorized owner. Surface the proven raw-versus-recorded
command assertion to the orchestrator first; it prevents predicting a green live
rerun from this path-only correction. A separate bounded oracle correction can
use the full authoritative records while checking every submitted field; it must
retain all captures and avoid response-derived expected values. The orchestrator
owns that scope decision. No blocker prevented completing this assigned correction.
