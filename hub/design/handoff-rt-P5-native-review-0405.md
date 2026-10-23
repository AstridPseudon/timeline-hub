## PASS — P5 independent qualification

P5 is qualified on the integrated pair for the requested scope: PLAN §3 P5,
PLAN-v1 §6 gates 2–4, and the approved commit-v2 §§1–7. This is not a P1 or
H3 GO claim.

### Exact identities and provenance

- Runtime: commit `62c454ac07fb46a1a67847d933f1ed5f53043e30`, tree
  `b84e048c455916c3b44cd1964aa8b55a3f4d8088`.
- Agent: commit `f894c3c9dda25ab03527eeb7f52da5da31d627c1`, tree
  `d24f25a65be282a56b3fcd814a8718a3c0587b9b`.
- Integration test blob:
  `899489213da5a6a5b1e29430359830463da95501` (both `HEAD:path` and
  `git hash-object` agree).
- Runtime provider, execution, and store imported from this review worktree:
  `runtime_protocol/{timeline_commit_provider.py,timeline_commit_execution.py,timeline_commit_store.py}`.
- Agent provider, commands, workspace client, and generated client imported
  from `/home/user/work/wt/agt-pin-f894c3c9` under `astrid.sdk.*` and
  `astrid_runtime_client.*`; no sibling/site-package fallback was observed.
  Provider identity is `astrid-v1`, interface `1`, contract digest
  `sha256:35c2d9c5e0b51ab8d8b7a4f4dbafbdfcb13d232d7bd22fff21cf73e250398d4c`.

The normal Agent lock has source commit
`34eac0041b0891e9011966b39bcbd26053fde5bc`, producer tree
`9853574865f25e08284e82ffb26c0bdecaa16a30`, schema/artifact values
`d106dfe8212500709b4072d7bc0486f83c27d5d8de33d215cb52b9ea7d46357d`,
`sha256:35c2d9c5…`, and `sha256:d5f98db3…`. An immutable git-object check
against producer commit `34eac004…` verified all 15 lock consumer mappings
byte-for-byte against both the producer manifest and the pinned Agent files.
`scripts/artifact_manifest.py --check` also passed. The direct
`vendor_lock.py check` invocation could not use the absent historical checkout
`/home/user/work/wt/rt-pin-34eac004`; the immutable commit/object check is the
replacement provenance evidence, not a re-vendoring.

### Test evidence

1. Independent collection, exact mandated command:

   ```text
   env PYTHONDONTWRITEBYTECODE=1 ASTRID_RUNTIME_CHECKOUT=$PWD ASTRID_CHECKOUT=/home/user/work/wt/agt-pin-f894c3c9 PYTHONPATH=$PWD:/home/user/work/wt/agt-pin-f894c3c9 /home/user/work/venv-agent/bin/python -m pytest --collect-only -q -o addopts= -p no:cacheprovider -m integration tests/test_timeline_commit_integration.py
   ```

   Result: **14 tests collected in 0.35s**. The integrated author’s one
   allowed execution used the same exact source blob and command, with **14
   passed in 24.82s**, no skips or deselections.

2. The 14 original assertions remain intact: the source has only the
   integration marker and parametrization, with no skip/xfail controls. The
   test blob is unchanged from the integrated qualification evidence. Its
   coverage includes native disjoint rebase and same-field conflict,
   concurrent edits, guarded inverse/ABA and track creation, renderer-off
   save/reload/undo, full-v2 native+`doc.patch` preview/accept/retry, fields
   versus atomic stale-head behavior, structured invalid replies, door
   authorization/project/origin checks, lost-ack restart retry, and tamper
   refusal.

3. Narrowly justified crash requalification (the prior 24-pass service used
   Agent `1951ee928…`, while the current Agent provider changed materially in
   `commit.py` and `_commit_patch.py`):

   ```text
   request-test integration:runtime marked-integration --files tests/test_timeline_commit_crash.py
   ```

   Service `runtime-marked-integration-1023040645-14341`, with external Agent
   `f894c3c9…`, ran the exact marked command and returned **24 passed in
   22.61s**. This covers current-provider commit/restore at pre/before/after
   SIGKILL boundaries, retained-input paths, exact retry without provider
   execution, changed-payload refusal, and the explicitly labelled host-boundary
   first-capture cases. The host-boundary cases do not substitute for the real
   Agent provider; the commit/restore and retained-input cases use it.

### Scenario and contract mapping

- Renderer-independent save is proven by the integration fixture’s import
  tripwire for rendering modules and `evaluate_closure`; the save and undo
  assertions still pass. Crash tests repeat the renderer-unavailable guard.
- Door authorization is an actual mounted Runtime door: `RuntimeDaemon` with
  `authoring_profile="astrid"`, provisioned product credentials, raw HTTP
  `DoorWorld` requests, the real Agent factory, coordinator, port, and store.
  Positive and negative auth/origin/project/scope cases assert durable no-write
  behavior; no fake provider or alternate executor is used for the positive
  path.
- Full-v2 request/reply coverage includes base revision/publication, semantic
  plus `doc.patch` commands, label, per-step patch/reads, `fields` and
  `atomic`, declared reads, dry-run, idempotency, and accepted/merged/conflict/
  invalid/preview (`would_status`) replies. History/readback assertions retain
  authoritative steps, reads, writes, bindings, selections, dependencies,
  effects, receipts, and undo metadata. Independent Agent 0353 and integrated
  0355 evidence on the exact Agent tree separately passed the provider/envelope
  and public-client checks for the v2/step-undo surfaces.
- Crash/retry and changed-payload-under-one-key promises are covered by both
  the current-provider 24-case crash run and the native lost-ack/restart case.

### Integrity and limits

- `git diff --check`: PASS; Runtime and exact Agent worktrees were clean.
- Crash-reuse source identities were checked: Runtime store blob
  `607012dd…`, execution blob `039f63d4…`, and crash-test blob
  `9a5a1dfb…` are identical to the prior crash tree
  `7a182a69fa7ec893987dbbd3ac34eb3ba577ec6f`. Because Agent had changed, the
  current-provider crash run above was performed rather than relying on those
  Runtime blob matches alone.
- Reused static Agent evidence from the independent 0353/integrated 0355
  reports: Agent 46 passed/39 deselected, Runtime envelope 48 passed/27
  deselected, Ruff 2151/2151, and private mypy 1915/1915 on the exact Agent
  tree. No source edits were made here, so py_compile is N/A; lint/type checks
  are reused unchanged-source evidence.
- No full suite, browser, heavy, gesture, gate-5, native14 duplicate, or Agent
  46 rerun was performed. P1/H3 and rendering/viewer parity remain outside
  this qualification.

No product, test, generated, schema, pin, config, or repository report files
were modified.
