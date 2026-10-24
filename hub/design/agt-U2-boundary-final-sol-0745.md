Repaired all three findings within the two allowed files:

- Restored the sixth original `future.result(timeout=5)`.
- Moved claim refusal into an unconditional pre-activation probe using a real enabled, registered Runtime client. It observes `remote_activation_missing`, no attempt ID, zero stored attempts and a queued task.
- Patched abort’s actual `terminate_group()` seam. Four cases verify retained-handle identity, no signaling, primary-exception preservation, uncertainty, bounded child exit and cleanup of a real matching ready marker.

Everything outside those two files remains exact `5783`, preserving the reviewed source union, production guards, custody and commit transport.

Validation:

| Command/check | Result |
|---|---|
| Central `authoring-current8ea-nodes`, five selectors; exact invocation in [service summary](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/tests/agt-U2-boundary-final-sol-0745-authoring-current8ea-nodes-1024074903-21347/summary) | **8 passed, 1 setup error** |
| `pytest -q -oaddopts= -pno:cacheprovider --timeout=45` on the three named startup-budget/capacity authority controls | **23 passed** |
| `pytest -q -oaddopts= -pno:cacheprovider --collect-only` on both allowed files | **628 collected** |
| In-memory `compile()`; Ruff comparison against `5783` | PASS; unchanged diagnostic identities: **247 + 3**, zero new |
| Original bounded-future AST inventory | **6/6 retained** |
| `scripts/vendor_lock.py check runtime.lock.json --producer /home/user/work/wt/rt-pin-45c3a7f4` | PASS |
| `scripts/artifact_manifest.py --check`; `git diff --check`; outside-two-files comparison | PASS |

The D18 selector failed **before its body ran**: the existing private generated-client loader cannot resolve Runtime’s relative import. That fixture remains unchanged; capacity-test execution is unverified. No full suite or external activation/render body ran. Full Ruff/mypy gates were not repeated because the relevant source scopes and diagnostic identities are unchanged.

Commit message and `DONE` written. Ready for independent HARD re-review; home integration remains pending PASS.