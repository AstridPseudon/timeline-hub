# M2 transcript corrected-wire reconciliation recheck

## Verdict

**Bounded SOURCE ACK.** The committed Agent successor closes both HOLD0215
mismatches. This is source/control evidence only; it is not native App/HTTP
qualification.

## Immutable source reviewed

Agent checkout `/home/user/peteromallet/astrid-agent` was clean. The exact
descendant chain is:

- `9d007f26c61f11a27f5082a6147cd70f90a10612` — persisted nested bundle carrier
  fix; tree `bba0c08651b7c93b9ee9c4e90c54cff1db8a93e9`.
- `b39ceb060d87cdb2038a17f610b7f270ef09c29e` — Main caption/review
  reconciliation; tree `3c4dcaf409f5cc947f7eb84369b6ca48e6a90cc4`.
- `53c2c6f95632bf104b8bb13698e7a262822ecfdb` — committed accepted-history
  reload control, reviewed source tree `265e06903721aa1bd27641cbbc3bfd6d8340be7e`.

The source uses only `parent.config.bundle.transcriptReferences` and
`parent.config.bundle.itemsBySchemaRef["astrid.transcript_segment/v1"]`.
Legacy parent-level carriers and `sourceItemsBySchemaRef` wire spelling refuse
before writes. Known legacy-to-canonical references reconcile through the
asset's paired media occurrence, including the App caption shape with no
`asset`. Text/style/timing, review state/payload, opaque siblings, source order,
and exact new/prior pins are retained. Destination collisions, ambiguous
ownership, and shared reviews refuse atomically.

## Evidence

- App compact no-asset caption/review fixture:
  `PYTHONDONTWRITEBYTECODE=1 ./node_modules/.bin/vitest run --config config/testing/vitest.config.ts --no-cache --maxWorkers=1 --no-file-parallelism src/tools/video-editor/data/typed/importTranscriptIdentity.test.tsx`
  — **6 passed**.
- App actual carrier save/publication/reload witness:
  `PYTHONDONTWRITEBYTECODE=1 ./node_modules/.bin/vitest run --config config/testing/vitest.config.ts --no-cache --maxWorkers=1 --no-file-parallelism src/integrations/runtime/dataProvider.test.ts --testNamePattern='atomically publishes edited transcript sources with the expected parent head and reloads them'`
  — **1 passed, 73 skipped by name filter**. It asserts `parent_composition.config.bundle.itemsBySchemaRef`, provider recreation, and reloaded equality.
- App reference-plane serialization control:
  `PYTHONDONTWRITEBYTECODE=1 ./node_modules/.bin/vitest run --config config/testing/vitest.config.ts --no-cache --maxWorkers=1 --no-file-parallelism src/tools/video-editor/hooks/useTimelinePersistence.test.tsx --testNamePattern='serializes only canonical transcript references while leaving rich project projections transient'`
  — **1 passed, 83 skipped by name filter**. It asserts both persisted bundle planes, including `transcriptReferences`.
- Exact Agent archive at `53c2c6f9`, with `ASTRID_RUNTIME_CHECKOUT=/home/user/work/runtime`, running:
  `PYTHONDONTWRITEBYTECODE=1 ASTRID_RUNTIME_CHECKOUT=/home/user/work/runtime PYTHONPATH=<immutable-agent-archive>:/home/user/work/runtime /home/user/work/venv-app2-native/bin/python -m pytest -q -rs -o addopts= -p no:cacheprovider tests/editing_conformance/test_recipe_film_transcript_association.py tests/editing_conformance/test_recipe_film_transcript_association_spike.py tests/editing_conformance/test_gate1_transcript_accepted_reload.py`
  — **19 passed**, with two existing warnings for unsupported `timeout` and `timeout_method` pytest options.

The accepted-history control verifies persisted nested carrier, inverse/redo,
restart, and exact new/prior pin dependencies. Per the task boundary, its
direct `RuntimeService`/private closure path is not trusted as normal daemon,
authenticated `/v1`, or App qualification.

## Live callers inspected

- `src/tools/video-editor/lib/project-transcript-host.ts` — the sole live
  `reconcileTranscriptReferences` consumer in `saveProjectTranscript`.
- `src/tools/video-editor/hooks/useTimelinePersistence.ts` — serializes the
  bundle planes and rehydrates both on reload.
- `src/tools/video-editor/lib/timeline-data.ts` — passes both loaded bundle
  planes into timeline data assembly.
- `src/tools/video-editor/hooks/useTimelineState.ts` and
  `src/tools/video-editor/hooks/useProjectTranscriptHost.ts` — host lifecycle.
- `src/integrations/runtime/dataProvider.ts` — Runtime load/save carrier.

## Decisions, limits, and next step

No product/App file, schema, generated pin, activation, route, writer, or
dependency was changed. The documented `venv-agent` path was absent, so the
already-provisioned read-only `venv-app2-native` was used; no installation or
shared dependency mutation occurred. No full, browser, socket, live route, or
normal genesis qualification was run. The next qualification step is the
separate normal authenticated `/v1` App cohort with the trusted bootstrap and
the same nested carrier, caption/review, reload, and two-pin assertions.
