# Final review — presenter mouth12 combined test batch

## Verdict

**APPROVE** for the intended clean-presenter `8a78c25ac` tree paired with the
Agent12 Composition consumer bytes/metadata from `f29a9475ee1`.

Minimal integration-order blocker: the combined patch is **not** applicable
directly to the full `f29a9475ee1` tree. A literal `git apply --check` there
fails because f29 deletes the old presenter helper/test seam that this patch
extends, and its `test_composition_package.py` context differs. This is an
apply-order constraint, not a test-correctness finding.

## Required apply order

1. Resolve the owner’s Agent12 consumer cohort with the clean presenter
   prerequisite (`8a78c25ac` source/test seam retained or equivalently ported),
   including the 0.0.12 artifact and matching package/lock/runtime metadata.
2. Apply `handoff-vw-m3-presenter-mouth12-test-batch-combined.patch` to that
   resolved tree. Do not force it onto full f29 as-is; if f29’s deletions are
   intentionally final, this unapplied patch is superseded and its tests must
   be ported to the replacement scene-host suite instead.
3. Re-run the targeted 33 + 5 lanes on the owner’s final tree.

## Verified scope and evidence

- `git apply --check --whitespace=error-all` passed against a disposable
  overlay archived from `8a78c25ac`, with only the f29 0.0.12 consumer
  artifact, package/lock, and runtime metadata overlaid. The patch has 15
  paths, all under `tests/`; no production source, source-authority factory,
  production join, or private-crop deletion was added.
- Exact artifact: 0.0.12, 58,444 bytes,
  SHA-256 `0a7b61529099ce994f807c6d7b1078303a09e7c0219144cc4b07467977f0f1a3`,
  lock integrity
  `sha512-490yQtC4k3cuBQJ4Aee5qEqOPNrlQrXPQkE0p6R8UDACAcT8amHe8EjCRI4vE+HtvXwUiy8zBjm7RcW7aTv9eA==`.
- The retained fixture archive was independently checked: 10,319 bytes,
  SHA-256 `e7f32e40aa1aa25d81f30d05fd5ccb83a8a19cd8ce4a5a560e9fd93dc73d7c39`;
  all six members are regular files with safe relative names and compare
  byte-for-byte to the five PNG/JSON fixture files plus `sha256.json`.
  PNG hashes are pinned and match: frame 0/4
  `6c3c819b5ac4a1b1848e3b72338e1e213e9159b6325eb1068f334dcfffc79ed5`,
  frame 3 `76715e2b9c0df4f57e5fb10d992011dbb0536534e4ac27a6e5e3797e12b04c73`,
  frame 5 `09b32c84599f3633fa5cf611216e25e667965041f971ab868f76bec354454108`.
  The original archive members and the 286-hash `presenter_ssr_before.json`
  are unchanged.
- The historical SSR lane keeps its explicit pre-12 black/Georgia theme; the
  real 0.0.12 `DEFAULT_THEME` assertion checks Agent navy `#050814`, foreground
  `#FAFAFA`, cyan `#67E8F9`, Arial, and 450 ms motion. All 286 historical
  hashes remain covered.
- The selected-cut lane is genuine: actual cut 3-of-3 changed pairs,
  half-open selection windows, sorted/duplicate frame keys, missing-image
  adjacency reset and denominator behavior, absent-file refusal, and strict
  15/799 versus 16/799 (`> 2%`) controls all pass. The public helper is
  explicitly test-only; production `mouth_box`/private statistics remain held.

## Commands and results

Using Node 20.19.4, shared Agent venv, and the existing shared Remotion
dependencies; no install, browser, socket, network, grant, or full-suite run:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=$OVERLAY \
ASTRID_NODE_EXECUTABLE=/tmp/vw-m3-agent-gate-node20.19.4/bin/node \
ASTRID_COMPOSITION_TEST_NODE_MODULES=/home/user/work/wt/vw-m3-scene-host-plumbing/remotion/node_modules \
/home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider --tb=short \
tests/packs/rendering/test_presenter_scene_capability.py \
tests/packs/rendering/test_presenter_crop_equivalence.py \
tests/packs/rendering/test_presenter_series_inspection.py \
tests/packs/rendering/test_presenter_selected_cut_aggregate.py
33 passed in 11.06s

PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=$OVERLAY \
/home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider --tb=short -m 'not integration' \
tests/packs/rendering/test_composition_package.py
5 passed, 1 deselected in 0.27s

/home/user/work/venv-agent/bin/python -m ruff check --no-cache --isolated --select E4,E7,E9,F,I,BLE [five touched Python test files]
All checks passed!

node --check [all four touched MJS helpers]
all passed

git -C $F29_FULL_OVERLAY apply --check --whitespace=error-all $PATCH
expected failure: f29 full tree lacks the 8a78 presenter test seam and has incompatible package-test context
```

No repository files were changed by this review.
