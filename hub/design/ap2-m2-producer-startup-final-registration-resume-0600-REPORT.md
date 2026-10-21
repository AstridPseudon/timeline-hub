# App M2 producer startup final-registration resume — 0600

## Result

BLOCKED at the required first central run. No startup smoke or producer actual
was run after the first failure; body count is 0.

## Registration/custody

Created owned gate:
`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-producer-startup-final-registration-resume-0600/producer-startup-final-custody-gate.sh`

Gate SHA-256:
`0e39303a1deebadeaeeaf1b7336e71c2ee9f55107452d86094ed74b2a2678282`.
It binds keeper `b8cc7e1c79ec5516b9eee3832b5c33d62dac1aa7`, tree
`fd16d32fd3487e56c9fe1ff16582dba240f63b77`, wrapper
`329cfca7ff6fcc6764e5eaa6cb53ba77a40e6aa842361d0ed6795ca5b4398352`, body
hashes `d91d0c1cce22f68119cd30fcb0a288346474b0ad4b64c84dcee3b730fa468d89`,
`50cbe5341f24c9a1ecc999018e2c6d975380a3440570abce151f9173c9752016`,
`5b880ceff883abce2575a3a85aaa4eda69d3bcb848768ff0e91f337d50cca4c0`, Agent
`8130a401bf44a518d5a40ae274d398b8c560be55`, Runtime
`2c4ac180c2220bdad966bc01e95ad230e99ce26a`, probe
`4beb7c22dfa06e04d28253dbab02f76ff2a9953f0accd4b12247514e4f0608f6`, and
tsx executable/CLI/loader/package bytes
`8729ecfb90d9d568939e4190e6f1d3317c946583b7d37a776e0c23a21c021cf8`,
`8729ecfb90d9d568939e4190e6f1d3317c946583b7d37a776e0c23a21c021cf8`,
`0b1c5b86192772fe9257710e739959cee5947c11ae1f93b61abfaa9b80c6def1`,
`6e764b21991c21595441f82387c1451ccd10a3e7a3f0973cc5e3649a12dea7d2`.

Registered suites: source preflight, startup smoke, dormant list, dormant actual.
The worker metadata now targets this worktree; no App source, guard, pin, caller,
probe, shared dependency, or original gate was changed.

## Central result

Command requested once:
`request-test integration:app ap2-m2-producer-startup-final-registration-resume-0600-preflight`

Local custody syntax check:
`sh -n .../producer-startup-final-custody-gate.sh` — PASS.

Result:
`app-ap2-m2-producer-startup-final-registration-resume-0600-preflight-1021060243-6364`

It failed before the source gate: `integration:app` ran against App tree
`4a5d7fd943a8ca6ef64ee7cf645c57784432a2dc`, not the required `fd16d32f…`.
The final custody gate therefore rejected the service root. No retry was made.

## Remaining prerequisite

Run the registered preflight once through the worker-scoped target, then one
startup-only smoke through that same exact source. Only after both pass may the
separate original producer actual be considered. No producer actual is qualified
by this record.
