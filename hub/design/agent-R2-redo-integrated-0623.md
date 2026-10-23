# R2/G4 readonly redo qualification — PASS

Agent `3e4261e9694c7bd7c1b5fada9bf01d91007bcc80` passed the exact six requested
integration nodes in one pytest process: **6 passed in 12.69s**. Runtime modules
were executed from the immutable `85dafdf46742b02ae5e4a300656cd6f5d68f0d4d`
archive (tree `80c3da43addffdbfb2aa95bac06e2abd5e011146`), with an external
observation-only plugin asserting all loaded origins and `validate_claims` before
and after every case. There were 12 origin records, six cases, 44 distinct
Runtime origins, and every origin resolved inside the archive; `validate_claims`
resolved to the archived `runtime_protocol/timeline_commit_auth.py` each time.

The focused source lane passed **30 tests** across `test_commit_boundaries_d12.py`,
`test_provider_occurrence_fork.py`, and `test_inverse_stage_images.py`.
Scoped Ruff/private mypy, normal Ruff (`2149/2149`), mypy ratchet (`1914/1914`),
vendor-lock, artifact manifest, and `git diff --check` all passed. Normal `34eac`
lock, `d106` schema, generated files, and tools were retained. No source/test or
generated changes were made. The three original redo cases are countable on the
current head. Stale-window source invalidation and map-locality remain open and
were not claimed.
