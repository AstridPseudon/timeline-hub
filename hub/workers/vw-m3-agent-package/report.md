Implemented the scoped migration: pinned the reviewed local 0.0.8 tarball, moved registry generation into host staging, passed instance-scoped maps to Composition, and replaced default stubs with shared imports. All **77 installed package files remained byte-identical** after generation and bundling. React 18.3.1 and Remotion 4.0.509 peers deduplicate.

Validation passed:

- `npm ci --prefix remotion` with the pinned toolchain.
- `npm run typecheck --prefix remotion`.
- Main-config bundle.
- Focused Python selection: **243 passed, 7 deselected**.
- Installed-package integration: **1 passed**.
- New cache checks: **2 passed**.
- `git diff 8c4bd850 --check`.

Exact commands, file selections, results and the conventional commit message are recorded in [commit-msg](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-agent-package/commit-msg).

**Remaining blocker:** the out-of-scope `scripts/reshape/remotion_gate.py` still requires npm schema/theme packages. Its probe fails on missing `timeline-schema`; the requested ownership grant was not received.

A wider targeted run also exposed four unchanged real-render tests refusing admission without launch validation; no independent baseline is claimed. Browser smoke, full suite, film/theme comparison and audio parity remain unverified. Next: remove the stale gate requirements, then run qualified central checks after integration. No evaluator-math migration was included.