# FAIL — OPS-farm-agent-full-v2 review

Packet: `16d707a21b245bfe007188e89dfff011c8706a84`  
Tree: `5df61c127ffb60aa0562ba94b1c7eb5c7f8c9ab0`  
Parent: `1d9ddba546f8fb1300f55ff62607ed492719cbaa`

Findings:

1. `registration-row.txt` contains only `ASTRID_RUNTIME_CHECKOUT` and `PYTHONPATH`. It omits required `PATH`/Node 20.19.4, `ASTRID_REMOTION_PROJECT_DIR`, `ASTRID_NODE_EXECUTABLE`, and `ASTRID_TIMELINE_SCHEMA_PYTHONPATH`. The normal managed registration does not inject these into an unrelated full-suite row.

2. Fixtures use a freshly initialized private Store, manually append the candidate row, and manually construct a separate synthetic environment. They do not execute the real candidate command through `test-run`, nor test the existing Store/full-farm-row update path.

3. README steps 2–3 refuse an existing Store and then initialize one, conflicting with the settled current-store/full-farm-row state and risking refusal or duplicate append.

4. Runtime source selection is honest: `1d9ddba…`/tree `f56c396c…` contains `external_pack_sources.py` (SHA `8931d2ae…`); declared `45c3a7f…` does not. All four canonical client hashes match. However, no authentic checkout, managed profile, normal receipt, or import-origin evidence is available, so publication remains blocked.

The packet was preserved unchanged due to FAIL.

Checks:

- Targeted pytest: `3 passed`
- Manifest SHA verification: PASS
- In-memory compile: PASS
- `bash -n ops-handoff/farm-agent-full-v2/registration-row.txt`: PASS
- Ruff: PASS
- `git diff --check HEAD`: PASS

No live Store, registry, provisioning, installation, dispatcher, full suite, or product files were touched. Status: not publishable.