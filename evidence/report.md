PASS — B-T1-role-source-2

Canonical fixture SHA-256:

`c779ef38d4f47368967a5afab2704548c70c0f27c646f8ebab6be74ad3cf63a7`

Agent and App consumers must vendor `conformance/fixtures/shot-layering-v1.json`
byte-for-byte and pin this digest.

Added the inner visual track `source-plate` with authored `role: source` to
`film-picture-over-type`. Its `vision-source-plate` media clip reuses the existing
footage asset and 0–12000 ms timing, preserving the existing transparent window.
Expected output includes `occ-vision~source-plate`, with
`app.group = {"id": "occ-vision", "sourceTrack": "source-plate"}`, and maps the
clip to that namespaced track. The track follows the existing inner visual tracks
and precedes the occurrence row. This tests provenance without excluding visuals.

Added one focused assertion test requiring the authored visual/source track, a
positive-duration clip on it, and the expected namespaced track, group tag and
clip mapping. Existing assertions remain intact, including all seven required
cases, recursive rejection of `UNKNOWN`, ordering, merged audio and transparency.
No projection product code changed.

Validation:

- `PYTHONDONTWRITEBYTECODE=1 PYTEST_ADDOPTS='-o cache_dir=/tmp/w-0fd7cf1fa3/pytest-cache' python -m pytest -q --basetemp=/tmp/w-0fd7cf1fa3/pytest-role-source tests/test_shot_layering_fixture.py`
  — **4 passed, 1 warning in 0.09s**. The existing warning is
  `PytestConfigWarning: Unknown config option: timeout`.
- `git diff --check` — passed, no output.
- `sha256sum conformance/fixtures/shot-layering-v1.json` — digest above.
- Read-only Python comparison against `git show HEAD:conformance/fixtures/shot-layering-v1.json`
  — removing only the new authored track/clip and expected track/group/mapping
  restores the entire original JSON structure, preserving all seven prior cases.

Blocked: nothing. Full suites, consumer product tests, browsers, sockets and renders
were outside scope and were not run. Next: Agent and App vendor these exact bytes,
update their digest pins, and run their fixture consumer tests.
