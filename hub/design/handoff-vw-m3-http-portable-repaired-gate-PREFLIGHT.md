# Normal PCM HTTP repaired-gate preflight

Pre-central verification for the repaired borrowed project at:

`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-pcm-http-portable-test/project`

The frozen candidate used for this check is the checked-in public-12
Composition artifact in the assigned Agent tree:

`remotion/artifacts/banodoco-timeline-composition-0.0.12.tgz`

Its SHA-256 is
`0a7b61529099ce994f807c6d7b1078303a09e7c0219144cc4b07467977f0f1a3`.

## Byte checks

- All 77 regular archive members were compared against the borrowed
  `node_modules/@banodoco/timeline-composition` extraction: PASS.
- `normal-audio-sources.mjs`: SHA-256
  `dc260d6980f3fc6ff0340b364d810cd4310cc3c663db836ab9c84f6ee5dd14e4`;
  borrowed copy byte-equal: PASS.
- `attempt-envelope-pcm.mjs`: SHA-256
  `db7bc06d2b3c9efecac015d59d965ef4dfa718e13f1ef303f190c3831bc95719`;
  borrowed copy byte-equal: PASS.
- `compiled-audio-source-clock.mjs`: SHA-256
  `6ce210e91547d8bca901dc23fe3b06eae0d463fa18d6e1cb79d23494f5145ffc`;
  borrowed copy byte-equal: PASS.

The frozen R4 SDK/Composition refs do not contain these public-12 helper
paths; they are not cited as the source of this candidate. The exact
checked-in artifact and helper hashes above are the candidate identity used
for this verification.

## Socket-free module import

Using Node 20.19.4 from the borrowed project, actual ESM imports of all three
helpers passed and exported the expected functions. Import created zero new
`Socket` or `Server` handles relative to the process baseline: PASS.

No project files, shared dependencies, caches, or product sources were
modified by this preflight.
