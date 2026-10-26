# Validation

- `bash ops-d141z-build-stop/check.sh` — PASS, exit 0, 33 purposes; unchanged
  acceptance SHA-256 `0486a6e6d6fd5f548f39accfb1ac3866a79b65606c74de9649a67eb2262f6099`.
- `python3 -B` AST parse plus redirected `py_compile` — PASS for both Python
  files; cache was outside the repository.
- `bash -n ops-d141z-build-stop/check.sh` — PASS.
- `RUFF_CACHE_DIR=/tmp/d141z-sol-independent-0944/ruff-cache ruff check --select F ops-d141z-build-stop` — PASS.
- `git diff --check HEAD --` and `git diff --check 32bc911afcb2648e54be4432c5aa96cbdacf4eae HEAD` — PASS.
- Independent scope/hash/byte-exact assertions — PASS: from 8e42 only
  check/lifecycle/install-map differ; from 32bc exactly four source files plus
  two authorized pyc deletions.
- Independent source-route/stop-custody assertions — PASS: PDEATHSIG,
  repeated parent checks, TERM/KILL, wait/reap, control descriptor, append-final,
  no private admission lock/second gate, and external owner metadata.
- F1 publication hashes and sizes — PASS; observed D68 publication mode 0644
  versus claimed original 0755 recorded as a custody follow-up.

Not run by instruction: real delivery build, dry-run, rehearsal, ZIP, full
suite, live dispatcher/test-run admission, service/queue/registry request,
canonical install, package install, network acquisition, browser/live sockets,
or historical 0741 replay. TypeScript is not applicable to ops-only source.
