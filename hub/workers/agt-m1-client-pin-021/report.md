Implemented the approved Runtime 0.2.1 pin.

- Updated generated client metadata/types and [`runtime.lock.json`](/home/user/work/wt/agt-m1-client-pin-021/runtime.lock.json).
- Pinned source: `6489e47e5d3efc996e9f92cc2fffcb831cc39a24`.
- Schema digest: `sha256:4e52f7df017db99483ffcd0c593ce414b6443d5d0214ada943bb26fdfcc1714d`.
- Manifest version: `sha256:82db7dfef7e6a09af94b78de384f672f9c202f4d3c80d1128775cfab1ddb4acf`.
- Compiled timeline schema remained byte-identical.

Tests:

```text
pytest tests/test_vendor_lock.py tests/stage1/test_vendored_workspace_client_parity_luna.py
29 passed

Typed import/signature/envelope smoke
passed

git diff --check
passed
```

No API mismatch remains after pinning. The prior handshake mismatch was the expected old-client `0.2.0` versus Runtime `0.2.1` digest refusal.

Updated `m1-agent-coordination.md` and wrote the harness commit message. Full/socket suites were intentionally not run per task instructions.