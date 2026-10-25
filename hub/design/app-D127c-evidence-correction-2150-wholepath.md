# D127c corrected bounded whole path

## Terminal result

The original 15200 element result remains `NO_GO_ORIGINAL_ELEMENT`: one body,
no retry or resubmission, source preflight and mounted readiness passed, and
the original element predicate failed. Source-custody correction does not
overturn that result or grant profiling credit.

The retained Runtime boundary was completed with HTTP 200, while provider
outcome, App response, caller receipt, and browser wall outcome remain
`UNKNOWN`.

## F001 — first seam correction

The safe cProfile projection is `EXACTMISSING`. That fact does not establish
that an actual summary omitted `cprofile`, does not establish that
`profile_eligible` was false, and does not identify an eligibility gate or
subgate. The exact selector predicate and operand remain `UNKNOWN` because the
safe packet omits the relevant private request fields.

The source relationship is conditional: if an actual retained helper summary
for this request was emitted and lacked `cprofile`, then the helper source makes
`profile_eligible` relevant. That conditional does not identify a Runtime cause
and does not support an optimization claim. Raw pstats is separately
`OPTIONAL_AND_UNCONFIGURED`; it is not a selection result.

## F002 — source custody correction

The product tuple is App `b5c9eadf…` / tree `8e10af09…`, Agent
`070dfc5e…` / tree `60564143…`, Runtime `ab1e4f61…` / tree `7d8e77b2…`, and
Composition `635f4de0…` / tree `5ab5191a…`.

The product Runtime `ab1e…` contains the repository helper at
`tests/helpers/p2_commit_phase_capture.py` with SHA-256 `6c9d…`. The reviewed
helper with SHA-256 `095c…` is a separate external helper recorded from the
normal-home Runtime receipt `cf0b82dd…` / tree `8d568370…`; it is not the
helper contained by product Runtime `ab1e…`. The retained preparation metadata
also records its repository-relative path and reviewed source commits
`368f53f4…` and `fb4addba…` separately from the product tuple.

The actual selected absolute helper path and actual selected helper source
commit are `UNKNOWN`: the retained 2113 manifest records the accepted hash and
explicit-path activation, but not the selected absolute path/source binding.
The normal-home receipt is dispatch-gate evidence only.

## Static caller boundary

The existing mounted App element caller uses the App save/outbox path and the
public Agent APIs through the registered Runtime commit service. Static source
evidence describes the path as ElementsLibraryPanel → mounted element adapter
→ `localSaveSession` → generated Runtime `commitTimeline` POST with
`Idempotency-Key`; this is not live behavior credit.

The C0v2 request context remains the existing contract: `api_version`,
`project_id`, `timeline_id`, `base_revision_id`, `base_publication_id`,
`commands` (including `schema_version`, `op`, `version`, `select`, `args`, and
required `created_when`), `label`, `steps` (including `id`, `label`, `intent`,
`tags`, `command_ordinals`, `patch`, and `optional_reads`), `merge` (`fields`
or `atomic`), `reads`, `Idempotency-Key`, `dry_run`, `source`, `rationale`,
and `group_id`. Replies remain accepted/merged/conflict/invalid/preview forms
under the existing contract; no Runtime acceptance is claimed here.

No credentials, hub writes, merge request, Git writes, upstream, M5, SWAP,
WAL, recovery, or full-tour work is included. No retry or alternate
qualification is proposed.
