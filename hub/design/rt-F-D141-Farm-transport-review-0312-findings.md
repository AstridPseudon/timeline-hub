# D141i independent transport/source review

Verdict: **PASS — corrected transport security controls. FARM_NOT_READY remains.**

## Findings

No new transport-security finding was reproduced in the frozen commit. The
previous 0253 findings are all closed in source and in the independent runs:

1. Duplicate tar members are refused before the member index is accepted.
2. Extra directories and all unknown/missing members are refused; the exact
   metadata-plus-RECORD closure is enforced.
3. Compressed and expanded archive input are each capped at 20 MiB.
4. `direct_url.json` is checked against the fixed pinned SHA and exact
   `242f9c…` URL/commit/subdirectory identity; refreshed closure metadata and
   sidecars do not authorize changed bytes.
5. Duplicate JSON keys and nonstandard JSON constants are refused recursively.
6. Receiving advice uses `--same-permissions` with `--no-same-owner`,
   `--keep-old-files`, cleared `TAR_OPTIONS`, private empty stage, and an
   independent-review gate. No broad ownership or permission repair is advised.

The actual tests observed 2 accepted positives and 14 rejected attacks in both
the replayed 0253 matrix and a separately written reviewer harness. The
corrected controls additionally verified exact bytes/modes/uid/gid and the
18-row, 12-hashed, six-named-unhashed closure without extraction.

## Bounded readiness findings

- `D141i-INPUT-001` — **OPEN / owner D139a installation-kit owner:** the
  current genuine installed-kit summary and separate matching `PASS_INSTALL`
  pair are still missing. The 2309 `PASS_INSTALL_COMBINED` receipt remains
  supporting only.
- `D141i-INPUT-002` — **OPEN / Farm distribution and original67 owner:** the
  authenticated original67 wheelhouse and genuine verifier manifest are still
  missing. No bootstrap substitution was made.
- `D141i-RECEIVE-001` — **NOT A DEFECT / scope boundary:** actual extraction,
  receiver check-only admission, installation, child, body, live kit, queue,
  and product execution were deliberately not run. `PASS_TRANSPORT_CLOSURE`
  is not a Farm READY claim.

No verifier, D131, authority, ownership, C0v2, or production-caller
relaxation was made. The production caller remains the supported
`receive-farm.sh --check-only` route.
