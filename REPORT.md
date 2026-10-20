# Render producer command handoff

Completed a source/design review, not a producer migration. The bounded handoff
is [docs/design/render-producer-migration.md](docs/design/render-producer-migration.md);
`orch/design/render-producer-migration.md` points to it for the owners.
No product or test files changed. Live producers remain intact; Runtime's held
410 must not merge on this evidence. M2 integration still requires the M1 record.

## Findings and ownership

- Assembly deterministically authors two clips/assets on one visual track from
  fenced, ordered child outputs. Its host hook actively forwards whole config
  and registry to `publishTimelineRender` before author-attempt settlement.
  Runtime replaces the projection Document and creates a render checkpoint/task;
  this is not a semantic command publication.
- `publish_stitched_render` delegates arbitrary snapshots to the same endpoint
  through the rendering-owned helper. Current source contains no production
  invocation, only the definition/export and negative test caller. This qualifies
  the inbox's active-producer inventory; it does not justify keeping the seam.
- Installed commands cover `clip.move`, `track.create`, inverse and restore.
  Only track creation suffices for assembly. R4 asset registration/media insertion
  are reference contracts, not installed operations; the handoff gives exact
  arguments and handlers. Agent's registry workers must own their port, including
  explicit replacement intent for populated targets. No second registry, generic
  replace command, inferred snapshot-diff intent or retrospective rewrite added.
- Exact registered output selection needs association/object/lifecycle version
  or generation/variant pins. Assembly currently emits only child task/object/clip
  identities. Generic outputs without authoritative variants are not sufficient
  for the current selection API. Preserve normal generation registration; never
  synthesize media catalog identities or silently change continuation asset keys.
- Normal Agent host routing also needs an authorized submitter: worker scopes
  omit `projects:write` and `tasks:write`. Attempt-fenced publication currently
  protects cancellation/stale attempts atomically; the ordinary command contract
  does not carry an attempt fence. Owners must resolve that guarantee explicitly,
  not replace it with a racy preflight check or grant the renderer edit authority.
- Existing render task admission can freeze the accepted revision using
  `canonical_head_revision_id`, or refuse if it advanced. Keep the publication
  receipt and pending render durably across the ACK/admission gap; the current
  command session clears its flight without a producer continuation.
- Runtime source freezes current-head inputs before looking up task idempotency.
  Thus render A / lost ACK / head C / restart / exact guarded retry can fail before
  replay. This is a source finding, unverified by execution. Runtime owns proof
  and correction through the existing task API/snapshot-ref lane. Do not weaken
  the revision guard or render latest to work around it.
- App's normal render router already admits render-only tasks with canonical
  guards; no nongenerated App publication-endpoint caller was found. Its source
  was read only; no shared dependency graph was loaded.

## Verification

No pytest, full suite, browser, socket, build, install or CPU check was run.
This is a documentation-only result. `QUIET.md` was not present in the accessible
supplied workspace or orchestration trees, so the required quiet-window file
could not be read. No behavior is claimed tested, migrated or fixed.

Documentation whitespace checks passed (each exit 0):

```text
git diff --check
git diff --no-index --check /dev/null docs/design/render-producer-migration.md
git diff --no-index --check /dev/null REPORT.md
```

Source inspection commands included:

```text
git status --short
git rev-parse HEAD
git -C /home/user/work/agent rev-parse HEAD
git -C /home/user/work/runtime rev-parse HEAD
git -C /home/user/work/app rev-parse HEAD
rg -n 'assemble_timeline|_publish_assembled_timeline|publishTimelineRender|publish_stitched_render|publish_authoring_proposal' astrid --glob '*.py'
rg -n 'publish_stitched_render\(' astrid tests
rg -n 'publishTimelineRender|publish_timeline_render' /home/user/work/app/src --glob '!generated*'
git show origin/codex/handover-timeline-r4-20261019-candidate-sdk:astrid/sdk/timeline/commands.py
```

Reviewed heads: own worktree and Agent integration
`fc324e838fd668fc06cae906e8bcfccace86ad62`; Runtime
`9f9b25c000485e919f30f1411831fe2d5a3c1316`; App
`2bfde69eac32335eae0bc5fa2820940c0b3c694b`.
The no-caller App search returned no matches; the stitch search found one
definition and one negative test invocation. Frozen code was read with git show;
no checkout/commit/merge/rebase/push or other worker/integration writes occurred.

## Decisions, blockers and next steps

Chose the permitted design-only outcome because the installed official
operations do not suffice. A thin owned adapter would either omit authored
behavior or invent an unauthorized writer. Required future tests are specified
in the design, including original intent/guards, exact retry identity, restart,
renderer-off acceptance, ACK/admission crash, head advance, stale/cancelled
attempts, duplicate media and artifact-only completion. Existing passing behavior
tests remain untouched; temporary lost behavior must retain its original
expectation with strict xfail/it.fails and a restoration requirement.

Next: Agent manager supplies ordinary registry coverage and the normal host's
authorized batch/continuation routing; Runtime proves retry and lifecycle
semantics. Viewing can then implement the smallest rendering-pack proposal and
focused tests. Keep slow media/artifacts, task completion/billing and relational
metadata. No Runtime 410 merge recommendation before full producer coverage.
