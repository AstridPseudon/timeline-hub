# M2 free multi-clip move: Runtime proof

Status: reviewed Agent/runtime acceptance proof; App TypeScript integration remains out of scope for this change.

The real-daemon acceptance test is [test_commit_runtime_free_move_set.py](../../tests/editing_conformance/test_commit_runtime_free_move_set.py). It seeds a normal authenticated Runtime project through registered `track.create` and `clip.add` commands, then proves the reviewed App geometry:

- `V1`, `V2`, `V3`; `clip-1` -> `V2 @ 1`, hold `2`; `clip-2` -> `V3 @ 3`, hold `2`;
- ordered selection `clip-2`, `clip-1`, with no `pinnedShotGroups`;
- `track.create(V3)` plus the sealed `clip.move-set` in one `/v1` publication;
- exact canonical reload, accepted history command captures, and opaque clip/app fields;
- durable lost-ACK retry after Runtime restart with the same request body, idempotency key, and receipt;
- guarded undo (moves restored before the created track is removed), redo with the same authored IDs, and refusal when a later clip depends on `V3`;
- disjoint-lane server rebase, and refusal after relevant lane-entry membership changes A -> B -> A.

This is evidence for the Python/Runtime command contract only. It does not claim an official generated TypeScript consumer or App artifact: the App-side gesture producer, generated-client consumption, and shipped artifact scope still require their own integration proof.
