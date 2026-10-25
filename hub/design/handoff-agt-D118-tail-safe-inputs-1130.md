# D118c retained-input safe metadata

Read-only join of the existing D108 original run and D118/30693 pinned run.
No new body, collector, credential, payload, command, or URL was read or
created. No product source was changed.

## Retained runs

| run | XML SHA-256 | body-log SHA-256 | Agent | Runtime | App | Composition |
|---|---|---|---|---|---|---|
| D108 / 2016 | `72872c77087719a692bff4b48b8d85ea62b9931d59a502c8e246daee0c81c18a` | `0f34700508bfe35c94d2811d502b442cc36d4db4c4643303d8ca5dfd8f5af001` | `070dfc5ef4f3dc35062fcb36a50cb571cd77fbd2` / `6056414359ae9fce08d999d54cbecf719fda33c3` | `1daca2a33f6d7b10053e07c539a54843e3984e19` / `a522511414947e48e317a5e5c2103483b121a750` | `04beedcd18b8abb49502f65cd3facaafbe93db4e` / `300d186a45d3d0b96ef2ae39582f1e9b4a760e7d` | `635f4de06fda22a85fc2e4cfc764d0153a4c9f40` / `5ab5191a296980a0a6bcd1178ab6902d6478a148` |
| D118 / 30693 | `483e5c13c3443147488da436acc49d0c0f322f7e4d3f020fbd656a548459139c` | `7bae40c4091d95ada10ea4c91980941acb06310ff5761004b6c8d66828565805` | `120d71202a9ebafa99011aec417cfca6d67fafc2` / `9a65a32e4462464825df6cfe4d913408694ad4c5` | `1daca2a33f6d7b10053e07c539a54843e3984e19` / `a522511414947e48e317a5e5c2103483b121a750` | `96d4754b4eef0591a208d6b51b60c30fc44b6915` / `3f9da34c4f116026ec21022421850e0608ba653b` | `635f4de06fda22a85fc2e4cfc764d0153a4c9f40` / `5ab5191a296980a0a6bcd1178ab6902d6478a148` |

The 30693 service summary contains an ambient tree label that disagrees with
the pinned manifest; the manifest, pinned checkout, and per-node source map
agree on Agent `120d71202a` / tree `9a65a32e`. This is metadata only.

## Exact retained nodes

Ordinals are 1-based positions in the original 2016 XML. The current XML was
reordered, so the D118 row is joined by exact node ID.

| scope | original ordinal | current ordinal | selector | run source SHA-256 | result and exact boundary |
|---|---:|---:|---|---|---|
| occurrence-create `[False]` | 1286 | 1455 | `tests/editing_conformance/test_commit_runtime_occurrence_create.py::test_bootstrap_birth_child_media_exact_history_inverse_redo_retry[False]` | `26ecb3e8da202dc9a1113f942cf9c1a7384600d8662cb9c1e8d983caf17afe6f` | `AssertionError`; outer fixture location `test_commit_runtime_occurrence_create.py:70`; helper `_prove_birth` at line 173; expected status 409, observed subprocess return code 1. No product/provider frame captured. No-write/prepared-record status: `UNKNOWN`. |
| occurrence-create `[True]` | 1289 | 1460 | `tests/editing_conformance/test_commit_runtime_occurrence_create.py::test_bootstrap_birth_child_media_exact_history_inverse_redo_retry[True]` | `26ecb3e8da202dc9a1113f942cf9c1a7384600d8662cb9c1e8d983caf17afe6f` | Same exact exception and frame boundary as `[False]`; failure-text SHA differs: `1b6fb40635fb3d07dad7f056e30744f0e369b4b09429261177ec7f762ab425a9`. No-write/prepared-record status: `UNKNOWN`. |
| prepared-video | 3116 | 3171 | `tests/editing_conformance/test_prepared_video_birth.py::test_prepared_video_public_preview_accept_retry_undo_and_no_write` | `4cc89a0a7bbc4e1020e3ca9c676e7125113ee60c517bfdf5e3cd0821620cdc2c` | `AssertionError` at `test_prepared_video_birth.py:251`: retained source asserted stale Runtime identity `6634a17f...`, while the run used released Runtime `1daca2a3...`. No product/provider frame. This is setup-pin boundary, not behavioral acceptance; no-write/prepared-record status: `UNKNOWN`. |

Original classification for all three was `UNCLASSIFIED_NO_UPSTREAM_EXACT_NODE`.
The 30693 per-node map records `assertion_failure` for the occurrence and
prepared-video rows and preserves the same no-upstream-exact-node status.

## Existing D118c source comparison

- Occurrence candidate source SHA-256 was `91b0d3e7f5815892e58cb0256640a08173fe3e7703cff0a4caa480d0e9bcf855`, changing only the caller wrapper metadata. The protected review rejected it as unapplied: omitted semantic label/steps remain compatible, and the added metadata does not affect the genuine line-70 / `_prove_birth` failure. No candidate diagnosis is copied here.
- Prepared-video candidate source SHA-256 was `ba4acbcdee2a42c85ab7070a26983a59915ddcdfc395214761feb727c8e44476`, changing only stale setup identity literals. The 30693 run used the pre-correction `4cc89a...` file, so its line-251 failure remains a setup boundary. The same file’s neighboring normalized-video tests passed in the original run, but that does not prove the retained public-preview behavior.
- A separate recipe occurrence-create selector passed under source `7b8dbb69afe814d92d0f8032b7fae8aa8d43c2aa1f826834d1b99ed2aadb4a4e`; it is not the same caller and is not treated as causal evidence for the two retained failures.

## D102 redacted-chain boundary

The already-captured D102 diagnostic contract is only the bounded chain
Runtime catch-all → one redacted diagnostic → source file/line/function plus
opaque correlation. No target-specific product exception chain, accepted
prepared records, or authenticated no-write proof is present in these retained
artifacts. Therefore product cause, accepted/merged/invalid reply semantics,
and no-write outcome are `UNKNOWN`, not inferred.

The production path remains the existing registered `commitTimeline` / real
Agent provider path. No auth, inverse, previous-value, ABA, request/reply,
registry, source, or caller ownership was changed.

Tests/typecheck/lint: N/A for this existing-artifact reader task.
