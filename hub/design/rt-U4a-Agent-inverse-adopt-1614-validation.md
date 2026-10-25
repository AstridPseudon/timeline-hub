# U4a validation

- Runtime receipt: `checkout-runtime-ab1e4f6141987706132916e2da16477f5a019464`; exact checkout `/home/user/work/wt/rt-pin-ab1e4f61`.
- Runtime before/after: clean; HEAD `ab1e4f6141987706132916e2da16477f5a019464`; tree `7d8e77b2f5a4af79305c9212ce5174d3ea9fd657`.
- Agent base: `20177e66564f9f91735ed1a11bac821682d60edf`; tree `68433c5f77be90063b1f43d3e8f1407346a50675`.
- Available-space admission: `5291933696` bytes (>= 5 GB).
- Refresh: PASS — `/home/user/work/venv-agent/bin/python scripts/refresh_runtime_client.py --producer /home/user/work/wt/rt-pin-ab1e4f61`.
- Vendor provenance: PASS — `/home/user/work/venv-agent/bin/python scripts/vendor_lock.py check runtime.lock.json --producer /home/user/work/wt/rt-pin-ab1e4f61`.
- Artifact manifest: PASS — `/home/user/work/venv-agent/bin/python scripts/artifact_manifest.py --check`.
- Private compilation: PASS — 7 scripts/client Python files compiled to a private `/tmp` directory.
- Diff hygiene: PASS — `git diff --check`.
- Focused tests: PASS — `PYTHONPATH=/home/user/work/wt/rt-U4a-Agent-inverse-adopt-1614:/home/user/work/wt/rt-pin-ab1e4f61 /home/user/work/venv-agent/bin/python -m pytest -q tests/test_vendor_lock.py tests/test_artifact_manifest.py` → `24 passed in 5.26s`.
- Initial test setup note: the same pytest command without the immutable Runtime checkout on `PYTHONPATH` could not collect because this Agent checkout does not contain tracked `runtime_protocol`; no source or dependency files were changed.
- Final Agent diff: only `runtime.lock.json`; generated client/schema/artifact/fixture bytes are unchanged.
