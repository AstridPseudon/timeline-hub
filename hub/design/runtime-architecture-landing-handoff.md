# Runtime architecture landing handoff

Status: ready for Agent-owned landing. This is a patch handoff, not permission,
merge, publication, pin, ZIP, or M4-complete claim.

## Frozen source and scope

- Agent source: `/home/user/work/agent`
- Exact Agent SHA before patch construction: `ce363f6d6d60e504dbd4d79803c2d6299f648ade`
- Source was clean at freeze and remained unchanged after verification.
- Historical R4 control archive remains unchanged at Agent control SHA
  `5249ac07903af36532840d5c5ed3f8960a2fe07c`; no `docs/projects/timeline-r4`
  deletion or rewrite is included.
- Current contract wording is Runtime013's immutable `artifactproducer2c`
  client/artifact producer (`2c4ac180c2220bdad966bc01e95ad230e99ce26a`,
  contract `0.2.13`) with compatible Runtime server `129493b`
  (`129493b2aff614560d9b7ac2577957e799cf30ec`). Agent public Composition
  `0.0.12` is integrated; App adoption and final viewing/writer gates remain
  pending.

## Applyable patch

`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/runtime-architecture-landing.patch`

It changes exactly these Agent paths:

1. Adds `docs/architecture/timeline.md` (401 words; one page).
2. Adds one relative link in `docs/timeline-editing-guide.md` to
   `architecture/timeline.md`.

The page describes the approved Read/See/Edit path, Runtime ledger-first
acceptance, the crash-safe outbox, guarded undo/restore, producer proposals,
and the current tuple. It explicitly leaves legacy/fallback writers,
cut-sheet migration, native capture authority, `RenderRequest` propagation,
frame/audio parity, export, and owner-film viewing open. It states that the
historical R4 control documents remain archived and that M4 is not complete.

## Verification

The patch was applied only to a temporary archive extracted from the frozen
Agent SHA, then the archive was removed. Exact commands and results:

```sh
git -C /home/user/work/agent rev-parse HEAD
# ce363f6d6d60e504dbd4d79803c2d6299f648ade

git -C /home/user/work/agent archive ce363f6d6d60e504dbd4d79803c2d6299f648ade \
  | tar -xf - -C "$PRIVATE_AGENT_ARCHIVE"
(cd "$PRIVATE_AGENT_ARCHIVE" && \
  patch --dry-run -p1 < /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/runtime-architecture-landing.patch)
# checking file docs/architecture/timeline.md
# checking file docs/timeline-editing-guide.md

(cd "$PRIVATE_AGENT_ARCHIVE" && \
  patch -p1 < /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/runtime-architecture-landing.patch)
# patching file docs/architecture/timeline.md
# patching file docs/timeline-editing-guide.md
```

The private archive checks found the link at guide line 3 and counted 401 words
in the new page. The existing Agent doc-reference checker was run against the
exact archive before and after patching:

```sh
python3 scripts/reshape/check_doc_references.py
```

Both runs: `0 error(s), 1 warning(s); checked 193 docs, 547 capability refs,
269 CLI refs`. The baseline warning, retained separately rather than repaired,
was `WARNING: astrid/packs:1: git unavailable; untracked pack-code check
skipped`. The patched run produced the same warning and no new errors.

## Agent owner acceptance

From a clean Agent worktree at the frozen SHA, review and apply only this
patch, then run:

```sh
test "$(git rev-parse HEAD)" = ce363f6d6d60e504dbd4d79803c2d6299f648ade
git apply --check /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/runtime-architecture-landing.patch
git apply /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/runtime-architecture-landing.patch
git diff --check
python3 scripts/reshape/check_doc_references.py
rg -n -F '[Timeline architecture](architecture/timeline.md)' docs/timeline-editing-guide.md
wc -w docs/architecture/timeline.md
```

Expected structural results are one guide-link match, no `git diff --check`
output, 401 or fewer page words, and the known checker warning only. Agent
ownership decides review, landing, and any later acceptance; this handoff makes
no merge or release claim.
