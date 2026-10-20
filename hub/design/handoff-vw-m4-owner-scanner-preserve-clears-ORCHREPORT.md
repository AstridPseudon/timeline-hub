# Portable owner-film scanner delivery report

## Result

Prepared the held version `1.0.2` review candidate from current Agent
integration `b46140036`. The Agent repository remains unchanged; all scanner
files and artifacts are ORCH-owned handoff files. The candidate contains the
same bounded three-category scanner as v1.0.1, with the whole-document
reference walk removed and one projector regression for an explicit
`clips[0].asset = None` clear.

The actual Agent projector accepts and preserves that clear. The scanner now
lets that projector/codec decide authored validity, retains exact valid string
IDs, omits non-string containers only at emitted report boundaries, and uses
fixed errors for malformed required scope IDs. Optional authored null/clear
values are not rejected merely because their field resembles a reference.
No second canonical validator, ID syntax, truncation, timing policy, or
authored-data rewrite was added.

The candidate remains held pending manager review and Agent canonical-policy
approval. No owner-film closure or production data was supplied.

## Minimal diff

Against the completed v1.0.1 source, v1.0.2 is **9 additions and 73
deletions** in the scanner: the version, required top-level scope/revision
sanitization, and removal of the prior whole-document
`_validate_closure_refs` walk. The tests add **20 lines** for one
projector-backed clear regression. The v1.0.1 source patch and metadata remain
preserved outside the new archives. The earlier v1.0.0 and v1.0.1 archives and
metadata were copied byte-for-byte and were not overwritten.

## Verification

- Baseline regression before the fix:
  `/home/user/work/venv-agent/bin/python -m pytest -q delivery/tests/test_owner_film_cliplook_scan.py::test_projector_and_scanner_preserve_explicit_optional_asset_clear --agent-root /home/user/work/wt/vw-m4-owner-scanner-preserve-clears`
  — **1 failed**, with `asset reference must be a string`, while the direct
  projector assertion passed.
- Targeted package tests:
  `/home/user/work/venv-agent/bin/python -m pytest -q delivery/tests/test_owner_film_cliplook_scan.py --agent-root /home/user/work/wt/vw-m4-owner-scanner-preserve-clears`
  — **19 passed**.
- Lint:
  `/home/user/work/venv-agent/bin/ruff check delivery/owner_film_cliplook_scan.py delivery/tests/test_owner_film_cliplook_scan.py delivery/tests/conftest.py build-release-v1.0.2.py`
  — **passed**.
- Syntax:
  `/home/user/work/venv-agent/bin/python -B -m py_compile delivery/owner_film_cliplook_scan.py delivery/tests/test_owner_film_cliplook_scan.py delivery/tests/conftest.py build-release-v1.0.2.py`
  — **passed**.
- Relocated CLI from a stripped environment with the qualified Agent Python,
  explicit Agent root, and synthetic valid/unknown/incomplete/malformed-scope/
  explicit-asset-clear closures — **passed**. Results were `complete`,
  `complete`, `incomplete`, `incomplete`, and `complete`; valid output kept
  `[30000, 1001]` and all three categories, malformed scope emitted no marker,
  and the explicit clear emitted no asset type error.
- Deterministic ZIP and flat TGZ rebuilds, extracted relocated tests, member
  manifests, bare SHA-256 files, and preservation checks for v1.0.0/v1.0.1 —
  **passed**; exact values are in the external `artifact-metadata.json` and
  preserved `v1.0.0-artifact-metadata.json`/`v1.0.1-artifact-metadata.json`.
- Full, browser, live socket, network, install, database, credentials,
  media, render, service, and owner-film scans — **not run by instruction**.

The package never writes the input closure and retains same-path, symlink,
hardlink, and atomic-output protections. The README retains the qualified
Agent Python prerequisite and owner-local command. The manager must inspect
the candidate and obtain Agent canonical-policy approval before publication
or any real owner-film run.
