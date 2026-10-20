# App ordinary014 current-cohort native-None qualification

## Result

Private branch qualification passed. No release, adoption, activation, integration pin, or Runtime source change was made.

Central suite: `e2e-app014-native-none-current-cohort`

Result: **2 passed**, one worker, 1.7m browser duration; the wrapper completed its exact source/artifact postflight. The two test IDs were:

- `M2 native None single: ordinary default crossfade clears raw mirrors, reloads, retries exactly after restart and undoes through Runtime`
- `M2 native None bulk: one original-basis atomic clear preserves unknown revision and opaque data; real conflict retains the whole draft`

Central result directory: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/tests/app-m2-ordinary014-current-cohort-native-gate-e2e-app014-native-none-current-cohort-1020182205-15702/`.

## Exact source/cohort

- App committed final staged branch: `67e26ef349b5a9e3a08d67acab0ae37a5cfda98f`, committed tree `604f6523a37c4d997afef02dab43421433b175ec`; the central snapshot required parent `67e26ef…`, so it did not run the stale `ed9728e…` base.
- Final central App snapshot tree: `5f1ab551b4323f107abb1c87196909630c78e22a`; central snapshot source commit printed by the lane: `087f4b231b6fcbe3a7cd11323968daf233c1ebd1`.
- Agent: `3c4f6de4fa777323b3386c01c7266b619b86af6d`, tree `aaf49eca6c2b119b21df1d89b0e56df5d1c60f9c`; public12 archive SHA-256 `0a7b61529099ce994f807c6d7b1078303a09e7c0219144cc4b07467977f0f1a3`, 77 regular files.
- Runtime server: `202074110717146fc7f08af2306a8dd7f695b0b1`, tree `ee39286bd0eb27d4075074cc4785d6d15e33f243`.
- Immutable Runtime producer: `a0dca16975dfe8f5e762703b99d9791a16cf7fd7`, tree `4b7dd0fe44be973c344bab3de568eaf0bdd28476`.
- App public13 archive SHA-256 `9412ae25c306d5118241f4d631e8eecc6eef9b2fb5a98302d40938e9f6d54738`, 77 regular files; unchanged.
- App/Agent lock source is producer `a0dca169…`, package `0.2.14`, producer artifact `sha256:f021e7714c1b40011b69ba624d288c217749d58013b8adf0352d283854f20fa0`.
- Producer manifest is `ecda762ebe682f266395161af055921c3db33ee9914fb00860626e7e4852d815`; all 75 manifest paths and hashes were checked.
- Raw command schema is `6ba7b51e9518e7fb08b27ad5b7225855276b657d0adebf704dd853f699768f2d`, with 55 definitions and 29 operation branches; generated schema is `ce3781c282564b650890456f6c257f3faabe2de3898a84363fecd47e48b30d59`.

## Changes and limits

Added the strict central wrapper and suite registration, carried the current staged App clip-scalar capture/gesture and Properties Panel wiring, preserved literal opaque transition keys through App cloning/outbox and the browser outbox inspection helper, and added the reviewed two-case native lane. Existing capture/outbox/lost-ACK/reload/Runtime-restart/undo/409 draft/legacy assertions remain active. No producer overlay or Runtime edit was used.

Local checks: `node --check scripts/testing/current014-native-none.mjs` and `git diff --check` passed. No full suite, project TypeScript check, install, or local browser run was performed.

## Runtime cd0 boundary / peer request

The required Runtime cd0 strict marker transition is not present in `202074…`. Exact evidence from `runtime-ordinary202-final-handoff.md`: diff `9cde47523803607f4dfd8d39885a9526de4ce8e7..202074…` contains only `tests/test_timeline_clip_replacement.py`; its carried test blob remains `183f14dbe64466c9a8c7aec5b34850da9272f107`, and the current public-schema imperative `pytest.xfail` transition remains. Runtime must add/carry the final test-only cd0 strict-marker transition, retain the qualified acceptance body and positive assertions, and requalify this exact Agent/Runtime cohort before integration adoption. This App gate does not claim that subgate passed.
