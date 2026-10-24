## Report

Implemented the P2 fix.

- Added pinned Runtime import bootstrap to `authoritativeParentHashes`.
- Added an extracted-helper subprocess control with `PYTHONPATH` unset.
- Verified old helper: `ModuleNotFoundError`.
- Verified new helper using `/home/user/work/venv-agent/bin/python` and Runtime pin `732c48c6`; canonical hash computation passed.
- Payload mutation changes both digest and revision outputs.

Tests passed:

- Focused Node controls: 3/3
- TypeScript node/app typechecks
- Scoped ESLint
- `git diff --check`

Protected source proof:

- Before: `f2d63c703ba506b52dfd8bb0ebaee56ed3f1f58600650c36f09ceaa76a154d10`
- After: `d68b773a14eccb287fa907c1bde80fb6987c74839e3b869670555a5811534562`
- Removing the single import line restores the exact before hash.

No browser/original/full suite was run, as instructed. Commit message and `DONE` marker are present.