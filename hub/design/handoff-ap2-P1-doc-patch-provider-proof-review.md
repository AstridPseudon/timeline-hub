# AP2 P1 doc.patch provider-proof review

## Result: FAIL

Reviewed candidate `edcd1b2baea3919c7730725d0df154e7d8c9447f`. The required
targeted run was **7 failed, 31 passed, exit 1**; Ruff, mypy, and `git diff
--check` passed. Full failure output is retained in the harness log:

`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-P1-doc-patch-provider-proof-review/log.txt`

Failure ownership:

1. Trim direct `execute`: **case/expectation defect**. The vector submits only
   `from`/`to`; generic `doc.patch` leaves `hold=17`, `app.astrid.for=19`, and
   `app.astrid.until=null`, while the expected native trim output requires
   `hold=4.0` and removes both keys. Add those three authored changes with
   exact guards (preferred to preserve the successful edit), or assert the
   literal patch result.
2. `params-absent`: **case/expectation defect**. `occurrence:o/clip:c` is
   rejected by the actual DocPatchChange schema. Use
   `internal-revision:ir`, path `clips/id:c/params`.
3. `params-null`: **case/expectation defect**. Same invalid occurrence root;
   use `internal-revision:ir` plus `clips/id:c` and preserve explicit null.
4. `params-remove`: **case/expectation defect**. Same invalid root on all four
   changes; use `internal-revision:ir` plus `clips/id:c` and retain guards.
5. Disjoint merge: **case/expectation defect**. Same invalid root; use
   `internal-revision:ir`, `clips/id:c/params/x`, then prove real landing-head
   merge on a complete Runtime closure.
6. Trim Runtime-service assertion: **case/expectation defect**, same native
   derived-effect mismatch as #1; the service accepted the literal patch.
7. Stale list move after target membership removal: **actual provider defect**.
   Contract §3 makes `list.*` read collection shape and requires
   `selection_changed` for membership changes; current rebase guard ordering
   reports `value_conflict` first. Fix provider precedence, retaining
   `value_conflict` for same-field edits.

The four occurrence refs are not legal generic `doc.patch` roots under the §2
closure-root table or the current schema; they are native entity spellings.
The valid generic form is the bound physical internal root plus
`clips/id:c/...`. If native aliases are intended to be legal submitted patch
refs, the contract/schema needs an explicit orchestrator amendment. Likewise,
if simultaneous item+collection overlap should prefer `value_conflict`, amend
the contract before changing this expectation; the current explicit membership
scenario requires `selection_changed`.

Fixture bytes from collection commit `250db8c8d9f5bda5f0130ecf3fe46bf78e298641`
and vector commit `309cb2d321cc74c06aabcee4998375a53403c8c6` were verified
identical by SHA-256. No product, generated, pin, schema, or assertion edits
were made during review. No full/browser/socket suite was run; unchanged
conformance-62 and neighbor-111 PASS results were not rerun.

H3 remains **NO-GO** pending corrected corpus plus integrated Runtime HTTP and
App/UI/outbox chain evidence.
