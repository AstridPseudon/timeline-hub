# Root-smoke controller environment fix — blocked reprepare

## Result

The ORCH controller now preserves the manager process's inherited `HOME`. It
requires `HOME` to be present and scopes only the child process's temporary
and browser/cache controls to the per-run staging directory:

- `TMPDIR=.../temp/tmp`
- `XDG_CACHE_HOME=.../temp/xdg-cache`
- `XDG_CONFIG_HOME=.../temp/xdg-config`
- `XDG_STATE_HOME=.../temp/xdg-state`
- `XDG_RUNTIME_DIR=.../temp/xdg-runtime` (mode `0700`)

The smoke invocation, source pin, public10 archive, consumer profile, and
browser grant path were not changed. No product files were changed.

Updated controller SHA-256: `46e7c0dd5c5ccaf3e210556941f76f1c8adfa67190f33f1f434105294fe421a4`.

## Red-before / green-after

Pure test: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-vw-m3-root-controller-env-fix-test.py`.

- Before the controller edit, the test failed (`exit 1`) at the assertion
  that the sentinel inherited `HOME` was preserved; this reproduces the
  `HOME=temp` defect.
- After the edit:

  ```text
  PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-agent/bin/python \
    /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-vw-m3-root-controller-env-fix-test.py
  PASS: inherited HOME is preserved; task-scoped TMPDIR/XDG paths are prepared
  ```

  Exit `0`. The test also checks that all five task-scoped paths exist under
  the supplied temp root and that the runtime directory is `0700`.
- `ast.parse` of the updated controller: passed.
- `git diff --check`: passed; assigned product worktree status: clean.

## Reprepare blocker

The original source worktree recorded by the READY handoff,
`/home/user/work/wt/vw-m3-root-smoke-central-ready`, has already been
removed. The assigned worktree has the exact pinned source SHA/tree
(`5acd7233df676bf42b2086d86cb0a6358398bf5f` /
`66898dd11df74e205af95903651782a29e9886b4`), so it was used read-only for
the attempted preparation.

Preparation could not complete because the borrowed graph at
`/home/user/work/wt/vw-m3-scene-host-plumbing/remotion/node_modules` has
changed since the existing READY snapshot. The old input had 21,495 entries
(21,462 files and 33 `.bin` links); the current graph has 139 links,
including self-referential package links such as
`@babel/code-frame/code-frame -> @babel/code-frame`. The controller's
existing inventory correctly fails closed with:

```text
RuntimeError: symlink cycle: .../node_modules/@babel/code-frame/code-frame
```

The normal prepare command also confirms the recorded source worktree is
missing (`fatal: cannot change to .../vw-m3-root-smoke-central-ready`). No
other graph/worktree was substituted and the shared graph was not modified.

Therefore the old `handoff-vw-m3-root-smoke-central-ready-READY.json` remains
intentionally bound to its old controller hash
`5728411e9254119723ca5af2736f0671b8c9e97b3ffeaf0679195c0eaf947acf`; it was
not relabeled as READY after the controller changed. A truthful source/input
reprepare requires the manager to restore or nominate the exact approved
graph, then rerun `controller.py prepare` and the existing offline verifier.

## Not run

No browser, renderer, localhost/socket, central test service, full suite,
grant, consumer10/12 substitution, or additional old smoke run was made.
