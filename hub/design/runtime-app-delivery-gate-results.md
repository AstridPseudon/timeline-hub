# M4 gate results — current inputs (DRAFT / BLOCKED)

Evidence snapshot: 2026-10-21. This file is an input to the final
`delivery-build` README, not a release result. No final ZIP, foundation-complete
claim, owner-film result, macOS result, or all-gates-green claim is made here.

## Source and adoption boundary

Published014 is the current normal source tuple, with separate producer and
server identities:

- Runtime producer `95bd3c5f6d00e9bc8cc8cbe5ef510b68ed660f3c`, tree
  `d3a290b407fa61e6ab2d476f50c068073f70df00`, contract/client `0.2.14`, and
  immutable `all76` artifacts (`sha256:54205b3ecb55038e416b31af936c9af26afa30dc1b05da16157ee4d861fe05ac`);
- compatible Runtime server `b92d3e7a05eec65c142294ef4873edd059e9b31d`, tree
  `6abc2f117391de8e7e35c0283f575a002199894d`, a compatible descendant that
  does not republish or change the producer/lock authority;
- Agent `091aa23ec83ea05ffd3b0115a640230d51c8c429`, tree
  `e3ae90fe482ba6cad6c3f94069127faf76ebceb6`, and App
  `3be3c116610c4ffdf019cba447464280fd7b8e06`, tree
  `d030e4b8b41a1d5ec46de1c0c245111cafa7e98a`, both using the normal Runtime
  producer pin;
- Composition13 `7bb54bbd64107e5090643ecca1e4d33164173e85`, tree
  `20467712e66dbadff4d562c0d5baae22b8c077a7`; Composition14 is not part of
  this tuple.

The published Runtime source and `all76` bytes remain immutable. A delivery
patch applied with `git am` creates a different synthetic commit; it must be
identified by the resulting target tree and checked artifact bytes, never
silently relabeled as producer `95bd…`. The supplied Runtime bundle or the
existing clean producer checkout `/home/user/work/wt/rt-pin-95bd3c5f` is the
source-authority route for the normal consumer byte check. No lock rewrite or
hand-copied generated artifact is part of delivery.

The generic neutral Runtime remains a separate behavior: its low-level
`runtime_protocol` commands do not load the Agent provider. The normal
installed product path is the existing private, non-editable Runtime/client/
Agent carrier followed by `astrid-runtime up --profile astrid`; it does not
change neutral defaults or add a provider fallback.

The current Runtime full is
`runtime-full-retained-owned-temp-integration-1021035028-28646` on `b92d3e7a`
and tree `6abc2f1`; it passed `6002 passed, 26 skipped, 15 xfailed, 12
warnings`, exit 0. The current TypeScript check is
`rt-m2-gate4-main014-ts-evidence-0407-ts-client-check-1021040813-12394`,
with `61 passed, 0 failed`, exit 0. The exact commands and source bindings
are recorded in `design/runtime-current-tuple.md` and
`design/runtime-gate4-main014-typescript-current.md`.

The installed source-matched launcher proof
`rt-m2-wc10-sdk-envelope-fixture-one-proof-0322-wc10-installed-launcher-integration-1021032335-4406`
is `1 passed` and remains launcher/carrier evidence only. It does not qualify
D13 rendering, consumer adoption, or delivery. Its exact command and
authority boundary are recorded in
`design/runtime-m2-current-launcher-merged-handoff-full-0332.md`.

App native initializer activation is current bounded evidence: merge
`1557c312` with actual `1021034025-7782` passed one run and retained the
native 61-assertion lane. Current mixed neighbor `4657` also passed, while the
whole mixed run was withdrawn. These facts establish native initializer
activation and one successful mixed neighbor only; they do not establish
all-writer retirement, physical parity, or the complete consumer journey.
The current App and Agent boundaries are in
`managers/app/STATUS.md` and `managers/agent/STATUS.md`.

Private016/da77 is superseded immutable evidence and was never adopted. The
sole open PRIVATE line is Private017: Runtime candidate
`42a7203f49bb89f299ec854cfbf2b1444e815a7c` (tree
`1f220b3d3a27e8eb061b15c944bad784c8fdb82e`), package `0.2.17`, is approved for
exact artifact identity only. The candidate carries Agent source
`ed5fd33c4a7fa9956178f9b24eb127415eaca9e6` / tree
`f4a632e4f627499e0b15d8477db9aaab78ebb3d2`, raw/canonical schema digests
`6dd2b082` / `9f5612ff`, inventory 65/37, Runtime health
`a8fad23f`, raw bundle `e6fb80`, artifact manifest `a0dc43`, and all76.
Agent reciprocal approval, normal private pin, native execution, RT03 proof,
and HTTP qualification remain pending. It is not published, pinned, adopted,
merged, or activated; no private017 actual HTTP proof is claimed. The exact
artifact review and Runtime approval are recorded in
`design/runtime-private017-42a-independent-review.md` and
`design/peer-runtime-to-agent-app2-20261021T075349-private017-final-approve.md`.
The prior ordered-record mismatch is retained as historical explanation only;
no later source is treated as published or released.
Private015 / C3d / 3e6c and older 392 / 952 are superseded, immutable
historical evidence and were never adopted. The former envelope question is
now scoped to App2's independently reviewed one-to-one fixture conversion; it
is not an unresolved launcher result.

