# R2 registry integrated qualification

## Verdict

**PASS — read-only qualification of the actual integrated Agent tree.** No
product, test, generated, lock, pin, or source files were edited or deleted.

The worker HEAD is `acd93e7114d22237bfc3149c6a1b89cc4c5de360` and its tree is
`738a7e77b26502e377ba32955e5adb8af488beb6`. The reviewed source base is
`22f1cb169bfd0f2aed79910c047581cd970c9541`, with the same tree
`738a7e77b26502e377ba32955e5adb8af488beb6`. `git diff --quiet 22f1cb169b
acd93e7114d` passed, proving the merge is an exact tree reuse of the reviewed
source. The merge's first parent remains the prior integrated Agent head; no
additional source delta was introduced by the merge.

## Final targeted evidence

Both commands used the requested venv and exact Runtime `2a9e347ff0e1df1dedff5ab7b59ddb27dfe3129d` checkout. Full command/output logs are in the worker evidence directory.

| Check | Result |
|---|---|
| `PYTHONDONTWRITEBYTECODE=1 ASTRID_RUNTIME_CHECKOUT=/home/user/work/wt/rt-pin-2a9e347f PYTHONPATH=.:/home/user/work/wt/rt-pin-2a9e347f /home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider tests/editing_conformance/test_recipe_m2_parent_media.py -k "missing_registry_containers_are_guarded_writes_with_exact_inverse_redo and not config"` | **6 passed, 79 deselected** in 1.61s |
| `PYTHONDONTWRITEBYTECODE=1 ASTRID_RUNTIME_CHECKOUT=/home/user/work/wt/rt-pin-2a9e347f PYTHONPATH=.:/home/user/work/wt/rt-pin-2a9e347f /home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider tests/editing_conformance/test_inverse_registry_containers.py` | **41 passed** in 3.03s |

The original selector is the exact six-node author selector; the 79
deselections are disclosed. No whole 85, neighboring 14, nested 8, SDK four,
c271, public redo, original 9, full, P1–P4, browser, 40, 281, or 58 suite was
run.

## Identity, origins, and integrity

- Normal producer Runtime: `34eac0041b0891e9011966b39bcbd26053fde5bc`, matching
  `runtime.lock.json` and passing `vendor_lock.py check ... --producer
  /home/user/work/wt/rt-pin-34eac004`.
- Execution Runtime pin: `2a9e347ff0e1df1dedff5ab7b59ddb27dfe3129d`.
- Source `inverse.py` SHA-256: `00c19d53ecc7d5b3940906ad16cabf9cb1d07335feda0012d5faf038dd87b01f`.
- Imported Agent modules resolved from this worktree; imported Runtime modules
  resolved from `/home/user/work/wt/rt-pin-2a9e347f`. The before/after probe
  hashes were identical, including `inverse.py`, `_command_state.py`,
  `commands.py`, `commit.py`, `runtime_protocol/__init__.py`, and
  `runtime_protocol/platform.py`; see `module-origins-before.log`,
  `module-origins-after.log`, and their zero diff status.
- Protected source, test, `runtime.lock.json`, and `artifacts.json` hashes all
  equal their `22f1cb169b` values; see `source-tree-audit.log`.
- `vendor_lock.py check`, `vendor_lock.py check --producer`,
  `artifact_manifest.py --check`, `git diff --check`, and clean worktree checks
  passed.
- The independent review on the exact same tree remains reusable without
  repeating broad lanes: Ruff **2149 = baseline 2149**, mypy **1912 = baseline
  1912**, tools/vendor/artifact/diff checks passed, and its credential scan found
  **0 matches across 1459 files**. This reuse is justified by the exact tree
  identity above; the original review evidence is
  `workers/agt-R2-registry-review-1758/evidence/`.

## Scope and limits

This proves the requested integrated Agent source and focused registry inverse
behavior. It does not claim a live public Runtime or full-suite qualification;
the focused provider tests retain their detached/test-fixture boundary. The
settled C0 request/reply contract, existing coalescer, guarded whole/selected
inverse path, no-write behavior, and normal pins were unchanged.

Evidence logs: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-R2-registry-integrated-1805/evidence/`.
