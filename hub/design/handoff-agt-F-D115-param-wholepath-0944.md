# D115 PARAM whole-path handoff

## Result

UNPROVED LIMIT / PRODUCT SEAM. No source or test repair is justified from the
available accepted-record artifacts. The candidate `3352791b974dfb9da11eb4399f4f7071b63798b2`
is invalid for D115's purpose even though its isolated lane is green.

## Exact case and root cause

D108b records exactly 16 accepted=True nodes at
`tests/sdk/test_selected_param_neutral_stage.py:219`, one for each physical
binding damage (`physical_ref`, `owners`, `revision_id`, `content_digest`,
`path`, the six boundary mutations, and the three image mutations). The old
accepted branch first committed, set `staged=()`, selected
`realm.entries[-1]['records']['commands'][0]`, and failed the clean authority
lookup with `selected PARAM authority is unavailable` before `_damage_binding`.
Thus the old run did target accepted history, but lacked a complete accepted
record/authority match; it did not establish that the mutations were safe.

The candidate instead executes a fresh plan before acceptance, retains
`staged=plan.records`, commits, checks only
`accepted_record['command'] == staged[0]['command']`, and applies all 16
mutations to `staged[0]`. This changes the authoritative object and stage. It
does not test accepted `bindings`, `effects`, `dependencies`, or `boundary`,
so 32/32 is a false qualification for the requested accepted-history proof.

## Correct boundary/object

- `accepted=False`: staged plan record, evaluated against the predecessor
  input head; mutation must leave the in-memory realm unchanged and refuse.
- `accepted=True`: durable accepted record from authenticated history, with
  `through=realm.head`, `staged=()`, and the accepted entry's
  `previous`/receipt-derived input boundary. Mutation must be applied to the
  copied accepted record and refusal must preserve head, entries, documents,
  and accepted state.

D82 may require checking both the original staged and durable recorded forms,
but that permits an additional exact comparison; it does not permit replacing
the durable accepted form with the staged form. All 16 mutations must be
applied against both forms when that requirement is active, with no omitted
binding/effect/dependency/boundary fields.

## Client-to-Runtime source comparison

The unchanged Agent caller at `astrid/sdk/timeline/commit.py:1423-1444` builds
`prepared['records']` from `plan.records` and passes that prepared candidate to
`port.accept`. `_commit_preview.py` copies command records without rewriting
their binding provenance. Runtime `timeline_commit_auth.py` requires exact
prepared-record metadata and command boundaries with `phase='input'`; its
sequential capture checks original input against the request base and landing
input against the prepared expected head. Runtime store acceptance validates
the candidate, then `_publish` persists the exact prepared records alongside
the receipt. Accepted replay uses `expected_head=previous` and revalidates the
same records.

The selected-authority resolver at
`astrid/sdk/timeline/_selected_param_authority.py:106-143` intentionally uses
`entry['previous']` for an accepted record and reconstructs prior recorded
writes over that sealed input closure. Therefore an accepted binding carrying
an output-side physical revision, or otherwise failing to replay against the
predecessor input boundary, is a producer/verifier fault. The passing current
staged control only proves the staged plan path; it cannot authorize changing
the accepted path.

The input/output transition is exact: `revision_id`, `content_digest`,
`physical_ref`, and `boundary.evaluated_head` describe the closure read at
command input (`phase='input'`); the durable output is the accepted canonical
document/accepted revision. The latter must not replace the former. Runtime
keeps exact boolean/integer types for ordinal fields, so no coercion is valid.

## Evidence and verification

See `evidence/wholepath-static.txt` for source hashes, exact node accounting,
XML/JSON parse results, in-memory compile results, and diff checks. The
complete accepted record is not present in the private artifacts, so exact
binding values and a missing hash are reported as a limit rather than
fabricated.

No tests, type checks, or lint were run: this was explicitly a read-only
investigation, and no product/test edits were authorized. Recommended next
step is an owner-side producer/verifier trace that exports the authenticated
accepted record and its predecessor-bound input images, then repairs the
producer or verifier before adding the D82 two-form assertion.
