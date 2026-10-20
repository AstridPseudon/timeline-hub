# Public12 scene source-carry qualification

## Verdict

**PASS for bounded direct source/scene compatibility on current Agent**
`de62afbbb44ff261ab2b0366141208fccddd3580`.

The worktree is unchanged and clean. The exact immutable Composition 0.0.12
artifact was tested through a private overlay; no package, lockfile, pin, or
repository source was changed. This is evidence for the current Agent unit and
the eventual Agent/consumer12 pair, not owner adoption or a cross-product gate.

## Immutable artifact and overlay

- Artifact: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-release12/artifacts/banodoco-timeline-composition-0.0.12.tgz`
- SHA-256: `0a7b61529099ce994f807c6d7b1078303a09e7c0219144cc4b07467977f0f1a3`
- Size: 58,444 bytes; manifest: 77 members
- The tar member set matches the immutable 77-file manifest, and every
  extracted member byte matches the archive. Details and per-member hashes:
  [handoff-vw-m3-scene-carry-public12-proof-hashes.json](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-vw-m3-scene-carry-public12-proof-hashes.json)
- The private overlay used a real `@banodoco` package directory and real
  `@remotion` scope directory; peer leaves were read-only links to the existing
  host peer graph. No shared dependency was written.

Shared dependency manifests were captured before and after testing and are
identical: 35,618 entries under `/home/user/work/app/node_modules` and 23,132
under `/home/user/work/wt/vw-m3-scene-host-plumbing/remotion/node_modules`.

- [before manifest](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-vw-m3-scene-carry-public12-proof-shared-before.json)
- [after manifest](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-vw-m3-scene-carry-public12-proof-shared-after.json)

## API/theme checks

[Package command and output](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-vw-m3-scene-carry-public12-proof-package-tests.sh)
— **PASS**. The extracted package reports version `0.0.12`; root and all
published subpaths import successfully, including evaluation, theme-api,
generated registries, registries, and package-json. The full public
`DEFAULT_THEME` object equals Agent’s current `BUILTIN_DEFAULT_THEME` exactly:
navy `#050814`, Arial/cyan, full sizes/weights/line-height/fade/canvas. An
explicit owner theme with id, background, heading family, and 640x360/24fps
canvas remains intact through `toRuntimeTheme`.

No fixture/default update is needed: the tested public12 default and current
Agent default are equal. The current worktree’s existing Remotion pin remains
`file:artifacts/banodoco-timeline-composition-0.0.10.tgz`; public12 was supplied
only through the test-only artifact override, as required.

## Tests

- [source and scene command](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-vw-m3-scene-carry-public12-proof-source-tests.sh)
  — `test_scene_source_carry.py` plus `test_capture_scene_labels.py`: **79
  passed in 17.28s**. This includes the native public Composition bridge and
  transport parameters against the exact public12 archive. Native preparation
  and scene query are real; runtime-status admission is test-doubled.
- [neighbor command](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-vw-m3-scene-carry-public12-proof-neighbors.sh)
  — neighboring rendering/filmstrip tests: **125 passed, 3 deselected**;
  four executor lifecycle nodeids: **7 passed**; targeted Ruff: **all checks
  passed**. The three deselected cases require rendering fixtures and were not
  weakened or reclassified.
- `git diff --check` — **PASS**.
- `git diff --exit-code de62afbbb --` and `git status --porcelain` — **PASS**;
  no source or repository files changed.

## Boundaries

Runtime admission remains doubled. The capture backend writes synthetic PNGs;
this does not certify host capture, rendered pixels, audio, browser behavior,
transport parity, or Gate 6. No full suite, browser, live socket, renderer,
install, network, Runtime service, or owner consumer adoption was run.

The graph-repair hold remains in force. Next step is owner-controlled adoption
of the immutable public12 artifact in the matching consumer cohort, followed by
the separately authorized Runtime/host/capture/parity qualification.
