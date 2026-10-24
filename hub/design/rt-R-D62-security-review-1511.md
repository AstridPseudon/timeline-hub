# PASS — independent security review

Reviewed joined Runtime tree:

- HEAD: `e02f3e3d9d972be74450536ec0ee49e8bc51c2ec`
- Tree: `a095ecbe8b01b0ff0a7825c4c19bbf41120ec3ed`
- Base: `e68cf231641db98a72805a586b51ab5c4fae2c16`

Findings:

- Runtime derives `recorder_abi` only after `_validate` accepts the records.
- Event and metadata authenticate ABI, request hash, records digest, and metadata digest.
- History/replay re-verifies event chains, records, request identity, mode, and metadata.
- ABI1 omission compatibility remains strict for command equality, claims, inverse restoration, bindings, reads, effects, and downstream checks.
- Forward-created omission is authenticated against exact owner, row identity, allocation fact, absent read, and root write.
- Invalid enum types, one-sided deletion, mismatches, post-accept stripping/full rewrite, and explicit inexact claims are rejected.
- D62’s deferred native-completeness gap remains visible; no custody seam was added.

Evidence and provenance:

- Exact producer blobs match `8825219b456d47579bc75f9b9d630ab9f4eaed82` and `943365586247bd4b395fbb70580773259e2d8315`.
- All wire/generated blobs and canonical-15 inventory match reviewed `6e8ae0142655eb7a6d10083d2d3ae5d434b5c94e`.
- Four neighboring test files are byte-identical to e68.
- Archived Agent `9460a44336643291f2ab4d5d5085e7cfc391c495` was used read-only. Six-file targeted matrix: **412 passed**. Provenance capture: **143 modules**, 139 reviewed Agent modules byte-equal; four Runtime client modules correctly came from Runtime.

Tests/checks:

- Targeted pytest with archived Agent source: **412 passed**, 158.71s; XML retained.
- Ruff: both scoped commands passed.
- Compile: all four changed Python files passed.
- `git diff --check`: passed.
- `generators/generate.py --check`: passed.
- `scripts/artifact_manifest.py --check`: passed.
- Pyright: 74 existing store diagnostics in both baseline/current, zero new normalized diagnostics; auth had zero diagnostics.
- Wire SHA-256: canonical schema `3654ca3c...`, runtime bundle `e4da5c0e...`.

Author result preserved without rerun: home Agent `68e82c0c...` had **411 passed / 1 failed**, unchanged `test_genuine_fork_recorder_authority_history_and_exact_retry[1]`, `RuntimeErrorBase: fork source binding changed`. The exact reviewed paired Agent source passes this control; this is an Agent-home adoption seam, not a Runtime-owned failure.

The forward author’s expanded **324-test** probe retained one deferred `write=True` producer-trust failure; final retained scope was **323 passing tests**, with no weakened assertions.

Limits: no full suite, HTTP/browser/live journey, socket proof, or actual Agent-home four-original completion. Exact behavior-change line retained: “Runtime does not prove a v2 producer's native coverage is complete at submit (Sol1422's 8 omission packets); such commits fail closed at fork/inverse use.”

Evidence retained under the worker `evidence/` directory.