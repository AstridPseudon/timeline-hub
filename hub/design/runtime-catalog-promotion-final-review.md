# Runtime catalog promotion final review

**Verdict: APPROVE** for candidate commit `4c1a1a30a6dfed4b1d0c7674fe6f8bfc23aab15f`, tree `67f0f65ff6df9595b452f23c2c0fbbf262898cee`.

## Scope and findings

- Compared the candidate against base `16acbb6` and Main `29d0954b6d78a7d7937d81bc36567b6dee7ca976`.
- `RuntimeService.promote_project_shot_candidate` and `_shot_revision_payload` are AST-identical to Main. `_record_legacy_shot_revision` differs only by removing Main's unused local assignment.
- The existing project-scoped route, `projects:write` credential gate, idempotency key handling, project lookup, and project-scoped shot lookup remain in place. No endpoint, DTO, schema/table, journal, or new command was added.
- The two original positive assertions remain intact. The private ephemeral bootstrap uses the existing published-shot projection helper; it does not require Agent startup, accepted SQL history, or a fake provider.
- Promotion remains receipt-first and transactionally atomic, including candidate provenance, managed-object ownership, CAS-byte verification, primary/superseded transition, invalidation result, revision recording, stale-head refusal, exact retry, and restart replay.
- The native prewrite guard now compares each occupied destination against its exact current `shot_revision_heads` revision. It permits exact immutable reuse and the existing owned-slot/history path, while refusing a newer catalog head before persistence. The tested guard does not impose a blanket historical-reuse ban, and accepted film heads/history/C4 pins remain unchanged.
- Product delta is exactly `+160` lines across the three product paths (`service.py`, `store.py`, `timeline_commit_store.py`); no product files outside the bounded change were touched.

## Evidence

Commands run:

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=$PWD /home/user/work/venv-runtime/bin/python -B -m pytest -q -p no:cacheprovider tests/test_shot_candidate_promotion.py::test_candidate_promotion_checks_bytes_and_rolls_back_before_receipt
# 1 passed

R=$(/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/request-test rt-m2-catalog-promotion-independent-review targeted --files "tests/test_shot_candidate_promotion.py tests/test_project_reference_catalog.py tests/test_timeline_shot_authority.py tests/test_timeline_commit_closure_invariants.py tests/test_timeline_projection_occupancy.py")
/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/wait-test "$R"
# cache hit on exact tree: 156 passed, 3 deselected, 34 setup errors
# The 34 errors are the existing missing ASTRID_CHECKOUT fixture, not failures in the promotion assertions.

R=$(/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/request-test rt-m2-catalog-promotion-independent-review occupancy-integration --files "tests/test_shot_candidate_promotion.py tests/test_timeline_projection_occupancy.py")
/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/wait-test "$R"
# 3 passed, 20 deselected; ASTRID_CHECKOUT=/home/user/work/agent

/root/.local/bin/ruff check --no-cache --select F runtime_protocol/service.py runtime_protocol/store.py runtime_protocol/timeline_commit_store.py tests/test_shot_candidate_promotion.py tests/test_timeline_shot_authority.py
# Seven F findings, identical in kind to base: two service, five store; no new candidate finding.

git diff --check 16acbb6..HEAD
# pass
```

The two original HTTP tests were also attempted locally but cannot bind localhost in this sandbox (`PermissionError: [Errno 1] Operation not permitted`); the central exact-file result above is the authoritative bounded result. No full suite was requested or run. The restoration design records the separate Agent-aware catalog-neighbor rerun as `35 passed`; it was not duplicated here.

## Recommendation

The manager may merge this exact candidate. After merge, run the manager-owned full Runtime suite once on the merged tree and retain the existing Astrid-aware catalog neighbor qualification. No further source change is required by this review.
