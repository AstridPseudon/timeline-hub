# Validation

Disposition: `FAIL7_CONFIRMED`; source-only, no behavior or receipt credit.

Commands run and results:

- `bash -n` on the published 0515 command-cut and command-pristine scripts — PASS.
- `ast.parse` with `/home/user/work/venv-agent/bin/python -P` on the published
  `check-source.py`, plus stdlib JSON parsing of controls, readiness,
  admission-derivation and source-manifest — PASS.
- `bash -n` on the published 0309 measurement command, `git show
  0710897c87834550d1ee68b3f120405a9c81fe8f:evidence/command.sh | bash -n`,
  and the current D73 launcher — PASS.
- SHA-256 readback of published 0515 command scripts versus review0626 —
  command-cut and command-pristine PASS; checker FAIL (review claim
  `c5afc8a5…8c128`, published bytes `c5af3e45…8c128`).
- Read-only `git rev-parse HEAD`, `HEAD^{tree}`, and clean-status checks on
  current Agent, Runtime, App and Composition — PASS for the specified tuple.
- Read-only `git show` on pristine Agent 64197afa — claimed
  `tests/v10/timelines_create.py` MISSING; actual
  `tests/v10/test_timelines_create.py` EXISTS.
- `rg` on the live `tests/suites.conf` — `agent-core-full` NOT REGISTERED;
  only the ordinary `agent full` row exists. No request-test/test-run request
  was created.
- Read-only inspection of ORCH `request-test`, `test-run`,
  `d141-validate-receipt.py`, current D73 launcher, the 0515 scripts and
  passing 0309/0318/0030 publications — completed; dataflow and line spans
  are in `findings.md` and `source-map.json`.

Input-path limits checked explicitly: the canonical contract exists at
`/home/user/timeline-hub/hub/design/commit-v2.md`; the requested literal
`contract-v2.md` does not. The requested literal files
`BOARD-HEADER-D141u-a.md`, `BOARD-HEADER-D141v.md`, and
`BOARD-HEADER-D141w.md` do not exist; their current D141u-a, D141v and D141w
entries were read from `BOARD-HEADER.md`. The current PLAN has no literal
`F/U2` heading; its §3 task graph and the host brief were read. These are
publication/path gaps, not substituted source or invented evidence.

Not run by authorization: pytest, collection, product import, provider,
preflight, request-test, test-run, live service/row installation, registry,
receipt admission, acceptance, body, full suite, package/network acquisition,
or any source/product/test/fixture change. No private export was copied and no
old held request was touched.

Checker limitations: the published checker is syntactically valid but cannot
be run as a complete packet because its referenced positive stub and manifests
are missing. Its implementation is also static/token-based and does not
execute the controls it claims to validate.
