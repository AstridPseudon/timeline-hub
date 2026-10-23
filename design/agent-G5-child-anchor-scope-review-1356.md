# G5 child-anchor scope review (Sol1345)

## Result

**PASS — scope finding only.** The source diagnosis is confirmed: the old
`Clip.nudge`/`Clip.on` writer genuinely supports a child cut whose `on`
value is a word moment, but the current registered `clip.anchor` carrier is a
parent-only native operation. This is not child-helper completion, a product
fix, a new API approval, or a P1 green result.

The missing boundary is an authenticated child-target capture/adapter
contract. No existing typed carrier was found that can supply the retained
child target's exact transcript pin, stable word choice, ownership, compiler
input, and inverse provenance.

## Inputs and provenance

- Agent base and Sol1345: `74b92b2a903ff988489b6dfaa2add01e848bdb1a`, branch
  `tl/agt-G5-anchored-helper-fixture-1317` / `tl/agt-G5-child-anchor-sol-1345`.
- Sol design: `design/agent-G5-child-anchor-sol-1345.md`.
- Flat packet SHA-256: `b07035a8594e0240c6e05c287eb7d6f83bb4afe0527833f6c992553a1f3f1726`.
- Escalation: `agent-20261023T1356-child-anchor-carrier-scope.md`.
- Runtime source authority remains the qualified `rt-pin-8592822f`; it is not
  the blocker.

The packet's two Runtime projects remain isolated: genuine capture
`af4f4b3d2f0c44f7ba809751b924e543`; retained positive
`bd69f5cef3e44108b4023ab9cd4ff8ac`. The positive receives no parent-fixture
credit and no transcript pin is transferred between projects.

## Exact old/new boundary

### OLD: child writer exists in the mutable helper

- `astrid/sdk/timeline/model.py:259-291` stores the authored moment in
  `Clip.on`, resolves it, and calls `retime`; `:356-371` makes `nudge`
  preserve an existing word moment by adding an offset.
- `astrid/sdk/timeline/reflow.py:352-390` resolves cut starts and child clip
  timing during `retime`; `:562-615` performs legacy word lookup and nearest
  occurrence pinning in mutable evaluator state.
- Therefore the retained topology/body is a real old behavior: target
  `occ-film/clip:inside`, cut `c2`, `on='"second"'`, `at=4.6`, followed by
  the same-child `Clip.nudge`/save/restart path.

### NEW: current native carrier is parent-only and requires typed capture

- The current command union requires `select` to match
  `^parent/clip:(?!.*::)[^/]+$` for `clip.anchor`
  (`tests/fixtures/current-union-command-schemas/agent-word-caea687e.json:1465-1485`).
- `native_word_anchor.py:286-287` repeats that refusal; `:230-234` refuses
  authored child `word_anchors`; `:243-250` extracts bindings only from
  `bundle['parent']['clips']`; `:131-133` constructs each
  `WordBinding.target` as `('parent', '', clip_id)`.
- `native_checkout.py:348-377` exposes the existing structured carrier only
  when the selected clip is parent-owned and refuses text-only/mixed values.
- The genuine control proves the carrier can hold an exact transcript pin,
  source occurrence/clip, and stable `word_ids`, but its captured target is
  `('parent', '', 'anchor-carrier')`, not the desired child
  `('occ-film', 'film', 'inside')`.

The pure kernel does accept an exact child-shaped `WordBinding.target`
(`compiler.py:58-79`, and `TimingInputs` requires captured `WordBinding`
objects at `:90-99`). That is a capability of a caller-supplied input, not a
frontend binding/capture path. It never discovers a word from generic physical
addressing or from the text `"second"`.

## Existing typed-carrier audit

No authorized existing carrier was missed:

1. The old helper has a mutable text lookup and nearest-word fallback, not a
   persisted exact `DocumentPin` plus stable word selection.
2. The current `clip.anchor` carrier has the exact typed choice and dependency
   records, but its target selector, handler, capture adapter, and compiler
   adapter are parent-only.
3. `doc.patch`/`emitter.py` is lossless physical addressing only; the emitter
   explicitly does not guess semantic commands or select words. It cannot mint
   transcript authority or convert a physical child address into semantic word
   choice.
4. `journal.py:113-169` observes the helper's consulted inputs and
   `:223-237` emits structural changes after the helper mutates the checkout.
   It has no captured child word binding to preserve.
5. Frozen R4 `compiler.py` and `transcript_binding.py` (read with `git show`
   from `origin/codex/handover-timeline-r4-20261019-candidate-sdk`) require an
   independently admitted frozen dependency and an explicit occurrence/word
   selection. That is a different frozen transcript format and cannot be
   transplanted or inferred into the current v1 carrier.

The packet's preflight attempted the actual child selector and received schema
refusal at `select`; its input remained unchanged. The source and desired
target are different physical sites even though they share the same internal
revision root, so this is not a same-site alias repair.

## Retained positive and fidelity

The original 13 function bodies/ASTs and the retained positive topology/body
were not changed. The retained request remains the original full-v2 shape:
exact scope/base pair; commands; label; step IDs/intents/tags/patches/
ordinals/reads; merge/read dependencies; idempotency key; dry-run/source/
rationale/group ID; and the accepted/merged canonical receipt fields,
bindings, dependencies, effects, history, undo steps, preview, required,
would-status, conflict/invalid code/path/head/hint/command fields. No
accepted or merged reply is fabricated for the invalid setup.

The Sol evidence records **3 PASS + 1 FAIL** acceptance evidence: the genuine
anchor and no-write controls pass, while the unchanged ["second"] positive
fails at `Cut setup` with `candidate.timing: missing exact word binding for
('occ-film', 'film', 'inside').on`. The 41 strict guard tests (29 + 12),
normal Ruff 2149/2149, private mypy 1912/1912, vendor/artifact checks, and
diff/integrity checks are reused from that exact packet/source provenance.

## Focused checks run for this review

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.:/home/user/work/wt/rt-pin-8592822f ASTRID_RUNTIME_CHECKOUT=/home/user/work/wt/rt-pin-8592822f /home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider tests/sdk/test_timing_compiler.py::test_binding_refusals_are_atomic_and_never_repair_by_same_text tests/sdk/test_timing_compiler.py::test_exact_binding_uses_selected_duplicate_word_and_preserves_authored_commands_and_clears tests/editing_conformance/test_commit_timing_validation.py::test_child_declarations_are_not_filtered_and_valid_relations_are_resolved
```

Result: **13 passed in 1.29s**.

Not run, as required: the original failed second-positive/full25,
native54/P1/P4, HTTP/browser/full/D17/58, or any product/runtime/schema/test/
generated/pin/contract/environment/dependency/guard change.

## Decision boundary / next step

The old writer behavior is real, but the current semantic carrier scope is
absent. Do not waive the child-declaration guard, substitute the parent
topology, transfer the parent binding, or make `doc.patch` infer a semantic
word. If the owner elects to retain this promised writer, a separate contract
decision must authorize caller-selected exact child binding input plus
authenticated ownership/fork, capture, compiler, inverse, and forged/stale/
foreign/ambiguous negatives. Until then this is **NO MERGE / G5 P1 NO-GO**.

