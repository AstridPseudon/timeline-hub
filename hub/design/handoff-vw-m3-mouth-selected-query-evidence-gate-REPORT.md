# D09a selected-query evidence gate

## Decision

**APPROVE for the caller-migration prerequisite only.** The completed
selected-cut public-query evidence is real and correctly selected. This does
not approve migrating or deleting the private mouth caller, crop/statistics
path, or cache fallback.

## Verified evidence

- The central result is tied to Agent commit `d051bee072cef25e706b060e3318a80aa104f29c`
  and tree `03f5f61d81bd88136886635454bca6deac60fa24`; the recorded result is
  **1 passed in 3.67s, 0 skips, 0 deselections**.
- The registered suite command uses the exact node
  `tests/packs/rendering/test_presenter_selected_cut_aggregate.py::test_actual_selected_cut_aggregate`
  with both `-o addopts= -p no:cacheprovider` and `-m integration`. The prior
  malformed request and 24-deselection run are not treated as evidence.
- The fixture pins Node `v20.19.4` (SHA256
  `43d6cf63f2a460b463eba6b19df5e9a259771c56f11b5130e04178a15bb99490`), the
  public12 tarball (SHA256
  `0a7b61529099ce994f807c6d7b1078303a09e7c0219144cc4b07467977f0f1a3`, 77
  members), and the read-only f816 peer graph. It checks resolved module
  origins/versions, discovers the `pack:astrid_motion` owner, and verifies the
  owner root and package/peer bytes before and after the query.
- The Node query actually uses the registered public `querySceneFrame` path and
  the component's `motionAt`, `mouthStateAt`, and `MOUTH_LEVEL` codebook. It
  requests exactly `[0, 3, 4, 5]`, asserts each returned `contentFrame`, and
  asserts the public motion/state rows.
- The query's changed-state, changed-codebook, and omitted-selection controls
  are executed and required by the Python test. The ordinary private caller is
  compared on the same retained props, 30 fps clock, and exact frame keys via
  `model.mouth_state`; no fixture certificate or original-runtime claim is
  used.
- The commit changes only the two test modules. Existing private callers,
  `mouth_box` crop/statistics, thresholds, and cache fallback remain present;
  no production caller migration or deletion occurred.

## Commands and results

- Read-only source/hash verification against `d051bee…`: **passed** (tree,
  selected-test SHA, selected-query SHA, artifact SHA, marker/options, exact
  selected keys, negative-control assertions, and two-file diff scope).
- Central test-service suite
  `integration-viewing-mouth-selected-cut-public-query`: **1 passed in 3.67s**;
  this was the already completed run and was not repeated.
- Worker local exact public test: **1 passed in 3.70s**.
- Worker static/pure controls: AST parse, Node `--check`, `git diff --check`,
  and neighboring controls: **3 passed in 0.40s**.

No central/full/browser/render/socket/network/install run was repeated. The
remaining prerequisite for any migration is a trusted public source/root/
component-zero join for every real private caller, including cache-only paths;
the separate crop-equivalence and actual-pixel qualification remain open.
