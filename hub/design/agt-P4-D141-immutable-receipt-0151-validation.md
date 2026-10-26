# P4 D141 immutable correction validation

Status: `PASS_READ_ONLY_CORRECTION`.

The independent quick check used only Python stdlib (`hashlib`, `json`, `shlex`, `xml.etree.ElementTree`, `pathlib`, and read-only `git` subprocesses). It did not import product code, collect tests, open sockets, rerun controls, run a body, install a kit, or alter a registry.

Checks passed:

- SHA-256 hashes matched for the 10086 request, status, summary, snapshot, external-version record, raw service log, retained 0055 manifest, runmanifest, argv, request-id, raw body log, XML, exits, and source before/after/final receipts.
- The retained normal manifest and runmanifest both preserve the original declared 0047 XML path and hash to `67ef4348…e5b9f` and `86595e66…04dc71`; the 0047 XML is absent.
- The actual production argv is `run -- -m pytest ... -m integration` with exactly the three original concrete selectors and `--junitxml` bound to the retained 0055 `body-evidence/p4-d141c.xml`.
- XML parsing found one suite, the three concrete selector/module-name mappings, `tests=3`, `failures=0`, `errors=0`, `skipped=0`, and `time=23.668` seconds.
- The recorded qualified source paths reproduce the frozen Agent/Runtime/App/Composition commit/tree tuple and are clean. The 10086/controller-0105 before/after/final source receipts are retained and byte-hashed; no source controls were rerun.
- 10086 is distinct from historical 1347 (`fail`, exit 1, zero selectors, no JUnit). Queued 19479 remains `queued`, has no exit or XML, and was not started or touched.

This file records a metadata binding only. It does not convert the retained 0114 custody `FAIL` into a new body result, does not substitute the later 0119 manifest, and does not make a P4 GO. App owns the cumulative verdict.
