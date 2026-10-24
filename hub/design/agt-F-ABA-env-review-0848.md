## F-ABA environment review

Result: **PASS**

Reviewed `tl/agt-F-ABA-row-env-sol-0839` against `bd635de857`. Diff is limited to:

- `tests/suites.conf.candidate`
- `tests/suites.conf.candidate.request.md`

Findings:

- Preflight and pytest now share the same explicit `env -i` environment.
- `--noprofile --norc` prevents Bash startup mutation.
- The service’s appended selector reaches pytest through quoted `"$@"`.
- Original 23 preflight assertions and 59 body assertions remain unchanged.
- Target Agent/runtime pins, auth blob `979225…`, auth hash `e172f8…`, source tree, and fixture hashes match the request.
- The actual failed service `26998` exited 4 before collection due to the old environment boundary; the original body did not run.
- Whole-path import trace resolves the apparent `8ea` mismatch: conftest imports `runtime_protocol.platform` from becfe before the body. Later `use_runtime()` only inserts 8ea into `sys.path`; it does not replace `sys.modules`. `RuntimeService`, `RealmStore`, and relative `timeline_commit_auth` imports therefore remain becfe.
- No later subprocess changes this RuntimeService path; daemon startup constructs the service in-process.

Checks passed:

```text
python3 -I ... suites.conf.candidate.request.md
OLD: environment scope and exact selector PASS
NEW: environment scope and exact selector PASS
PASS: bash syntax, service serialization, 23 unchanged guards, source/oracle hashes, 59 body assertions, failure propagation

bash -n candidate command: PASS
bash -n with exact appended selector: PASS
git diff --check: PASS
```

No original test body, Runtime realm, browser, full suite, or live registry operation was run. Actual body behavior remains unverified and should be run once by the manager using the exact selector after installation.

Commit message and `DONE` marker were written.