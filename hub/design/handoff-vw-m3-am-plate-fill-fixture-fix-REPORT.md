# AM snap-plate fill fixture migration

## Result

Fixed the independent-review rejection from `handoff-vw-m3-am-plate-final-review`.
The stale neighbor no longer inspects component source locations. Fill and draw
behavior is asserted through the registered component's existing SSR test:
assetless fill, token resolution, image drawing, and explicit
`background`-over-`fill` precedence are checked while the existing 10 variants ×
9 frames hashes remain pinned.

The normal `astrid/packs/rendering/elements/catalog.ts` projection was regenerated
with `scripts/gen_element_catalog.py`; only the AM plate revision changed.
No product capability, generator code, root artifact policy, crop/outer-animation
unknown handling, or D09 scope changed.

## Red before green

- `tests/packs/test_am_snap_plate_fill.py`: **1 failed, 2 passed**. The failure
  was the extracted `FILL_TOKENS`/background logic still being required in
  `component.tsx`.
- `scripts/gen_element_catalog.py --check`: **exit 1**, catalog stale; only
  the AM plate revision differed.

## Green after

- Fill neighbor: **2 passed**.
- Claimed targeted set (the c35 direct tests plus 94 neighbors): **108 passed
  in 31.60s**.
- Registered-component SSR test (10 variants × 9 frames): **1 passed in
  3.99s**; all existing hashes unchanged, with the added explicit precedence
  and drawing assertions passing.
- Targeted strict TypeScript: **exit 0**.
- Ruff on touched tests: **exit 0**.
- `git diff --check`: **exit 0**.
- `scripts/gen_element_catalog.py --check`: **exit 0**.

## Exact commands

See the companion command log at
`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-vw-m3-am-plate-fill-fixture-fix-REPORT/commands.txt`.

## Decisions and limits

- Removed the obsolete source-string test rather than replacing it with an
  import/string check. The registered public component SSR test is the behavior
  proof for the extracted helper and retains the original fill precedence and
  drawing expectations.
- Refreshed the Agent-owned normal catalog artifact because its normal freshness
  command required it. Any separate normal effect-registry/host-map lifecycle
  refresh remains the Agent owner's gate responsibility; no installed
  Composition artifact was touched.
- No full suite, browser, local renderer, socket/listener, network, install, or
  central test-service run was performed. This is not a parity, current-API,
  crop/outer-animation qualification, gate-6, or D09 completion claim.
