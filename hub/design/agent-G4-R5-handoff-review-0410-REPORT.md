# G4/R5 handoff independent review

**Verdict: FAIL.**

Reviewed Agent `5f0fb2edb72aae37ba86e3ffe28f5e79b63aa026`, Runtime reference
`ad823e0a0f5be4a7acf1d3006df6f794709da63d`, PLAN §3, `design/commit-v2.md`
§§1–5, BOARD-HEADER, and the flat handoff
`peer-agent-to-runtime-20261023T0405-G4-R5-requester-handoff.md`.

The 20-node Runtime inventory is accurate: 17 authority nodes (including the
9 malformed-target parameter cases) and 3 fenced publication nodes. The Agent
seam mapping for session scope, admission target/media pins, producer guard,
fence, outbox retry/replay, preview, and exact canonical render pin is also
accurate as a seam description.

Two corrections prevent a PASS:

1. Exact `5f0fb2e` has no production `RemoteTasks.admit`. The publication
   helper calls `client.tasks.admit` after commit, but the 15 Agent tests add
   that attribute as a fixture fake. Therefore the post-commit caller is not
   executable in the frozen source. The report must explicitly retain this
   known active0408-owned caller block; it must not call `5f0fb2e` executable or
   adoption-done, and must not call the fake 15 coverage of all 20 Runtime
   behaviors.
2. The handoff claims complete v2 forwarding including `group_id`, but exact
   `publish_authoring_proposal` → `commit_assembly` → `TimelineSession._flush`
   has no `group_id` parameter/state/body path. That claim needs a precise gap
   flag and owner.

Permitted targeted command:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD:/home/user/work/runtime" \
  /home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider \
  tests/sdk/test_timeline_assembly.py tests/sdk/test_timeline_render_publication.py
# 15 passed in 2.74s
```

No Runtime R5 body/browser/native14/full run was executed. No product, test, or
pin changes were made. Recommended next steps are to let active0408 wire the
real renderer admission caller, add production-client coverage, add complete
`group_id` forwarding, and then port/requalify all 20 Runtime scenarios.
