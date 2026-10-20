# Stereo corrected post-commit gate

Verdict: **NARROW_REJECT** for the runnable manager handoff. The exact App
commit and guards are approved by the offline evidence below, but the literal
post-commit launcher path in the handoff points at a recycled worktree, so a
clean committed `--prepare` could not be run without creating a new App
worktree (outside this worker's authority).

## Exact source

- App ref: `tl/vw-m3-stereo-owned-state-guard-fix`
- Commit: `6323b5bd6fdfc1bb680eba6f8a1a46f21acf6adb`
- Parent: `bca5ed45cb741e0cb7ea47ed81baad914dfe983c`
- Tree: `132ed7f49cc42398676c3d32f80d445ca106e9be`
- Eight changed instrument files only; exact patch SHA-256:
  `89832a12796edb0b5f9c748980bf5d7cc8e16b1205cb87b6844c59a7aaf4c171`
- All tracked source: 5,835 files,
  `dc912e773a36c40271b13ab0abdeac6824cef394790d26658952e7c5763630fb`
- Guard input set: 19 files,
  `a75115d344f8e67d94401c144a740700cc82a365d94c03ae776f2c3bfc1adba6`

The committed source retains the admitted Node `v20.19.4` executable and
full hash `43d6cf63f2a460b463eba6b19df5e9a259771c56f11b5130e04178a15bb99490`,
stereo run-mode binding, worker-owned state/cache/discovery constants, and the
native `ffprobe` channels-2 refusal before decode. No channel coercion was
added; the existing mono tone-presence threshold remains unchanged.

## Offline evidence

From an exact temporary archive of the committed source, with only the
readonly private12 `node_modules` graph symlinked:

```text
node --check controller: PASS
node --check analysis: PASS
bash -n setup launcher: PASS
node --test analysis.test.mjs controller.test.mjs environment.test.mjs: 3 passed, 0 failed
Playwright --list: Total: 1 test in 1 file, exit 0
```

The discovered test was the native Chrome155 tab-audio probe. `--list` did not
launch Chrome or run the probe. The temporary source, task temp, and review
state subdirectories were cleaned up; the readonly private graph was not
modified.

Environment identities retained by the committed controller and checked
against the existing READY evidence:

- private12 graph: `4a54ed6f3300cba740b377e3c780f330996ead23147647f9c963ed4dd5bdd7a4`, 32,382 files/links;
- Composition public12: `71b44e67e4eeffb0f904bb3a21e24d12ba06c4b2e41d43592a859aced3bb3139`, 77 files;
- package graph: `c433236a7e8626217be122d71db0bccd980db4c04c03f45d5cf2d5c9c86039fb`;
- Chrome: `155.0.8059.84`, package `155.0.8059.84-1`, executable hash `cb19b59995072b86cc7f887b3b1c7ab1f63518a7f2ed9f0d33249e1a040e2c76`, full tree `5b9b48fad617dc414d4a18ccfe9c7933c7bc4a8efd78c70d4f7a9e853808de0e`, 255 files;
- six Remotion/Player peer hashes are retained in the committed controller and were covered by the environment test;
- resource floor: 12,239,921,152 bytes free at review;
- browser flock: re-entry refused while held;
- fresh task temp: direct `/tmp/timeline-tab-audio-*`, mode `0700`, uid/gid `0/0`;
- controller-visible QUIET guards: absent.

No grant, browser launch, capture, render, network, install, live socket, or
full suite was run. Source pre/post and one-shot marker logic was reviewed in
the committed controller, but not exercised through `--prepare` because the
exact clean worktree is absent.

## Blocker and next step

The handoff command names:
`/home/user/work/wt/vw-m3-stereo-owned-state-guard-fix/tests/e2e/timeline/setup-tab-audio-capture.sh`.
That worktree does not exist. The current `/home/user/work/app` is a
different integration head and must not be used as a substitute. Rehydrate a
clean worktree at the exact commit, link its own `node_modules` symlink to the
readonly private12 graph, then run the literal `--prepare` command in the
companion COMMAND file. Only after that fresh committed preflight should the
manager issue a new grant; no old grant or marker is valid.
