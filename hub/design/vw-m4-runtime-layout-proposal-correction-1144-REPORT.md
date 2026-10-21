# Corrected unapplied Runtime layout proposal

## Result

Prepared one unapplied patch:

`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/vw-m4-runtime-layout-proposal-correction-1144.patch`

It changes only the proposed `bin/make-runtime` script. The composition base
is `tl/integration` at `df7b86308902fae90eda1dc3080d17d8fc30ea78`; no
Composition product file, Runtime file, Agent worktree, shared runtime, or
environment file was changed.

The patch replaces rejected 1134's flattened layout with one isolated runtime
root whose final shape is:

```text
$D/
  remotion/       # Agent SHA's remotion archive; project, lock, node_modules, CLI
  astrid/         # same Agent SHA's astrid/packs/rendering archive
```

This makes the actual import from `$D/remotion/src/LiveSceneClip.tsx` resolve
`../../astrid/...` inside `$D`. The old 1134 layout is intentionally not
reused: its `$T/src/LiveSceneClip.tsx` resolves `../../astrid` at `$T`'s
parent, while 1134 placed `$T/astrid`.

## Exact patch and compatibility

- Archive `remotion` into `$T/remotion` with the existing `--strip-components=1`.
- Archive `astrid/packs/rendering` into `$T` as the sibling source carrier.
- Accept only the known frozen `editor/live-scenes` or current
  `ui/threejs-live-editor` Root import pair.
- Check `SceneSurface.tsx`'s `./runtime` and `./diagnostics` edges and require
  the three direct closure files before `npm ci`.
- Preserve runtime name validation, new-runtime-only immutable guard, exact
  lock SHA check, Node 20 toolchain, normal `npm ci`, read-only output guard,
  and `request-runtime` unchanged.
- Keep the public runtime name and API unchanged. The existing
  `ASTRID_REMOTION_PROJECT_DIR` generated for a new `$N` becomes
  `/home/user/work/runtimes/$N/remotion`; generated suite/env references and
  the version-reporting CLI path are retargeted consistently. Existing old
  runtime directories and env files are not edited.

The source carrier is the smallest existing closed rendering-pack archive that
contains both the frozen d0a path and current Main/integration's renamed path;
there is no source factory, resolver alias, import rewrite, symlink escape, or
generic dependency crawler.

## Source-only proof

Fixture:

`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/vw-m4-runtime-layout-proposal-correction-1144-source-fixture.mjs`

It uses `path.resolve` from the actual final `LiveSceneClip.tsx` path, follows
the imported `SceneSurface`, then follows `SceneSurface`'s `./runtime` and
`./diagnostics` imports. Shell `git archive` prepares only the selected
`remotion/` and `astrid/packs/rendering/` source trees; no dependency graph is
copied.

The fixture passed for both source layouts:

- d0a `d0a5072bbe7b7ce9489f43aa0a81027ec400343b`: old1134 **FAIL as expected**;
  corrected nested **PASS** through `editor/live-scenes`.
- current Main/integration `1a50cf3f30398500e9f1ccf0b94d59fe7a8bdb3f`:
  old1134 **FAIL as expected**; corrected nested **PASS** through
  `ui/threejs-live-editor`.

The final fixture root was created and recorded as
`/tmp/vw-m4-runtime-layout-1144-fixture.5tCgTE`, checked by exact `realpath`,
and removed by exact path only. The patch-check root was likewise
`/tmp/vw-m4-runtime-layout-1144-check.EkS9te`.

## Required independent custody review

Before the lead installs or queues this proposal, an independent reviewer must
confirm the exact current `bin/make-runtime`, env template, suite source line,
and dispatcher contract; verify both archives come from the same Agent SHA;
verify the nested relative imports and three-file closure with the fixture;
verify a disposable new runtime would use `$D/remotion` for its generated env,
suite, lock, and in-project CLI paths; and byte-compare all old immutable
runtimes/env files before and after. Any change to source scope, env binding,
runtime name/API, or guard behavior requires a new review.

## Tests and limits

Passed: patch dry-run/apply in a private task-owned copy, `bash -n` on the
patched builder, Node syntax check for the fixture, source-only d0a/current
layout proof, and `git diff --check`.

Not run: npm install/ci, build, full graph/source copy, browser/helper,
Runtime/server/socket/central/physical/render proof, and full suite. No test
suite was applicable to this unapplied proposal.

The rejected 1134 patch/report remain untouched as history.
