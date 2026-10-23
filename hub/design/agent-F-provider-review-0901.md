# F-provider independent Luna review — PASS (bounded source)

Reviewed `tl/agt-F-provider-0847` at
`fad05679ae45ff4eb32190fdae40ae1cd1e56db6`, parent/base
`e837e18c5156e762eca05e6d9bb15779cf847b60`, against PLAN §3 R1/R2/F and C0
§§2/3/5.

## Verdict

**PASS bounded source repair; FAIL as a whole-ten acceptance claim.** The exact
ten-node group independently reproduces **7 failed, 3 passed**. All unchanged
video-unplace variants independently pass (**4 passed**). The candidate’s
source change is limited to emitting existing authenticated materialization
proofs for synthesized legacy semantic steps. It does not alter inverse.py,
Runtime auth, schemas, pins, shared dependencies, or the full v2 request/reply
surface.

## Source/authentication finding

`CommitPatch.before` captures the actual pre-command bundle, `after` captures
the actual post-command bundle, and inverse segment pairs come from the
existing executed inverse stages. The new materialization loop consumes these
closures plus execution records. It does not consume caller step patches or
caller bindings, and it does not synthesize authority by matching bytes or
searching history. Existing `_materialization_sites` validates the persisted
source physical ref, revision, digest, owner, successor, both managed-edge
endpoints, evaluated head, phase, ordinal and step; missing or damaged proof
remains `history_unavailable`. Full records/steps/bindings, input-output
digests, effect ranges, previous-value and ABA guards, surviving-consumer
checks, refusal state, and undo/redo allocation provenance remain intact.

The added test preserves the four original positive cases and checks proof
presence plus closed refusal for missing or altered proofs on pooled
intermediate-image cases. This is aligned with C0’s authenticated continuation
rule and does not grant caller-controlled materialization authority.

## Evidence

- Exact ten-node pytest command from the authorbrief, independently run with
  the prescribed Runtime checkout/Agent venv: **exit 1, 7 failed, 3 passed,
  22.39s**. The full command is recorded in the worker report.
- Exact unchanged video-unplace parameter sweep: **4 passed, 13.52s**.
- Scoped Ruff and normal Ruff: pass; normal count **2149/2149**.
- Exact-tree author evidence for mypy: **1912/1912**; my independent wrapper
  retry was silent/long and stopped, so no stronger independent typecheck claim
  is made.
- Vendor lock, artifact manifest, and `git diff --check`: pass.
- No full/P1/P4 HTTP/native14/crash24/heavy browser/tour or Runtime 58-matrix
  duplicate was run.

## Seven remaining failures / exact next owners

1. Recorded graph-root net-zero inverse — **R2 existing inverse owner/review0836**:
   sequential restoration writes versus a coalesced absent-to-absent oracle.
2. Native add/delete net-zero `[False]` — **same R2 owner/review0836** and
   same recorder/oracle cause.
3. Native add/delete net-zero `[True]` — **same R2 owner/review0836** and
   same recorder/oracle cause.
4. Provider parent-media preview — **R1 preview/capture owner**: the provider
   records a context-derived ordinal-2 `commit.input` physical binding absent
   from the direct recipe record; make the oracle context-aware without losing
   exact selections, dry-run/no-accept, records or canonical output.
5. Stale old parameter basis — **V2 scalar fixture owner**: initial add lacks
   uniquely retained authentic project schema metadata; repair fixture setup,
   not validator authority, and retain the stale-basis refusal.
6. Authenticated child staging — **V2 graph fixture owner**: initial child
   timing violates half-open bounds (`hold=3s` versus `duration_ms=2000`);
   repair authentic timing while retaining exact closure and undo/redo.
7. Render pin ClipLook test — **V3 Composition adoption-test owner**: the
   regex rejects the SHA-named adopted `.tgz` artifact before behavior runs;
   resolve through existing adoption metadata/behavior without changing pins.

No upstream-preexisting or guessed deferred attribution is made. Runtime
intermediate whole-inverse authentication remains owner `0853`; this review
does not duplicate that repair or the 58-matrix/HTTP run.
