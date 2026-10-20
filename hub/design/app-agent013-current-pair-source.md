# Agent current-pair source keeper

## Result

KEEP. This worktree is the approved Agent current tuple, with no product,
dependency, generated, install, or package-build changes:

- Worktree: `/home/user/work/wt/app-m3-agent013-current-pair-source`
- `HEAD`: `d8749a9ce12a699672faf3ad96b4e4cbea9245c2`
- `HEAD^{tree}`: `75354d38c898729bac09619679f5421faba319ed`
- Branch: `tl/app-m3-agent013-current-pair-source`
- `PYTHONPATH`: `/home/user/work/wt/app-m3-agent013-current-pair-source`
- Existing Python executable: `/home/user/work/venv-agent/bin/python` ->
  `python3` -> `/usr/bin/python3` -> `/usr/bin/python3.13`

The approved merge is `d8749a9c` (parents `cf7448ed` and `bfaa241c`), not the
`905a4f0f` candidate. I did not relabel `905a4f0f` or move any Agent HEAD.
The worktree was clean at the end.

## Tuple checks

Read and applied the settled decisions in:

- `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/agent-safe-s2-current-adoption.md`
- `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/runtime-current-tuple.md`

The current source contains the exact normal tuple:

- `runtime.lock.json` source commit: `2c4ac180c2220bdad966bc01e95ad230e99ce26a`
- client `0.2.13`
- schema `sha256:8de823011a121359b9ad021e283b45afb6baeabc8a154a02bd086d1260a8b8f4`
- producer artifact `sha256:6f000bc615a9cb24fb00cc69a97af75eae71006ebfe87e3caa272fcdbbb1af56`
- local lock covers 15 files

Agent S2 source proof is exact:

- `astrid/core/timeline/schema/edit-command.schema.json` SHA-256:
  `a6f1aaa9dfcc31828bd04c908158fd7fd9a825df6c9f88f79b81779273a190ef`
- 48 schema definitions and 22 registered operations; no parent/init/word/text
  successor expansion
- Existing composed-source evidence records 973 current targeted checks, 18
  central integration checks, and 26 source guards plus 2 existing strict xfails.

The immutable Composition artifact in this Agent source is version `0.0.12`,
58,444 bytes, SHA-256
`0a7b61529099ce994f807c6d7b1078303a09e7c0219144cc4b07467977f0f1a3`, with 77
regular archive members. Existing theme equality proof remains in
`tests/packs/rendering/test_presenter_scene_capability.py` and
`tests/packs/rendering/presenter_scene_capability.mjs`: the test serializes
Agent `BUILTIN_DEFAULT_THEME` and asserts `deepEqual(DEFAULT_THEME, ...)`.

## Exact checks performed

```text
git rev-parse HEAD
git rev-parse HEAD^{tree}
PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-agent/bin/python scripts/vendor_lock.py check runtime.lock.json
sha256sum astrid/core/timeline/schema/edit-command.schema.json
git diff --check HEAD
git status --short
```

Results: exact HEAD/tree above; `vendor_lock.py check` passed; schema hash
matched; whitespace and worktree checks passed. Archive hash/member/version
were independently checked with Python `hashlib`/`tarfile` and matched
`0a7b…f0f1a3` / 77 / `0.0.12`.

The prescribed producer checkout
`/home/user/work/wt/rt-m2-pin-2c4ac180` is absent in this sandbox. Therefore
the producer-side `--producer` verification was not rerun here; the exact
Runtime identity and 75-artifact evidence remain as recorded in the two design
docs above and the prior Agent review. No full, browser, socket, TypeScript,
install, or package-build run was made.

## Handoff

App may use this exact Agent source with `PYTHONPATH` set as above for its
current-root browser/CLI gates. Retain the prescribed Runtime checkout path
when available. App qualification, browser/socket gates, and full-suite status
are not inferred from this Agent keeper.
