# D136c handoff

## Owner and disposition

Runtime already owns the producer and public refusal envelope in
`runtime_protocol/timeline_commit_auth.py`, `runtime_protocol/timeline_commit_store.py`,
`runtime_protocol/timeline_commit_port.py`, and `runtime_protocol/service.py`.
The missing reporting seam is outside that contract: the Agent/Proof
test-reporting owner owns the existing original-nine JUnit handoff.

The finite result is **BOUNDED_SEAM_FOUND**: Runtime safe fields survive to the
mounted `RuntimeErrorBase.details` reply, then are omitted by pytest JUnit's
error serialization. Actual field values are **UNKNOWN** in the retained
original-nine artifact. Do not classify this as product gap or setup-only.

## Smallest supported existing approach (proposal only)

At the existing caught-exception/report boundary, retain a detached projection
of `RuntimeErrorBase.details.safe_diagnostic` as a sidecar in the existing
JUnit result/report channel. Validate the closed 13-key schema before writing:
booleans, fixed enums, bounded ordinals or `UNKNOWN`, and one-way digest hash
only. Preserve the existing guard, status/code/message, exact authored inputs,
all 43 assertions, 11 bodies, 54 fixture statements, no-write behavior, and
privacy. Do not publish raw exception text, traceback, IDs, refs, paths,
payloads, images, keys, URLs, user content, or private paths.

This is a proposal only; no implementation or body was authored. No additional
original-nine run is needed for this seam. The single D136c body is spent; any
new body requires recorded owner approval. D130 SWAP/WAL/recovery/related
qualification remains on hold.
