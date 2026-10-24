## D69 investigation report

No product files were changed. Worktree remains clean at `61f0fb613a`.

### Whole path

`src/shared/lib/placement/placementService.ts`

`placeGeneration()` (496–523) → `mutateTimelineDocument()` (367–397) → `createPlacementLocalSaveHandoff.flush()` (211–235) → `LocalSaveSession.flush()` (315–320) → persisted outbox dispatch (158–209) → `RuntimeDataProvider.commitTimeline()` (751–768) → generated POST with `Idempotency-Key` (`generated.ts:202–204`) → Runtime execution → Agent `RuntimeCommitService.commit()` → rollback → `retryRejected()` (336–344) → new load/reapply/new POST.

The request includes the required base pair, `doc.patch` command, source, label, steps, merge/reads, rationale/group, and idempotency key. Accepted responses are validated for canonical document, digest, ID map, accepted head, compiler/provider metadata, and receipt (`dataProvider.ts:807–840`).

### Finding

Current `isClassifiedStaleHeadConflict()` (`placementService.ts:123–130`) authorizes replay using only:

```text
outbox kind === conflict
details.status === conflict
```

That is unsafe. Agent semantic failures such as `dependency_changed`, `binding_changed`, `value_conflict`, `selection_changed`, `atomic_scope_changed`, and `intervening_write` produce HTTP 409 with exactly that status shape, plus a semantic `details.reason` and conflict payload (`agent/astrid/sdk/timeline/commit.py:1407–1420`, `_commit_errors.py:90–110`).

Therefore the current path converts a definitive Runtime refusal into `TimelineVersionConflictError`, resolves the rejected outbox, and semantically replays it. This violates C0.

The existing placement stale-head fake is under-qualified: it returns `status: "conflict"` without a reason (`placementService.test.ts:167–174`). It is not evidence of a real Runtime-safe replay signal.

### Safe correction seam

Qualify the retry decision at the placement handoff boundary, before converting the LocalSave failure into `TimelineVersionConflictError`:

- Require an explicit Runtime/source-qualified stale-head retry marker.
- Never authorize replay from `status` alone.
- Keep all semantic reasons and nonempty conflict payloads as retained refusals.
- Preserve `LocalSaveSession` rollback, durable rejected intents, and exact-request retry behavior.
- Runtime/Agent currently handles CAS contention internally; exhausted contention becomes `head_busy`/`refused`, which belongs to exact-request retry, not semantic replay (`commit.py:1287–1403`, Runtime `timeline_commit_port.py:650–660`).

Until an explicit retryable marker is source-qualified, the C0-safe behavior is to avoid `retryRejected()` for Runtime 409 conflicts.

### Existing evidence

Passing upstream controls retain rejected requests, roll back the visible document, preserve details, and perform no second send after recovery:

- `src/tools/video-editor/commands/localSaveSession.test.ts:308–335`
- `src/tools/travel-between-images/components/shotTimelineDataProvider.a3.test.ts:704–723`

The placement controls cover refused, invalid, and transport failures, but not real `dependency_changed`/binding conflicts (`placementService.workspaceV1.test.ts:218–230`).

### Verification

No tests were run, per the read-only investigation brief; no browser, HTTP, full, or original suites were invoked. Read-only `rg`, `nl`, `git diff`, and `git status` inspections completed successfully.

Commit message written to the requested path; `DONE` marker created.