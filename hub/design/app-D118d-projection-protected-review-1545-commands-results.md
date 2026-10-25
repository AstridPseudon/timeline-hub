# D118d protected review commands and results

- Disk admission: `df -B1 /tmp` reported `5089345536` bytes available at exact own9 dispatch; ongoing stop floor was `4000000000` bytes. Ending availability was `5089251328` bytes.
- Exact own9 command from the brief, with all nine author-listed nodeids and pinned Runtime `5e9ad1c6f74241d8771d3284fdd2ce7a214fd344`: **FAIL**, exit 1, 9 setup errors. First failure: `tests/sdk/test_timeline_capture_projection.py:284`, `bundle_from_document(document)`, `AuthoringBundleError: project scope belongs on the canonical document`. Private raw outputs: `own9.xml` and `own9.log` in this evidence directory.
- `/home/user/work/venv-agent/bin/ruff check tests/sdk/test_timeline_capture_projection.py`: **PASS** (`All checks passed!`).
- `/home/user/work/venv-agent/bin/mypy --cache-dir $TMPDIR/mypy --follow-imports=skip tests/sdk/test_timeline_capture_projection.py`: **PASS** (`Success: no issues found in 1 source file`).
- `PYTHONPYCACHEPREFIX=$TMPDIR/pycache /home/user/work/venv-agent/bin/python -m py_compile tests/sdk/test_timeline_capture_projection.py`: **PASS**.
- `git diff --check`: **PASS**.
- Independent AST/hash review: **PASS** for conservation checks; base blob SHA-256 `90c4625a7481fdcd570ec8b85bbe95325f4d3c57f0a3a26017dd405b8269b638`, candidate blob SHA-256 `4c85d15814c2b1b8128be5af5bac447cded17a72babd2d3450efdd6147fffb48`, +52/-0 lines, 43 original assertions preserved plus one setup-status assertion.
- `git diff --name-status 20177e66564f9f91735ed1a11bac821682d60edf..HEAD`: **PASS**, only `M tests/sdk/test_timeline_capture_projection.py`.
- `git diff 28081580dc95f02470d82ad81b826335d8e4bd09..HEAD -- tests/sdk/test_timeline_capture_projection.py`: **PASS**, no diff; candidate setup exactly matches historical commit.
- `git cat-file -e 92443771676ef2bbb547d0a103d708fa8bec4c63:tests/sdk/test_timeline_capture_projection.py` in `/home/user/peteromallet/astrid-agent`: **ABSENT**, status 128.
- Runtime custody: `/home/user/work/wt/rt-pin-5e9ad1c6` is clean at commit `5e9ad1c6f74241d8771d3284fdd2ce7a214fd344`, tree `de2954a0ceadb4455903d9abdfec3b773318a50f`.
