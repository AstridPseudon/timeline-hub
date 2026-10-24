# Contract/caller facts retained for the verdict

The captured source and the approved C0 contract retain the full v2 request
shape: `api_version`, `project_id`, `timeline_id`, `base_revision_id`,
`base_publication_id`, `commands`, `label`, `steps` with
`id/label/intent/tags/command_ordinals/patch` and optional `reads`,
`merge=fields|atomic`, request `reads`, `dry_run`, `source`, `rationale`, and
`group_id`, with mutation `HTTP Idempotency-Key`.

The captured caller predicates retain the Runtime commit door for the real
CLI, Python `timeline.open()`/commit, and sheet paths. The actual three-leg
run exercised CLI/sheet, one shared ten-note Python commit with ten steps and
per-step undo entry, and the conflict/rerun public-function path.

The retained reply predicates are:

- `accepted`/`merged` success with authoritative canonical closure,
  normalized commands, records/effects/bindings, steps, history and a durable
  receipt;
- preview with `would_status` and a null receipt;
- conflict with current head and reason;
- invalid with code, path, hint, and suggested command.

The three service selectors directly exercised accepted, structured conflict,
authoritative canonical/records/steps/history/receipt, and bounded rerun
assertions. Preview and invalid are contract/source predicates, not claimed as
executed by this actual service. No new semantic source audit was performed;
Runtime Sol1932's released helper/author checks and the captured source hashes
are the authority for this bounded review.
