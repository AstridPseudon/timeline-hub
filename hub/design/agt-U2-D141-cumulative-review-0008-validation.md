# Validation record

## Source and provenance

| Check | Result |
|---|---:|
| Exact candidate | `b4eb5db76fda523407b90a9dbe820f4e20cc1f1d`, tree `2ebe2ddf5a61f013953ab1e21d51ebaab746e58a` |
| Ancestry | PASS: upstream `8b6ed211…` and `c585cb2…` are ancestors |
| Cumulative scope | PASS: only `artifacts.json`, `runtime.lock.json` vs `aa5a91…` |
| Outside generated blobs | PASS: 0 mismatches across the remaining tree |
| Reused source conservation | PASS: prior 2357 proof, 19 upstream-only / 922 current-only, zero mismatches |
| D100a blobs | PASS: `09cbeedd…` / `39ed571d…` exact |
| `git diff --check` | exit 0 |
| Conflict markers | none |
| Worktree | clean committed index |

## Normal generated/provenance tools

- `PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-agent/bin/python scripts/vendor_lock.py check runtime.lock.json --producer /home/user/work/wt/rt-pin-6a011d58` — exit 0.
- `PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-agent/bin/python scripts/vendor_lock.py check runtime.lock.json` — exit 0.
- `PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-agent/bin/python scripts/artifact_manifest.py --check` — exit 0.

The clean producer receipt is `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/queue/done/checkout-runtime-6a011d58e69173d70e2e9bb3ac434ac8f9e87d8d`.

## Targeted tests

- Agent profile verification: `zod` 4.4.3 at the immutable
  `/home/user/work/runtimes/agent-remotion-current/node_modules`.
- `bun run check:chat-bundle` — exit 0.
- `bun test ./astrid/chat` — exit 0; 200 passed, 0 failed.
- Required Python file set, exact integrated Runtime pin, one run — exit 1;
  476 passed, 61 failed, 73 errors, 1 skipped in 495.85s.
- Reused unchanged `node --test remotion/tests/am-footage-cover.test.cjs` —
  prior exact-source PASS, 1/1.
- Reused exact-source parent inventories: Ruff 574 and Mypy 168 inherited
  findings; no whole-repo rerun.

Private raw evidence:

- `/tmp/agt-U2-D141-cumulative-review-0008/python-targeted.log`
- `/tmp/agt-U2-D141-cumulative-review-0008/targeted.xml`
- `/tmp/agt-U2-D141-cumulative-review-0008/bun.log`
