# AP2 M2 producer exact tree topology — 1110

## Result

Applied only the exact `b8cc7e1c..09171792` working-tree delta. The
baseline-to-target enumeration is exactly these three paths:

```text
M scripts/testing/run-producer-public13-list.sh
M tests/e2e/local/producer-ownership-current-pin.spec.ts
M tests/e2e/local/support/producer-ownership-current-pin.ts
```

The wrapper was already present in `b8cc7e1c`; the applied delta changed only
the spec and helper. No live callers changed (NONE; source/test-only).

## Verification

```text
git diff --quiet 09171792bd626f5eabd421d1f1c2b497a4fc9786 --
PASS: working tracked tree equals target tree 31b0f77c6ef4e9fdbeff3e4f88cc4705f0891e89

git diff --name-status b8cc7e1c79ec5516b9eee3832b5c33d62dac1aa7 --
PASS: exactly the two source-delta paths above; no untracked files

git rev-parse HEAD^; git rev-parse HEAD^^
PASS: b8cc7e1c; 17d2518c (frozen baseline; its parent is 7fafee1f)

sha256sum spec helper config
PASS: 6666c0365d13f302725788e6fbfcce9e0fb283e4b30c40661886522a67f270e6
      df1faac404b69efa8a5fb06297814e6ca3b5d52b4a5856633706c7ac2e3ae949
      5b880ceff883abce2575a3a85aaa4eda69d3bcb848768ff0e91f337d50cca4c0

git diff --check b8cc7e1c
PASS
./node_modules/.bin/eslint --no-cache --no-warn-ignored --max-warnings 0 \
  tests/e2e/local/producer-ownership-current-pin.spec.ts \
  tests/e2e/local/support/producer-ownership-current-pin.ts
PASS
sh -n scripts/testing/run-producer-public13-list.sh
PASS
```

The target-equal spec blob preserves the `at`→`on` wire lowering and the four
zero-legacy-verb assertions byte-for-byte. No preflight, controls, build,
browser, socket/service, actual run, install, or full suite was run.

## Commit-dependent next step

The harness must commit this worktree so the resulting source commit has tree
`31b0f77c…`, parent `b8cc7e1c…`, and therefore the required two-link ancestry
to frozen baseline `17d2518c…`. After that commit, bind any source-commit
identity to the harness-created SHA; retain strict equality and
`APP_SHA=17d2518c…`. Do not replace `APP_SHA` with HEAD or weaken the guard.

Decisions: no guard change and no source implementation/test edits beyond the
exact existing delta. Blocked: nothing in this task; downstream binding is
commit-dependent.