Generic neutral Runtime commands remain a separate no-provider path. The
published014 installed launcher and App/Agent bounded evidence do not change
the normal publication, pin, version, adoption, or release boundary.

## Seven gates

The current Agent full result remains a visible failure boundary, not a
delivery-wide green result: run `21969` on Agent source `cc37291a` / tree
`0698a30b` recorded `15,840 passed, 138 failed, 4 errors, 456 skipped, and 4
xfails`. The Agent manager's latest status groups the 142 terminal nodes by
cause and owner; 110 name missing Runtime imports directly or through retained
chains, and the remaining 32 have separate causes. This source-scoped failure
is not relabeled as historical or repaired by the Runtime full pass; the exact
status source is `managers/agent/STATUS.md`.

| Gate | Evidence at this snapshot | Status and exact limit |
|---|---|---|
| 1. Lossless semantics | Bounded Agent current-source conformance and connected occurrence/source, opaque-field, clear, reload, inverse/redo, stable-word, and rational-timing lanes are recorded; the current Agent full failure is scoped above. | **OPEN.** The full editing-conformance corpus and complete CLI/Python/sheet coverage are not claimed. |
| 2. Atomic acceptance | Published014 retains the qualified 95bd producer evidence and the compatible descendant server source; the current coordinated consumer journey is not represented by that evidence. | **PASS within the retained Runtime/producer scope; OPEN for the final coordinated normal pair.** |
| 3. Renderer-independent save | Agent records 26 renderer-fenced controls and renderer-stopped commit/reload/undo with honest unavailable-preview behavior; the qualified ordinary014 lane includes 11 real-daemon cases. | **OPEN.** Cross-product coverage, live Composition parity, and physical frame/audio parity are not established. |
| 4. Transport | Current TypeScript check `12394` passed all 61 tests on the current b92 tree; published014 retains the normal `0.2.14` producer/client, `all76` artifact bytes, and compatible server source. | **PASS within the retained producer/client scope; OPEN for the final coordinated `/v1` consumer result.** |
| 5. Adversarial App journey | App native initializer `1557` / actual `7782` and one current mixed neighbor passed within their bounded scopes. | **OPEN.** No current normal-pair browser proof yet establishes intervening edit, lost ACK, newer local edit, exact retry, restart/reload, undo, and zero legacy snapshot traffic together. |
| 6. One writer, one viewer | Native initializer activation and the successful mixed neighbor do not establish all-writer or physical parity. | **OPEN.** All-writer retirement, direct legacy-endpoint rejection, planted frame/audio mismatch detection, and physical parity remain unproven; the owner-controlled physical launch is blocked on its helper. |
| 7. Delivery | Fresh rehearsal `runtime-delivery-owner-extras-integration-dryrun-1021070937-11141` passed in 84 seconds (exit 0) on exact Agent `b79fec587dc7bab3fcb0624785d38faa519b3c93` / Runtime `b92d3e7a05eec65c142294ef4873edd059e9b31d` / App `42b0c6c8434e2c491f8dbdf00a210ed755e41a95` / Composition `7bb54bbd64107e5090643ecca1e4d33164173e85`. Fresh-main patch, bundle, and source tree equality passed for all four repositories; scanner and owner-instructions inputs were unchanged. The added integration-scoped suite used the reviewed builder and extras unchanged. Historical `30942` remains scoped to its old tuple; `26457` was withdrawn after a wrong-tuple cache hit and is no pass. | **OPEN.** This is rehearsal evidence only: no fresh current-tuple ZIP, owner-film viewing, physical parity, final source refresh, or final ZIP verification is claimed. All remaining gate, deletion, macOS, and owner limits remain outstanding. |

The Agent full failure above remains current source-scoped evidence. Historical
red runs remain historical and are not reinterpreted as current passes or
current failures. The compatible Runtime server/full evidence does not close
physical frame/audio parity, global consumer adoption, owner-film viewing, or
final ZIP delivery.

## Delivery carrier and frozen owner inputs

The installed carrier is
`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/delivery-build`,
SHA-256
`3dfd5c28a9be9ab809e6c1fe1e9a83fbf8417ea888afc1b10eec5f751023e990`.
When the final build is authorized, retain these exact existing `--extra`
arguments and source hashes:

```sh
--extra "extras/owner_film_cliplook_scan-v1.0.8.zip=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-vw-m4-owner-scanner-delivery-payload-scanner-v1.0.8.zip" \
--extra "extras/owner-film-differences.md=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-vw-m4-owner-scanner-delivery-payload-owner-film-differences.md"
```

Scanner ZIP SHA-256:
`204a7aac78177824219954574f67fcaf4c56ac81620d533ecb376030340c93ee`.
Owner-instructions SHA-256:
`969fe3034ca1e7b7aab061ff16575fe7f7d973d9c9ec1f81c347464c4d9da220`.
These are scanner code and instructions, not an owner-film scan or viewing
result. The prior private-stage proof had 12 members and unchanged README,
bundle, and patch hashes; it did not publish a ZIP.

All evidence above is Linux/local evidence. macOS remains OPEN and is never
implied by a Linux pass. Owner-film viewing, physical frame/audio parity, the
global consumer journey, a fresh current-tuple delivery build, and final ZIP
verification remain required before release.
