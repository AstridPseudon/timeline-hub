# P4 D141l owning receiving validation

## PASS_OPERATIONAL_SOURCE

- Read the settled `PLAN.md` and normal ORCH `design/commit-v2.md`; no contract or product decision was changed.
- Verified the four clean integration homes and exact SHA/tree/parent/origin tuple in `source-manifest.json`.
- Recomputed the supported profile lock, Composition archive, registry, Runtime lock, Node version, launcher and installer hashes.
- Preserved the single selected CLI test and unchanged three-test aggregate guard. Candidate argv retains `run -- -m pytest -q -o addopts= -p no:cacheprovider --timeout=45 -m integration` and one durable future JUnit path.
- Ran the unchanged production launcher in `run` mode with a fresh manifest: preflight `0`, stub-only body `17`, counter `1`; launcher materialization hash equals the separate input manifest hash.
- Ran the Agent-SHA-only poison through the same launcher: exit `1`, `D73 launcher: agent SHA mismatch`, counter `0`, no body receipts.
- `check-source.py` checks current source bytes, profile custody, source origins, manifest/materialization identity, selector row, and the no-body boundary. It does not import pytest or request/install a suite.
- No repository files, test files, pins, profile files, registry, CAS, service rows, or shared dependencies were modified. No pytest, collection, request-test, install, body, or JUnit XML was run.
- `git diff --check` and JSON parsing are final checks; product types/lint are N/A because this is operational-only.

The named P4 admission remains unresolved for any later body: the native named row is currently LIGHT/floor `5000000000`, while the recorded controller derivation is `4714564096`; this worker installed no override and assumed no forced run. Original controller/source receipts, hosted path failure, and held `19479`/`8912` remain untouched.
