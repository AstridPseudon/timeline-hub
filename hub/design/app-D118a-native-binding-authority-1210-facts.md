# D118a evidence facts

- Base: `cf7b8d7c2b4cb980de1d873f0498784d5210d508`.
- Production path changed: `astrid/sdk/timeline/native_text_binding.py` only.
- Additive control: `tests/sdk/test_native_text_binding_authority_fields.py` only.
- Parent RED: `1 failed, 1 passed` for the additive node. The native output omitted `binding_id`/`head`, and incomplete Runtime authority was accepted.
- Candidate GREEN: `4 passed in 1.12s`.
- Candidate behavior: an existing `{binding_id, head, event_stream_id}` tuple is retained only when complete, typed, and paired with the same media descriptor; new births remain projection-field-free; malformed or changed pairs refuse before writing.
- Public caller proof: the native command's actual output row is passed directly to `read_composition_script`; no authority fields are restored in setup.
- Privacy proof: the command does not contain `_runtime_document`; no new cache, schema, route, channel, or authority field was added.
- Runtime proof status: no live provider/browser/full suite was run. The direct native/public-reader control is green; protected independent review and exact immutable Runtime qualification remain held for manager queue.

## Exact checks

- `PYTHONPATH=$PWD:/home/user/work/runtime /home/user/work/venv-agent/bin/python -m pytest -q -o addopts= tests/sdk/test_native_text_binding_authority_fields.py` → `4 passed in 1.28s`.
- `PYTHONPYCACHEPREFIX=/tmp/w-5b66c97ba0/pycache /home/user/work/venv-agent/bin/python -m py_compile astrid/sdk/timeline/native_text_binding.py tests/sdk/test_native_text_binding_authority_fields.py` → pass.
- `... -m ruff check --isolated astrid/sdk/timeline/native_text_binding.py tests/sdk/test_native_text_binding_authority_fields.py` → pass.
- `... -m mypy --follow-imports=skip astrid/sdk/timeline/native_text_binding.py tests/sdk/test_native_text_binding_authority_fields.py` → pass.
- `git diff --check` → pass.
