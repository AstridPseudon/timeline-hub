The guarded completion auto-placement builder (step 1) is done and green under `tests/editing_conformance`. It covers image and video with the anchor-after rule and the absent-anchor fallback. It is for exact occurrence bindings only. Parent-owned completion is not covered because this stack has no parent media birth. I wrote the commit message and `DONE`.

## What I built
- **Builder:** `auto_place_completion(bundle, owner, clip_id, media, *, ownership, verified_media, anchor=None, duration=None)` in `astrid/sdk/timeline/native_auto_placement.py`. It is pure and returns `{'commands': [one ordinary EditCommand], 'capture': {...}}`.
- **Image:** emits `placement.create` with a 5 s hold, whatever `duration` the caller passes.
- **Video:** emits `occurrence.add-media` with `from 0`, `to d`, `hold d`, `speed 1`. `d` is the supplied duration or 5 s, and it may not exceed the verified media duration.
- **Start rule:** half-open, in frames at the rational fps, using the compositor's own end-frame function.
  - Anchor present: the new item starts at the anchor's end frame.
  - Anchor absent (no id, or no such clip in the occurrence): it starts at the occurrence lane's end, or at the occurrence start if the lane is empty.
  - Anchor present but with unusable timing: it refuses and never falls back.
- **Selected variant:** the new clip is bound to the exact five-field pin passed in. The gallery primary and the latest variant are never consulted.
- **Replay and inverse:** the start is written into the command as a literal, so replay and inverse are exact and resolution is never re-run.
- **Design note:** `design/m2-auto-placement.md`, including the step 2 needs.

## Evidence
- **Command:** `bin/request-test agt-m2-auto-placement-completion targeted --files "tests/editing_conformance"`.
- **Result:** 1305 passed, 4 skipped, 5 xfailed. The skips and xfails were already there.
- **New tests:** `test_recipe_m2_auto_placement.py` (also run earlier on its own, where the only failures were the golden tests awaiting their fixture) and the golden `fixtures/recipe_m2_auto_placement.json`.
- **What they cover:** image and video, anchor present and absent, empty lane, defaults and over-long video duration, exact variant binding, shared/parent/unbound refusal, unusable anchor timing, anchor moved and deleted during replay, guarded undo/redo, and provider undo/redo.
- **Not run:** lint, because I could not run Python directly in the sandbox.
- **Golden scope:** it holds the commands, the capture and the created child row. Authoritative records are checked by the replay test, not stored.

## Decisions and gaps
- **Anchor moved after capture:** replay keeps the recorded start. This is not a conflict, because there is no read-only guard op. A no-op `placement.move` would write `fixed_start` intents. Guarding it needs a schema change.
- **Anchor deleted after capture:** replay refuses through the existing membership guard. A rebuild then falls back to the lane end and records `absent`.
- **Video shared-owner check:** `occurrence.add-media` does not re-check exclusive ownership at replay, so the builder enforces it at capture only. Adding a one-line `_exclusive` check to `add_media` would close this but changes that op's existing goldens. I left that for the owner.
- **Parent-owned completion:** it needs `clip.add-media`, which this stack lacks.
- **Step 2 needs:** the list is in the design note. It covers the shared 4 s hold, shared append, lane inheritance, start-frame shift, pool membership, `keepAsPooled`, the Runtime schema pair, and the App's durable continuation.

I moved a temporary dump test out of the worktree into the scratchpad because `rm` was denied. It is not in the diff.
