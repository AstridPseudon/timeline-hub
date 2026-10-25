# F-D86 Runtime input assessment

Result: a genuine unused managed pin exists in held Runtime fixtures.

| Fixture | Project / timeline / revision | Accepted publication(s) | Unused managed pin |
|---|---|---|---|
| `precut-baseline-v31.tar.xz::explicit-media` | `95640e46f62b4d0ca20c97d66f792782` / `main` / `parent-media` | `txn-effa95754bc941a4b8b6946df663496e` (event 2) | `sha256:0851b1debd871ed81bc8548f294b95ac233ba1d7fb7f41c0ed6060c6ed644e29` |
| `precut-repeat-media-v31.tar.xz::repeat-media` | `03a205650e4f42c7af930fc55734793f` / `main` / `parent-media` | `txn-a142d9625a7d40178507195db97c2dbc` (event 2), `txn-dcb9f5268a934b8dac42af63e7121f9d` (event 3) | Same pin |

Evidence:

- The unused pin is an authenticated `audio/wav` CAS object, 12 bytes, listed in `cas-manifest.json`, `project_objects` as `managed`, and the accepted `dependency_manifest.media`.
- It is absent from parent, shot, and internal-timeline payloads.
- The other managed pin, `sha256:20dcb0d3fabda9b4f2ad6e20491e0c6447c117ebd4ce3b8471c82b876`, is consumed by the parent live-scene payload.
- Repeat fixture hashes: archive `acada05f8f9425c71ec5c3dd82b35cfeb6f35627938ebbf77ab6be930a470e9a`; manifest `a14056833cdb78099802c5fd6c1ea7878e91e244cc41fcde255449323013152d`; CAS manifest `d4fbab5cd02fedd4e06cac8e6c10dc99769b81c13a3818d5e1d9b9b0a9c0641f`; database `786fcbcbbf1ca5e19d9a4d22ae7748b70a9996e9133083db07a217aed7447ebf`.

Important limitation: these are genuine schema-31 legacy accepted publications. Their head has `publication_id = NULL` and `timeline_commit_history` has no current commit edge. Current source-copy validation requires an authenticated history pair, so direct current `commitTimeline` consumption remains unverified and may return `history_unavailable`. I did not reconstruct history, run helpers, or modify Runtime.

Checks:

- Read-only source, JSON, archive, CAS, and SQLite inventory completed.
- No tests/services/browser/builds run, as explicitly prohibited.
- Worktree clean.
- Commit message written; `DONE` created.