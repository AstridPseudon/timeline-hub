# A-review-T2-export-r1

## Verdict: PASS

Reviewed worker commit `1e594103a1` against `tl/zoom-integration`
(`7c4e6e2956d63a2e7930544760099f073c126ed6`). The diff is confined to the
T2 render boundary and its focused contract tests; no existing test assertions
were removed, weakened, skipped, or rewritten.

The implementation resolves project-pack refs from the exact Runtime-admitted
document and snapshot object, validates the descriptor and portable bytes, and
carries the frozen selection in the render snapshot. The selected source is
staged into private pack-shaped trees and is reused by managed validation,
registry lookup, generated effect/animation/transition dispatch, webpack
aliasing, bundling, and asset staging. Full revision digests are present in
render keys, import scopes, generated owner keys, and asset paths, so two
revisions coexist and an older pin does not consult the current catalog.
Missing documents/admissions/objects/descriptors, corrupt bytes, and digest
mismatches fail closed with snapshot-specific errors. The source is rebundled
from the verified tree; no prebuilt bundle is stored. The existing global
render lock remains around selected registry generation and render execution,
and selected registries/source trees are under invocation-private temporary
roots with cleanup. Built-in paths remain on the existing catalog/registry
behavior.

Trace points checked: `registry.py`, `_effect_registry.py`, `run.py`,
`managed_timeline.py`, `remotion/webpack-alias.mjs`,
`project_packs.py`/verified fetch paths, `root_preparation.py`, storage, and
managed invocation plumbing.

## Test evidence

- Worker focused group: **89 passed, 1 deselected**. The deselected case is
  the existing CJS/native-ESM integration lane.
- Worker render-registry/locking group: **28 passed, 5 deselected**. The
  deselected cases are the existing localhost-port lock/render smoke cases.
- Worker Ruff, Node syntax checks, and `git diff --check`: **passed**.
- Reviewer local replay with Runtime source explicitly on `PYTHONPATH`, the
  private Composition probe, Node 20.20.0, and private pytest caches:
  **13 passed** for `tests/packs/rendering/test_pinned_project_elements.py`.
- Required central first group: **infrastructure qualification failure**,
  exit 4 before collection. Its isolated command omitted the Runtime source
  path and failed importing `runtime_protocol` from `tests/conftest.py`; this
  is not a product pass/fail result.
- Required second central request was not accepted: the service reported
  `no worker A-review-T2-export-r1-registry`.

## Scope and follow-up

The worker did not run a live Remotion/Chromium render, MP4 export, browser
journey, or sampled zoom-frame parity check; those remain required acceptance
work. The owner frame-session environment also does not yet admit the two new
alias environment variables. Rerun the central targeted groups with the
Runtime source path available, then perform the real export/sample-frame
qualification before final delivery.
