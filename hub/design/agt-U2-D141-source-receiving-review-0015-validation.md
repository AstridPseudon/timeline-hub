# U2 / U4a D141 source validation

Result: `PASS_SOURCE_QUALIFICATION`.

## Exact source identity and conservation

| Check | Result |
| --- | --- |
| `git rev-parse HEAD` / `HEAD^{tree}` | `b4eb5db76fda523407b90a9dbe820f4e20cc1f1d` / `2ebe2ddf5a61f013953ab1e21d51ebaab746e58a` |
| Candidate merge `aa5a91a...` tree | `c3ad6cca753bf1bfd033bf016c1d93e4b9f07127` |
| True parents | `c585cb2aa73c5298d474e614cb2144f58f27e605`, `8b6ed2116fd1803d24b2be5bc08bd9490407fe4a` |
| Parent ancestry checks | PASS for both parents |
| Cumulative diff after `aa5a91a...` | Exactly `artifacts.json`, `runtime.lock.json` |
| Actual parent-tree conservation | 19 upstream-only / 922 current-only; 0 mismatches |
| D100a source/test bytes | PASS; exact approved blobs and SHA-256 values |
| Generated chat bundle | PASS; author SHA-256 `821ff6b1c2e96dab49a0f4dfa73a6e0d8f731930438b0cf2ce4ba421ca5ad6da` |

## Normal scoped commands

All commands were run read-only against the current worktree and the clean
Runtime pin; no tests, imports, product bodies, or new diagnosis were run.

```text
PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-agent/bin/python scripts/artifact_manifest.py --check
```

Exit 0: `artifacts.json is current`.

```text
PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-agent/bin/python scripts/vendor_lock.py check runtime.lock.json
```

Exit 0: `ok runtime.lock.json`.

```text
PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-agent/bin/python scripts/vendor_lock.py check runtime.lock.json --producer /home/user/work/wt/rt-pin-6a011d58
```

Exit 0: `ok runtime.lock.json (matches producer manifest)`.

```text
PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-agent/bin/python -m json.tool artifacts.json
PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-agent/bin/python -m json.tool runtime.lock.json
```

Exit 0 for both JSON parses.

```text
git diff --check HEAD^ HEAD
git diff --check aa5a91a618f4d28308772169bc08e8e79274cd6a..HEAD
```

Exit 0 for both checks.

The read-only canonical comparison checked all 15 lock entries against the
`c585cb2` Agent parent and `/home/user/work/wt/rt-pin-6a011d58` (commit
`6a011d58e69173d70e2e9bb3ac434ac8f9e87d8d`, tree
`ac5b862744bece65b2e30565db1777bacd60da28`). Mappings, bytes, POSIX modes,
and producer-manifest hashes all matched.

## Pending and exclusions

The earlier 2357 failure record is retained and not reclassified. Python 0008
completion, final Farm/App normal-vendor proof, full REG, and ship proof remain
owed. This result is source-intake qualification only; it is not behavior
PASS, REG0, ship credit, or a policy waiver.
