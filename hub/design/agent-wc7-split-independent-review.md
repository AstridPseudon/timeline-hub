# WC7 attached parent split independent data-loss review — APPROVE

Date: 2026-10-20T23:00:57Z

Reviewed exact target `tl/agt-m2-wc7-owned-parent-split` at `404422aa3`
(tree `d77ebacc3e216bd147e607f729c3284826451e95`) against its meta base
`b43cd9571`. The product delta is limited to the attached native checkout
publisher and its split coverage. I found no concrete data-loss or durable-
outbox counterexample. APPROVE.

## Review checks

- `AttachedClip.split(on, *, id=...)` is parent-only and documents `on` as
  absolute timeline seconds. The existing command schema requires a finite
  numeric `on` in seconds, and the native handler independently checks it is
  strictly inside `at .. at + clip_timeline_duration`; string/timecode and
  frame-like values do not enter this path.
- The real HTTP fixture uses the verified registry-backed source window
  `[0, 5.5]`, matching `hold=5.5`, with `speed=2`, and splits at timeline
  second `1`. The captured result is exact: the right row is `[from=2,
  to=5.5, hold=3.5, speed=2]`. Existing native split controls additionally
  cover exact source halves, half-open frame contact, literal `for`, fractional
  speed, and opaque data.
- Capture is owner-stable and read-backed: the command selects the parent clip
  collection, reads the exact parent clip and parent registry asset, reads
  dependency-bearing neighbor fields, binds `split.target`, records the
  original collection/order proof, and records one created ref. It does not
  capture a whole-timeline snapshot or refresh claims at publish/retry time.
- The caller supplies `right_id` once. The command stores that identity in
  `args` and `created`; `_queue` captures before the atomic outbox stage, and
  `_flush` seals the exact request body, rationale, key, and flight before
  transport. Reloaded publish validates the stored flight and does not recapture
  or allocate another ID. The focused test explicitly forbids `commands.execute`
  during retry; the central real-HTTP control verifies lost-ACK, restart,
  exact-body/key retry, stale rebase, and undo.
- Refusal is atomic. Unsupported neighbor transitions fail during command
  execution before `_stage` writes the outbox or exposes a new preview. The
  existing mixed-draft and basis-change controls keep pending edits and any
  existing flight intact; publication still requires exactly one publishable
  parent command.
- The inverse uses the recorded created row, authored writes, and collection
  insertion boundary. It restores both raw parent clip arrays to their exact
  original order/content, including opaque fields, removes only the created
  right row, and preserves the unrelated peer edit. The split test asserts all
  of these after reload/retry/undo.
- Outbox isolation remains bounded to the explicitly supplied session. The
  unchanged controls prove unrelated/global pending or in-flight state is not
  discovered or consumed, while detached and occurrence-scoped publication is
  held. Scope checks still include realm, actor, project, and timeline.

## Evidence

- Local socket-free decisive probe:

  ```text
  PYTHONPATH="$PWD" /home/user/work/venv-agent/bin/python -m pytest -q tests/sdk/test_timeline_owned_move_publish.py -k 'split' tests/editing_conformance/test_recipe_m2_clip_split.py
  82 passed, 9 deselected in 7.96s
  ```

- Exact-tree central HTTP lane already supplied by the worker/test service:
  `agt-m2-wc7-owned-parent-split-current-owned-parent-delete-http-1020225628-21843`,
  tree `d77ebacc3`, running the parent-delete and parent-split real HTTP
  controls: **2 passed in 23.06s**.
- Supplied candidate qualification: **91 focused tests passed**, plus Ruff and
  `git diff --check`; reused unchanged rather than rerun broadly.
- Local source diff check: `git diff --check b43cd9571..HEAD` — passed.
- No full suite, browser suite, or additional live-socket run was performed.

No product code was changed by this review. No blocker or REQUEST CHANGES
finding remains for this bounded attached-parent split slice.
