# D132 protected verdict

Source review: PASS.

The tree is based on `134d9787c791b54db695a2332bd352ca1c0a6a78`. Against the required normal baseline `20177e66564f9f91735ed1a11bac821682d60edf`, the only changes are:

- six v2 request-envelope metadata lines in `tests/sdk/test_timeline_commit_graph_roots.py`;
- the owner-approved authored fixture input `gain: None` to `gain: 1` in `tests/editing_conformance/test_recorded_graph_roots.py`.

The fixture has 22 test bodies, 90 assertions, and 6 parametrization decorators before and after. The graph consumer has 11 test bodies, 33 assertions, and 7 parametrization decorators before and after. Test-body, assertion, and parametrization ASTs are equal. Canonicalizing only the approved gain literal makes the fixture source byte-identical to the baseline. No consumer contains a gain/null-purpose assertion, and no Runtime, Agent product, schema, generated, or dependency file changed.

The actual D60 Agent object exists at `92443771676ef2bbb547d0a103d708fa8bec4c63` in `/home/user/peteromallet/astrid-agent`, and both graph paths are absent from its tree. The frozen R4 candidate SDK ref also lacks both paths. The owner-named `d11417a59` object is unavailable and was not used as absence evidence. Fixture introduction `84db8bde88f695fede81f32a2fddb30622c6781f` exists in this repository, its parent lacks the fixture path, and the introduction commit adds it.

Scoped Ruff, mypy, Python 3.11 compilation, and `git diff --check` passed.

Own9 then ran exactly as authorized against clean Runtime commit `5e9ad1c6f74241d8771d3284fdd2ce7a214fd344` (tree `de2954a0ceadb4455903d9abdfec3b773318a50f`) with the registered `astrid` provider. All 9 exact nodes failed at the frozen Runtime schema boundary: `PreparedCommit` rejected `canonical_document.shot_revisions[1].payload.metadata` because its existing value was `None` rather than an object, with the validation frame at `runtime_protocol/timeline_commit_validation.py:173`. This is outside the approved gain edit. No source fix, retry, alternate route, or ambient Runtime substitution was used. Raw XML and log are private in `own9.xml` and `own9.log`.
