# Filmstrip inventory owner packet

## Decision requested from Viewing

Apply the accompanying unapplied patch if the source owner accepts the
smallest cohesive extraction. It moves the complete attempt-local audio-cache
unit out of `filmstrip_execution.py` without changing any cache key, file
layout, retention limit, call order, or returned value.

## Evidence

- Main (`main:a9a3550c`) has 2,015 lines in
  `filmstrip_execution.py`; its rationale entry records 2,015.
- Current integration (`HEAD:04fdd642`) has 2,072 lines. The unchanged
  tolerance is 50, so the current drift is 57 lines, or 7 beyond tolerance.
- Main/current AST comparison found one added top-level wrapper,
  `_execute_scene_only`, and five changed cohesive functions:
  `execute_input_only`, `_render_input_projection_png`, `_render_paired_rows`,
  `_compose_synchronized_surface`, and `execute_filmstrip`.
- The current additions are cross-cutting provenance/scene-dispatch plumbing
  inside those functions. Extracting only those additions would split their
  output construction and dispatch responsibilities, so it is not proposed.
- The existing audio unit is contiguous and self-contained: `_audio_cache_path`
  (945–950), `_cached_audio` (953–961), and `_store_audio_cache` (964–970).
  The two public call sites are both in `execute_filmstrip` (1818 and 1822);
  there are no other consumers.

## Proposed patch

`agent-filmstrip-inventory-owner-proposal.patch`:

- Adds private `timeline_visualize/_audio_cache.py` with the three unchanged
  helpers.
- Imports the two callers from that module and removes the old 28 physical
  lines from `filmstrip_execution.py`.
- Declares the new implementation in the existing rendering pack resource
  closure.
- Updates the rationale entry to the post-extraction count, 2,045 lines. That
  is 845 lines over the 1,200-line threshold and remains within the fixed 50-line
  tolerance. No threshold, waiver, or behavior exception is introduced.

The patch is deliberately unapplied; this worker did not modify the product
file or rationale.

## Verification

- `python3` read-only AST/line check comparing `main` and current: PASS.
- `git apply --check /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/agent-filmstrip-inventory-owner-proposal.patch`: PASS.
- `git apply --numstat .../agent-filmstrip-inventory-owner-proposal.patch`:
  `34 0` new helper, `1 28` execution-file import/removal, `2 0` pack resource,
  `1 1` rationale count/description.
- No six-node rerun, full suite, renderer run, or behavior test was run, per
  task instruction; the packet relies on static AST/line checks only.

## Next step

Viewing should review/apply the patch on its source-owned branch, then run the
structure-contract node and the focused filmstrip neighbors there.
