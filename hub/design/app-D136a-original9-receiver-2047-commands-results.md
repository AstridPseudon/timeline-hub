# D136a preparation commands

| Command/check | Result |
| --- | --- |
| `git status --short --branch` | PASS; clean base branch at `3082cad490ce1cee764ff137f99cb791a67ddd08` |
| Candidate object/blob inventory via `git show`/`git rev-parse` | PASS; candidate `c99214a227154df5fbaf681c2e0fc52c54500025`, tree `515fca228e943e35ef2d58b5de1300aedbd9fc60`, exactly three approved paths |
| Base tree inventory | PASS; tree `84e9d485a7ee8fdf2969eaf19d159e400f0ca1d4` |
| Held D100 and projection SHA-256 inventory | PASS; full 64-character values recorded |
| Retained own9 selector inventory | PASS; 9 selectors recorded, no raw XML/log exported |
| Runtime final-2034 PASS publication check | NOT READY; no qualifying publication found |
| Candidate import onto base | NOT RUN; gated by Runtime final-2034 PASS |
| original9 behavior run | NOT RUN; gated by Runtime final-2034 PASS |

The future exact command is intentionally recorded only as a gated recipe: `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=<ownsource>:/home/user/work/wt/rt-pin-ab1e4f61 ASTRID_RUNTIME_CHECKOUT=/home/user/work/wt/rt-pin-ab1e4f61 /home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider --timeout=45 --junitxml=<private-own9.xml> <same-nine-selectors>`.
