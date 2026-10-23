# G3/P4 reader clean port — PASS

Source-only package on current base `6131704b36807e165575fa944ba984cc847059c8`.
Donor `a8132afba38ca66b1c815ed2c99404a66a02337f` has that exact parent. Imported
only the four intended reader/test paths; excluded donor root `report.md`.

Exact current blobs equal donor blobs:

- `astrid/sdk/_remote_timeline.py` — `bc8b9fceb9be561f2b77529743a0754e76b092b8`
- `astrid/sdk/authoring_revision_diff.py` — `db106a74fef4e656c4255bc488eaebc55c4f11cd`
- `tests/sdk/test_authoring_revision_diff.py` — `8f59a4b15cffb746d37b59c2086fa2d7435bc599`
- `tests/sdk/test_remote_timeline_owner_scope.py` — `7fffe374a0c6db8999135f41a17c71ac7004fd12`

Current status has exactly those four paths; no root report or unrelated,
generated, pin, schema, fixture, or dependency change exists. Base tree is
`b4a194abe8601470ea7fa9b38ea54e258dc673c3`; donor tree is
`bdb58ee065961732d1a21b8c9b52a35427521f36` and includes the excluded report.

Readonly reviews: prior `47aa77266` review **FAIL** (repaired by donor); local
45-test/source-quality review **PASS**; independent exact-`a8132afba` final
review `agt-P4-shared-read-final-review-0606` **PASS**. Production wiring is
`timeline.open → store.fetch_bundle → RemoteTimelines.open_bundle` and
`RemoteTimelines.diff → read_authoring_revision`.

Evidence: exact target pytest **23 passed**; scoped Ruff/mypy **PASS**;
`make ruff` **2149/2149**; `make mypy` **1914/1914**; pinned vendor lock,
artifact manifest, import-origin/caller smoke, and `git diff --check` **PASS**.
No full/browser/live HTTP or Proof-owned HTTP body suite was run.
