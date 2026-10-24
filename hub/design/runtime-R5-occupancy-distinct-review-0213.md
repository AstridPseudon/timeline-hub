## Report

Verdict: **PASS for reviewed fixture delta; R5 full occupancy remains HELD.**

- Commit: `fad2ddd1eb84f73a2155590ade81a7c51ec50695`
- Tree: `864e1d5ee865902fb545095be6de3e989e36f0c7`
- Delta from `51c2d6aac`: 1 file, `+41/-5`; worktree clean.
- No product/schema/client changes.

Checks:

- Exact targeted pytest: **3 passed in 8.41s**
- Ruff (`/home/user/work/venv-agent/bin/ruff check tests/test_timeline_legacy_occupancy.py`): **passed**
- Pyright: final **0 diagnostics**; original `458595850` baseline had 20; **0 new normalized identities/multiplicities**
- AST/property mapping: **passed**
- `git diff --check`: **passed**

Verified:

- Full HTTP status/code/message/details refusal tuple.
- SQL dump, CAS/head, owner shot, owner item, and receipt no-write invariants.
- Distinct missing-head inputs: retained `shot-revision:<revision>` versus new `shot:shot-1` root input.
- All other cases unchanged from `51c2d6aac`.
- Historical-reuse cases remain unchanged and held.

Remaining scope: Agent’s authenticated cross-timeline historical-shot carrier is still unresolved. No full-16 qualification or merge claim is made.