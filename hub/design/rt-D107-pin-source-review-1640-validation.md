# D107 independent result review validation

## Verdict

**FAIL (custody packet defect); substantive source result: PASS; behavior: FAIL/behavior pending.**

The exact Agent `b4b3805da5e8611490401122f986e203f67f21b4` and Runtime
`5e9ad1c6f74241d8771d3284fdd2ce7a214fd344` source map is reproducible. The
production path is:

`current seed/provider -> accepted canonical dependency_manifest.documents ->
Runtime commit_manifest_json and immutable input content/binding/link rows ->
restart/revision_closure -> Agent _hydrate -> pinned_documents -> word-anchor`

The two retained authorized cases both stop at
`tests/editing_conformance/test_m1_current_equivalent.py:317` with
`exact transcript pin is missing or revoked or ambiguous`. This is not a
functional GO. The source owner is **UNKNOWN**. The smallest missing genuine
record is the exact authenticated transcript `DocumentPin` at the accepted
persisted-manifest/input-link boundary versus the restarted Agent
`pinned_documents` capture; status is **EXACTMISSING**.

## Read-only checks and exact results

- Recomputed all seven hashes in the prior `source-map.json` with `git show`:
  PASS, all exact at the stated Agent/Runtime refs.
- `git diff --name-status 20177e66564f9f91735ed1a11bac821682d60edf b4b3805da5e8611490401122f986e203f67f21b4`:
  only `tests/editing_conformance/test_m1_current_equivalent.py`.
- `git diff --check 20177e66564f9f91735ed1a11bac821682d60edf b4b3805da5e8611490401122f986e203f67f21b4`:
  PASS.
- `python3 -m json.tool` on prior `source-map.json`, `wholepath.json`,
  `purpose-map.json`, and `validation.json`: PASS.
- Protected original, cited product, pin, and fixture hashes: PASS for
  base/candidate equality. The intentional current-equivalent test delta is
  exactly the requested history `5 -> 8` assertion plus its explanatory
  comment.
- Source citations were checked read-only: Agent `_hydrate` reads the
  canonical document manifest and calls `transcript_source`; Runtime
  `revision_closure` reads `commit_manifest_json` and `_verify_inputs`; Runtime
  acceptance calls `_persist_closure` and `inputs.persist`; the compiler
  requires exactly one matching pinned capture.
- Same-process comparator `test_commit_document_input_capture.py:43-63` was
  inspected read-only. It proves consuming-command capture, not restart
  persistence/hydration.
- Retained artifact inventory contains no SQLite/database, canonical manifest
  dump, immutable input rows, or private restarted hydration capture. The
  2421-byte XML contains only two failure tracebacks and has zero occurrences
  of those record names; it has four occurrences of the reported error text.

## Exact custody defect

`workers/rt-D107-purpose-review-1550/evidence/validation.json` and its
`evidence/review.md` record the protected original M1 SHA-256 as
`23451aa80279f47d126e5e5699f51272a6418402ba559617c243bcd6b15041`, which is
62 hex characters and omits `b8`. The recomputed 64-character hash at the
base, candidate, and approved refs is:

`23451aa80279f47d126e5e5699f51272b8a6418402ba559617c243bcd6b15041`

This makes the retained custody packet FAIL, but it does not change the
independently verified conclusion that the protected original file is
unchanged. No source blame or behavior closure is inferred from the compiler
guard, and no missing record was reconstructed.

## Scope

No tests, provider, collector, full suite, source, pin, fixture, Git ref,
Runtime worktree, credential, hub, or design file was modified or rerun.
No new evidence helper was authored; configured static checks for one are
N/A. Recommended next step is inspection of the accepted head's persisted
manifest/content/binding/link rows together with the restarted provider's
private `pinned_documents` capture, followed by the authorized two-case rerun.
