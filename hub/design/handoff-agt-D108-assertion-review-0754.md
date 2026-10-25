# F-D108 independent assertion-map review

Overall verdict: FAIL.

| finding | verdict | result |
|---|---|---|
| Source identities | PASS | `d6294843`, `b943270a`, `08e6b905`, `92443771`, and `c456b328` are present Git commits and match the map's named identities. |
| Captured-versus-normal scope | FAIL | `d629..b943` changes six paths, including D110 `astrid/sdk/timeline/inverse.py` and `tests/sdk/test_inverse_removed_shot_owners_runtime.py`; it is not D07-only. |
| Fallback predicate direction | FAIL | With declared old=`d629` and current=`08e6`, AST multiset accounting is 189 changed bodies, **310 removed**, and **119 added** assertion/raise fingerprints. The artifact reverses 119/310 and therefore also reports the wrong residue: correct residue is `60 / 197 / -168`, not `60 / 6 / 23`. |
| Authoritative aggregate handling | PASS | The named rehearsal manifest is absent at its exact recorded path; `129 / 113 / 287` remains `EXACTMISSING` and is not cleared. |
| Crosswalk hash | FAIL | `approval_inputs.crosswalk_sha256` (`37e559...a4504`) is the retained crosswalk's missing-manifest expected hash, not the SHA-256 of `design/handoff-rt-D108-python-0700-d108_citation_crosswalk.json` (`e131b68c...1515`) or its Markdown (`135f2e0b...1d5b`). |
| Required fallback rows/maps | FAIL | The 4,098-byte JSON has totals, algorithm text, and statuses only: no `changed_bodies`, `removed_assertions`, `added_assertions`, line/blob/body-hash rows, verdict mappings, or disjoint review groups. This is author omission, not an `EXACTMISSING` consequence. |

The smallest correction is to amend the review artifact, not to promote the
fallback: correct the normal-source scope and fallback direction, record the
actual crosswalk-file hash separately from the missing manifest hash, and
either retain the required finite fallback rows/groups or explicitly mark
that deliverable as unproduced. Keep the authoritative `129 / 113 / 287`
membership `EXACTMISSING`; do not force 113 or treat the reversed delta as
missing upstream predicates.

Checks were source-only: JSON parsing, exact Git-object reads, stdlib AST
comparison, hash/object checks, in-memory compilation, and whitespace/diff
checks passed for this review. No product tests, imports, collection, or
body execution were run.
