# Agent owner review: current extent fixture portability

## Verdict

**APPROVE** `tl/vw-m3-current-extent-fixture-portability` at
`5d0f1ddcad54936b36cedf1d89bf34f45fa612b5` for merge onto the current
integration branch.

Reviewed against `tl/integration` at `e5c2ff5f78ae4a96e436ea1f118f655c05df2b27`;
the candidate/integration merge base is `df2739f903edac02bd36b4446deeea847524c040`.
The candidate contains the previously reviewed extent unit `da10b0b7690a8c2a4032e75eb3d4a3e988121997`
and the requested portability commit `5d0f1ddc`. The portability commit itself
is one test-file change: 15 insertions and 1 deletion in
`tests/packs/rendering/test_remotion_layer_tail_compat.py`.

## Review findings

- The portability helper reads the committed `file:` dependency from
  `remotion/package.json`, resolves it relative to `remotion/`, rejects a path
  escaping that directory, and checks that the archive exists. The candidate's
  dependency is the current `banodoco-timeline-composition-0.0.12.tgz`.
- The extent unit measures the original render view before native layer
  filtering, carries the original clip clocks, and passes the original extent
  as an invocation-only metadata value. Native isolated layers retain their
  absolute `FrameWindow`; `supports_windows: false` continues through the
  existing sliced legacy path with a null window.
- Remotion accepts the carried extent only for a valid native layer stamp and
  a bounded pre-tail clock. It refuses malformed, conflicting, overlong,
  legacy-window, unlayered, and ordinary-tail cases. Root's two compositions
  share the same metadata callback and preserve the original full duration
  while legacy local-window metadata remains local.
- The native and legacy Three/live-scene cases retain the original scene
  payload, local slice, pin/hold behavior, alpha choice, and source-time
  mapping. The source timeline remains unchanged.

The full candidate delta has only these seven paths: the three rendering
product files, the Root metadata test, the live-scene test, the native extent
test, and the tail compatibility test. There is no package/package-lock or
pin change; no PCM activation or PCM implementation path was added; no
serializer definition changed; and no old 0.0.10 archive is referenced by the
candidate delta. The remaining 0.0.10 mentions in the tree are pre-existing
documentation/historical test data, not this fixture's dependency.

## Evidence run by this review

All tests ran from a private `git archive` extraction of `5d0f1ddc` with the
shared Agent venv and shared Node modules treated as read-only.

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-review-extent-current/candidate-review-20261020 /home/user/work/venv-agent/bin/python -B -m pytest -q -o addopts= -p no:cacheprovider --tb=short --basetemp=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-review-extent-current/pytest-basetemp-20261020 \
  tests/packs/rendering/test_native_layer_extent.py \
  tests/packs/rendering/test_remotion_layer_tail_compat.py \
  tests/packs/rendering/test_live_scene_composition.py -k 'not real_render'
```

Result: **112 passed, 1 deselected** in 33.52 seconds.

```text
/tmp/vw-m3-agent-gate-node20.19.4/bin/node remotion/tests/root-metadata.test.cjs
```

Result: **7 passed, 0 failed**.

```text
/home/user/work/venv-agent/bin/python -B -m ruff check --no-cache \
  tests/packs/rendering/test_native_layer_extent.py \
  tests/packs/rendering/test_remotion_layer_tail_compat.py \
  tests/packs/rendering/test_live_scene_composition.py
```

Result: **All checks passed**.

```text
git diff --check df2739f903edac02bd36b4446deeea847524c040 \
  5d0f1ddcad54936b36cedf1d89bf34f45fa612b5
```

Result: **passed**.

The producer/final-gate report additionally records 177 bounded checks
passing (166 pytest and 11 Node) in a fresh tracked extraction; this review
did not treat that report as a substitute for the focused rerun above.

## Limitations

No full suite, browser/live-render test, encoder/decoder run, pixel/audio
parity check, or Runtime qualification was run here. The one real-render
live-scene test was intentionally deselected under the worker rules. These
limitations do not block this narrow fixture-portability approval, but the
broader viewing and Runtime gates remain separate.

