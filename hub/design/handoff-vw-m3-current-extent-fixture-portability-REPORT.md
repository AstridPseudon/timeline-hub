# Current extent tail-fixture portability

## Change

`tests/packs/rendering/test_remotion_layer_tail_compat.py` now resolves the
composition archive from the committed `remotion/package.json` `file:`
dependency. The helper confines the resolved archive to `remotion/` and the
existing probe continues to extract `chunk-SE4TPVLW.js` and execute the actual
`Root.tsx` callbacks. No product source or archive was added or changed.

## Evidence

- Old baseline: `11 failed, 11 passed`; every failure attempted the absent
  `remotion/artifacts/banodoco-timeline-composition-0.0.10.tgz`.
- Updated target: `22 passed`.
- Fresh tracked Git archive (`git archive HEAD`, current test diff applied in
  `/tmp`, no untracked files or private archive): `22 passed`.
- Tail/extent neighbors:
  `/home/user/work/venv-agent/bin/pytest -q tests/packs/rendering/test_native_layer_extent.py tests/packs/rendering/test_remotion_native_window.py tests/packs/rendering/test_composition_package.py`
  -> `103 passed, 1 deselected`.
- `ruff check tests/packs/rendering/test_remotion_layer_tail_compat.py` -> all
  checks passed; `git diff --check` passed.
- The three product files from `da10b0b76` are byte-preserved relative to
  `HEAD`: `astrid/core/rendering/service.py`,
  `astrid/packs/rendering/rendering/renderers/remotion/run.py`, and
  `remotion/src/Root.tsx`.

## Protected hashes

- Current public 0.0.12 archive:
  `remotion/artifacts/banodoco-timeline-composition-0.0.12.tgz`
  SHA-256 `0a7b61529099ce994f807c6d7b1078303a09e7c0219144cc4b07467977f0f1a3`.
- Extracted public 0.0.12 duration chunk `package/dist/chunk-SE4TPVLW.js`:
  SHA-256 `887441a18596fd09bd145381f6745ca986372cd32fb59278733f6b8d161f494b`.
- `remotion/package.json` SHA-256
  `58460ce59e2473d74f44238a2e5e78e2d4bd8a79a0bd94e430f7ae5eb6c2778a`.
- `remotion/src/Root.tsx` SHA-256
  `afde359fcf7324f0885543e3f3292372bd1b94bb3f219477bd15a2a4ee704f90`.

## Scope

One test file changed: 15 insertions and 1 deletion. No product codec,
semantic, render-clock, or fixture-archive change. No full/browser/socket/
install/network suite was run.
