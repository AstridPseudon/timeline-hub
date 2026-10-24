## Report

Implemented in `working-service-binding.py` and `working-service-binding-control.py`:

- Frozen current D59 source tuple with all parents and `tl/integration` refs.
- Added exact client/runtime artifact mappings.
- Added fixed P2/P3 template, boundary, protected-span, body, and environment hashes.
- Rejected injected/duplicate markers and protected mutations.
- Added explicit Agent `CPY` and Runtime `RCPY` launch bindings.
- Added negative attacks and argv/export/failure controls.
- Historical recipe is refused.

Validation passed:

```text
PYTHONDONTWRITEBYTECODE=1 python3 -m py_compile working-service-binding.py working-service-binding-control.py
python3 working-service-binding-control.py
python3 -O working-service-binding-control.py
bash -n adapted P2/P3 candidates
git diff --check
```

Production caller integration remains intentionally unmodified and unverified. No live service, browser, HTTP, native, or full-suite execution was performed.

Commit message written; `DONE` marker created.