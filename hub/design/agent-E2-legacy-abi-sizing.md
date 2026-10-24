# E2/D81 sizing

Implementation estimate: **52 worker-hours total**.

* 34 worker-hours permanent follow-up: owner-approved status projection/read,
  explicit post-cutover refusal, pre-inverse status gate, and conformance
  integration using existing Runtime history authority.
* 18 worker-hours one-time migration tool: source reverify/digest,
  classification, transactional cursor/resume/idempotency, partial state, and
  unknown/tamper reporting.

This is an implementation estimate, not measured design time.  Risk is **high**
because a partial physical-binding record can look modern under the current
“any physical binding” classifier, and because exact old retries and immutable
history must remain byte-preserved.  Dependencies are C0, the existing Runtime
history/event/receipt verifier, the existing Agent inverse gates, a complete
modern producer audit, and owner approval after the ZIP.

The estimated source budget is 87 removable lines versus 64 additions (34
permanent plus 30 one-time-tool), for approximately 23 fewer lines.  If the
implementation exceeds the additions budget or needs a new trust surface, the
owner should mark E2 NOT READY.

POST-ZIP proof must cover the same P1–P5 and affected core gates, old exact
retries, migration crash/resume/partial/unknown/tamper, safe whole/per-step
inverse and A→B→A, immutable bytes, and source/owner/order/read/previous-value/
range guards.  The source-only acceptance checks in the design are not that
implementation proof.
