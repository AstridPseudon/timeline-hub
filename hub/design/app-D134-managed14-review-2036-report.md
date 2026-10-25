# D134 independent managed14 review

Verdict: **PASS_UNAPPLIED**.

I independently confirmed the author’s exact 14 node IDs, source bytes/AST
hashes, authored input hashes, topology, and protected predicate map. The
authorized three files are byte-identical to base `a30e74e90`; no source,
fixture, schema, product, auth, provider, or generated file changed.

The production registration audit is finite and covers `occurrence.create`,
`shot.set`, occurrence media, placement, `doc.patch`, duplicate, fork, shared
placement, timeline duplicate, and restructure. `occurrence.create` creates an
empty `items` list. `shot.set` only writes name/settings. Media and placement
commands create or remove occurrence clips and bindings; media replacement can
update an existing item’s media ID but requires its existing item identity.
Generic patch allocation has no shot-item allocation, and the item map rejects
an item correspondence change. Duplicate/fork/shared/timeline-duplicate routes
copy an already authenticated source closure; restructure derives from the
current authenticated closure. The exact caller has no initial authenticated
item-bearing source to use, so no faithful supported construction exists.

The positive source comparator is
`tests/editing_conformance/test_recipe_occurrence_media.py:90-149`: it preserves
`item-1` during a registered media swap/replay when the item already exists.
That comparator establishes the supported precondition, not a birth path from
the empty shot. The smallest missing capability is an authenticated semantic
birth/restore that allocates the authored item and records its source/item map,
media dependency, and managed edges. Owner remains `unknown_unproved`; no
implementation is proposed.

Validation passed: exact source/hash checks, Python 3.11 compile, scoped Ruff,
scoped mypy, `git diff --check`, and clean read-only worktree. No pytest or
provider/body execution was run, as required. Evidence is in `evidence/`.

No source merge is recommended for this no-change result.
