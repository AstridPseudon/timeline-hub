# RT03 independent negative review and proof result

Date: 2026-10-21 UTC

## Disposition

**Independent delta review: APPROVE.** The 28-line test-only delta from
`d653442` to `1fe255e` is limited to
`tests/test_timeline_owned_reference_integration.py` (26 insertions, 2
deletions). The changed-payload case now mutates only the request-level,
schema-valid `rationale`, calls the actual Runtime `validate_request`, keeps
the original `exact-reference-key`, and asserts the command list is unchanged.
The former `role="target"` mutation is retained as a separate explicit 422
control. Both the 409 and 422 controls retain complete SQLite dump, head, and
commit-history no-write assertions. Existing positive, receipt, projection,
ownership, placement, retry, tripwire, occupancy, inverse, and closure
assertions are unchanged.

The central body was authorized only after fresh preflight, ran once, reached
the semantic body, and failed at the unchanged foreign-ownership assertion.
No retry, ordered sibling, oracle chase, source change, qualification, or
adoption claim was made.

## Independent review evidence

- `git diff --stat d653442 HEAD -- tests/test_timeline_owned_reference_integration.py`:
  one file, 28 changed lines.
- `git diff --check d653442 HEAD -- tests/test_timeline_owned_reference_integration.py`:
  **PASS**.
- Runtime source trace: `commit_timeline` validates the closed request before
  request hashing/idempotency; the request hash includes the complete body;
  durable lookup rejects a changed rationale under the same key with 409;
  `TimelineReferenceArgs.role` is a schema `const: "source"`, so the retained
  role mutation is a pre-idempotency 422.
- Actual frozen request-schema probe: changed rationale **PASS**; invalid role
  **PASS** as `ValidationError: invalid CommitRequest: 'source' was expected`.
- The reviewed file remained hash-identical before and after execution:
  SHA-256 `7cfae619be59002598d5ff868016c3657b1fe61e778730a84444f9c0c3bb68ec`.

## Fresh preflight

- Review Runtime: commit `1fe255ec1038726a06874a49640bb3e1861d5125`, tree
  `bbb6c448a3f4b60c1a1880dd9e7f9fe90b45fabc`; no source difference from the
  Runtime42a producer outside the reviewed test.
- Exact producer: Runtime commit
  `42a7203f49bb89f299ec854cfbf2b1444e815a7c`, tree
  `1f220b3d3a27e8eb061b15c944bad784c8fdb82e`.
- Exact normal Agent: commit
  `6c1989adf723ae0ea0f4205c1cc8f1c0e4b22e79`, tree
  `cc0a8dd1360324a1b440ba7d318a083e7f8814cc`.
- `/home/user/work/venv-runtime/bin/python /home/user/work/wt/rt-pin-42a7203f/scripts/artifact_manifest.py --check`:
  **PASS**, 76 artifacts, version
  `sha256:a0dc430a146f4093f64da29c1bbda32ebf25c3a1565eee2bb7860c3ec00298b0`.
- Agent `vendor_lock.py check ... --producer /home/user/work/wt/rt-pin-42a7203f`:
  **PASS**, 15 lock entries; source and producer version match Runtime42a.
- Frozen Agent schema: raw `6dd2b082ebdb630b4fc8ec3eeeea3b40c1eebe910c84557e45ab8fab05322b16`,
  canonical `9f5612ff34a5758ecacae948d5c0bfb1acc867d6ecb7a6af037bf8e3974fd9d6`,
  65 definitions / 37 `EditCommand.allOf` clauses.
- Runtime bundle SHA-256:
  `e6fb80e7961b3e9eb34908b532a042a9f024e52b5178cd906d9c1d45a18a5f8f`.
- Client/runtime metadata: version `0.2.17`, schema
  `sha256:a8fad23f5b46636fe219b6219bdfdeb143ee42937e2e72996c90c947e92905fd`.
  Runtime, Agent, and client imports resolved to the requested worktrees;
  `load_timeline_commit_provider("astrid")` returned provider `astrid-v1`,
  interface 1, with the matching contract digest.
- Private RuntimeService health probe: **PASS**, status `ok`, protocol
  `workspace.v1`, matching schema; private temp realm was removed.
- Read-only realpaths were direct paths for the review Runtime, producer,
  Agent, `venv-agent`, and `venv-runtime`. Disk availability was
  `10,921,168 KiB` in both `/home/user/work` and `/tmp`, above the 5 GiB floor.
- Targeted collection: **1 test collected**. Targeted `--setup-plan`: **PASS**;
  closure included `tmp_path_factory`, `tmp_path`, `film`, `monkeypatch`,
  `astrid_importable`, and `agent`; no body ran during preflight.

## One authorized central execution

Command:

```text
/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/request-test rt-m2-rt03-valid-negative-review-proof-1040 private017-agent6c-integration --files 'tests/test_timeline_owned_reference_integration.py::test_actual_provider_preserves_original_owned_unplaced_reference_contract'
```

Result ID:
`rt-m2-rt03-valid-negative-review-proof-1040-private017-agent6c-integration-1021104229-23372`

Result: **1 failed in 1.33s**. The central snapshot used Runtime tree
`bbb6c448a3f4b60c1a1880dd9e7f9fe90b45fabc`. The first actual semantic failure
was unchanged line 228:

```text
assert refused.value.status == 409
E AssertionError: assert 404 == 409
NotFoundError: raw media is not a managed project object
```

This occurred in the foreign-project raw-media refusal case, after the earlier
positive acceptance, restart exact retry, corrected 409 rationale mutation,
and explicit 422 role mutation had executed. Per instruction, no further body
was run and no expectation was changed.

Full log:
`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/tests/rt-m2-rt03-valid-negative-review-proof-1040-private017-agent6c-integration-1021104229-23372/log.txt`

## Limits and next step

The task is complete with a recorded first actual failure. The foreign raw
ownership status mismatch is the blocker for this proof; Runtime/Agent owners
must decide its contract separately. Do not retry this body or run the ordered
sibling from this result. No full, old44/186, HTTP/socket/browser/render,
install, generation, pin, source, marker-conversion, or public-adoption work
was performed.
