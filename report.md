## R5 replay joined proof — PASS

Manager’s staged merge-forward was present before testing. The staged Runtime
delta was limited to the archive replay candidate files:

- `runtime_protocol/service.py`
- `runtime_protocol/store.py`
- `tests/test_timeline_commit_archive_replay.py`

The required two-node gate passed, so the original-20 follow-up was run on the
same snapshot. No product, test, schema, client, pin, or artifact changes were
made by this worker.

### Provenance

- Runtime origin: `https://github.com/banodoco/banodoco-workspace-runtime`
- Runtime base: `73c5137f9e969b1ef3419ab9ecfed0096f38f57a`
- Archive candidate: `66829e2eb37374c2d9b82274fea5108bd855c7bf`
- Agent origin: `https://github.com/peteromallet/astrid-agent`
- Agent pin: `33fc387968c0b1bd4a78e828c34677d6f9cadd21`
- Test-service Runtime snapshot: `04697aed584c62690d6c85f516f36fd75bae8f60`
- Frozen R4 refs verified unchanged:
  - SDK `11caf1d9de291d76f491cf69f7942606b7471d7a`
  - Runtime `31c7ac3a00f7a205f507bf5bd4d4625628d429bd`
  - App `8f0c2484463e9b666d184a744d52e252984e551a`
  - Composition `c82eb7c459d0a41263954bf007071a6a0e8e0a6a`

### Acceptance results

1. Required two formerly failing nodes:

   Command:

   ```text
   R=$(/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/request-test rt-R5-replay-joined-proof-0518 r5-render33fc-integration-nodes --files "tests/test_timeline_render_publication.py::test_prepared_checkpoint_resumes_on_retried_attempt_after_runtime_restart tests/test_timeline_render_publication_authority.py::test_exact_published_checkpoint_replays_before_live_target_changes") && /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/wait-test "$R"
   ```

   Result ID: `rt-R5-replay-joined-proof-0518-r5-render33fc-integration-nodes-1023051739-9901`

   Result: **2 passed in 10.04s**.

2. Original render publication files, only after both nodes passed:

   Command:

   ```text
   R=$(/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/request-test rt-R5-replay-joined-proof-0518 r5-render33fc-integration-nodes --files "tests/test_timeline_render_publication.py tests/test_timeline_render_publication_authority.py") && /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/wait-test "$R"
   ```

   Result ID: `rt-R5-replay-joined-proof-0518-r5-render33fc-integration-nodes-1023051811-28660`

   Result: **20 passed in 40.07s**.

The test-service command verified the Agent pin before execution and used the
normal authenticated commit/provider/store/render admission path. The tests
retained their authority, fence, target, restart, replay, render-pin, raw
`{data, receipt}` equality, and public-enrichment assertions.

### Disposition

This is a proof result for the staged R5/R2r replay candidate only. It does not
claim whole G4 or home readiness; R5 remains explicitly gated on A3/G4 as
specified by the plan. No full, browser, native, crash, route-broad, or
renderer-execution suite was run.

