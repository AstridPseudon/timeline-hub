# U4a D139 receiving validation

Verdict: **PASS**.

The reviewed source is commit `4fec53e0b14aea355e51c96c883fd75eef67a17c`, whose parent is the requested current integration commit `cd63be424d62226e3ee5c26fc5ce03227f5394a5`. `cd63..4fec` contains exactly one commit and exactly one changed path: `runtime.lock.json`. The diff is one metadata line only:

```diff
-  "source_commit": "ab1e4f6141987706132916e2da16477f5a019464"
+  "source_commit": "f103bb46866999c961a8865636f2e66d544e0c9b"
```

The lock has 15 entries. Fresh Git-object and SHA-256 checks show every schema, client, and fixture consumer byte is unchanged from `cd63`, equals the canonical-15 packet, and equals its `f103bb46866999c961a8865636f2e66d544e0c9b` producer source. The source-manifest records all 15 paths and object IDs. The producer checkout `/home/user/work/runtime` was clean at `f103bb46866999c961a8865636f2e66d544e0c9b` / tree `5d0cedf2e5134acf895e8d43191cc5fdc09f9883` before and after the checks.

## Exact commands

All commands were run from `/home/user/work/wt/agt-U4a-D139-provenance-review-2242`:

```text
/home/user/work/venv-agent/bin/python scripts/vendor_lock.py check runtime.lock.json --producer /home/user/work/runtime
ok runtime.lock.json (matches producer manifest)
exit 0

/home/user/work/venv-agent/bin/python scripts/artifact_manifest.py --check
artifacts.json is current
exit 0

git diff --check 4fec53e0b14aea355e51c96c883fd75eef67a17c^ 4fec53e0b14aea355e51c96c883fd75eef67a17c
exit 0
```

The independent scoped receipt is `/home/user/timeline-hub/hub/design/rt-D139-six-result-review-2219-review.json` (SHA-256 `sha256:9362a871a17f1b99a93bbf0f3cd123fe2513ae55c9a7745d162e3d1a4a4b8564`). It is a D139 PASS for runtime `f103...`: 1,571 collected, 1,571 passed, 0 failed/errors/skipped, with clean-before-and-after true and all six body comparisons equal.

This is a lock-only normal-tool provenance review (D56). It does not claim product behavior, semantic/security, functional/core, REG/D100, or release qualification. No product tests, body/HTTP tests, typecheck, lint, refresh, regeneration, edit, or new product commit was needed or run.
