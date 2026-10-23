# P1 integrated-head review — PASS for review slice

## Verdict and boundary

**PASS for the packet/integrated-head review checks. Final v2/P1 qualification is UNVERIFIED, not a P1/H3 pass.** The detached actual provider still reports legacy `rebased` for the disjoint merge vector; the v2 contract requires a new disjoint success to report `merged`. The fixture correctly retains this as an open gap. H3 remains **NO-GO**.

This review did not modify the repository, import or add tests, run a full/heavy/browser/socket suite, or run the mounted App/HTTP chain. The evidence is the existing detached service's actual Agent provider only. Product merge eligibility remains Agent-owned.

## Exact revisions and tree evidence

- Integrated head: `cf31566e8ca01596e959c7a992618cb27c1d59a6`, tree `b4ee5f92b2775ab774bf4776d24e28ffb5f665e2`.
- Candidate: `6d1cec47cfdd61f30e73976665c24759c45c1225`, tree `49d15de9c3c4fac93b8282c149651c095fc9a5ac`.
- Candidate parent/provider base: `b7a32c5238f0948a913869b06437f174a277172c`, tree `ee0e29d7af05b836ceac233664410147ab64701d`.
- Packet donor: `52e9c0ea659123c86d6cbadc94f78ef972d74308`, tree `2d7cc2a16535b96dfc392a6d270dc097beabc7b8`.
- Integration merge `3da84905c781efd9647330cdaafe155f90c0c33f` has candidate's packet tree `49d15de9c3c4fac93b8282c149651c095fc9a5ac`.

Candidate versus integrated differs only by the separately integrated V4 cleanup: `artifacts.json`, `docs/plans/astrid-naming/inventory.md`, and the six `astrid/packs/rendering/{editor,ui}/live-scenes/*` files. Candidate versus `b7a32c52` changes only the three packet test paths; no product/schema/generated/pin/lock/launcher files are in the candidate patch.

All 15 packet paths are byte-identical in donor, candidate, and integrated trees (the three test files plus the 12 `tests/sdk/fixtures/p1_feasibility/*` files):

```text
tests/sdk/test_p1_case_corpus.py
tests/sdk/test_p1_doc_patch_provider.py
tests/sdk/test_p1_doc_patch_requests.py
tests/sdk/fixtures/p1_feasibility/{canonical_clip_trim.json,canonical_created_ids.json,canonical_disjoint_rebase.json,canonical_params_absent.json,canonical_params_null.json,canonical_params_object.json,doc_patch_requests.json,manifest.json,sample_hype_full.json,sdk_selected_param_accepted.zip,sdk_tiny3.json,sdk_tiny_publishable.json}
```

The common blob IDs for those paths are respectively the committed IDs shown by `git ls-tree -r --long` on all three revisions; the audit returned `exact` for every path. The candidate packet diff has `50/28`, `409/0`, and `46/28` line changes for the fixture, provider test, and request test respectively; no assertion was deleted or weakened. Marker scan found no `skip`, `xfail`, expected-failure, TODO/FIXME, or pytest marker. Assertion/raise counts match donor and integrated trees: provider `24`, requests `117`, corpus `36`.

## Targeted evidence

Commands were run from `/home/user/work/wt/ap2-P1-current-R1-integrated-review` against the integrated head:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.:/home/user/work/runtime ASTRID_RUNTIME_CHECKOUT=/home/user/work/runtime /home/user/work/venv-app2-native/bin/python -m pytest -q tests/sdk/test_p1_doc_patch_provider.py tests/sdk/test_p1_doc_patch_requests.py tests/sdk/test_p1_case_corpus.py
42 passed, 1 warning in 5.65s

/root/.local/bin/ruff check tests/sdk/test_p1_doc_patch_provider.py tests/sdk/test_p1_doc_patch_requests.py
All checks passed!

/root/.local/bin/mypy --follow-imports=silent tests/sdk/test_p1_doc_patch_provider.py tests/sdk/test_p1_doc_patch_requests.py
Success: no issues found in 2 source files

git diff --check
exit 0, no output
```

Logs:

- `pytest.log`
- `ruff.log`
- `mypy.log`
- `diff-check.log`

All are under `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-P1-current-R1-integrated-review/`. Pytest's sole warning is the shared environment's unknown `timeout` config option.

The 42 tests preserve and exercise the required trim, created-ID, absent/null/remove, opaque-value, alias, order, inverse, no-write/head/history, same-field `value_conflict`, and collection membership/order `selection_changed` assertions. The real provider tests execute the accepted cases and refusal cases through `create_runtime_commit_service` and the detached realm.

## Contract and remaining qualification

The request fixture records the v2 envelope requirement (`label`, `steps`, and `Idempotency-Key`) but explicitly has no Runtime publication IDs or idempotency keys, so those envelope facts are not guessed into the source vectors. The detached helper synthesizes its local request context. Its disjoint result is `data.status: "rebased"` with `rebased_onto`, not v2 `"merged"`; the request fixture's expected status is also deliberately `rebased`. This is legacy detached evidence, not v2 merged proof.

The fixture status remains `provider-executed on real R1; membership-removal precedence red; Runtime HTTP/App H3 proof pending`. The mounted App/HTTP production caller and the split → trim-new-clip → intervening-Agent-edit → lost-ack → restart chain remain unexecuted. Full v2 request/reply coverage (label/steps, `fields|atomic`, reads, dry-run, idempotency, complete accepted/merged/conflict/invalid envelopes, effects/dependencies and authoritative attribution) therefore remains unverified. No assertion was changed to hide this gap.

## Recommended next step

Run the required actual production caller through the detached service/Runtime HTTP boundary with v2 wire fields and verify `merged` (not legacy `rebased`), then separately run the mounted App/HTTP H3 chain. Do not mark P1 or H3 green from this detached 42-test result.
