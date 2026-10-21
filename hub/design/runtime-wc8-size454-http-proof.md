# Runtime WC8 retained size HTTP proof

Date: 2026-10-21

## Result

The retained detached `am-type` size route has one actual current Runtime HTTP
proof. The new test
`test_current014_detached_size_clear_uses_one_native_http_commit_and_guarded_inverse`
uses the historical closure fixture, loads the retained sheet before editing,
and sends one ordinary `/v1` commit containing the existing `clip.set-params`
operation for an explicit size clear.

It checks original basis/publication pins, exact command capture, raw reload
preservation of opaque/null/absent fields and sibling order/isolation, and
guarded inverse/redo with exact restoration of the original `size=32` value.

## Exact qualification tuple

| Input | Identity |
|---|---|
| Agent base | `4542b759c7cdc9074260d8f6d0f193a7147f72a1` |
| Central source tree | `2d3712e84afb0e1268089e0440cd68db81c5336d` |
| Current Runtime server | `b92d3e7a05eec65c142294ef4873edd059e9b31d` / `6abc2f117391de8e7e35c0283f575a002199894d` |
| Published producer | `95bd3c5f6d00e9bc8cc8cbe5ef510b68ed660f3c` / `d3a290b407fa61e6ab2d476f50c068073f70df00` |
| Client / Runtime wire | `0.2.14` / `sha256:7d4afa05962b8cd61643213fc79cdde41e16046c4e2a777bd299b48af0f31816` |
| Ordinary raw schema | `sha256:6ba7b51e9518e7fb08b27ad5b7225855276b657d0adebf704dd853f699768f2d` |
| Artifact | `all76`, `sha256:54205b3ecb55038e416b31af936c9af26afa30dc1b05da16157ee4d861fe05ac` |

## Test evidence

Central test ID:
`rt-m2-wc8-size454-one-actual-proof-0743-rt-wc8-current14-integration-1021074723-46`

Result: `1 passed in 4.27s`, exit `0`. Collection preflight collected exactly
one node. Independent size safety review approved its direct unit neighbors
(`92 passed`). No full, browser, renderer, install, or direct-socket run was
performed.

The central validator rejected one initial absolute selector before execution;
the final request used the suite-required relative file/node selector. Two
early executions failed only on over-specific assertions in this new test
(retained-vs-rendered sheet banner and canonical parameter-key order); they
were corrected. The final result is the only qualifying evidence.

The only live production size bridge is the pre-existing
`apply_sheet` → `_duration_sheet` path. This proof adds no callers and makes no
whole-WC8 retirement claim. HOME current-preserving port and orchestrator
disposition remain next steps.
