# App Composition14 counterpart-gated adoption candidate

Status: **READY as a current-preserving staged candidate; bounded HOLD for
integration, publication, activation, native/browser/full/physical proof, and
caller changes.**

## Exact source and scope

- Worktree: `/home/user/work/wt/app-m3-composition14-counterpart-gated-compose-r29`
- Base: `HEAD a3a2164535b82b8f9622ea703e737d9c013c1a98`, tree
  `17e179b540b30c71896695e09f0690f915121a8f`
- Donor: `tl/app-m3-composition14-normal-app-pin-stage-r26`, committed
  `e704a6a1c9093957f826b929bec2e7aeab18a44a`, tree
  `6aad796a95e55086d6acebd75a3c5f066fcbad65`; independent r28 approval is
  recorded by the donor branch/review source.
- Donor paths copied exactly: `package.json`, `package-lock.json`,
  `config/vite/timelineCompositionPackage.test.mjs`, and
  `vendor/artifacts/banodoco-timeline-composition-0.0.14.tgz`.
- Candidate is uncommitted here; the harness will assign its final commit/tree.
  The four staged blob identities are `95941009c04f5957f2550c9b5802b929cf090115`,
  `f085ca5dd047f5a66027b904cd7d74c06d6277b9`,
  `93694fc1873e81d5430d5c1cca2df7d80b40e51d`, and
  `c1e65c5aaa9ce95208f398d04328d77a55dc1543`, respectively.

## Immutable14 and current preservation

- Archive: `@banodoco/timeline-composition@0.0.14`, 72,134 bytes, 80 regular
  members, SHA-256
  `21fde4d2a5d62a83f97a85d4b8d9f9d3f707a6489c07eb421c6331eccf893e6e`.
- Lock integrity: `sha512-Bgf9lHdk3CJCTsA3Jbd5WW9UYCHEZQTF3VFM1YO6dimZ+q8bQ8cX6CZ4FCfClBNgg10DQ1bozGMqFCpkGNXvvw==`.
- `package-lock.json` is byte-identical to the donor (`git` blob
  `f085ca5d…`) and the package metadata points to the exact archive.
- Existing Runtime14/95 is preserved: `runtime.lock.json` source commit
  `95bd3c5f6d00e9bc8cc8cbe5ef510b68ed660f3c`; generated contract version is
  `0.2.14`; live `initializeBootstrapTimeline` remains present.
- Existing current source changes, including the occurrence-media capture
  source/tests relative to `tl/integration`, remain untouched. Public13 and
  its 58,477-byte/77-member archive remain unchanged.

## Agent counterpart

The exact committed normal14 counterpart is present; no peer request was
needed:

- Commit `255b6856cc1c96f4d40ddac05d4e3d98bb81051c`, tree
  `aed2ccf7596add9118b272afad831c214ede11fe`.
- Hub/design records identify it as the independently approved Agent stage;
  the runtime preflight names review1137 as the adoption gate and keeps the
  immutable runtime request separate/not requested here.
- Agent counterpart carries the same archive identity and is scoped to normal
  consumer checks; no inspectionMouth, old physical proof, or Runtime
  successor is part of this candidate.

## Evidence

- Archive and lock identity assertions: **PASS** (72,134-byte archive hash,
  lock integrity, and package/lock target all agree).
- Donor private-cache package boundary test — **10/10 passed** — and its
  installed-80-file byte identity, public exports, Scene-clock-PCM, and source
  qualification are reused as instructed; no reinstall, rebuild, or private
  package override was performed here.
- A local full `node --test config/vite/timelineCompositionPackage.test.mjs`
  attempt was **not qualification evidence**: it ran against the shared
  `node_modules` install, which remains 0.0.13 by design, and failed the 0.0.14
  installed-package assertions. No reinstall or override was performed to
  change that shared install.
- `git diff --check`: **PASS**.

No integration merge/publication, native/browser/full/physical run, old proof
execution, Runtime change, caller change, or source override was performed.
