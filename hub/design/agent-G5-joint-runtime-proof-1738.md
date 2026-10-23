# G5 joined-source original Runtime qualification

## Verdict

**Joined source: PASS. Original Runtime qualification: BOUNDARY / not a PASS.**

The four reviewed donor paths were imported byte-exactly from `d1d41c4056f509ce24af916ee20b7b683ac8f8f1` onto `bda966e9c491e1fa4b683cda8913dddeaa14c63d`. Three-way comparison found no actual overlap: the three modified current blobs equal donor parent `63baa707b4bce52b36c06dc3345d2fd357b10f66`, and the new test path was absent. The worktree contains exactly those four changed paths; no other code, test body, fixture, dependency, or Git ancestry was changed.

## Preflight

D21 report-all preflight passed before qualification on Runtime `d9e2a71e87c827290a3ff58a94f6fb8b4bc11e0b` / tree `9b07545cac9a8bbafb16246aaa6f72050ef7cffe`. It recorded joined source hashes, actual module origins and hashes before/after trivial Runtime boot, the authentic archive SHA-256 `2915bd4ac0d46954d19c30f87a517b82074218699978e650fab03fcba81b72d3`, normal reader closure, exact revision/publication pair, digest, source/body fingerprints, and the old-route scan. The normal reader saw one project, one timeline, schema 31, head `{'publication_id': 'txn-11c90075be6c4c8bb9e2627366f0fe4f', 'revision_id': 'a3e671256f1c42b8837d3e118c97b21b'}` and digest `sha256:b6069d1ddccc0279e871b142773b63b73b107ebf9d0adc11ab73832b69097afb`.

The imported authenticated fixture provides read-only per-call capture hooks with bounded JSON flushes for request, canonical/store/history before calls, candidate/baseline/source bundles/restoration records, replies, and refusals. No return value or claim was altered. No credentials are included in the packet.

Full preflight JSON: `/tmp/w-a525d31f0b/d21-preflight.json`.

## Required original cases

The exact ORIGINALFOUR command ran once with the pinned Runtime and authentic fixture:

```text
PYTHONDONTWRITEBYTECODE=1 ASTRID_RUNTIME_CHECKOUT=/home/user/work/wt/rt-pin-d9e2a71e PYTHONPATH=.:/home/user/work/wt/rt-pin-d9e2a71e TMPDIR=/tmp/w-a525d31f0b timeout -k 5 40 /home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider -m integration tests/sdk/test_timeline_checkout_history_runtime.py
```

Result: **2 passed, 2 failed in 27.13s**. The two failures are genuine next boundaries, not Agent join conflicts:

- `test_checkout_reload_undo_cli_redo_uses_retained_history`: Runtime/public redo refused with `conflict`, message `nested inverse ranges differ from accepted history`.
- `test_retained_restore_does_not_reopen_consumed_draft_steps`: after restore, the draft base/document did not equal the original exact authenticated closure; the base moved to a generated authoring revision.

The two passes were `test_open_bundle_keeps_http_rows_raw_and_round_trips_canonical_images` and `test_catalog_recover_uses_real_http_and_preserves_closure_before_revision_restore`.

The requested restructure name was absent. The retained original body is `test_restructure_whole_inverse_redo_and_intervening_overlap_refusal`, covering forward, whole undo, redo, and later overlap/no-write. Its first marker-qualified selection executed zero tests and exited 5 because the function has no integration marker; this was not counted as a qualification run. The corrected single-node command without `-m integration` then ran once:

```text
PYTHONDONTWRITEBYTECODE=1 ASTRID_RUNTIME_CHECKOUT=/home/user/work/wt/rt-pin-d9e2a71e PYTHONPATH=.:/home/user/work/wt/rt-pin-d9e2a71e TMPDIR=/tmp/w-a525d31f0b timeout -k 5 40 /home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider tests/sdk/test_timeline_restructure_guarded_runtime.py::test_restructure_whole_inverse_redo_and_intervening_overlap_refusal
```

Result: **1 failed in 17.14s**. Forward and whole undo passed; redo failed before the later overlap/no-write assertion. Runtime returned `validation_error`, `status=refused`, `reason=invalid_records`, message `inverse stage native writes do not cover its authenticated effect image`. No retry or repair was attempted.

## Quality and preservation

- Scoped Ruff: PASS.
- Vendor lock against frozen producer `34eac004`: PASS.
- Artifact manifest: PASS.
- `git diff --check`: PASS.
- Independent donor source quality is reused: d1d reported 27 focused provider/store tests plus 80 neighbors; prior G5 quality evidence remains 1911 mypy / 2148 Ruff. No new baseline, dependency, schema, or generated-file deviation was introduced.

The flat bounded packet is `/tmp/w-a525d31f0b/g5-qualification-packet.json`. Its SHA manifest is `/tmp/w-a525d31f0b/g5-sha256-manifest.txt` and credential scan is `/tmp/w-a525d31f0b/g5-credential-scan.txt`. Private Runtime artifacts remain under `/tmp/w-a525d31f0b` and are represented by hashes only.

## Classification and next step

The reviewed Agent join is ready as a draft, but the required original proof is not green. Ownership is Runtime: resolve the nested inverse accepted-history range mismatch, authenticated effect-image coverage on restructure redo, and retained draft exact-base hydration. Keep P1 NO-GO; do not merge or override it. No broader suite, integration request, Git mutation, or daemon/hand-environment change was made.
