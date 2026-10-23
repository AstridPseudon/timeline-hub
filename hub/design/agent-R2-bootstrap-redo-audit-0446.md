# R2 bootstrap redo: owner-ready seam

## Attribution

The bootstrap/pristine and first-clip redo failures are inherited from
`5f0fb2ed`, not introduced by `f677e9bab`: the latter changes only
`astrid/sdk/remote.py` and tests. Existing positives are the crash/reload
bootstrap, exact idempotent retry, native first-clip path, exact undo/redo,
physical restoration, and occupied/retired-ID/ABA guards. The new direct 14
and live production journey pass.

The request remains full v2. The failure is in the authenticated provider
record/closure correspondence. In Runtime
`runtime_protocol/timeline_commit_auth.py:652-676`, `command_output()` projects
`writes + derived_writes` and requires every changed intermediate physical
image to have a matching following input binding (`physical_ref`, input
phase, digest, exactly one revision). During inverse redo, the provider's
restored `inverse_stages`/materialization closure and its following input
binding describe different physical image bytes. Runtime correctly rejects
that mismatch as `invalid_records`.

The correction must retain the complete `{data, receipt}` contract: accepted/
merged status, authentic historical rebasing, canonical document/head/revision/
digests, records, effects, steps, dependencies, history, undo steps, conflict
reason/head, invalid code/path/hint/suggested command, and preview REQUIRED with
`would_status` accepted/merged.

## Minimal production correction

Owner seam: `astrid/sdk/timeline/inverse.py:604-720` captures stage before/after
bundles; `_commit_patch.py:372-380,395-527` turns them into inverse-stage,
effect, and materialization bindings. Preserve the exact authenticated
physical image produced by each preceding recorded stage and derive the next
input binding from that same image. Keep all request/response fields,
metadata/effects/observations, undo ABI, physical restore, surviving-consumer,
and ABA guards. Keep Runtime strict; no auth waiver, dropped observations, or
final-image substitution.

The production caller uses this provider path through the native
`TimelineSession`/Runtime commit service. The separate legacy
`commit.py:1101-1107` missing request/head replay defect remains owned by
`agt-R1-legacy-replay-fix-0442`; it is not duplicated here and does not fix
this `undo_of` path.
