# Runtime integrated WAV scope gates

Date: 2026-10-20 UTC

## Scope and snapshot

- Worker base: `e2db1e8cc7c176fafa1e4e651da3639b6e3a89dd`.
- Prerequisite merge completed before testing: `4ec5d592176355bd5758a74dec696d8be7ef9b0c` (`tl/integration`), with clean status.
- Snapshot tree: `de34d64765611dd2baa09ff3533c448f11cab702`.
- The worker worktree remained at its base and was not merged or changed.
- The requested design path was supplied as the literal placeholder `ABSOLUTEORCH`; this report is at the resolved orchestrator design root.

## One central test request

Request directory: `tests/runtime-targeted-1020172349-28464`.

```text
target=integration:runtime
suite=targeted
files=tests/test_generation_publish_v1_settlement.py tests/test_worker_security_settlement.py tests/test_timeline_verified_media_http.py
```

The central service recognized the exact snapshot tree as already tested by
`rt-m2-speech-wav-null-rate-fix-targeted-1020170406-29206` and reused that
result. This is the only test request made for this task.

Exact command and result:

```text
/home/user/work/venv-runtime/bin/python -m pytest -q \
  tests/test_generation_publish_v1_settlement.py \
  tests/test_worker_security_settlement.py \
  tests/test_timeline_verified_media_http.py
29 passed in 11.24s
```

## Source and public-byte gates

- `8292b94dc463e28808cd57e20a6aa372d474837b` is an ancestor of the integration HEAD. Its exact changed paths remain `runtime_protocol/cas.py`, `runtime_protocol/service.py`, `runtime_protocol/store.py`, and `tests/test_generation_publish_v1_settlement.py`.
- The integrated source contains the explicit-null regression, zero-rate regression, explicit-duration preservation, and authenticated HTTP selected-media proof in `tests/test_generation_publish_v1_settlement.py`.
- CAS WAV inspection retains one verified descriptor, rejects non-positive rates as unknown, catches the division boundary, and rechecks identity after inspection. Transient raw duration presence is passed only through settlement; it does not become a wire presence flag.
- Existing strict parent coverage remains present and unchanged, including `tests/test_runtime_child_delegation.py::test_parent_success_requires_managed_verified_child_outputs`.
- `contract/artifacts.json` is unchanged from public Runtime `2c4ac180c2220bdad966bc01e95ad230e99ce26a`: 9,210 bytes, SHA-256 `129abdbbf1f877643618b5290b39a5dd9225ba95b4c8fe8f2bb005ea4cf85497`, 75-entry manifest. Contract/schema/client paths also compare byte-identically to that public source.

## Limits and non-claims

- This qualifies only the normal Runtime managed-API settlement, selection,
  replay/CAS safety, and authenticated HTTP read neighbors.
- The Speech SDK does not provide intent/effect here; no SDK intent/effect
  qualification is claimed.
- No outer voiceover adapter, RIPPLE behavior, real model, render, or full
  suite claim is made. No variant append or regeneration behavior is claimed.
- No Runtime source, generated artifact, schema, API, table, or shared
  dependency was modified. No tests were weakened or skipped.
