# Runtime capture composition on current base

Worker: `rt-m3-capture-final-current-compose`, 2026-10-20.

The approved retained-candidate validation from `5628c6be1358db145c0dbd50514c39b06c34b0a7` (reviewed `082a905` provenance) and the complete approved alias/claim-identity changes through `e6abb5bd181a80eb553f99bff82b158b41589955` are composed onto current Runtime base `8609333456b9537339ee1a5dfc7ffd9609242de8`. No design decision changed.

## Construction and authority

The existing startup-loaded Agent provider supplies optional pure `capture_candidate_inputs(document, candidate=...)`. Runtime compares the complete retained placement map, every placement and shot source value, both child bases, embedded Runtime document and the full derived publication. Existing revision closure validation, immutable document pins, digests and scope checks remain. All comparisons precede the existing projector and admission writes. Missing candidate hook refuses candidate certification; explicit CAS and candidate-less previews retain their existing uncertified behavior. Legitimate new/clone/rename/delete/drop authoring and retained source aliases remain supported.

The Agent continues to own candidate construction and the single `project_runtime_parent_composition` projector. No second projector, stored state, DTO, endpoint, IO or renderer/save dependency is introduced. The surviving Agent verifier is retained.

Claim-time inspection covers all three snapshot aliases in nested and outer authority contexts. Rejected references are identified by `(alias_ref_key, canonical_json(full_reference))`. Thus exact copies in dictionaries, lists and JSON arguments are relabeled CAS-only while a valid nested claim sharing the same CAS digest retains its independent scope/revision/candidate identity. Relabeling returns a worker view; immutable stored spec/history and original retry identity remain intact.

## Source identity and live provider

The only changed product file is `runtime_protocol/capture_validation.py`: 151 base lines -> 225 current lines, +74 net (+93/-19). Its SHA256 is `572d4c8ec61e2705ce56aa3d5733b500c64ba06b9e5addca885bd457388f6b75`, exactly the independently reviewed private composition in `runtime-alias-identity-final-review.md`. Non-claim functions retain the approved candidate-basis implementation; the claim function/import retain the approved alias implementation.

Resulting Runtime tree: `51cfde210a3f55a6184a4ba1eac50e13d7d52bbc`. Two existing files change and two approved test modules are added. All 405 other base blobs are byte-identical; all ten original top-level definitions in `test_capture_candidate_actual.py` are AST-identical. Each test file is byte-equal to its approved source.

The exact approved Agent pair is `92427b3af0bfaba2ff604791cf3e5165125b6d54`, tree `525bdabe863a42bc177f5ff331560133f77ce634`. The central paired lane's fixed source archive was verified against all 3,008 Git blobs, with no extra files. The live Agent integration at `a2ba1bca3cb68a15abb62a1260162c4cb73903af` contains both approved provider methods unchanged, through the merged port `0d9d0764aaa74f8d8786f2161b3280f2b2e0f147`. The original approved SHA is not its ancestor because the hook was ported to the current integration root; method equality and the port's ancestry were checked directly. No missing-hook integration hold applies. Paired capture tests still use the exact frozen approved archive; this is not qualification of every current Agent consumer.

## Qualification

All four central selections passed on the exact tree above, one request per distinct selection. No full/broad suite or repeat selection was requested.

| Selection | Result (exit 0) | Request |
| --- | --- | --- |
| Paired capture | 141 passed in 117.52s (0:01:57) | `rt-m3-capture-final-current-compose-capture-agent92427b3a-integration-1020112540-5907` |
| Claim matrix | 25 passed in 21.54s | `rt-m3-capture-final-current-compose-capture-agent92427b3a-integration-1020112540-8594` |
| Ordinary snapshot | 41 passed, 170 deselected in 35.69s | `rt-m3-capture-final-current-compose-targeted-1020112541-18408` |
| Commit integration | 9 passed in 19.79s | `rt-m3-capture-final-current-compose-commit-integration-1020112541-28128` |

The ordinary lane’s 170 integration deselections are not passing-provider evidence. The exact marked 141 and 25 cases execute against the approved capable provider. The 25 cases include all six full-claim-identity saved/candidate preservation controls and 19 neighboring alias/outer-context/mixed-result cases. The commit lane uses the recorded live Agent integration. No skips or xfails were reported. Direct Ruff, whitespace and read-only source audits passed. Exact commands, source inventory and qualifications are in `workers/rt-m3-capture-final-current-compose/DetailedReport.md` and `source-audit.json`.

## Boundaries

This bounded composition does not close the four external RenderRequest `verified_source` propagation requirements or three SDK invocation early-guard requirements cited by the independent reviews. Their status must be decided from their separately owned successor evidence. They are not reclassified as passing or refusal behavior here. No renderer, Composition/pixel/audio parity, SDK enqueue/CLI transport, broad/full suite, delivery ZIP or Gates 1/7 qualification was performed. Frozen-provider seam tests and host-materialization positives do not establish actual export behavior.

Next: inspect the harness commit, then let the Runtime manager/orchestrator decide integration of the exact qualified composition. No merge, push or publication is performed by this worker. Keep verifier removal and external consumer qualification separate.
