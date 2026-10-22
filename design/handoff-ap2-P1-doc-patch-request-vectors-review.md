# Review handoff: AP2 P1 doc.patch request vectors

## Result: FAIL

Reviewed committed delta `9859b3d3d1bfb667a7ad281d930ca753fc77dcd0` against
base `3f1ceaed144d33a7b14c76164ea3c6e6d92bda61`, PLAN v2.1 §3, current
`commit-v2.md` §§1–5, and `BOARD-HEADER.md`.

The real source/canonical fixture hashes match and the delta does not modify
the pre-existing corpus. The collection-only boundary is correctly stated: no
provider execution, H3 GO, Runtime acceptance, merge, inverse, or lost-ack
claim is established. The vectors are operand fragments rather than complete
HTTP requests, and the missing Runtime publication/idempotency facts are
explicitly recorded. That boundary is acceptable for early P1 preparation.

The set cannot be approved as-is because the following contract and validation
issues remain:

1. `vectors[id=same-field-refusal].expected.code` at
   `tests/sdk/fixtures/p1_feasibility/doc_patch_requests.json:360-363` is
   `field_changed`. Current §4 names the conflict detail code
   `value_conflict` for a later write to the same field; `field_changed` is not
   one of the current stable reasons. Correct the witness to
   `reason: value_conflict` and `code: value_conflict`, or remove the protocol
   code until a provider reply exists.

2. `test_commands_use_the_contract_doc_patch_shape` lines 155–158 accepts any
   `before.state`, accepts `present` without a `value`, and accepts extra
   `value` on `absent`. §2 requires exactly `{"state":"absent"}` or exactly
   `{"state":"present","value":...}`. Assert both the state enum and the
   exact key/value shape; this is required even though the current eight
   values happen to be legal.

3. Finite JSON is not verified. The module loads with Python's permissive
   default `json.loads` at lines 19–21, which accepts non-standard NaN and
   Infinity, and no recursive finite-number assertion exists. Add a finite
   raw-JSON check (or equivalent `parse_constant` rejection plus recursive
   validation) for the request fixture and preserved values. The current bytes
   contain only finite values, but the test does not prove that contract.

4. The tests do not establish the requested meaningful after/order/preservation
   witnesses. `test_expected_authored_deltas_match_the_submitted_operands`
   lines 181–197 compares expected deltas only to the same submitted operands;
   it never compares to fixture output. In particular:

   - `trim-internal-clip-window`'s derived `hold`/`app.astrid` effects are
     unchecked against `canonical_clip_trim.json` output.
   - `created-track-and-clip-list-inserts`'s expected orders and opaque-field
     preservation are not checked against `canonical_created_ids.json`, and
     created claims are not linked to the inserted IDs/paths.
   - The three parameter vectors' tagged-state/preservation expectations are
     mostly self-assertions; source output is not checked.
   - `disjoint-field-merge`'s `head_change_preserved`, `exact_expected_fields`,
     and `merged` expectation are not checked against `head_bundle`/
     `rebased_bundle`.
   - `ordered-list-move-and-order-refusal` lines 224–231 only compare literal
     expected values. They do not derive `order_after`/membership from the
     real collection, validate the collection read against that collection, or
     validate the refusal witnesses. `created` and list order guards are also
     only shape-checked.

   Required correction: derive the relevant before/after field, preserved
   sibling/opaque fields, created-ID claims, collection members, and order from
   the real input/output or explicitly named scenario fragments. Keep provider
   statuses unexecuted, but do not let the test pass by asserting the fixture's
   own expected literals.

5. `same-field-refusal` cites
   `test_recipe_m2_clip_trim.py::test_replay_consumed_source_identity_bounds_and_selection_but_preserves_disjoint_data`,
   but that source test (lines 238–267) exercises registry/source-consumption
   refusals, a disjoint params edit, and collection deletion; it does not
   provide the claimed head change `parent.clips[id:clip-a].from: 2 -> 3`.
   The base field is real, but the head witness is synthetic while the
   provenance is presented as exact. Use an actual source scenario and cite
   its node, or label this head as a separately constructed, unexecuted
   scenario instead of claiming it is source-derived.

6. The handoff should explicitly preserve the approval distinction required by
   the BOARD header: the C0c addressing principle is adopted for correctness
   review, but formal C0c approval is still pending. The current wording
   (`C0 + C0b + adopted C0c`) can be read as treating C0c as approved. Add the
   pending-approval statement; it does not block collection-only addressing
   review.

## Evidence

Required targeted checks from the review worktree:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.:/home/user/work/runtime /home/user/work/venv-app2-native/bin/python -m pytest -q tests/sdk/test_p1_doc_patch_requests.py tests/sdk/test_p1_case_corpus.py
20 passed, 1 warning (unknown pytest config option: timeout)

/root/.local/bin/ruff check tests/sdk/test_p1_doc_patch_requests.py
All checks passed!

/root/.local/bin/mypy --follow-imports=silent tests/sdk/test_p1_doc_patch_requests.py
Success: no issues found in 1 source file

git diff --check
clean (no output)
```

No browser, socket, provider, heavy, or full suite was run. The required
correction is test/fixture review work only; no product code or existing corpus
bytes were changed by this review.
