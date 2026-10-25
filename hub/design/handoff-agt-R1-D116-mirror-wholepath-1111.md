# D116 mirror wholepath handoff

## Result

Candidate `7c717062128f61adacf613b6ee05a0992abb9024` is source-qualified, not
full-green: the retained protected sample is 6 PASS / 2 FAIL / 0 error / 0
skipped. Both failures are genuine current-form recipe failures at
`bundle_from_document` → `lookup._parent_clip_list` (`lookup.py:343`), where
`parent.clips` and `parent.config.clips` disagree.

The exact D116 source pairing is the three changed conformance files on the
candidate commit. Their SHA-256 values and the retained XML digest are in
`workers/agt-R1-D116-mirror-wholepath-1111/evidence/source-facts.md` and
`.json`.

## Trace and C0 purpose

The source trace is: current-form seed → registered Agent provider → full v2
request (base, commands, label, ordered steps, merge, reads, dry-run, source,
rationale, group and Idempotency-Key) → Runtime commit → canonical readback →
`bundle_from_document` → current word recipe compiler → `_parent_clip_list`.
The first-use accepted record retains the transcript pin and retries exactly
after restart. The retained rejected controls cover unavailable pin/digest/
document, short occurrence and raw source window. No source, auth, previous
value, inverse/ABA, opaque, FPS/timing or short-negative purpose was relaxed.

## Attribution

Earliest changed mirror/field owner is **UNKNOWN**. The emitter’s deliberate
single-list projection, Agent patch applier mirror rules, and Runtime output
projection are all visible in source, but no retained actual-boundary image
shows where the pair first diverges. Do not normalize one side or infer a
production fault from the exception.

Exact next owner: **held `82b6` producer owner and the Runtime output-projection
owner**. They need an authenticated boundary-level pair capture and must keep
C0 lossless raw/config mirror behavior and D101 field-union rules. No competing
product writer is indicated.

## Scope

No product/test/generated/pin/registry/ledger files were edited. No tests,
typecheck or lint were run; this was a static source/hash/JSON/AST publication
task. No raw requests, stacks or credentials were exported.
