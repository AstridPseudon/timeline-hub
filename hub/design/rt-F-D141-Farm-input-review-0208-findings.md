# D141 Farm input-producer independent review

## Verdict

**FAIL, bounded documentation correction required.** The 22-row map is useful and the venue remains `NOT_READY`, but the packet incorrectly says Runtime/App checkout receipt closure is absent. The actual 01:50Z Farm pre-child census passed the Agent, Runtime and App checkout receipts; only the Composition receipt was mismatched because the earlier filename used 39 hex characters.

## Finding F-D141-REVIEW-001 — stale Runtime/App absence claim

The source packet's `findings.md:8-12`, `findings.md:41-47`, and `handoff.md:21-22` ask for Runtime/App queue receipts and list their closure as missing. That contradicts the actual census packet `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/peer-farm-to-lead-runtime-20261026T0150Z-core-census-NOT_READY-full-packet.md`, whose durable output hash is `8532e8de9f0cf38ae281aa0097e1ab2c0d705d9a6877babc40a0522db45dc7f2`: Agent/Runtime/App receipts passed and Composition was the remaining receipt mismatch.

Smallest first return: correct only those prose claims and the handoff step. Preserve the map's 22 actual non-pass rows, the corrected Composition receipt, and all receiver/producer code.

## Passing findings

- The nine original producer files were recovered byte-identically from commit `2912e517`; the original custody limit is disclosed and no path-only reauthoring was repeated.
- `input-map.json` addresses all 22 rows once with parser fields, types/shapes, concrete producers, owners, next commands and absent prerequisites. It distinguishes supplied artifacts from Farm control-plane observations and output destinations.
- Full SHA-256 values, current four-repo commit/tree pins, maker/requester/checker/verifier/launcher identities, and the Composition receipt provenance are valid. Historical installed-kit/schema and 2149/2216 census material are not presented as current installed bytes or a current D141 result.
- The C0 summary matches the frozen Runtime schema: request base/commands/optional metadata, requested/accepted steps, `fields|atomic`, declared reads, accepted/merged/rebased result shapes, conflict/refusal/invalid details, preview with null receipt, and separate history/receipt shapes.

## Limits

No Farm census, child, import, control, service, core, install, acquisition, Store, product, live-kit or network action was run by this review. No READY, behavioral, REG or delivery result is claimed.
