# App cap8488 / Composition public13 paired gate

## Verdict

**APPROVE the bounded paired gate** for App commit `8488f9c1c2e3eafd924720e5bcd49a950798ffed` with the immutable Composition 0.0.13 leaf overlay.

This is a consumer-correction qualification only. It makes no App product edit,
root change, dependency pin change, cohort change, PCM13 decision, or Track
Inspector change. It does not claim actual Player pixels, actual render output,
normal-13 adoption, or product-wide parity.

## Immutable public13 input

- Artifact: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/artifacts/banodoco-timeline-composition-0.0.13.tgz`
- SHA-256: `9412ae25c306d5118241f4d631e8eecc6eef9b2fb5a98302d40938e9f6d54738`
- Archive members: `77`; exact match to `handoff-vw-m3-release13-member-manifest.txt`
- Archive package version: `0.0.13`

The private overlay used a real `@banodoco` scope directory and one real
Composition leaf at `/tmp/vw-m3-cap848-public13.Ve1XoR/...`; all other package
leaves were read-only links to the existing shared graph. The shared App graph
was not modified and remained Composition `0.0.12`.

## Evidence

- Public 0.0.13 root/evaluator probe: **PASS**. Both stored-cap cases exercised
  frames 105, 119, and 120: 4000 ms yielded opacity `0.5`, active at 105/119,
  inactive at 120; 4500 ms yielded opacity `1`, active at all three frames.
  Public root draw durations were 120 and 135 respectively.
- Public13 App consumer lane: **4 files, 35 tests passed**. This covers the
  stored 4000/4500 atomic delivery, flattened-config identity, still boundary,
  Player vector/extent/provenance delivery, and canonical render-bound helper.
- Client-route render lane: **5 passed**, with 62 tests excluded by the exact
  `client renderer` name filter. This was the existing mocked client-render
  route lane; no actual render ran.
- ES2020 App project check against the private public13 declarations:
  **PASS, exit 0**, `tsc --noEmit`.

## Pre/post and limits

The App worktree was clean before and after the gate. `git diff --check
HEAD^ HEAD` passed. The correction commit's 11 files are consumer/test files
only; no `package.json`, lockfile, root, or pin file changed.

Not run: full suite, 304-case matrix, browser, actual Player capture, actual
render/export, network, install, live socket, normal-13 adoption, PCM13 work,
or Track Inspector work. Existing public12 final-review evidence remains
historical and was not relabeled as public13 evidence.

## Handoff

The exact commands and outputs are in the paired `-COMMAND.md` file beside this
report. Branch is ready after this gate, subject to the orchestrator's merge
queue and the separately owned PCM13/Track Inspector work.
