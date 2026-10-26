# OPS D141 measured-trace validation

## Source and static checks

| Check | Result |
|---|---|
| Frozen candidate commit/tree | PASS — `159acdc84eb953f617697b753156dc69c787acf8` / `7b9a54111ada389c601363d91a1de8089ab92a8b` |
| `bash -n ops-d141-measured-floor/bin/test-run` | PASS |
| Python AST parse of all five control modules | PASS |
| `ruff check ops-d141-measured-floor/controls/*.py` | PASS |
| `git diff --check 635f4de06f 159acdc84e` | PASS |
| Candidate worktree status | PASS — clean after removing only the AST-generated pycache file |
| `shellcheck` | UNAVAILABLE in environment |

## Real isolated control run

`python3 -I ops-d141-measured-floor/controls/real-controls.py` exited 0 and printed a complete PASS result. It exercised candidate subprocesses in a temporary root, including D141g, D141h with `full-d141-pristine-targeted15`, synthetic P5, measured equality/above/below, default floors, global 4.5GB guard, one-heavy occupancy, malformed `df`, duplicate JSON, path/hash/symlink rejection, failure cleanup and cancellation cleanup. It did not touch the live queue or invoke `--run`.

The PASS is control-mechanics evidence only. Its held-ID controls used bare synthetic `8912` and `19479`, so they do not qualify the real caller.

## Exact full-ID caller checks

Using the same candidate subprocess harness with actual normal-caller-shaped IDs:

1. `rt-pin-fa9cd546-full-d141-pristine-1026005231-8912` admitted and reached `pass`; required result is held/refused.
2. `agent-p4-current-becfe-http-3legs-1026012948-19479` admitted and reached `pass`; required result is cancelled/refused.
3. `runtime-d141-p5-cut-1026013331-6934` with `P5-service6934` receipt returned `3` and rejected `P5 decision is not bound to service 6934`; the exact full ID must be the only accepted P5 binding.

These are private temporary-root subprocess checks, not live requests or product proof.

## Contract/source conclusions

- Default light/core/heavy floors and strict/inclusive boundary behavior are unchanged; measured receipts make the measured floor inclusive while preserving the global `<= 4.5 GB` stop guard and 4.0 GB stop line.
- Receipt validation is strict on duplicate keys, types, integer arithmetic, owner/group, regular/no-follow paths, hashes, source head/tree, suite command, scope and authorized decision.
- D89d explicitly records start/end bracket semantics rather than asserting a continuous peak. Heavy traces independently bind job/body/source/times and retain first/periodic/final raw rows.
- The corrected supported Runtime targeted-15 suite name is `full-d141-pristine-targeted15`. The source-prep shorthand `full-d141-targeted15` is not the candidate allowlist name. The existing central `full-d141-pristine` row remains the old queued 8912 row.
- The separate targeted-row validator fail-closed issue belongs to Luna0247 and is intentionally not duplicated in this review.
