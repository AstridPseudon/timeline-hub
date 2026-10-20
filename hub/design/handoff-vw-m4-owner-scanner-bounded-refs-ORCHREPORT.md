# Owner scanner bounded-reference correction — v1.0.1

## Result

Corrected the ORCH-only portable scanner copied from the completed v1.0.0
release package. The Agent integration worktree remains clean: no Agent
product/repository files were changed. The v1.0.0 archives were preserved
byte-for-byte; v1.0.1 is a new review candidate and remains HELD pending
manager inspection and Agent canonical-policy approval. No owner data was
used.

The fix validates declared scope, identity, and report-reference fields as
strings before projection output is copied. Malformed object/list/bool/null
references are omitted, produce fixed type errors, and make the report
incomplete or the affected finding unknown. Valid string IDs and pins remain
exact. No container is stringified, no valid ID is truncated, no ID syntax or
timing policy is invented, and exception/value payloads are not reported.
Opaque authored fields remain unprinted and unchanged.

## Artifacts and manifest

| Artifact | Size | SHA-256 |
| --- | ---: | --- |
| `delivery/owner_film_cliplook_scan-v1.0.0.zip` (preserved) | 20,310 bytes | `16b37fad6f3953b547c8d9dbeec914b1dcbf684faa95a71143b5a918eca16656` |
| `delivery/owner-film-viewing-tools-v1.tgz` (preserved) | 15,871 bytes | `fc9d90a4cf2019882ba3dbb6fd4cb38e6193770d14e2e9d1ad279dddd0517308` |
| `delivery/owner_film_cliplook_scan-v1.0.1.zip` | 22,155 bytes | `2cb2a28fc917496128fe63463f11ea8b78b5267a6e6f66afe43826704d052fad` |
| `delivery/owner-film-viewing-tools-v1.0.1.tgz` | 17,765 bytes | `1ed933809f6449cd2893f62a278d1be849ae7c5d45fd752c86c76a58b5c579d7` |

v1.0.1 has this exact sorted flat manifest in both archives:

```text
FILELIST.md
ORCHREPORT.md
README.md
VERSION
owner_film_cliplook_scan.py
reference/extension-ORCHREPORT.md
reference/extension-owner-film-differences-scan.json
reference/predecessor-ORCHREPORT.md
reference/predecessor-owner-film-cliplook-scan.json
tests/conftest.py
tests/test_owner_film_cliplook_scan.py
```

The machine-readable copy is `artifact-metadata.json`; `v1.0.1-source.patch`
is the minimal source diff against the extracted v1.0.0 ZIP member.

## Evidence

- `/home/user/work/venv-agent/bin/python -m pytest -q tests/test_owner_film_cliplook_scan.py --agent-root /home/user/work/wt/vw-m4-owner-scanner-bounded-refs` — **18 passed** (the prior 10 cases plus 8 bounded-reference/mtime regressions).
- `/home/user/work/venv-agent/bin/ruff check owner_film_cliplook_scan.py tests/test_owner_film_cliplook_scan.py tests/conftest.py` — **passed**.
- `/home/user/work/venv-agent/bin/python -B -m py_compile owner_film_cliplook_scan.py tests/test_owner_film_cliplook_scan.py tests/conftest.py` — **passed**.
- Relocated CLI with `env -i PATH=/usr/bin:/bin PYTHONNOUSERSITE=1`, explicit
  input/Agent root/output, and synthetic valid, unknown, incomplete, and
  malformed-reference closures — **passed** (`complete`, `complete`,
  `incomplete`, `incomplete`; marker absent from output).
- Final ZIP extraction: the extracted test file passed **18 tests**, and the
  extracted CLI rejected no valid path and emitted an incomplete report for a
  malformed-scope fixture without the nested marker.
- Rebuilt ZIP and flat TGZ twice from the same source — **byte-identical**
  metadata/digests on the repeat build. ZIP/TGZ timestamps, order, uid/gid,
  and mode metadata are deterministic.
- v1.0.0 digest recheck — **passed**; hashes above are unchanged.
- No full, browser, live socket, network, install, database, credentials,
  media, render, or real-film scan was run.

## Decisions / handoff

The correction is deliberately a report-boundary sanitizer, not a second
canonical validator: existing Agent projector, clip-field codec, registry,
rational-FPS, and duration helpers remain the semantic authorities. The
README retains the qualified-Agent-Python prerequisite and explicit owner-local
run command. Manager publication is not authorized by this worker; Agent
canonical-policy review is still required.
