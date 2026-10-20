Implemented the 161-line helper/CLI with catalog readiness and guarded cleanup. Viewing’s handshake, full report, and both commit messages are written.

Validation:

- `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=$PWD /home/user/work/venv-agent/bin/python -m pytest -q tests/packs/rendering/test_real_pack_host.py` — **6 passed, 1 deselected**.
- Central `real-pack-host-integration` — **1 passed, 6 deselected in 56.50s** on final source, proving real startup, catalog readiness, cleanup, and Runtime survival.
- Focused Ruff and `git diff --check` passed.

Decision: calls production `ensure_pack_host` directly because DirectHarness lacks neutral-launcher catalog state. No product changes or credential elevation.

App/browser/render parity remains unverified. Next: Viewing wires its wrapper. Branch held; no merge requested.

[Full report and exact central commands](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-m2-real-pack-host-helper/notes/report.md)