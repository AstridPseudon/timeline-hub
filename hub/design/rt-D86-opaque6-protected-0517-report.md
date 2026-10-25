## F-D86 opaque6 protected source review

**Verdict: PASS — source-only.**

Reviewed candidate `3c742a9cfa1509234ca70048612e7302e4e2298c` against parent `6aefd11766c019f8deff0ca5a1bfe18e9e730822` and reviewed source `eb5c794b2377a5ed862cdb9e12b7fd723ffd5ca5`.

- Only changed file: `tests/editing_conformance/test_commit_runtime_opaque_items.py`
- Candidate tree: `f41fe5094b2ea419117a7023ffcae0be3198cfca`
- Candidate blob: `339bf63752f509c1c0cb6b1fce30cda385dd2065`
- Candidate SHA-256: `3a5558085a78f3d8558219921da81029b3cb648e876b84eaefaf713d1e6e722a`

The helper now copies the exact ordered `doc.patch.args.changes` into `steps[0].patch` for both setup commits. It does not filter fields, mutate commands, alter `created`, or alter request/step `reads`. The real `Editing.body` and Runtime `commit_timeline` path remain used.

Preserved:

- Six parametrized cases: two tests × `item_id`, `id`, and `both`
- All 29 source assertions
- Unknown opaque values, item IDs, metadata, physical closure, revision pins/digests, timing, graph structure, branches, retry/restart, and inverse predicates

Checks:

- Candidate and parent compile: PASS
- Ruff baseline: `2143` findings on both; zero diff
- Mypy baseline/candidate: identical 14 environment diagnostics, exit `2`; zero diff
- `git diff --check`: PASS
- No pytest, collection, fixture, service, browser, build, or behavior suite run

Mypy remains environment-blocked by missing YAML stubs and the installed NumPy stub requiring Python 3.12+, but this is unchanged from baseline.

D72 appendix:

> F-D86 opaque6 — protected source review PASS. Candidate `3c742a9cfa` changes only the assigned opaque conformance test; both setup commits claim exact ordered `doc.patch` changes. Six parametrized cases and 29 assertions are conserved. C0 request shape and true SDK/Runtime route remain intact. Behavioral qualification is deferred to MAIN.

Commit message and `DONE` marker created.