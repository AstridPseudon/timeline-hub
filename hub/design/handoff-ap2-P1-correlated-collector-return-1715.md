# Handoff — ap2-P1-correlated-collector-return-1715

PASS for the bounded first-return correction on App `439f6ddbf` relative to `4c4c9c77c`.

The detailed failure caller no longer emits raw/requestBody/body/reply payloads. It retains structural route/status/head/count and basis summaries, while the in-memory `post.raw` and exact retry assertions remain unchanged. Source-window snapshots use immediate bounded DOM `evaluateAll`; missing, ambiguous, and detached nodes are `UNKNOWN`, and unique attached hidden nodes are `false`. Priority packets retain a parseable causal core under 16 KiB rather than collapsing to `priority_over_budget`.

Evidence: pure diagnostics 8/8; root/App/Node TypeScript; scoped ESLint; exact Playwright list of 2; diff check; allowed-path identity; original suffix SHA `582dc8fbc3cdf1991b981dce969e3981b63484b70aaeb70f331d907f5b2fc9bd`; frozen Composition archive SHA `819acf6b3815d6eeabe772a9569581fedbe4f9c9cce35946efca9454e2040234`.

The worker used Node `v22.22.0`, not the requested Node `20.19.4`; no browser/body/HTTP/service/full execution was run. Actual mounted capture/basis/adoption and Runtime refusal remain UNKNOWN. Fresh independent review is required.
