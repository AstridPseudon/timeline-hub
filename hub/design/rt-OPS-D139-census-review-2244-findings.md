# D139 census adapter review

Verdict: `PASS_SOURCE`.

## CENSUS-005

Resolved. The checker now recognizes the authenticated Agent 2149 packet by
its fixed schema, exact 4c/ab1e source tuple, fixed packet SHA-256, complete
1,146-row membership, and exact row field shape. It maps `module` to the
checker name only after authentication, derives classification from the
canonical `category`, preserves every input field and row order, and probes
both the 10 `unconditional_required` rows and the 12 `missing` rows. The
12 missing rows are reported separately from installed requirements.

The source-backed classification controls keep relative source, stdlib,
platform conditional, optional, dynamic-unresolved, and external
`typing_extensions` distinct. Malformed, truncated, tuple-tampered,
schema-tampered, row-tampered, reordered, or hash-tampered canonical input
refuses before probing. Caller-supplied legacy classification cannot select
the canonical probe policy.

The exact supporting-system CLI returned exit 1 with 1,146 census rows, 22
attempted modules, 12 missing-census modules, and 12 failures. It did not
claim a real registered child. All-missing behavior was exercised privately
without first-abort behavior.

## Scope limits

This is a source/security review only. No source, test, generated file, pin,
installer, Store, registry, provider, package, child, or body was changed or
run. The 12 registered-child and 5 optional/plugin missing classifications
remain the prior finite evidence classification; they are not genuine child
acceptance. The owner-approved physical schema carrier and genuine child
receipt remain outside this review and are not claimed here.

The shared runtime venv diagnostic lane lacks `typing_extensions`, so its
invocation of the pre-existing synthetic external-import test returned one
environmental failure. The exact system-Python focused lane passed all 57
tests and is the recorded acceptance result.
