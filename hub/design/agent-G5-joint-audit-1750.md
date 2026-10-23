# Independent G5/R2 source-and-evidence audit

## Verdict

- **Source join: PASS.** `d32f87b838cdd58d4ac0539c152e8cd0ff9ea091` is a direct child of `bda966e9c491e1fa4b683cda8913dddeaa14c63d` and changes exactly the reviewed d1d four-path union. Every joined blob matches `d1d41c4056f509ce24af916ee20b7b683ac8f8f1`; no other product/test path is changed.
- **Qualification evidence: FAIL / unproven.** The retained log records ORIGINALFOUR as 2 passed/2 failed and the retained c271 body as forward+whole-undo pass followed by redo failure. The prior report’s blanket Runtime attribution and “durable” packet claim are not supported by surviving evidence.
- **Gate: P1 NO-GO remains.** This audit does not authorize integration, repair dispatch, rerun, or a qualification override.

## Source join and hash correction

The target commit has parent `bda966e9c491e1fa4b683cda8913dddeaa14c63d`, tree `d389da2cd99c6f5dcef6924b446b3d3243b84d1b`, and exactly these changes:

```text
M astrid/sdk/timeline/_commit_timing_validation.py
M astrid/sdk/timeline/commit.py
M astrid/sdk/timeline/validation.py
A tests/editing_conformance/test_authenticated_legacy_restore.py
```

The current target blobs equal the d1d donor blobs byte-for-byte:

```text
1a8c2821235e04a588f756f8208005383f86489d  astrid/sdk/timeline/_commit_timing_validation.py
7a893c63553b3294e6db047636151ae031f315d2  astrid/sdk/timeline/validation.py
86be6ff6e7c79621335f880fa22587820cf09672  astrid/sdk/timeline/commit.py
95b2d8f3481384aa41cca7fdde3649cf5f19bd35  tests/editing_conformance/test_authenticated_legacy_restore.py
```

The donor’s parent is `63baa707b4bce52b36c06dc3345d2fd357b10f66`; the three modified current blobs equal that parent’s blobs, and the added test path was absent. This is a clean reviewed leaf import, not an overwrite of divergent G5 work.

There is a full-SHA typo in the surviving integrated R2 memo: it names the authenticated restore parent as `d1d41c4056f509ce24af916ee20b7b683ac8f8f2`. The actual Git object and all refs are `d1d41c4056f509ce24af916ee20b7b683ac8f8f1`; the `...f8f8f2` object is absent. Thus the surviving evidence supports “stated f2, actual f1.” The audit brief’s f1/f2 direction is reversed relative to the repository evidence; no f1→f2 correction is asserted.

The D21 AST locks are reproduced exactly with `ast.get_source_segment`:

```text
test_checkout_reload_undo_cli_redo_uses_retained_history  lines 128-160  cc761fb486d617cdecf4dd6c7ac40486073b50d693c28fcacff0b370b4f4deeb
test_restructure_whole_inverse_redo_and_intervening_overlap_refusal lines 570-689  839470f2e8a32c5a1ca4cfa869bd246bea7b2fbc93f1012dd2eedad41e3440a9
```

The imported authentic-fixture file is a new path with four parametrized test functions; it is not a substitute for either locked D21 body. No body/test source was edited by this audit.

## Recovered qualification facts

The following are recovered from the retained worker log, not rerun here.

ORIGINALFOUR ran once with the pinned Runtime `d9e2a71e87c827290a3ff58a94f6fb8b4bc11e0b` and the joined Agent tree:

```text
PYTHONDONTWRITEBYTECODE=1 ASTRID_RUNTIME_CHECKOUT=/home/user/work/wt/rt-pin-d9e2a71e PYTHONPATH=.:/home/user/work/wt/rt-pin-d9e2a71e TMPDIR=/tmp/w-a525d31f0b timeout -k 5 40 /home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider -m integration tests/sdk/test_timeline_checkout_history_runtime.py
```

