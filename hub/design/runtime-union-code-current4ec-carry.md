# Runtime union code current4ec carry

Base: `a1f5106b4cad8c8a2cf32e6ef14e5fdb8f4f4962`.

## Result

Carried the exact current `4ec5d59` five-path delta:

- `runtime_protocol/cas.py`
- `runtime_protocol/service.py`
- `runtime_protocol/store.py`
- `tests/test_generation_publish_v1_settlement.py`
- `tests/test_timeline_clip_replacement.py`

The first four paths carry Wav829 settlement behavior: verified WAV duration inspection, explicit-null and zero-rate handling, and the authenticated HTTP selection proof. The clip replacement test carries the strict D05 route marker and keeps the original positive assertions under its strict xfail.

All six private materialization/ownership paths from `a1f` remain byte-identical, including source/owner/global-item/head-fence/C4 joins. The raw-media exact-BASE/declared-pin/single-FD/tamper rechecks remain untouched. No schemas, artifacts, generated clients, version metadata, root rewrites, or normal generation were changed.

## Verification

- `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD" /home/user/work/venv-runtime/bin/python -B -m pytest -q -p no:cacheprovider --basetemp=/tmp/rt-m2-union-code-current4ec-carry-tests -k 'not verified_media_is_exact_over_authenticated_http' tests/test_generation_publish_v1_settlement.py tests/test_timeline_raw_audio_port.py tests/test_timeline_materialization_join.py tests/test_timeline_materialization_authority_review.py tests/test_timeline_projection_ownership.py` — **221 passed, 4 deselected**.
- Central targeted: `request-test rt-m2-union-code-current4ec-carry targeted --files "tests/test_generation_publish_v1_settlement.py tests/test_timeline_clip_replacement.py"` — **15 passed, 15 deselected, 10 existing D04 xfails**; includes the authenticated WAV HTTP test.
- Central integration marker lane: `request-test rt-m2-union-code-current4ec-carry occupancy-integration --files "tests/test_timeline_clip_replacement.py"` — **2 failed, 13 passed, 10 deselected**. This is the known private-14 transition: the carried D05 refusal marker is a current-013 compatibility assertion, while `a1f` already accepts `ownership: parent`; the positive consequently XPASSes strict. The settled handoff explicitly defers version-qualified adaptation to the later adoption step. The assertions were not dropped or weakened.
- Syntax compilation of all five changed Python files — **pass**.
- `git diff --check` — **pass**.
- Ruff F-check on the three changed Runtime product files — **7 pre-existing findings** (duplicate imports/unused locals in carried current code); no lint edits made.

No full suite, native pair, publication, version bump, or shared-dependency mutation was performed. No implementation blocker remains for this authorized source-only carry; the D05/private-14 marker transition is intentionally deferred.

