# Exact unapplied ordered project-data removal patch

Date: 2026-10-21 UTC

## Result

Exported the concrete three-path delta recovered from worker 1118 to:

`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/ap2-m2-remove-ordered-carrier-UNAPPLIED.patch`

The patch is unapplied to the product worktree. It contains only:

- `src/tools/video-editor/commands/projectDataMember.ts`
- `src/tools/video-editor/commands/clipMovePrimitives.ts`
- `src/tools/video-editor/commands/projectDataMember.test.ts`

It excludes the generated `timeline-commit-types.ts` binding, the temporary
`private-agent-write-proof.ts`, all repo documentation, pins, generated files,
and `.git` content.

## Exact identity proof

The retained 1118 transcript identifies the tested source base as:

- commit: `0cc2583aaf07e89190b9344b5ac82849d6279586`
- tree: `320e74a93676c781e83885b86ec237b4a1465d80`

All three source files were mode `100644`, with these exact base and tested
candidate blobs:

| path | base blob | tested candidate blob |
| --- | --- | --- |
| `src/tools/video-editor/commands/projectDataMember.ts` | `5d4dd26be9e5b296c18fab1372a67ebef2d8d78f` | `a8ce58a4097d1a56bc9806bf47a23ca487defb89` |
| `src/tools/video-editor/commands/clipMovePrimitives.ts` | `401c559c179eb4d4f675e5e3eff052abadf4c3ac` | `442c5ba4a497d3147fcccad8948025b5610a0c5b` |
| `src/tools/video-editor/commands/projectDataMember.test.ts` | `704baa3652086b949161638173d8f75bde8b6ada` | `e140a59955753b6113f17f1ff28e45260459c8d0` |

The patch was applied in a temporary isolated archive of the exact base
commit, then the resulting blobs matched all three tested candidate hashes.
This proves the exported source bytes are the tested 1118 candidate, rather
than a fresh reimplementation.

## Delta recovered

The source change adds the existing Agent `project-data.write` remove mode,
lowers the already-public `project-data.delete` input to that command, prunes
empty/null namespaces and empty `config.app`, and carries raw sibling order
only for a pruned namespace. `AuthoredState.set` validates and restores the
recorded order; ordinary writes and absent-leaf absent→absent writes omit the
carrier. The direct tests cover serialized command replay, inverse restoration,
middle-key order, null/opaque/sibling preservation, absent-leaf behavior, and
existing replace/merge behavior.

## Verification

Commands run for this export:

```text
git apply --check --whitespace=error-all .../ap2-m2-remove-ordered-carrier-UNAPPLIED.patch
=> passed

git apply --stat .../ap2-m2-remove-ordered-carrier-UNAPPLIED.patch
=> 3 files changed, 171 insertions(+), 33 deletions(-)

git archive 0cc2583aaf07e89190b9344b5ac82849d6279586 | tar -x -C <temporary isolated directory>
git -C <temporary isolated directory> apply --whitespace=error-all .../ap2-m2-remove-ordered-carrier-UNAPPLIED.patch
=> passed

git -C <temporary isolated directory> hash-object <three paths>
=> a8ce58a4097d1a56bc9806bf47a23ca487defb89
=> 442c5ba4a497d3147fcccad8948025b5610a0c5b
=> e140a59955753b6113f17f1ff28e45260459c8d0

git status --short
=> clean
git diff --check
=> passed
```

The temporary reconstruction directory was trap-cleaned. No product source
was changed.

Per the task instruction, I reused 1118's prior targeted evidence because the
candidate bytes are now proven identical; I did not rerun tests without a new
cause. 1118 reported:

```text
vitest ... projectDataMember.test.ts visualSeamProjectDataMember.test.ts genericPatchCapture.test.ts
=> 3 files passed; 33 tests passed

tsc --noEmit --strict --skipLibCheck --target ES2022 --module ESNext \
  --moduleResolution bundler /tmp/ap2-m2-remove-private/private-agent-write-proof.ts
=> passed

eslint src/tools/video-editor/commands/projectDataMember.ts \
  src/tools/video-editor/commands/clipMovePrimitives.ts \
  src/tools/video-editor/commands/projectDataMember.test.ts --max-warnings 0
=> passed
```

The generated binding and containing release remain prerequisites for applying
this source proposal. No full, browser, HTTP/socket, install, pin, activation,
native, UI, product merge, or lifecycle qualification was performed.

## Attribution and next step

Recovery source: worker 1118 log
`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-remove-ordered-carrier-unapplied-1118/log.txt`, especially the
final candidate diffs and hash outputs around transcript lines 7331–10354.
Semantic/evidence source:
`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/ap2-m2-remove-ordered-carrier-unapplied-1118-REPORT.md`.

The orchestrator can review/apply the patch only after the normal generated
`AgentWrite.insertion_order?: Array<string>` binding is landed in the
containing release. The App worktree remains at its live baseline.
