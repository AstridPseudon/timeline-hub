## Report

- Restored only `/home/user/work/runtime/contract/artifacts.json` to exact `HEAD` bytes.
- Verified:
  - Regular non-symlink file
  - SHA256: `7c541b705a9dbc0827ed2e81a847455402b1d475491de702cde7ef85f4a8235d`
  - Byte-equal to `git show HEAD:contract/artifacts.json`
  - Main HEAD unchanged: `458595850c354f4403dabc58a72b98bebbc2c3a3`
  - Main `git status --short`: clean
  - Worker worktree: clean
- No tests run; no source changes were authorized or made.
- Commit message written and `DONE` marker created.