# Runtime raw-base eligibility fix

Date: 2026-10-20
Worker: `rt-m2-raw-base-eligibility-fix`

## Result

Restored `RequestCommitPort.media_info` eligibility to the authenticated
original request base closure. A raw pin must now be an exact
`{media_id, content_digest}` pair, be declared in the request/closure context,
and appear in the original `base_revision_id` dependency manifest before memo,
descriptor, or CAS metadata reads. No observed document, current head, new
candidate, command fallback, or other revision is used as the base.

The existing descriptor-safe single-FD/hash/fstat path, consumed-media
acceptance recheck, and accepted-retry ledger-first behavior were not changed.

## Regression coverage

Added one permanent test using a real same-project ingest (not handcrafted
accepted-history SQL): a pin declared in the request but absent from the
accepted base closure is refused, while the base-owned WAV pin remains
readable. The existing outside-base and storage-race tests remain intact.

## Evidence

- `PYTHONPATH=. /home/user/work/venv-runtime/bin/python -m pytest -q -p no:cacheprovider tests/test_timeline_raw_audio_port.py` — **8 passed**.
- `PYTHONPATH=. /home/user/work/venv-runtime/bin/python -m pytest -q -p no:cacheprovider tests/test_timeline_raw_audio_port.py tests/test_timeline_commit_port.py tests/test_timeline_commit_contract.py tests/test_timeline_raw_payload_contract.py` — **122 passed**.
- `PYTHONPATH=. /home/user/work/venv-runtime/bin/python -m pytest -q -p no:cacheprovider tests/test_timeline_commit_acceptance.py` — **59 passed, 1 deselected**.
- `git diff --check` — passed.
- No full suite, HTTP/browser/live-socket suite, or duplicate native Agent/Runtime pair was run.

## Source identity and handoff

Base commit: `b73139121169b72a2af9371f7808999ee91a1471`  
Base tree: `2c9452aea8ef0c65d2ef2e902f46a91fa4409ee7`  
Pre-harness changed paths:

- `runtime_protocol/timeline_commit_port.py`
- `tests/test_timeline_raw_audio_port.py`

Pre-harness binary patch fingerprint: `e592cc3ba52949af7fafa11bce11e44912b3571950bf0c8b5b86c6dee9255144`.

The final commit SHA/tree is intentionally **pending the exit harness commit**
because workers cannot commit in this sandbox. Replace this pending identity
with the harness-assigned commit SHA and tree before citing the fix as a
committed pair or running the one requested native qualification.

Existing `rt-m2-ordinary014-raw-media-compose` output remains **HOLD** until
this guard is carried into its candidate. No public schema, DTO, table, API,
ABI, release, or raw-add authority was introduced.
