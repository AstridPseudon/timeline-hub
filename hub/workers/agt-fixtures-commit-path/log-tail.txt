The fixture rebuild is partly done: the 9 projection-fixture setup errors and the authoring-media roundtrip now run, but 18 integration tests across these files still fail, none because of a fixture. The escalation's premise is also wrong, and I did not rebuild the `source_runtime` fixture.

**The escalation's premise is wrong.** `publish_parent_composition` is not retired at Runtime tip. `runtime_protocol/service.py:2596` is a stub that raises `RetiredRouteError`, but a second `def publish_parent_composition` at line 2738 overrides it. It only refuses heads that already carry a `publication_id`, with `ConflictError("tracked timeline publication requires a timeline command")`. Untracked heads, meaning no commit provider registered yet, still publish. Section 0.2 of the census was wrong on this.

**What I changed**
- **New helper:** `tests/helpers/trusted_seed.py` adds `seed_trusted_parent(service, publication, idempotency_key=…)`. It accepts a saved closure through Runtime's `TimelineCommitStore`, using the same pattern as Runtime's `tests/test_timeline_null_speed_retained.py`. It is labelled as test setup, not Agent acceptance.
- **Projection golden fixture:** `tests/sdk/test_timeline_capture_projection.py::saved_closure` published `parent-golden` after the provider was registered, i.e. onto a tracked head. It now seeds through the helper.
- **Authoring-media roundtrip:** `tests/timeline/test_authoring_media.py::test_real_runtime_import_and_parent_publication_roundtrip` registered a shot text binding through `create_project_shot` and `set_project_shot_text_binding`, both retired at tip. I dropped that setup and set `text_bindings = []`, as the sibling bundle test already does. The test makes no assertions about text.

**Not changed:** `test_capture_source_runtime.py::source_runtime` publishes while the head is still untracked, so it works at tip. `test_authoring_bundle.py:1035` also passes untouched, and `test_commit_runtime_m1.py` needed no seeding change.

**Results** (`commit-integration`, source tree 3b86cbcd), baseline versus now:

| | Baseline | Now |
|---|---|---|
| failed | 17 | 18 |
| passed | 2 | 10 |
| errors | 9 | 0 |
| xfailed | 6 | 6 |

The failed count went up by one only because 9 setup errors became 2 real failures, while the media test moved from failed to passing.

**Still failing (18)**
- **`test_commit_runtime_m1`, 2 failures:** the runtime health schema digest `a4e1eebd…` does not match the Agent client's expected `89a396aa…`. This is Runtime/Agent schema skew and already failed in the baseline.
- **`test_missing_candidate_certificate_refuses_before_admission_writes`, 2 failures:** Runtime `create_task` no longer raises when a working-copy snapshot arrives without a candidate. That is a Runtime behaviour change, and it already failed in the baseline.
- **`test_arbitrary_capture_cannot_acquire_canonical_source`, 12 failures:** these are strict XPASS. They already failed in the baseline with the same result, so the `xfail(strict)` marker ("needs verified source 435357ae") is stale. I left the marker alone because it is your call whether to remove it.
- **Two projection goldens, `…full_pins_golden` and `…entire_expansion_golden`:** the fixture now seeds and the tests run, but they fail on a real product gap. `project_capture` emits `content_digest` on each shot row, while `managed_timeline._project_exact_parent_head` (around lines 975–990) omits it. Adding `"content_digest": shot["content_digest"]` there would likely close it, but that is an Agent product change that may affect other tests. I did not make it. The other 7 projection tests now pass.

I could not run pytest directly in the sandbox, so every run went through `request-test commit-integration --files …`, which also runs `test_commit_runtime_m1.py` first. No xfails or skips were added, and no assertions were weakened. The commit message and `DONE` marker are written. The worktree holds the new helper and the two edited test files, with no stray files.

**Next steps**
- Runtime: decide whether the dead stub at `service.py:2596` should go (the duplicate def hides it) and whether the retired-route plan covers `publish_parent_composition`.
- Agent: add `content_digest` to the `managed_timeline` shot rows.
- Agent: drop the stale xfail on the arbitrary-capture test.
- Agent/Runtime: reconcile the schema digest for the m1 daemon tests.
