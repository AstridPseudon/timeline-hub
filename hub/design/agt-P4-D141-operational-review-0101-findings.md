# P4 D141c independent operational source review

Verdict: `FAIL`

## Decisive findings

1. The corrected 0055 candidate is not installed. Read-only inspection of the active `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/tests/suites.conf` shows row SHA-256 `d58f649a2e48994501766c28fdb9ab4d08a21cfe12543e81af70f5f69e1459f9`, exactly the old 0047 row. The corrected candidate in `evidence/candidate-row.txt` is SHA-256 `21f407285a7f1476e9507add8d8d54e723776d6ce5074ac7cbbe8be5773c2f0b` and is not equal to the active row.

2. The active row still has `run -- -m integration` and therefore omits the required `-m pytest` interpreter module. It also sets both `P4_D73_MANIFEST` and `P4_D73_EVIDENCE` under the same 0047 evidence directory, so launcher materialization targets the input manifest itself. The preserved actual service `agent-p4-current-becfe-http-3legs-1026005145-1347` records the resulting `cp ... are the same file` failure, exit 1, zero selectors, and no JUnit.

The source-level correction itself is present and locally qualified: the candidate parses as `run -- -m pytest ... -m integration`, retains the three exact original selectors, timeout 45, `-o addopts=`, `-p no:cacheprovider`, and JUnit under its durable body-evidence directory. The copied normal manifest is byte-identical to the registered 0047 manifest (`67ef4348b4b77eb02b74abe20ad6fefdb075f980dc8ca563c0a3c79d1f0e5b9f`). The four frozen source pins, parents, trees, launcher hash, installer hash, and clean source worktrees all match.

## Production-run controls

Using only the approved stdlib stub through the unchanged production launcher in the final `p4-d141c-normal` destination:

- positive `run`: preflight 0, stub exit 17, counter 1; copied manifest hash equals input;
- agent-SHA-only poison `run`: exit 1, counter 0, `D73 launcher: agent SHA mismatch`;
- input/materialized manifest: distinct realpaths, `samefile=False`, distinct inode, neither symlink;
- `bash -n tools/p4-d73-pinned-launch.sh`: pass.

These controls did not run pytest, imports of product code, collection, provider, sockets, or any original body. They do not repair the active registry and do not grant behavior credit.

## Historical conservation

The 1347 service failure remains unchanged and is referenced by its original result/log and SHA-256. No source, test, launcher, guard, schema, kit, pin, registry, shared dependency, or original evidence was modified by this review.
