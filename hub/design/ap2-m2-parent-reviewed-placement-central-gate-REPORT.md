# Parent reviewed-placement central gate

## Result

**Failed at the first positive native-POST milestone; not qualified.** One exact
central run used the committed `ap2-m2-parent-positive-real-causal-repair` source
(`54c145906343c4b62038ce1433a92cd192438f07`, tree
`519962eaf5b7220079b6ab6e5af272201cb2f9f3`) and the narrowed private014 manual-drop
driver. The named suite listed exactly one test before build and ran only that test.

Central result:

- Suite: `ap2-m2-parent-reviewed-placement-central-gate-ap2-m2-parent-drop-real-central-qualification-1020215701-15138`
- Result: exit 1, one failed test, 286 seconds
- Test: `three-products.spec.ts:1141:1` — “M2 real mounted manual video drop…”
- Log: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/tests/ap2-m2-parent-reviewed-placement-central-gate-ap2-m2-parent-drop-real-central-qualification-1020215701-15138/log.txt`

## First-failure facts

The wrong-selection leg completed before the positive leg: the verified-selection
request returned an allowed refusal status (`404` or `409`; the test intentionally
only retained that set), the mounted clip count stayed at its baseline, Runtime
head and history stayed equal to the original, and a verified-selection read was
observed. The exact refusal code and a UI alert were not retained by this test.

The positive leg then completed these checks: media import response `201`; selected
media fields matched the imported asset/generation/variant/object; verified lookup
response `200`; verified response selection equaled the ordinary selection; and all
five verified query fields, including `catalog_digest`, matched. The first failure
was the post-attempt diagnostic after 90 seconds: the test's counter was `attempts: 0`
(the counter increments before its `route.fetch`). No completed POST response,
accepted revision, accepted-history entry, retry, undo, or post-loss assertions were
available. This is not treated as proof that no underlying request was ever made;
the observer recorded no POST attempt, and the cause remains unresolved.

The runner's trace/error-context path was printed, but the existing driver cleaned
its disposable run root on exit. No trace survived outside that root, so there is no
independent trace-based diagnosis and no rerun was made.

## Guards and scope

The runner passed the required pre-build and source guards: Agent `3c4f6de4`, Runtime
`2020741107`, producer `a0dca169`, artifact `f021`, schema `6ba7`, 75-artifact
manifest, and Composition 0.0.13 package/archive checks. The previously recorded
graph-integrity result `22557` passed separately and was not rerun. The hosted build passed. The
worktree remained clean; no source, schema, API, pin, dependency, or adoption change
was made. The reviewed five-file placement/refusal delta and all existing negative,
draft, native-add, retry/restart/reload, undo, opaque, no-double-placement, and
zero-legacy assertions were left unchanged.

No full suite or local browser/socket run was performed. The exact central run above
is the only gate result.

## Next step

Do not qualify this candidate or infer a zero-POST root cause from the counter.
Preserve browser artifacts in a non-disposable output location in the driver, then
diagnose the first missing positive native request before any further gate request.
