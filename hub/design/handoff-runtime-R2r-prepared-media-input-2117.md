# R2r prepared-media source assessment

## Result

No product changes were made. Existing Runtime verification is sufficient, but the immutable A4 packet cannot carry the required authority.

Existing path:

- Public selector: `runtime_protocol/service.py:2562-2571`
- Selection resolution: `runtime_protocol/timeline_commit_port.py:819-855`
- Managed-object, project, completion, metadata, and CAS verification: `runtime_protocol/timeline_commit_port.py:921-1022`
- Commit-port authority capture: `runtime_protocol/timeline_commit_port.py:350-357`
- Acceptance revalidation and manifest authorization: `runtime_protocol/timeline_commit_port.py:515-557`
- Frozen Agent semantic capture requires `args.media` and invokes `selected_media`: `astrid/sdk/timeline/commit.py:388-441`

The exact packet (`33934817…`) instead contains only `doc.patch` changes. Each inserted registry entry has a synthetic non-digest `media_id`; `dependency_manifest.media` is empty; no five-field `MediaSelection` appears in commands, reads, or steps. Therefore `RequestCommitPort.__declared` cannot contain a selection (`timeline_commit_port.py:124-128`), and the existing provider correctly refuses it. This is an App emission/harness authority limitation, not a Runtime or Agent guard defect.

The current App production path already demonstrates the required shape: `ShotTimelineMediaControls.tsx:74-77` requires `selectedMedia`, and `useTimelineCommandsService.ts:741-756` emits a semantic command carrying the selection.

## Exact packet identities

- Missing hold: `38afc047…c66c738a1`
- Explicit null hold: `a422aaf9…e268269f1`
- Subminimum duration: `99cf8093…603f17f5`
- Incoming transition: `e1f05b38…35f602825`

All four remain correctly refused with `dependency_changed`; no acceptance, history, or realm writes were produced.

## V2 envelope requirements

The valid request must include scope, base revision/publication pair, commands, label, complete step fields (`id`, `label`, `intent`, `tags`, `command_ordinals`, `patch`), `merge`, `reads`, `dry_run`, source, and transport idempotency key (`contract/commit-v2.md:175-257`).

Accepted/merged replies require `{data, receipt}` with canonical closure, digest, normalized commands, steps, merge mode, head/base IDs, accepted revision, publisher, and durable receipt/history authority (`contract/commit-v2.md:703-715`). Conflicts/invalid replies require structured `code`, `path`, `hint`, `suggested_command`, head/base/conflict details and no receipt (`:1265-1274`). Preview replies use `data.status: "preview"` and `receipt: null` (`:1423-1434`).

## Evidence

Command:

```text
/home/user/work/venv-runtime/bin/python -m pytest -q \
  tests/test_timeline_media_selection.py \
  tests/test_timeline_verified_media.py
```

Result: `41 passed in 4.11s`.

Blocked: exact A4 positive acceptance remains blocked until App/A2-A3 supplies authentic Runtime-verified selection inputs through the existing route. No fixture, schema, tuple, manifest, guard, or product workaround was added.

Commit message written: `chore(runtime): assess prepared media source path`