# D140 independent receipt security review

Verdict: `FAIL_SOURCE`; readiness: `NOT_READY`.

Reviewed exact candidate `0634ea013b29ba2ab02f619a99328b1f5ca81c7a` (tree
`7493f07a49d8df5b2d0abe6fbd10c63431fb5d23`) on parent
`d7727b99fb9cb063d4c0ee73fdfa54d752666135`.

## Findings

### FAIL — D140-RECEIPT-005A: kit producer/schema is still wrong

`receipts.py:106-152` accepts the historical
`timeline.ops.d137.installed-kit/v1` summary and `PASS_INSTALL` JSON. The
whole-path producer map identifies the normal Farm distribution producer as
`verify_farm_distribution_inputs.py`, whose canonical format is
`timeline.farm-distribution-inputs.v1` with `roles`, `lock`, `distributions`,
`ownership`, and `component_identity`; dependency retention closes through
`.farm-receipt.json`. The candidate does not parse or authenticate that format.
Its positive test constructs the old summary, so it cannot prove genuine Farm
distribution/dependency receipt compatibility.

### FAIL — D140-RECEIPT-005B: D73 retained path/report closure is missing

`receipts.py:231-253` compares `FARM_D73_RECEIPT` bytes with
`P4_D73_MANIFEST` and checks the pinned launcher and tuple fields, but never
binds the receipt to `P4_D73_EVIDENCE/$P4_D73_REQUEST_ID.manifest`, the
request-id file, or the launcher-created runmanifest. `receive-farm.sh` only
checks that the evidence directory exists. A detached valid manifest can pass
without retained producer/evidence closure.

### FAIL — D140-RECEIPT-005C: digest handoff is only prose/env trust

`authenticated()` accepts any caller-provided `<binding>_SHA256` that matches
the artifact. The README and commands document these variables but no actual
caller/handoff source in the reviewed tree obtains or authenticates them.
Tests compute them locally. This is equality checking, not independent Farm
authentication; absent real handoff inputs must remain `NOT_READY`.

## Closed controls (source-level only)

PASS: pre/post phase ordering; complete missing census; D139a 18-row/12-hash/
six-unhashed/direct-URL/manifest path checks; field-only poison; failed import
stop before dry/core; durable XML/raw/start-stop/disk/KEEP and 22-root selector;
unchanged C0 request/reply documentation.

These are not Farm execution results and do not raise the verdict to GREEN.

