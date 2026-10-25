# D107 custody final review validation

## Verdict

**PASS for the corrected derivative evidence only.** The historical 1550
packet remains **FAIL_NONCLEAN** because it recorded a 62-hex-character
protected-file value. The independent1640 substantive source review remains
PASS, while the whole path remains **FAIL_BEHAVIOR_PENDING** and
`functional_go: false`.

The corrected value is the full 64-hex SHA-256:

```text
23451aa80279f47d126e5e5699f51272b8a6418402ba559617c243bcd6b15041
```

The historical value is retained verbatim for custody transparency:

```text
23451aa80279f47d126e5e5699f51272a6418402ba559617c243bcd6b15041
```

No historical 1550 or independent1640 artifact was rewritten, and this
review makes no historical-packet-passed claim.

## Exact protected-file identity

Protected file: `tests/editing_conformance/test_commit_runtime_m1.py`.

```text
git show 20177e66564f9f91735ed1a11bac821682d60edf:tests/editing_conformance/test_commit_runtime_m1.py | sha256sum
23451aa80279f47d126e5e5699f51272b8a6418402ba559617c243bcd6b15041  -
PASS

git show b4b3805da5e8611490401122f986e203f67f21b4:tests/editing_conformance/test_commit_runtime_m1.py | sha256sum
23451aa80279f47d126e5e5699f51272b8a6418402ba559617c243bcd6b15041  -
PASS

git show 2e3331ee2f035e302f5ca52488832cd0e22bb3aa:tests/editing_conformance/test_commit_runtime_m1.py | sha256sum
23451aa80279f47d126e5e5699f51272b8a6418402ba559617c243bcd6b15041  -
PASS

sha256sum tests/editing_conformance/test_commit_runtime_m1.py
23451aa80279f47d126e5e5699f51272b8a6418402ba559617c243bcd6b15041  tests/editing_conformance/test_commit_runtime_m1.py
PASS
```

All four byte sources identify the same genuine original file. The old value
is 62 hex characters; the corrected value is 64 hex characters.

## JSON, schema, source, and invariance checks

```text
python3 -m json.tool workers/rt-D107-custody-correction-1644/evidence/correction.json
PASS: corrected packet is valid JSON.

custom required-field/schema check on correction.json
PASS: all required top-level sections, three protected checks, and five
preserved-original records are present; old/new hash lengths are 62/64.

git diff --name-status 20177e66564f9f91735ed1a11bac821682d60edf b4b3805da5e8611490401122f986e203f67f21b4
M tests/editing_conformance/test_m1_current_equivalent.py
PASS: the sole candidate delta is the authorized history assertion/comment.

git diff --check 20177e66564f9f91735ed1a11bac821682d60edf b4b3805da5e8611490401122f986e203f67f21b4
PASS
```

The protected original M1 test, product source, pin, and fixture paths are
byte-invariant from Agent20177 to b4b380. The seven carried source-map hashes
were recomputed directly at Agent b4b380 and Runtime `5e9ad1c6` and all
matched. The approved reference was used for the exact protected-file
identity check above; no claim is made that it is byte-identical to every
candidate product source file.

The five retained 1550/1640 evidence files were independently re-hashed and
all matched the correction packet's `preserved_original_evidence` values.

## Behavior and custody boundary

The retained XML has two failures, both at
`tests/editing_conformance/test_m1_current_equivalent.py:317`, with:
`exact transcript pin is missing or revoked or ambiguous`. The cases are
`disjoint-rebase-undo` and `touched-basis-conflict`. Source owner remains
**UNKNOWN**; the accepted persisted manifest/private restarted capture remains
**EXACTMISSING**. No provider, collector, body, compiler guard, test, or
behavior rerun was performed, and no private record was reconstructed.

The carried production path remains:

```text
current seed/provider -> accepted canonical dependency_manifest.documents
-> Runtime parent_composition_revisions.commit_manifest_json plus immutable
input content/binding/link rows -> restart/revision_closure
-> Agent _hydrate -> pinned_documents -> native_word_anchor.binding exact-pin guard
```

The C0v2 request envelope remains the full `api_version`, project/timeline,
base revision/publication, commands, label, steps, merge (`fields|atomic`),
reads, `dry_run`, source, rationale, group, and `Idempotency-Key` shape;
command fields remain schema version/op/version/select/args and step fields
remain id/label/intent/tags/command ordinals/patch/reads. Replies retain
accepted/merged success data, conflict reason/head, invalid code/path/hint/
suggested command, and preview `would_status` with null receipt. This is a
shape check only; accepted, merged, refusal, and preview behavior are not
claimed by this evidence-only review.

## Scope

No tests, full suite, compiler fix, new collector, private record
reconstruction, provider/body/original/profile/build change, hub/Git mutation,
upstream/credential change, or M5 work was performed. Nothing was deleted.
