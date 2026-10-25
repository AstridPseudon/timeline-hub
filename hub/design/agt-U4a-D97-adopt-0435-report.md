Implemented U4a D97 tool-only adoption.

- Updated only `runtime.lock.json`: Runtime pin `6634a17f…` → `0c62dfa63db9…`
- Runtime HEAD/tree: `0c62dfa63db9…` / `e22cdd54b668…`
- Lock SHA256: `54c4baf…` → `7c16b70…`
- Generated artifacts: unchanged; only lock diff

Checks:

- `refresh_runtime_client.py`: exit 0
- `vendor_lock.py check`: exit 0
- `artifact_manifest.py --check`: exit 0
- `git diff --check`: exit 0

No tests, services, installs, or security review run per brief. Commit message and `DONE` marker created.