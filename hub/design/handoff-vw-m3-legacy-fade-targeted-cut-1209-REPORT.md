# VW-D09 legacy fade targeted cut

## Result

Added a dormant, one-to-one public Composition14 replacement for the exact
independent-fade film:

- `tests/packs/rendering/d09_same_film_public.mjs`
- `tests/packs/rendering/test_d09_same_film_public.py`

The legacy private assertion remains unchanged. The new integration-marked
tests retain both required behaviors: independent fades are DIP only in
frames `[16,30)`, while the canonical incoming transition remains COVERED.
No Agent package pin, lockfile, archive, version, product source, or peer
package was changed.

The private `astrid/core/timeline/onscreen.py` fade code is still live source,
not a dead legacy leaf: `astrid/sdk/timeline/check.py:93-119` calls
`onscreen.coverage`, and `astrid/packs/rendering/actions/timeline_visualize/overlays/labels.py:53-60`
calls `onscreen.visible_at`. It is retained as the host adapter. The exact
remaining migration dependency is the public source join, not Gate6 physical
parity.

## Evidence

Passed:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD:/home/user/work/runtime" ASTRID_NODE_EXECUTABLE=/home/user/work/toolchain/node-v20.19.4-linux-x64/bin/node /home/user/work/venv-agent/bin/python -B -m pytest -q -o addopts= -p no:cacheprovider tests/core/timeline/test_onscreen.py tests/core/timeline/test_onscreen_more.py tests/sdk/test_coverage_empty_cut.py
19 passed in 0.61s
```

Log: `/tmp/vw-m3-legacy-fade-targeted-cut-1209-private-tests-runtime.log`.

Passed static checks:

- `python -m py_compile tests/packs/rendering/test_d09_same_film_public.py`
- `python -m ruff check --no-cache tests/packs/rendering/test_d09_same_film_public.py`
- `node --check tests/packs/rendering/d09_same_film_public.mjs`
- `git diff --check`

The explicit public14-gated command was run against the immutable qualified
0.0.14 archive in a private temporary overlay with the read-only 0.0.13 peer
graph. It failed closed with **2 failed** because the current Agent source
does not bind `prepareFootageScene`; the public answer is UNKNOWN rather than
the required `rect` capability. Log:
`/tmp/vw-m3-legacy-fade-targeted-cut-1209-public14-gated.log`.

Exact command:

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD:/home/user/work/runtime" ASTRID_COMPOSITION_TEST_ARTIFACT=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/artifacts/banodoco-timeline-composition-0.0.14.tgz ASTRID_COMPOSITION_TEST_NODE_MODULES=/home/user/work/runtimes/agent-remotion-viewing13-d0a5072b/node_modules ASTRID_NODE_EXECUTABLE=/home/user/work/toolchain/node-v20.19.4-linux-x64/bin/node /home/user/work/venv-agent/bin/python -B -m pytest -q -p no:cacheprovider -o addopts= --basetemp=/tmp/vw-m3-legacy-fade-targeted-cut-1209-public14-gated -m integration tests/packs/rendering/test_d09_same_film_public.py
```

This is not a public14 behavior pass and is not relabeled as one. The current
Agent and stage255 source both lack the binding, so the dormant test correctly
names the real adoption blocker. No full suite, browser, socket, physical
proof, or Gate6 run was performed.

## Decision / next step

Keep this patch dormant until Agent adopts the reviewed AM-footage capability
source/binding together with the qualified Composition14 consumer stage, then
rerun this exact two-test integration lane and obtain Agent-owner review before
retiring the old private assertion. Close the D09 legacy-fade source row
separately from Gate6; Gate6 physical parity is not part of this source cut.
