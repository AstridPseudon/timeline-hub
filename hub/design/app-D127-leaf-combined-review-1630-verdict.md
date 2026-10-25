# D127 independent combined leaf review

Verdict: **FAIL**.

The candidate preserves the normal and reviewed-legacy validator arms, adds the exact reviewed-new helper hash `4ee0424b63f1f9847995a605dc1050ad7cb8ca75f4d64b8c36d851cfe723f41e`, and keeps the requested exact keysets, privacy checks, bounds, phase contradiction checks, leaf/inclusive frame checks, loss/share/denominator checks, retention checks, and mutation negatives.

Blocking finding:

- `tests/e2e/local/support/p2-runtime-phase-bootstrap.test.ts:257-280`: reviewed-new lifecycle is not cross-checked against the phase map, duration state, or `retention.final_request.outcome`. The validator only constrains the enum and nulls some durations for `raised`/`pending_at_stop`. It accepts contradictory completed/returned-without-response phase and duration states, and it accepts a summary lifecycle different from the final retention outcome. This violates the frozen lifecycle derivation and strict cross-field custody requirements. App owns the seam.

Proof split:

- Source/scope: partial pass. Only the assigned App validator file is in the candidate diff; no source edits were made by this review. Helper source is byte-exact at SHA256 `4ee0424b…`.
- Focused proof: partial pass. D105 + D127 validator/mutation controls passed; D78 passed with qualified Runtime `ab1e4f61`; reviewed-new bootstrap passed through the normal harness with qualified Runtime product source and the external exact helper/hash hook.
- Not qualified: strict-islands typecheck remains red on the documented missing generated/virtual modules and unrelated implicit-any diagnostics. No full suite, browser journey, original tour, native, collector, activation, SWAP, or unrelated profile was run.

The prior 1613 overall FAIL is retained, not erased. No App or Runtime source was changed.
