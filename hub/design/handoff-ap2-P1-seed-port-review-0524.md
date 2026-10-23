# P1 seed-port review handoff

## PASS

The current-base port is limited to
`tests/e2e/local/three-products.p1-chain.spec.ts` and exactly matches the
independently reviewed donor `ec8e8a25cf7ac29247d06bc5a224b94145ee71c3`.
The spec SHA-256 is
`926cdadd0370f0648e03b4bba743b56c1e7c80f0ff3fa1887ba985e9bc772fd1`.

- Base: `18354adfa3e8f12b24816a159f28a9a6cbb9a3f6`
- Source SHA: `5c57947185717c5726cd9c31c4e0331a0502158f`
- Source tree: `71a9bc1cbf1926a82f92768c375153caf9a09358`
- Own commit: `5c57947185717c5726cd9c31c4e0331a0502158f` (only commit in base..worker)

The only code delta is the top-level-authoritative Runtime GET slug correction
`project.body.data.slug` → `(project.body.data ?? project.body).slug`. Both
original P1 cases and all C0 v2 assertions remain unchanged. Outside blobs equal
base; `support/astrid.ts` remains the current-base blob. The separate support-env
request and donor product ancestry were not imported.

Checks passed: exact two-test list, `npm exec tsc -- --noEmit`, scoped ESLint,
`git diff --check`, donor hash/blob, outside-path/blob, and one-own-commit guards.

No body/browser/service/build/full run was performed, and the existing actual
two-case run was not duplicated. This is source-port PASS only, not H3 GO. The
central actual journey remains required because the production caller needs the
real body and accepted/merged/refused plus lost-ack/restart evidence.
