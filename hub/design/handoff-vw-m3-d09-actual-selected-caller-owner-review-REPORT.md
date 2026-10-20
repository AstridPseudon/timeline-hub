# Independent review: APPROVE — HELD

## Scope and lineage

Reviewed only the selected-cut caller candidate in Agent. The integration base
is `b43cd95717a5018940f5ffa4123d2db3ff34b8f0`; the exact candidate lineage is:

- `fa4904185caff54fcae4dccd6e2048b8c0294b29` — selected-cut public aggregate test join.
- `b153dd2f8994cfb43968739915545e4b8dd37b8b` — production caller hunk under review.

The delta from the integration base is four rendering files. No unrelated Main
endpoint diff is included.

## Production finding

`astrid/packs/rendering/actions/timeline_visualize/layers/builtin.py:512`
changes:

```python
box = model.mouth_box(presenter, 0)
```

to:

```python
box = None if public else model.mouth_box(presenter, 0)
```

This skips the private crop only when `_public_mouth_facts(...)` has already
accepted the exact selected frame series. The existing public crop conversion,
frame loop, missing-image adjacency behavior, denominator, and strict `> 0.02`
threshold remain unchanged. If public facts are unavailable, partial/default/
raw-invalid, mixed-mode, stale, missing, or forged, `public` is `None` and the
private path remains active.

## Custody review

The live caller consumes the same `ctx.shared` handoff produced by
`motion/sheet.py`; it does not call the test aggregate helper. That handoff is
published only when every requested key is present and every row is from one
evidence mode (`fresh_capture` or source-bound `cache`). `CaptureSceneLabels`
binds source identity, basis, projected addresses, exact frame, and successful
fresh PNG retention. The source-bound cache path additionally requires the
frozen source and owner-integrity checks; the default cache remains PNG-only.
The caller then checks basis/fps, answer frame and dimensions, presenter ID,
address, exactly one presenter layer, known finite public ROI, and a valid
public mouth state. No second evaluator or guessed clock/hash/ROI is used by
the production hunk.

## Evidence

- Final bounded Agent lane: **40 passed in 11.31s** using pinned Node
  20.19.4, Composition 0.0.13, and the read-only viewing13 peer root.
- Prior source-bound cache qualification was reused: **97 passed** for cache /
  source-carry controls and **40 passed** for this selected-cut plus direct
  presenter neighbors. Its planted stale/forged, changed-source, mixed-batch,
  and default PNG-only controls remain green.
- AST parsing, Node syntax check, and `git diff --check`: passed.
- Worktree status: clean; no source edits, merge request, install, network,
  browser, full suite, or render was performed.

## Hold and next step

No REQUESTCHANGES finding. This is an approval of the source-only candidate,
held from activation. No actual managed Scene proof, physical four-still
replay, activation, or private-crop deletion was authorized or claimed. The
next step is the separately authorized managed/physical prerequisite gate;
until then this hunk must not be treated as Gate 6 completion.
