# D118d facts

- The assigned file is unchanged from Agent HEAD `20177e66564f9f91735ed1a11bac821682d60edf` (tree `68433c5f77be90063b1f43d3e8f1407346a50675`), SHA-256 `6a0787475f0b032500e769379a2e3f556a4ba5cabc07fa3996350200083a1284`.
- The retained pre-setup-fix source is SHA-256 `37a57c0de8bb9e2a5911fa0f833dae4dccd4adb479f886848548695cdc3382d0`. Commit `7d85895ba18637231adc12fc0130f51f8be96608` already applied the causal setup-only fix: the archive locator uses an environment override with the exact authenticated archive fallback instead of requiring the environment variable.
- The archive exists at the fallback path and hashes to the asserted `2915bd4ac0d46954d19c30f87a517b82074218699978e650fab03fcba81b72d3`.
- The current genuine setup registers `create_runtime_commit_service()` on `RuntimeService` and uses the real service transport. No production/shared fixture/auth/store/emitter source is touched.
- AST comparison: all seven test functions are identical to the retained pre-setup-fix source. Only the `reader` fixture setup AST differs, and the difference is limited to archive selection. No authored input or assertion changed.
- Own-node execution was not permitted: free disk was `4,832,747,520` bytes, below the required `5,000,000,000`-byte floor. The exact 16 retained node IDs are listed in `facts.json`.
- Frozen upstream924 tip is `92443771676ef2bbb547d0a103d708fa8bec4c63`; the assigned file is absent there. The requested short object `d11417a59` is unavailable in this repository.

Conclusion: no further supported source-only change exists in the assigned file. The existing baseline already contains the causal setup correction; adding another change would duplicate or risk altering the retained behavior.
