# P4 D141l owning receiving review

Result: `PASS_SOURCE`.

## Findings

1. The author packet’s checker is fixed-root only. `check-source.py` accepts no arguments, derives `ROOT` from `__file__`, and hard-codes the sibling `inputs/`, `private controls/`, launcher, installer, and source paths. The exact absolute author checker was run read-only at its original path and exited 0. Independent reviewer outputs were not substituted into it, because it has no supported independent-path arguments. This is a reported checker limitation, not a source failure.

2. Later native admission is unresolved for the behavioral body. The installed `test-run` classification keeps `p4-current-becfe-http-3legs` as LIGHT with the 5,000,000,000-byte floor; the recorded D89d4714564096 controller floor is source evidence and does not override that row. The body therefore remains unrun and earns no behavior credit. The eventual continuation must obtain genuine native admission, own one heavy run, and maintain the 4,000,000,000-byte/5-second condition. No forced run, new suite name, kit, floor, or service override was used.

## Qualified evidence

- Current Agent/Runtime/App/Composition homes match the exact ecdc242/95d98f/82e9e1/635f4de commit, tree, parent, and origin tuple; all are clean.
- Owner custody matches the genuine Agent profile: Node `v20.19.4`, lock/archive/registry hashes, Runtime lock hash, composition `0.0.14`, and schema digest.
- Unchanged launcher and installer hashes match the author packet. Launcher `run` mode was exercised only by the tiny controls: positive preflight `0`, stub body `17`, one call; Agent-SHA-only poison `1`, zero calls, expected mismatch.
- Input and materialized manifests are distinct files with equal SHA256; the durable future XML path is consistent across candidate row, manifest, and runmanifest and does not exist before the body.
- The selector is exactly `tests/editing_conformance/test_p4_cli_sheet_v2_runtime.py::test_cli_sheet_v2_runtime_preserves_document_and_reads_back`; pytest predicates and the original three-test aggregate guard are retained.
- `design/commit-v2.md` was read as the settled contract. The v2 request/reply field inventory remains contextual evidence only; no authority, schema, or source was changed.

No product source, tests, pins, Git refs, shared dependencies, registry, CAS, service row, or historical receipts were changed. Keep 19479/8912 untouched. Do not claim P4 behavior, REG0, build, ZIP, or full-suite credit from this packet.
