# U4a-v2 envelope-normal producer adoption

Agent base: `7d356202826ce60ff676d6e46151187aad9f4a70`.

Adopted the exact immutable Runtime producer, not the moving integration
checkout or superseded pins:

- source commit: `34eac0041b0891e9011966b39bcbd26053fde5bc`
- producer tree: `9853574865f25e08284e82ffb26c0bdecaa16a30`
- producer checkout: `/home/user/work/wt/rt-pin-34eac004`
- manifest file SHA-256: `7c541b705a9dbc0827ed2e81a847455402b1d475491de702cde7ef85f4a8235d`
- producer version: `sha256:d5f98db3213e91d96d4a7f5b184e17bf5268357b37dc06eaa5b568c4b788a572`
- contract version: `0.2.14`
- unchanged `SCHEMA_DIGEST`: `sha256:35c2d9c5e0b51ab8d8b7a4f4dbafbdfcb13d232d7bd22fff21cf73e250398d4c`
- generated Python client: `sha256:9b5686c388347108898956c3475b16960e2434d64adcefcc71a26fc269cdd904`
- canonical inverse/edit-command schema: `sha256:d106dfe8212500709b4072d7bc0486f83c27d5d8de33d215cb52b9ea7d46357d`

The production import origin is the lock mapping
`astrid_runtime_client/generated.py <- packages/python/astrid_runtime_client/generated.py`
from that producer. The only product change is the regenerated generated client,
plus the lock selector/hash/version. The only additional tracked change is the
obsolete positive fixture in
`tests/stage1/test_vendored_workspace_client_parity_luna.py`, completed with the
actual required receipt fields and preview `would_status`.

All 15 consumer hashes match the producer manifest and lock:

| Consumer | SHA-256 |
| --- | --- |
| `astrid/core/timeline/schema/timeline-config.schema.json` | `sha256:4d74a4ae34fcfa89ce66e4ccad90a3871a3ef9d3adb26c9219ae7dec72deb3bd` |
| `astrid_runtime_client/__init__.py` | `sha256:78a69901f7c68d67b152410732f1c42dd30954ca07e7b4b9a319d4ddbd9035e6` |
| `astrid_runtime_client/contract_metadata.py` | `sha256:a79b2e12de96ec8f2c4bf7b6811ccb3538baf18ca839172f7a3d7bf525029aae` |
| `astrid_runtime_client/generated.py` | `sha256:9b5686c388347108898956c3475b16960e2434d64adcefcc71a26fc269cdd904` |
| `astrid_runtime_client/timeline_commit_types.py` | `sha256:88c67d9eb650b445b8ad04c9011c1f44f1ec5e9f72a4a733050515de7ec0b616` |
| `tests/fixtures/runtime-responses/events_page_1_200.json` | `sha256:6aaaabe512589beddddd5ef64f2307c39d365a99565c5a3291a15933a114be0d` |
| `tests/fixtures/runtime-responses/events_page_2_200.json` | `sha256:d5bffdc93e9939779c92a18c047e70df21711f12e16c345f43f3cbdec5b27eb2` |
| `tests/fixtures/runtime-responses/invalid_cursor_400.json` | `sha256:16a1db399e06b8d059472f567a091b4bd579d13d8885595376f61835646bfbff` |
| `tests/fixtures/runtime-responses/managed_outputs_200.json` | `sha256:6bcef19aca4ad8d574c60d738b54ba57fce6a3a9d4e1481c6f8f088dd460858d` |
| `tests/fixtures/runtime-responses/not_found_404.json` | `sha256:4a40fedbeccd345f24944e4af368c50430593d976a923c12af93ba21af6` |
| `tests/fixtures/runtime-responses/publish_conflict_409.json` | `sha256:19d664d035691202da03b22b858456c49983e253c7485a6347baa1cf350eea57` |
| `tests/fixtures/runtime-responses/task_admission_201.json` | `sha256:108559a92c9e681e3ade37fa6b567e1eaac3edce221665a07a81c2c2c06bb48c` |
| `tests/fixtures/runtime-responses/task_read_200.json` | `sha256:cc590c4f7d34820382b684d737f1cdb45eebeb20fbad2d5edda2dadac8ab2829` |
| `tests/fixtures/runtime-responses/validation_error_422.json` | `sha256:2a02a9147bc0a8b74727d9c577803b0aca333bd0dd035602dafcf2503b00ff1a` |
| `tests/fixtures/visual-boundary-v1.json` | `sha256:1fc778b42f7a5ef91a1fd8620fd92417131e44f97dd5c6a238c78f13bcabfc55` |

`artifacts.json` is current. Protected schema,
contract metadata, timeline types, provider/source, and reviewed R2/R3/meta/R1/
V1/V3/V4 files are unchanged. No G2/G3/G4/V2 imports or consumer workaround.

## Probes and gates

- Normal vendor update/check: PASS.
- Artifact manifest generation/check: PASS; 165 artifacts current.
- Agent targeted lane: **46 passed, 39 deselected**.
- Official Runtime public-client envelope controls: **48 passed, 27 deselected**.
  This covers complete accepted/merged/historical-rebased and preview accepted/
  merged envelopes, full v2 request metadata, partial receipt refusal, missing
  preview `would_status` refusal, invalid receipt fields, nonfinite values, and
  mismatched preview errors.
- Ruff ratchet: **2151/2151**, PASS.
- Private mypy ratchet: **1915/1915**, PASS.
- `git diff --check`: PASS.

Direct Ruff on generated files still reports inherited generator-style `I001` and
`E701` findings; generated output was not hand-formatted. No full/browser/native14
run was requested. Runtime owns its single native14/P5 qualification after home
adoption.

## Commands

```text
python3 scripts/vendor_lock.py update runtime.lock.json --producer /home/user/work/wt/rt-pin-34eac004
python3 scripts/vendor_lock.py check runtime.lock.json --producer /home/user/work/wt/rt-pin-34eac004
python3 scripts/artifact_manifest.py
python3 scripts/artifact_manifest.py --check
git diff --check
PYTHONDONTWRITEBYTECODE=1 ASTRID_RUNTIME_CHECKOUT=/home/user/work/wt/rt-pin-34eac004 PYTHONPATH="$PWD:/home/user/work/wt/rt-pin-34eac004" /home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider tests/sdk/test_workspace_client_timeline_commit.py tests/stage1/test_runtime_client_cutover.py tests/stage1/test_vendored_workspace_client_parity_luna.py tests/sdk/test_timeline_commit_v2_errors.py tests/sdk/test_p1_doc_patch_provider.py
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD:/home/user/work/wt/rt-pin-34eac004" /home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider /home/user/work/wt/rt-pin-34eac004/tests/test_timeline_commit_contract.py -k 'generated_python_commit or generated_python_refuses_nonfinite or generated_python_rejects_mismatched_preview'
RUFF_CACHE_DIR=/tmp/agt-U4a-v2-envelope-normal-0339-ruff-cache make ruff PY=/home/user/work/venv-agent/bin/python
MYPY_CACHE_DIR=/tmp/agt-U4a-v2-envelope-normal-0339-mypy-cache /tmp/astrid-u2-typecheck/bin/python -m scripts.reshape.compare_mypy_baseline
```

The strict fixture adjustment was required by the new producer contract and did
not weaken any negative, metadata, or value assertion. Next step is independent
Luna review, then the home merge queue; Runtime performs the one deferred native14
qualification.
