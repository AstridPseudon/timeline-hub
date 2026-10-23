# D20 integrated proof

**Result: PASS** on the required Agent/Runtime integrated tuple.

## Exact tuple and provenance

- Agent integration HEAD: `8c355a48e4cc2a8ec9d5ed6873a585d2540a2dbe`
- Agent merge parents: `f6116e1b658514021cbbf08d5a6f16a240523f1a` and reviewed
  `aa72cb4894dbfa6f966f9839da1da651be9d7b6a`
- Agent HEAD tree: `c4d72b065d6e68c92e4335120cc016cadf53b06a`
- Reviewed `aa72cb489` tree: `c4d72b065d6e68c92e4335120cc016cadf53b06a`
- Content comparison `aa72cb489..HEAD`: clean; the normal integration merge
  retained the reviewed tree without conflict edits.
- Runtime checkout: `/home/user/work/wt/rt-pin-8592822f`
- Runtime HEAD: `8592822fd11275540f596562f43c715676f2bc0f`
- Runtime tree: `ed9856f43a4e44a058bf2230badea2c4c7080050`

The independent review at
`design/agent-D20-shared-placement-review-1320.md` is a final PASS for
`aa72cb489`. Its reviewed source blobs are retained in the exact integrated
tree above. No Agent product, test, configuration, schema, generated-client,
dependency, or pin changes were made by this proof worker.

## Required test

Command run exactly against the pinned Runtime, with private durable evidence
and `ORCH` set:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.:/home/user/work/wt/rt-pin-8592822f ASTRID_RUNTIME_CHECKOUT=/home/user/work/wt/rt-pin-8592822f D20_EVIDENCE_DIR=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-D20-integrated-proof-1329/evidence ORCH=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch /home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider tests/editing_conformance/test_occurrence_shared_d20.py
```

Result: **9 passed in 10.17s**; **0 skipped and 0 deselected**.

Evidence is at
`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-D20-integrated-proof-1329/evidence/`:

- `public-shared.json` (562055 bytes) contains the full before/after closure,
  request, preview, accepted result, undo, redo, retry/reopen result, history,
  negative replies, and origins.
- Stable JSON SHA-256 guards for the canonical documents are:
  - before: `b628703e72ec5c2e26401e891da5ff8faa3526b8f0ba8e0df31416c93e83c3aa`
  - after: `077e2c55ed0f97d2750115f7c663937a1d50fe9972d9e4a297413d7c43dd5deb`
- Recorded origins are Agent
  `/home/user/work/wt/agt-D20-integrated-proof-1329/astrid/sdk/timeline/commit.py`
  and Runtime
  `/home/user/work/wt/rt-pin-8592822f/runtime_protocol/service.py`.

The public Runtime proof covered preview/accept, exact retry, close/reopen and
retry, undo, redo, undo-of-redo, and six no-write refusals: occupied, foreign,
forged, foreign-timeline, retired, and stale (`dependency_changed`). The
provider guard cases also checked source, membership, order, occupied, foreign,
and forged mutations without changing head or entries. The evidence preserves
the complete v2 request/reply fields, including base pair, commands, label,
steps, merge, reads, dry-run, source, rationale, group ID, canonical data,
records, bindings, effects, dependencies, history, and undo metadata.

The independent review's exact-tree results are reused legitimately: **110
focused tests passed**, **13 additional tamper/no-write probes passed**, Ruff
was **2149 current / 2149 baseline**, mypy was **1912 current / 1912
baseline**, and `git diff --check` passed. The current tree is byte-for-byte
the reviewed `aa72cb489` tree, so no fork or altered-blob qualification is
being claimed.

## Actual interface for Proof's original shared-popup fixture

The old fixture described in `agent-D20-old-shared-writer-fact-1254.md` cloned
the source occurrence, assigned `f2-occurrence-copy`, retained the physical
`shot_id`/`shot_revision_id` and internal/media closure, changed only placement
to `12000` ms, and submitted a full publication to the retired composition
publication route. Proof should preserve those behavioural assertions while
migrating the write to the existing v2 commit carrier.

The exact semantic command is:

```json
{
  "schema_version": 1,
  "op": "occurrence.place-shared",
  "version": "1",
  "select": "occurrence:SOURCE_OCCURRENCE_ID",
  "args": {"occurrence_id": "f2-occurrence-copy", "on": 12},
  "intent": {"ownership": "occurrence"},
  "created": ["occurrence:f2-occurrence-copy"]
}
```

`on` is seconds and is stored exactly as milliseconds (`12000` here); it is
not frame-quantized. `created` is required and must name exactly the one new
occurrence. The caller supplies no shot, revision, source-document, media, or
alias input. The provider resolves the source only from the authenticated
same-timeline base closure, requires an unchanged published source, appends
the new occurrence, and regenerates derived identity while retaining the
physical shot, internal revision, media, registry, variants, opaque fields,
and original rows.

Agent-side fixture setup may use:

```python
capture_occurrence_place_shared(
    bundle_from_document(before),
    "occurrence:occ-0",
    "f2-occurrence-copy",
    on=12,
)
```

For the App popup, wrap that command in the normal existing v2 commit/outbox
envelope (base revision/publication pair, `commands`, label, per-command
`steps`, `merge`, `reads`, `dry_run`, `source`, `rationale`, and `group_id`).
The popup group may remain `"popup"`; the command itself must remain the
public shape above. Send it through the existing commit endpoint/outbox, not a
full `parent_composition` body and not a new Runtime port. The migrated
fixture should assert the same before/after closure equality, exact retry,
reopen/retry, accepted/preview replies, undo/redo, and no-write refusal cases.

No App browser/HTTP tour was run here; this is the authoritative interface
handoff for that Proof migration, not a claim that the original P2 journey is
qualified. The known unrelated whole-undo fork baseline failure, full suite,
P1/P4, D17, native14/58, and browser work were not rerun or credited.
