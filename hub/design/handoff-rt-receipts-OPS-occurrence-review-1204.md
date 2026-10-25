# Runtime receipts and occurrence-boundary review

Disposition: **A receipt validated with an exclusion-evidence caveat; B UNAPPLIED**.

## A — `rt-OPS-ended-log-return-1150`

The receipt lists 737 gzip outputs. Independent streaming checks found all 737
archives present; every compressed SHA-256/size and every decompressed
SHA-256/size matched the receipt. The exact worker-log allowlist passed, no
listed plain file remains, and the decompressed-byte sum is 225,695,370.

The receipt reports 178,210,050 logical bytes reduced and an observed free-space
delta of 7,118,848 bytes; the latter arithmetic matches the receipt's before
and after counters. These are receipt-reported observations, not an
orchestrator approval or a claim of durable free space.

The fresh guarded count is 737 versus the prior inventory's 1,709, a
972-candidate discrepancy. Receipt guards state that log contents were not
read or printed, retirement followed verified gzip output, recursive deletion
was false, and no safety/permission refusal occurred. Path checks found no
protected session/current-proof/evidence/report/manifest/XML/source-worktree/
toolchain/bench-store path. One selected worker directory contains the
literal token `refusal` as part of a review-task name; the receipt does not
include a refused-target exclusion manifest, so that family exclusion cannot
be reconstructed independently without widening the review.

No further compression, deletion, cleanup, or sweep was performed.

## B — `rt-R2-occurrence-boundaries-1152`

Disposition remains **UNAPPLIED**. Runtime commit `7070f1378d1917fcce69857ebd33cd2b3015568b`
resolves to tree `cd68015cb9fe85a6ecd2d15dd7e2eac69f67e2b1`; Agent commit
`547e10456250c1b5bcf63b44a50c90ff0563ce1e` resolves to tree
`68df11fad2b082fa12d99ca20404e1e40e350cd7`. The registered Runtime provider,
Agent occurrence/producer capture, inverse, sequential capture, and commit
seams cited by the prior handoff all parse as Python AST.

The retained App peer packet remains tied to Runtime pin
`42aad0e92f6da8ea83dd0a382a87e3acd12651b0`. Its two observed guard outcomes
are consistent with current Runtime source at `timeline_commit_auth.py:1645`
and `:2267`, but the packet does not establish producer, verifier, or test
setup ownership. Missing evidence is the accepted source `commit.effect`
before-image, inverse `inverse.stage`/`commit.materialization` bindings and
closure images, following child-media physical-promotion bindings, and the
original/landing sequential outputs with their prepared canonical closure.

Closest passing controls are the four symbols listed in the JSON evidence
artifact. No semantic waiver, auth-guard change, collector/body, or new
whole-path change is justified.

Evidence: `workers/rt-receipts-OPS-occurrence-review-1204/evidence/verification.json`.
