# D134 exact clean normal source intake

Result: PASS. Imported exactly the three reviewed donor blobs into the clean
Agent integration base a30e74e901a28b39c28facba3deb00d76f186e23.

Source checks:

- Donor A commit 9a7c9e38cf9baa72a4b10b7b6a50cf47b6447430 changed only the
  inverse regression file; the current blob matches exactly.
- Donor B commit 9e85402544af522a2b5bb2716731b2dfe4413652 changed only the
  Gate1 and prepared-video files; both current blobs match exactly.
- git diff --name-only contains exactly those three paths.
- M1 remains byte-identical at SHA-256
  838c77332683358877059f1357267a49cd130a985be4e4755a9655ec3f930d01.
- git diff --check: PASS.

Static commands and results:

    RUFF_CACHE_DIR=/tmp/d134-history-source-intake-2119.Nc5CmS/ruff /home/user/work/venv-agent/bin/ruff check tests/editing_conformance/test_inverse_stage_runtime_regressions.py tests/editing_conformance/test_gate1_fresh_word_transcript_frontends.py tests/editing_conformance/test_prepared_video_birth.py
    PASS - All checks passed!

    PYTHONPYCACHEPREFIX=/tmp/d134-history-source-intake-2119.Nc5CmS/pycache311 /usr/bin/python3.11 -m py_compile tests/editing_conformance/test_inverse_stage_runtime_regressions.py tests/editing_conformance/test_gate1_fresh_word_transcript_frontends.py tests/editing_conformance/test_prepared_video_birth.py
    PASS - Python 3.11.17

    MYPY_CACHE_DIR=/tmp/d134-history-source-intake-2119.Nc5CmS/mypy PYTHONPATH=. /home/user/work/venv-agent/bin/python -m mypy --cache-dir=/tmp/d134-history-source-intake-2119.Nc5CmS/mypy --config-file pyproject.toml tests/editing_conformance/test_inverse_stage_runtime_regressions.py tests/editing_conformance/test_gate1_fresh_word_transcript_frontends.py tests/editing_conformance/test_prepared_video_birth.py
    PASS - Success: no issues found in 3 source files

Functional tests were not run by task instruction: no live own11, M1, service,
browser, full, or other behavior suite. M1 behavior remains UNKNOWN.
