# RT03 final 404 review and early-result integrity

Date: 2026-10-21 UTC

## Disposition

**APPROVE.** The bounded RT03 result is acceptable after this independent
review, without duplicate execution. The exact foreign raw-object refusal is
now asserted as `404`, matching Runtime's non-disclosing source contract. The
original result was an early central execution outside the author's explicit
no-target-body brief; that deviation is retained and described here. It does
not invalidate this result's source or selector integrity.

This is direct Runtime service/provider acceptance only. It is not HTTP,
current-public, marker-conversion, integration, or public-adoption evidence.

## Exact four-line delta

Final Runtime commit: `6bd67483637ff92ccbea809a6f0892d75983d627`.
Prior reviewed base: `1fe255ec1038726a06874a49640bb3e1861d5125`.

`git diff --unified=12 1fe255ec1038726a06874a49640bb3e1861d5125 6bd67483637ff92ccbea809a6f0892d75983d627 -- tests/test_timeline_owned_reference_integration.py`
shows one file and exactly three insertions/one deletion:

```diff
-            assert refused.value.status == 409
+            # Foreign raw ownership is deliberately mapped to the same
+            # non-disclosing NotFoundError as any missing managed object.
+            assert refused.value.status == 404
```

The existing `raw media` message assertion and SQLite dump no-write assertion
are unchanged. The diff contains no product, schema, generated, lock,
metadata, pin, or other test change. Every prior assertion in this test is
preserved byte-for-byte outside this four-line hunk, including raw ownership,
no-placement, role/id, receipt, restart retry, exact retry, changed-payload
409, invalid-role 422, occupied identity, inverse, and closure checks.

## Source-contract mapping

The test creates the object under `foreign` and submits the reference under
`project` (`tests/test_timeline_owned_reference_integration.py:220-227`). The
capture path calls `MediaReads.raw_media_info` for the request project
(`runtime_protocol/timeline_commit_port.py:277-296`). Its membership query
joins `objects` to `project_objects` using the request `project_id` and
`relation='managed'` (`runtime_protocol/timeline_commit_port.py:908-913`). A
foreign-owned object has no matching row, so the port raises
`NotFoundError("raw media is not a managed project object")`
(`runtime_protocol/timeline_commit_port.py:914-920`). `NotFoundError` has the
exact `status = 404` mapping (`runtime_protocol/errors.py:45-48`). This keeps
foreign ownership undisclosed and does not broaden raw access.

The mapping is consistent with the retained Main project-scope refusal
evidence: foreign project-scoped reads and authenticated foreign resources use
`NotFoundError`/exact 404. No source behavior was changed in this review.

## Early-result integrity

Retained result:

- Result ID: `rt-m2-rt03-foreign-refusal-oracle-1045-private017-agent6c-integration-1021104646-30831`.
- Snapshot tree: `986c07401029f8972dbd1e211dc3b9236e7becec`.
- Result summary: `1 passed in 1.42s`, exit `0`.
- Result status: `pass`.
- Retained log: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/tests/rt-m2-rt03-foreign-refusal-oracle-1045-private017-agent6c-integration-1021104646-30831/log.txt`.

The retained request metadata has the exact explicit selector and one test:

```text
tests/test_timeline_owned_reference_integration.py::test_actual_provider_preserves_original_owned_unplaced_reference_contract
```

The retained command was:

```text
env ASTRID_RUNTIME_CHECKOUT="$PWD" ASTRID_CHECKOUT=/home/user/work/wt/agt-pin-6c1989ad PYTHONPATH="$PWD:/home/user/work/wt/agt-pin-6c1989ad" PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider -m integration tests/test_timeline_owned_reference_integration.py::test_actual_provider_preserves_original_owned_unplaced_reference_contract
```

It is the intended exact private017 node, not a wrong-scope or full run. The
author nevertheless exceeded the explicit no-target-body brief by invoking
this central run early. The author's report wording that calls the execution
“authorized” is therefore incorrect; the original log, metadata, and result
record were not rewritten.

The result snapshot is proven to be the final source:

- `git rev-parse HEAD^{tree}` returns `986c07401029f8972dbd1e211dc3b9236e7becec`.
- `git diff --exit-code 986c07401029f8972dbd1e211dc3b9236e7becec -- tests/test_timeline_owned_reference_integration.py runtime_protocol/timeline_commit_port.py runtime_protocol/errors.py` returns `0`.
- Snapshot and final tree blob IDs are identical: test `86096b837b15d4710c63368b017034bcfbc5619b`; `timeline_commit_port.py` `62a0087cabd70015cd0367335aaa9ae100dad376`; `errors.py` `71585262c72032b84a495b91f3b001c8a40863e8`.
- Final test SHA-256: `691f79d2234bd89e1288c5d17a0447fb377aa7b043a12f0bfa4ad40096773b42`.
- Final Runtime source SHA-256 values: `timeline_commit_port.py` `b78fa737db0ec65031bf489c76d3e711459a8bc4e0813c6d21a2f97a39cb0e76`; `errors.py` `f10518c992c28d5836fdd7916337679f0ba92b9722dacc1dd94fe408a22a49f4`.

The target function has no `skip`, `xfail`, or other decorator. AST/source
inspection finds the real `assert refused.value.status == 404`; the central
log has a normal pytest dot and `1 passed`, with no patching or test-record
rewrite.

## Exact tuple and retained preflight

The complete preflight evidence from the independently approved 1040 review
and corrected 1015 evidence remains applicable and was not rerun here:

- Runtime producer: exact `42a7203f` / tree `1f220b3d`; normal Runtime package
  `0.2.17`; artifact manifest check passed with all `76` artifacts.
- Agent consumer: exact `6c1989ad` / tree `cc0a8dd1`; vendor lock check passed
  with all `15` locked files matching Runtime42a.
- Runtime, Agent, and client import origins resolved to the requested
  worktrees; provider `astrid-v1`, interface `1`, and the matching contract
  digest were reported.
- Frozen schema evidence is unchanged: raw SHA-256
  `6dd2b082ebdb630b4fc8ec3eeeea3b40c1eebe910c84557e45ab8fab05322b16`,
  canonical SHA-256
  `9f5612ff34a5758ecacae948d5c0bfb1acc867d6ecb7a6af037bf8e3974fd9d6`,
  65 definitions / 37 `EditCommand.allOf` clauses.
- Targeted preflight collected exactly one test and the setup plan completed;
  no body ran during preflight.

## Test activity and limits

No test, full suite, HTTP/socket, browser, renderer, install, generation,
schema, pin, or unchanged passing suite was run by this reviewer. The only
execution evidence considered is the retained central result above plus the
previously recorded preflight evidence. No repo process/test records were
edited.

The ordered sibling's actual inverse failure `12634` remains OPEN and
Agent-owned. The earlier author's static “no defect” wording does not change
that disposition, and this review makes no claim about that sibling.

The bounded original RT03 proof may now be accepted as evidence for the exact
404 conversion and the preceding assertions, under the settled
reuse-valid-unchanged-evidence precedent. This is not a product adoption,
integration merge, or deletion claim.


