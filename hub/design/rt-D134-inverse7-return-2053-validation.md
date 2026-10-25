# D134 inverse7 bounded source-first return

## Result

Applied the single approved D120 correction in the exclusive assigned test:
the strict Agent source identity guard now selects current normal-home Agent
commit `a30e74e901a28b39c28facba3deb00d76f186e23` and its exact current
`commit.py`/`inverse.py` hashes. The historical Runtime source receipt remains
exactly pinned to Runtime commit `6634a17f3ffd885567ba3c91b6c7a560df7375a4`.

The seven original inverse node IDs and their bodies are unchanged. The AST
predicate map records every parameter input, call input, raises context and
assertion before and after. The only source change is four module-level
identity literals (Agent commit plus two Agent file hashes; Runtime unchanged).

Original FAIL packets were not overwritten:

- `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-D134-inverse7-source-2045/evidence/`
- `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-D134-twelve-protected-review-2046/evidence/`

## Exact source tuple and hashes

- Parent Agent commit/tree: `a30e74e901a28b39c28facba3deb00d76f186e23` / `ece8e0887e48e45cb1fce85b1256c49a0f6126c0`.
- Current Agent origins: normal current worktree `/home/user/work/wt/rt-D134-inverse7-return-2053`; no private U2 ancestor.
- Current Agent `astrid/sdk/timeline/commit.py`: SHA-256 `2b81e46ac0f3553d1de812cf0533be2a9aecbd8cdfcaab118ac671eff75107b3`.
- Current Agent `astrid/sdk/timeline/inverse.py`: SHA-256 `6c794734cb763c21cec386f764bc63b94f3a74b4dd9f8464136a285c628d0423`.
- Retained historical Agent authority: commit `bd3c95b1cebe3bf27c4a82919e5839efb37519db`, tree `e928423ce87e62959b458afca1d62da172271c9c`; its source hashes remain recorded in the original packet and were not selected as current.
- Retained Runtime source: commit `6634a17f3ffd885567ba3c91b6c7a560df7375a4`, tree `47b376717ce7a919a697c62133de3e74dc9f6d3a`, from `/home/user/banodoco/banodoco-workspace-runtime` immutable Git objects.
- Runtime `runtime_protocol/timeline_commit_auth.py`: SHA-256 `4ac2b8792fe0389afb6eb710a348c35fa196131a13cab175bd3646f7d2cc0aeb`.
- Runtime `runtime_protocol/timeline_commit_store.py`: SHA-256 `2a68990b180326585b7f0abaf1ee54c8ff9340e83663f17cd1efff1b2bd78a5c`.
- Provider binding remains `use_runtime(commit=6634a17f3ffd885567ba3c91b6c7a560df7375a4)`, which materializes an immutable archive; no mutable Runtime checkout was silently selected.

Changed-path hashes:

- Parent test blob/SHA-256: `b97bd6a6b6da650cd60b48f78a31fabd7471f26b` / `6c02629fded13bbd97a2cd62d5954083c04cbead04a67e6b30df500f2a4fc1f1`.
- Current test blob/SHA-256: `55e7cec5da3463360a4f862986bc28e6a1e39345` / `c578ec36e41ec2d68fe6de8a7d3a443aab8477cbb8492f7cbd786abb9e48ddd3`.

## Static validation

Commands ran against the assigned file only, with private cache paths:

```text
/home/user/work/venv-agent/bin/ruff check tests/editing_conformance/test_inverse_stage_runtime_regressions.py
PASS — All checks passed!

PYTHONPYCACHEPREFIX=/tmp/d134-inverse7-pycache /home/user/work/venv-agent/bin/python -m py_compile tests/editing_conformance/test_inverse_stage_runtime_regressions.py
PASS — exit 0

MYPY_CACHE_DIR=/tmp/d134-inverse7-mypy-cache PYTHONPATH=. /home/user/work/venv-agent/bin/python -m mypy --cache-dir=/tmp/d134-inverse7-mypy-cache tests/editing_conformance/test_inverse_stage_runtime_regressions.py
PASS — Success: no issues found in 1 source file

git diff --check
PASS — exit 0
```

An initial compile attempt using the mandated worker `tmpdir` cache failed
before compilation because that path is a pre-existing regular file rather
than a directory (`[Errno 20] Not a directory`). It was preserved; the private
`/tmp/d134-inverse7-pycache` retry passed.

Read-only source proof also passed: the historical Agent `bd3` and Runtime
`6634` commits exist, and `git show` of all four retained Runtime/Agent source
files reproduced the recorded SHA-256 values.

## Functional status

`df -B1` observed `4,497,645,568` available bytes, below the mandated
`5,000,000,000` functional floor and above the `4,000,000,000` source-only
stop line. Therefore no pytest/provider/body run was admitted, including the
seven assigned node IDs; `originals.xml` was not created. No behavior, product,
Runtime caller, or history qualification is claimed from source checks alone.

## Next step

After an independently protected review, owner intake may run exactly the seven
assigned node IDs once when a fresh light admission reaches at least 5 GB.
