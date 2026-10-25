# Validation

## Result

PASS for the requested source-only review. No Agent source was changed and no
integration, build, network, clone, ZIP, Store, D130, or M5 operation was
performed. Type/lint/tests are N/A because this worker changed evidence only.

## Exact source and scope checks

Read-only source root: `/home/user/work/agent`.

- `git -C /home/user/work/agent status --short --branch` → `## tl/integration`
  (clean).
- `git -C /home/user/work/agent rev-parse HEAD` →
  `547e10456250c1b5bcf63b44a50c90ff0563ce1e`.
- `git -C /home/user/work/agent rev-parse --abbrev-ref HEAD` →
  `tl/integration`.
- `git -C /home/user/work/agent show-ref --verify refs/remotes/origin/main` →
  `886a3183bd4a4a44f0a2c08fabec4e8edcbf7b55`.
- `git rev-parse BASE^{tree}` →
  `a81a8c7f262e4416dcdefc0720fd760e026d766b`.
- `git rev-parse OURS^{tree}` →
  `68df11fad2b082fa12d99ca20404e1e40e350cd7`.
- `git rev-parse UPSTREAM^{tree}` →
  `f53cc8426ccef8760021ef6207303bce7b80e777`.
- The qualified census first-20 list has exactly 20 paths and is disjoint
  from the second-half partition.
- Direct diffs against the same base count exactly 35 ours hunks and 95
  upstream hunks. `git merge-tree --trivial-merge BASE OURS UPSTREAM` counts
  exactly 62 merge-tree hunk blocks for these 20 paths.
- The 60 recorded base/ours/upstream blobs in `source-manifest.json` all
  resolve as Git blobs; all recorded ours/upstream byte sizes match
  `git cat-file -s`.

## JSON and crosswalk checks

- `python3 -m json.tool evidence/review.json` → PASS.
- `python3 -m json.tool evidence/source-manifest.json` → PASS.
- Semantic disposition header count (`grep`/regex over
  `evidence/semantic-disposition.md`) → 95 exact upstream hunk headers.
- Review totals: 20 paths, 35 ours hunks, 95 upstream hunks, 62 merge-tree
  hunks; 18 ours EOF-only, 15 ours generated, 2 ours dispatch-import; 80
  upstream auto-composable, 15 generated-rebuild, 0 genuine mutual-intent.

## Patch and diff checks

Command:

```text
git -C /home/user/work/agent apply --check /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-F-tail-Agent-A-1928/evidence/trivial-resolutions.patch
```

Result: PASS. `git apply --stat` reports 18 files changed, 18 deletions, and
no additions. The patch is deletion-only EOF whitespace normalization and
does not include `service.mjs` or `dispatch.py`.

```text
git -C /home/user/work/agent diff --check BASE UPSTREAM -- <first-20-paths>
```

Result: PASS, zero findings.

```text
git -C /home/user/work/agent diff --check BASE OURS -- <first-20-paths>
```

Result: expected exit 2 with exactly 18 findings, one “new blank line at EOF”
per trivial file. Those are precisely the preimages removed by the private
patch; no non-whitespace finding exists.

No patch was applied, and no source worktree or Git state was mutated.

## Explicit non-claims

- Whole actual clone was not performed; this remains explicitly unverified.
- Generated `astrid/chat/service.mjs` was not hand-merged or regenerated here;
  regeneration is a later merge-worker action after source composition.
- No product tests, typecheck, lint, browser/live-service checks, or full
  suite were run.