Observed result: **2 passed, 2 failed in 27.13s**. The failures were `test_checkout_reload_undo_cli_redo_uses_retained_history` with `nested inverse ranges differ from accepted history`, and `test_retained_restore_does_not_reopen_consumed_draft_steps` with a document/base mismatch after restore. The two passes were the raw HTTP-row round-trip and catalog-recovery cases.

The requested restructure selector was absent. The retained original c271 body was `test_restructure_whole_inverse_redo_and_intervening_overlap_refusal`. Its marker-qualified attempt deselected one test and exited 5; the corrected single-function command ran once:

```text
PYTHONDONTWRITEBYTECODE=1 ASTRID_RUNTIME_CHECKOUT=/home/user/work/wt/rt-pin-d9e2a71e PYTHONPATH=.:/home/user/work/wt/rt-pin-d9e2a71e TMPDIR=/tmp/w-a525d31f0b timeout -k 5 40 /home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider tests/sdk/test_timeline_restructure_guarded_runtime.py::test_restructure_whole_inverse_redo_and_intervening_overlap_refusal
```

Observed result: **1 failed in 17.14s**. Forward and whole undo passed. Redo failed before the later overlap/no-write assertion with `validation_error`, `status=refused`, `reason=invalid_records`, and `inverse stage native writes do not cover its authenticated effect image`.

## Causality and ownership limits

The service error is only a throw seam, not ownership proof. Read-only source inspection establishes:

- Agent `_step_undo.py:154-173` validates nested inverse `native_write_range`/`effect_range` against accepted history and can produce the `nested inverse ranges differ from accepted history` failure. Agent `inverse.py:839-844` records inverse-stage native ranges, and Agent `_commit_patch.py:523-535` assigns effect ranges. These are distinct Agent seams; `_commit_patch.py` remains the R1 transcript seam.
- Runtime `runtime_protocol/timeline_commit_auth.py:1352-1354` rejects when the native image does not equal the authenticated effect image. That identifies the Runtime verifier location only. The cause could be the Agent-produced stage/effect records, Runtime/provider preparation, or retained authenticated history.
- The retained-draft failure can be in Agent draft hydration or Runtime restore response/closure handling. The visible assertion does not establish an owner.

The brief’s existing ownership map is preserved: registrySol1750 owns `inverse.py`, nestedSol1750 owns `_step_undo.py`, and R1transcript1735 owns `_commit_patch.py`; no competing author was found. C0 request/reply/history fields (including the full base/commands/steps/reads envelope and accepted/merged canonical receipt/records/bindings/effects/dependencies) are unchanged by this audit, but the deleted per-case packet cannot verify them for these failures.

The full request, prepared provider input, authoritative records/bindings/effects, source history, intermediate images, SQL snapshots, and per-case module-origin captures are **LOST** with `/tmp/w-a525d31f0b`. The prior report’s claim that that packet was durable is incorrect. The preflight’s before/after module snapshot plus one post-case import snapshot cannot establish per-case in-process module tracking. No owner is assigned from the service error, and no Runtime repair should be dispatched without a causal packet.

## Evidence disposition

- **Recovered artifacts:** only facts printed in the worker log and facts still present in committed source/Git objects, preserved in the accompanying evidence files.
- **Audit reconstructions:** the JSON summary and hashes in `workers/agt-G5-joint-audit-1750/evidence/` are newly assembled from those surviving facts and current read-only source inspection; they are not the deleted packet.
- **Lost:** the original full D21 JSON, packet, manifest, credential scan, per-case observer JSON, complete prepared/history/records/effects captures, and private Runtime artifacts. They are not reconstructed or claimed.

The preflight log also records one old-route scan match in `astrid/packs/rendering/docs/SKILL.md:229`; therefore “old-route zero” is not a supported blanket claim from that scan output.

No tests, typecheck, lint, full suite, HTTP/socket run, source edit, test edit, pin/schema/Git/daemon/environment change, merge, or deletion was performed by this audit. Next step is manager-controlled causal capture by the one relevant owner, while preserving P1 NO-GO.
