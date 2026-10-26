# Validation

Disposition: `PASS_COMMAND`; zero finite findings.

Commands and results:

- `bash -n .../agt-F-D141i-terminal-floor-return-sol-0309/evidence/measurement-command.sh` — PASS.
- Independent read-only Python static check — PASS: JSON packet parse, bounded diff against 0253, unchanged helper bodies, exact native row and original receipt/brief paths, two identical 22-root argv copies, exact `-q -n3 -o addopts= -p no:cacheprovider --timeout=45`, one launcher, no second 4.7 GB post-preparation check, source/before/after 4 GB checks, five-second monitor, absent production runroot.
- Independent source custody/hash check — PASS: all 28 physical and 386 historical readbacks; four frozen commits, trees, parents, origins, exact paths, and clean states; venv-agent interpreter, profile lock, launcher, schema/client bindings unchanged.
- Independent exact terminal block controls — PASS: 4,000,000,001→0; 4,000,000,000→0; 3,999,999,999→78; unreadable→97; unwritable→98; monitor failure→124; body failure→17.
- Independent exact admission helper controls — PASS: genuine 0249 receipt/brief→0; `/dev/null` malformed receipt→78; missing receipt→78. No body or service was invoked.
- Independent launcher dry controls — PASS: positive preflight 0, stub 17, one call; positive serialized/materialized manifest bytes equal and JUnit path matches; agent-SHA-only poison exit 1, zero calls, no materialization.
- `/home/user/work/venv-agent/bin/ruff check --no-cache` on the four packet drivers — PASS.
- `/home/user/work/venv-agent/bin/mypy --cache-dir=/tmp/.../mypy-cache --follow-imports=skip --ignore-missing-imports` on the four packet drivers — PASS.

Exact final packet hashes:

```text
measurement-command.sh  cc16a840e049cfbabaa662b175cf094eba10af871bb166123a5339741adbc6d8
service-row.txt         81ee29eebf05bb687c39449ca8551a6fde19340055d5472c54f9d493dbe3f43a
positive.manifest       5a4d5640ff927e0c3b4d7d1ad19ecc40e77fcf6298a173d822e8b3dfe5c0d643
poison.manifest         222693fc9fb9b8a9abc5620c6f49eb1b872dd8d42a73c38abb8a69b319d3c1fc
```

No pytest, collection, measurement body, request-test, row installation, registration, queue action, dependency installation, or full suite was run. No test outcome, REG/nonREG classification, or ship credit is inferred. The assigned `tmpdir` path was a regular file, so harmless scratch used `/tmp`; no packet or product files were modified.
