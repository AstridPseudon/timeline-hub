# Handoff: P3 snapshot-preflight OPS review

Review result: PASS for the existing P3 source-vs-snapshot guard and retained
synthetic-object qualification.

- Retained 14896 snapshot `be75f72121d465d4d4e504723162d8afb045ddc2` has sole
  parent `1117c15f7e37a087a1175ea0e923958ce8a4132d` and tree
  `654a66946da8a4da65248576a9eb5e32a9e8d382`; corrected guard accepts it.
- Retained 20262 snapshot `cf189516aacea4e6438c9f29eaf872ceb14efa1e` has sole
  parent `0cdc76782833d594776452e07706acb406c51553` and the same tree; corrected
  guard accepts it.
- Real wrong-tree, multiple-parent, and unauthenticated-parent contexts reject.
- P3 digest is `48499e7d96c570ce32065d5e4981002d416a471c955ad83a17bda65c451668d1`;
  P1 is `234e7430dd785285ed4faa8ee5ff287555310aedda53b70c0ee5b4e33229418c`;
  outside rows are `4907fc1a7e1cc6d1679e33b4137e0eb42e97af146cee4fa0f4b112dab28215ae`.
- Static prelude through the shared-install boundary, source/file/origin/pin
  checks, private graph/lock checks, and Python imports passed read-only.

The detached service worktrees were already removed. No actual service/body
PASS is claimed. After manager authorization, the existing route for exactly
one changed OPS run is:

```text
/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/request-test ap2-P1-reviewed-compose-0959 ap2-P3-gate5-h6-0348 --no-cache
/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/wait-test <returned result ID>
```

No row mutation, Git write, browser, HTTP/body, build, full suite, request-test,
or worker-process operation was performed.
