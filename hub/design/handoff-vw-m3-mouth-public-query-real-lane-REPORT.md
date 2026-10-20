# D09a selected-cut public-query real lane

## Result

Actually qualified the existing test-only selected-cut public aggregate through
the normal registered presenter query fixture. The lane now selects only
`test_actual_selected_cut_aggregate` with explicit `-o addopts= -m integration`,
so the repository default marker exclusion cannot silently deselect it. The
fixture uses the retained Node 20.19.4 binary, public12 package, and read-only
f816 peer tree.

The public Node query covers exactly retained selected keys `[0, 3, 4, 5]` and
executes the changed-state, changed-codebook, and omitted-selection controls.
The Python positive compares the public presenter states with the existing
ordinary `model.mouth_state` caller. No synthetic samples, omitted frames, or
Node substitute were used.

## Evidence

- Central named integration lane: **1 passed in 3.67s**, zero skips and zero
  deselections; result directory is
  `tests/vw-m3-mouth-public-query-real-lane-integration-viewing-mouth-selected-cut-public-query-1020151841-32447/`.
- Local exact public test: **1 passed in 3.70s**.
- Local pure/static controls: Python AST parse, Node `--check`, `git diff
  --check`, and **3 passed in 0.40s** for the existing mouth-state and cut
  selector controls.
- The service command is registered exactly once in `orch/tests/suites.conf`.

## Scope and decisions

No production callers, private helpers, crop/statistics, thresholds,
`_timing_evaluators`, cache fallback, source callback, or Runtime certificate
were changed. Private migration/deletion remains unqualified because cached
cards do not retain public scene rows and the real `LayerContext` caller lacks
the trusted final Root/source/component-zero join. The separate source-callback
and currentRoot evidence is not relabelled as this selected-cut proof.

The earlier malformed service request passed an `.mjs` file to pytest; the
other request omitted `-o addopts= -m integration` and consequently ran with
24 deselected tests. The named lane fixes both actual selection errors without
weakening behavior expectations.

## Not run / next step

No full suite, browser, renderer/capture, localhost/live socket, install, or
network test was run. The next deletion prerequisite remains a trusted public
source/root join for every real private caller, including cache-only fallback.
