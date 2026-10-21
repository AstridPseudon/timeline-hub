# Composition 0.0.14 release input — HOLD

This is a preparation handoff, not a qualified release. No 0.0.14 archive or
hash exists yet.

The release source is the reviewed current Composition tree:

- commit `7bb54bbd64107e5090643ecca1e4d33164173e85`
- tree `20467712e66dbadff4d562c0d5baae22b8c077a7`
- package version `0.0.14`
- normal `CHANGELOG.md` release line already present
- independent producer755 review: APPROVE
- source full: 84 passed, 0 failed

Packing is held until the sole public13 executor has a terminal result proving
an actual physical export/browser attempt. The latest coordinator update says
the executor remains blocked on App integration ancestry; no grant, marker,
render, or capture has been consumed. Public13 remains immutable archive SHA
`9412ae25c306d5118241f4d631e8eecc6eef9b2fb5a98302d40938e9f6d54738`.

The guarded command is at:

`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m4-release14-packed-0211/COMMAND`

After the hold clears, it will run the normal build, focused public Scene /
geometry / opacity / animation / registry tests, strict NodeNext declaration
build, package smoke, and source/tree drift checks. It will write the new
archive only under the worker's private `release-output` directory and record
its exact SHA-256 and member manifest.

Consumer requirements after independent packed-byte review: Agent and App
must adopt one coordinated immutable 0.0.14 archive/hash pair. Runtime 0.0.14
is a separate pin and is not activated by this packing task. Packing changes no
live callers.
