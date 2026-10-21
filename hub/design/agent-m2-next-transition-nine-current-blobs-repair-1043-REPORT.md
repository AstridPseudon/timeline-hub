# Agent M2 current-blob repair 1043

## Result

Restored exactly the nine paths named by `git diff --name-only c4b964f6a b3c96a758` from `b3c96a758` into the future transition source based on `eebfe1035839b628e472b204c0c204a1d4127e2f`.

No other path was changed. No schema, transition feature, generated pin/client, generation, native activation, DTO/store/authority, or public release work was performed.

## Identity

- Base commit: `eebfe1035839b628e472b204c0c204a1d4127e2f`
- Base tree: `141e34d3e2bf95589841aabe0a7aba0f152e6480`
- Source commit: `b3c96a758c1cfa2a609d1498e0e9ee401b32cc40`
- Source tree: `3467b7bffb0fe6edf9178c9a9de4d446c8ab8857`
- Prior 6c commit/tree: `6c1989adf723ae0ea0f4205c1cc8f1c0e4b22e79` / `cc0a8dd1360324a1b440ba7d318a083e7f8814cc`
- Corrected provisional tree (temporary index): `236fa26cd9cf3e31c2dc25ef45045f2c155f16a8`
- Harness commit SHA: pending harness commit

## Exact nine-blob verification

All nine working-tree SHA-1s matched their `b3c96a758:path` blob:

| Path | Blob |
| --- | --- |
| `astrid/sdk/media_transcript.py` | `138a6adc64f2bdaa59eef1f267f6211139965912` |
| `astrid/sdk/timeline_sheet.py` | `6ae8d494d6684a9706ef533f825d419f34bf8d42` |
| `astrid/sdk/timeline_transcripts.py` | `60e4d68fac867019e9919e0526e8cf6b3ed35587` |
| `tests/editing_conformance/test_commit_runtime_occurrence_media.py` | `857fe815bd080ec4b999de89ee4425491968ca6c` |
| `tests/editing_conformance/test_commit_runtime_parent_media_swap.py` | `66ba1bf4c77da3a008f762df749c74866e0e77dd` |
| `tests/editing_conformance/test_native_sheet_ordinary_runtime.py` | `f561128f89b756eb3c624264a81a0e1402032872` |
| `tests/integrations/test_generic_host_remotion_render.py` | `d2a996a2541a24ae206b44f65d6434af535ff1c2` |
| `tests/sdk/test_media_transcript.py` | `f65d4822ce8c6e0ca692e6e2506e46b0fc6dec45` |
| `tests/sdk/test_timeline_sheet_native.py` | `ced2be78f65d48028061fd0c1cd8a3cf604d495f` |

The changed-path allowlist compared exactly equal to these nine paths.

## Safety matrix

| Area | Current corrected source | Prior 6c / base safety |
| --- | --- | --- |
| Nine current-preservation paths | Exact `b3c96a758` blobs above | Prior 6c hashes were not reintroduced; later b3c current blobs are restored |
| Transition schema | Raw SHA-256 `95193e5a1f90a8072f55deb19f8b7ac63dc5054130c14eab097f0dd73f149729`; canonical SHA-256 `8500046e82587856c16cd6e241f27c886f9089538884a0b806fa75138a57cb49` | Unchanged from base; no schema file in allowlist |
| Existing pin/client | `runtime.lock.json` `a9046ae72a4ee1ff9cb7e8062f301d599803f826eb6f2dbb025e7cc5b1d27a6c`; `astrid_runtime_client/__init__.py` `7e602716931ca03930e1801596e098b83aa7344b7c54fe34b26e2308f82f15b2`; `contract_metadata.py` `e6d8286ca342bbb7a7d6554bb37357548b95bf2df123e7d46f60d6fce8fe53b1`; `generated.py` `e58f0fbe652b2baf8a3cd113def468dde3b32d1522f946a733c2b2a3b8461350`; `timeline_commit_types.py` `af295393450db831c43e6559eb0aa8f645e6cd0e79f4beb078df949bdb58e0d3` | Each equals prior 6c and base; none is in the changed allowlist |
| Feature/other paths | No changes | `git diff --name-only HEAD` is exactly the nine-path allowlist |

For reference, prior 6c schema hashes were raw `6dd2b082ebdb630b4fc8ec3eeeea3b40c1eebe910c84557e45ab8fab05322b16` and canonical `9f5612ff34a5758ecacae948d5c0bfb1acc867d6ecb7a6af037bf8e3974fd9d6`; those are historical floors, not replacements for the current transition schema.

## Live callers

The restored production modules are consumed by the existing timeline paths: transcript ID/schema consumers in `astrid/sdk/timeline/native_source_inputs.py`, `astrid/sdk/timeline/_timing_evaluators.py`, `astrid/sdk/timeline/native_transcript_association.py`, and `astrid/sdk/timeline/commit.py); transcript synchronization from `astrid/sdk/timeline/publish.py` and `astrid/packs/timeline/cli_working.py`; NativeSheet from `astrid/sdk/timeline/checkout.py`, `astrid/sdk/timeline_address.py`, `astrid/packs/timeline/cli_show.py`, `astrid/packs/timeline/cli_native.py`, and `astrid/packs/timeline/cli.py`. No caller was added or activated.

## Tests

Passed:

- `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD:/home/user/work/runtime" /home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider tests/sdk/test_media_transcript.py` — **13 passed**
- `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD:/home/user/work/runtime" /home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider -m integration tests/editing_conformance/test_commit_runtime_parent_media_swap.py::test_legacy_composition_writer_checker_rejects_planted_product_write` — **1 passed**
- `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD:/home/user/work/runtime" /home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider tests/sdk/test_timeline_sheet_native.py::test_detached_parameter_cells_keep_presence_and_literal_text tests/sdk/test_timeline_sheet_native.py::test_detached_mixed_edit_with_opaque_neighbor_is_staged` — **5 passed**
- `git diff --check` — passed
- Exact blob, allowlist, schema, pin/client, and provisional-tree checks — passed

Not qualified here:

- The WC8 daemon-backed test was attempted directly and correctly failed at localhost socket setup in the sandbox.
- Central targeted execution without suite configuration failed before collection because `runtime_protocol` was absent from PYTHONPATH.
- The correctly provisioned central named lane then ran the WC8 test but failed both its appended tests on the existing Runtime/Agent health schema mismatch (`7d4afa…` runtime vs `a8fad2…` client), before behavior assertions. This is environment/contract evidence, not a repair regression.
- Theme/render, transition, floor, full, browser, generation, native activation, and public pin suites were not run as directed.

The independent 1039 review remains pending; this repair does not treat it as approved.

