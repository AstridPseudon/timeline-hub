## G4 assessment

No repository files changed. The existing Runtime authority can support exact historical occupancy reuse, but the current Agent carrier is insufficient as-is.

Findings:

- `timeline.duplicate` already captures the five-field `source_ref`, authenticates it through `source_revision_closure`, and hydrates media, but requires a fresh identity map and empty destination.
- `occurrence.place-shared` is the nearest carrier, but currently only accepts an existing same-timeline occurrence.
- Runtime already verifies foreign project/timeline scope, accepted publication/revision/digest, immutable media, and exact `shot_closure`. Exact immutable shot reuse does not update the mutable global shot projection; newer global shot heads do not invalidate the historical pin.
- The retired writer in `cbe78b4` handled both inline and reference-style child payloads by resolving exact existing shot/internal revisions. Current `publish_parent_composition` and `create_reference` reject through `_require_timeline_command`; the reference projection is media-only and cannot carry occupancy.
- The Agent gap is real: `commit.py` only resolves foreign source material for `timeline.duplicate`; `document_from_bundle` and inverse source handling assume the authenticated working closure is same-timeline.

## Bounded proposal

Extend provider-only `occurrence.place-shared`; do not add a public operation or Runtime executor.

- Arguments: existing `occurrence_id` and `on`, plus existing five-field `source_ref` and a `source_occurrence_id`. Use `select: "parent"` for the cross-timeline branch.
- Source capture: call `port.source_revision_closure(source_ref)`, locate the exact source occurrence, call `shot_closure` for its exact shot/revision, validate all source media with `raw_media_info`, and hydrate authenticated inputs.
- Candidate effect: copy the source occurrence’s authored fields, replace its destination occurrence ID and start time, retain the exact source `shot_id`, shot revision, and internal timeline revision. Add only `occurrence:<destination-id>` to `created`; never create a shot or internal revision.
- Working closure: merge the authenticated foreign shot/internal images into the destination candidate’s in-memory runtime document so compilation can emit the exact immutable references. Do not use `source_bundles` or a synthetic local inverse.
- Records: destination parent collection/order reads; exact `source_ref` authority dependency; exact source occurrence/shot bindings; source media/document dependencies. Runtime remains the acceptance and revalidation owner.
- Undo removes only the destination occurrence. Redo must re-resolve the retained foreign source authority. Existing same-timeline inverse binding logic needs a structured foreign-source retention/history guard.
- Inline/reference fixtures should remain two fixture variants of the same carrier, producing identical physical shot/internal identities—not a new command mode.

Required refusals include foreign project, same timeline, invalid publication/digest, missing or ambiguous source occurrence, changed source shot/internal bytes, missing media, archived source at acceptance, destination occurrence collision, incompatible destination track/order, and any attempted child substitution or fresh-shot allocation.

Conclusion: no orchestrator contract question is needed. Runtime’s existing private source-authority seam is sufficient. The missing implementation seam is Agent-side authenticated foreign-closure installation plus inverse/redo retention; assign that semantic ownership to the Agent G4 owner before writing the carrier.

Checks run:

- AST parsing of relevant Agent and Runtime files: passed.
- `git diff --check`: passed.
- Worktree remains clean.
- No pytest/full/browser/HTTP/vendor checks run; this was a read-only assessment.