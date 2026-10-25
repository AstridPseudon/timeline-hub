## Report

- Ran exact immutable D73 proof for source `b415a427…` with Runtime `6634a17f…`, App `24865fa2…`, Composition `635f4de0…`.
- Mandatory 8 selectors only; optional 5 held because their bindings were not independently verified.
- Controls:
  - `bash -n`: exit 0
  - Valid positive control: exit 17, body exit 17
  - Poison control: exit 1, zero body bytes
- Proof command used `pytest -q -n 3 -o addopts= -p no:cacheprovider --timeout=45`; preflight exit 0.
- Result: **NO-GO** — 6 failures, 2 setup errors, body exit 1.
  - Parent tests: `provider dependency union omits a captured read`
  - Word tests: `clip.add v1 does not support on`
- XML, command, logs, manifests, imports, tuple/source/profile receipts preserved under `evidence/` (416 KB).
- Worktree unchanged. `commit-msg` and `DONE` created.

Unverified: same-ID-after-restart behavior was not separately exercised after the failed body; no optional selectors were run.

Next step: resolve the Runtime/Agent incompatibilities, then request a fresh proof.