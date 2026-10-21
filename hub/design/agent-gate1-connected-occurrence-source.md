# Agent Gate1 connected occurrence/shared-source evidence

## Scope

This is the staged Agent candidate for Main `6efc81500a0e0688c2bb41e736503f0fc3e04abb` with Runtime `95bd` (`/home/user/work/wt/rt-pin-95bd3c5f`). It covers one equivalent occurrence move through Python, CLI, and NativeSheet on the existing `/v1` Runtime door.

The test extends `tests/editing_conformance/test_native_sheet_current_runtime.py` and reuses the existing App three-products closure from `app_closure()`. Setup ingests private copies of every referenced `media_id` and `object_id`, then accepts the closure through the existing trusted real-Runtime seed helper. No public schema field, endpoint, adoption path, or framework was added.

## Proven semantics

- Target: `occurrence:f2-occurrence/clip:f2-agent-clip`, moved to `on=9`.
- Frontends: `TimelineSession.move`, `astrid edit --clip`, and `NativeSheet.export(...).preview/apply` all produce the same `clip.move` command and one Runtime commit.
- Shared-shot ownership: the moved occurrence receives the normal materialized target shot required for an occurrence-owned edit; `occurrence:shared-sibling` remains on the original `shot-shared` source and its complete row/source pin is unchanged.
- Source/transcript retention: the accepted `move.images` dependency pins the original shot, revision, and internal-timeline revision. The materialized target retains the original `voiceover` text binding (`hello`), and this survives Runtime restart/reload. Undo restores the original source pin; redo restores the exact accepted canonical document.
- Unknown data: the target’s existing `app.f2Opaque` namespace and the neighboring `f2-agent-clear-clip` row remain intact. The move’s normal `app.astrid` timing metadata is allowed by the existing command semantics.
- Timing ownership: at 30 fps, the moved clip owns `[270, 360)`, including frame 359 and excluding frame 360.
- Acceptance: the exact command, accepted response, receipt/history dependency, reload, inverse, and redo are checked for all three frontends. The retired `publish_parent_composition` path is monkeypatched to fail, so a passing case demonstrates the connected EditCommand path.

## Central evidence

Named suite added to `scratchpad/orch/tests/suites.conf`:
`gate1-connected-occurrence-source-main95bd` with the explicit Runtime95bd, Node20, and Main95bd environment.

Final central run:

```text
R=$(.../scratchpad/orch/bin/request-test agt-m2-gate1-connected-occurrence-source gate1-connected-occurrence-source-main95bd) && .../scratchpad/orch/bin/wait-test "$R"
4 passed in 17.67s
```

The four cases are the three frontend parameters plus the existing after-V2/restart retained-pin control. This is staged candidate evidence, not public integration qualification; no full, browser, or render suite was run.

