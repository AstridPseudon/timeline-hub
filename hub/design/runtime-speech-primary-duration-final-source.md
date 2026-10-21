# Runtime speech primary-duration positive restoration

Date: 2026-10-21 UTC

## Final source identity

- Base/source commit: `d7597d5440d5ed5d5912235d547cb4380d226980`
- Expected post-harness source tree: `6abc2f117391de8e7e35c0283f575a002199894d`
- Harness commit: pending harness commit (workers do not commit; the commit
  message is supplied at the assigned commit-msg path).
- Changed repository path: `tests/test_generation_publish_v1_settlement.py`
- Product source and artifacts: unchanged from d759.

The production blob `runtime_protocol/store.py` is Git blob
`5415a62fbc4692c110017245ceda12260e25629b` and SHA-256
`67bfde020b41d624d2530915bd5bc187755b9af14afec897441825ce18e20b03`, exactly
matching d759. The only worktree delta is the bounded test restoration.

## Bounded restoration

`_speech_effect` now accepts an optional `output_port`, defaulting to the
existing `speech` case. Only
`test_speech_settlement_derives_wav_duration_for_exact_media_selection` is
parameterized over `audio` and `speech`. Its assertions and test body are
otherwise the original positive settlement, exact selection, verified read,
CAS identity, provenance, and no-canonical-write checks.

The `speech` parameter retains the d759 positive behavior. The exact-replay,
malformed-WAV, explicit-null, zero-rate, explicit-duration, and authenticated
HTTP controls remain single speech cases with their original bodies and
assertions. No production code, marker, skip, refusal conversion, metadata
workaround, caller duration, sidecar authority, C3d mutation, or generation /
version / pin was added.

## Evidence and assertion mapping

- Restored parameter only:
  `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD" /home/user/work/venv-runtime/bin/python -m pytest -q -p no:cacheprovider 'tests/test_generation_publish_v1_settlement.py::test_speech_settlement_derives_wav_duration_for_exact_media_selection[audio]'`
  — **1 passed**.
- Cheap collection/diff check: **2 positive parameters collected** (`audio`,
  `speech`); normalized helper and positive speech body are identical to d759;
  `store.py` and all non-test paths are unchanged; `git diff --check` passed.
- Reused central evidence from the approved speech-duration source:
  `tests/test_generation_publish_v1_settlement.py -k 'not authenticated_http'`
  plus imported-media and timeline-selection neighbors — **36 passed, 1
  deselected**; central targeted settlement file — **16 passed**.

No full, browser, render, model, socket-capable duplicate, integration merge,
or C3d mutation was run. This report notifies Runtime of the compatible
private-C3d-descendant source; no public activation or pin is claimed.
