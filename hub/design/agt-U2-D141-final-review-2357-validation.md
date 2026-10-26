# U2 / D141 validation record

## Source and repository checks

- Candidate identity: `aa5a91a618f4d28308772169bc08e8e79274cd6a`
  / `c3ad6cca753bf1bfd033bf016c1d93e4b9f07127`.
- Parent identity: current `c585cb2aa73c5298d474e614cb2144f58f27e605`,
  frozen upstream `8b6ed2116fd1803d24b2be5bc08bd9490407fe4a`.
- `git status --porcelain=v2 --branch` — clean committed index/worktree.
- `git ls-files -u` — no unmerged entries.
- exact marker scan of committed tree — no conflict markers.
- `git merge-base --is-ancestor` for both parents — exit 0.
- `git diff --check` — exit 0.
- D100a exact blob and SHA-256 comparison — PASS.
- Author-generated `service.mjs` and resolved lock SHA-256 values — match
  author evidence exactly.

## Normal provenance/artifact gates

- `PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-agent/bin/python scripts/vendor_lock.py check runtime.lock.json --producer /home/user/work/wt/rt-pin-fa9cd546` — **exit 1**; producer manifest mismatch/missing artifacts as listed in `findings.md`.
- `PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-agent/bin/python scripts/vendor_lock.py check runtime.lock.json` — exit 0, consumer bytes only; not accepted as producer qualification.
- `PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-agent/bin/python scripts/artifact_manifest.py --check` — **exit 1**, stale am-footage component digest.

## Targeted command record

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=/home/user/work/wt/agt-U2-D141-final-review-2357:/home/user/work/wt/rt-pin-fa9cd546 /home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider --timeout=45 tests/core/execution/test_generic_host_actions_v3.py tests/core/execution/test_render_storage.py tests/core/rendering/test_storage.py tests/packs/rendering/test_render_registry_editor_metadata.py tests/packs/vibecomfy/test_local_server_run.py tests/test_generic_host.py tests/test_installer_runtime_error.py tests/test_vibecomfy_invocation_preflight.py tests/test_vibecomfy_production_engine.py
```

Incomplete at the 30-second tool boundary after 11%; actual output contained
collection/runtime `E` and `F` results. No final exit code was available.

```text
node --test remotion/tests/am-footage-cover.test.cjs
```

Exit 0: 1 passed, 0 failed.

```text
BUN_INSTALL_CACHE_DIR=/tmp/w-7f7b2f21ef/bun-cache bun run check:chat-bundle
```

Exit 1: `zod` could not be resolved from the immutable shared dependency tree.

```text
BUN_INSTALL_CACHE_DIR=/tmp/w-7f7b2f21ef/bun-cache bun test ./astrid/chat
```

Exit 1: 29 passed, 18 failed, 18 errors; missing `zod` import prevented a
valid chat-family qualification.

The temporary `node_modules` symlink was removed; no shared dependency was
modified.
