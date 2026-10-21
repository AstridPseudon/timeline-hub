# AP2-M2 bootstrap baseline ledger mapping report

## What I did

Updated only the D01-app-bootstrap row in `design/deletion-ledger.app.md`.
The row remains `OPEN`, and all prior evidence is preserved.

The new note records the approved one-to-one mapping from the old raw history
length of 1 to exactly 2 raw entries in order: the normal Main
`parent_composition.publish` baseline followed by exactly 1 native
`timeline.commit`. It specifies the required baseline and native receipt,
publication, scope, intent, previous/head, ancestry, and native command-order
assertions, including `timeline.init`, two `track.create` commands, version 1,
and `select: parent`.

The note explicitly says this is conversion mapping only. It does not claim
native activation, a browser or acceptance gate, or a Runtime redesign. The
current013 rollback9bda/213 guards and same14pin/activation actual gate remain
required.

## Source decisions

- Proposal `ap2-m2-bootstrap-main-baseline-contract-0047`: Main behavior has
  an intentional baseline publication plus the later native commit.
- Independent review `ap2-m2-bootstrap-baseline-conversion-review-0055`:
  **APPROVE** for the exact test-conversion candidate. No HOLD or defect was
  required.

## Verification

- `git diff --check` — PASS.
- `git status --porcelain=v1` — clean; no repository code, tests, or build
  output changed.
- `rg -c '^\\| D01-app-bootstrap \\|' design/deletion-ledger.app.md` — PASS;
  exactly one D01-app-bootstrap row remains.
- Manual row inspection — PASS; no other ledger row or status was edited.

No product tests, browser suite, full suite, new audit, or new suite was run,
as required for this documentation-only mapping task.

## Blockers and next steps

Nothing blocked this documentation update. The orchestrator should retain the
OPEN status and require the existing same14pin/activation gate and current013
rollback9bda/213 guards before treating bootstrap as qualified or activated.
