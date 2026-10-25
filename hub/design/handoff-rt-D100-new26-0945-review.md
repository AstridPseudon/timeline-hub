# D100 NEW26 result review

Result: the durable corrected candidate body contains 26 members, 20 PASS and
6 FAIL. The old-red comparison contains 26 members, 16 PASS and 10 FAIL. The
candidate six are one shared failure group; they are not six independent
Runtime CAS failures.

## Identity and acceptance checks

- Old-red: Agent `6aefd11766c019f8deff0ca5a1bfe18e9e730822`, tree
  `6f6aee59e510a0d6baea023486b97302db58477b`; Runtime `0c62dfa...`.
- Candidate: Agent `dd2fc40d94e35f93b3428210b58e8d58b3156a4a`, tree
  `757e848ddb62c06a800588167448ee324dd9cd1d`; Runtime `1daca2a...`, tree
  `a522511414947e48e317a5e5c2103483b121a750`.
- App `7841a946...` and Composition `635f4de0...` were fixed once in the
  manifest. Candidate and old-red corrected XML are durable and each has 26
  testcase members; their SHA-256 values are recorded in `outcomes.json`.
- The 26 selector map and argv each contain 26 entries. The four reviewed
  candidate source blobs match the recorded Git blob/SHA-256 values and parse
  with Python AST. Route `bash -n` passed. Corrected preflight exited 0;
  positive sentinel exited 17 and poison sentinel exited 1. The registry
  restore hash is the recorded `c4486fce...` value. The Runtime worktree is
  unchanged and `git diff --check` passed.
- The initial green attempt collected zero tests because of private dotted
  selector syntax. That setup event is preserved; only the private selector
  paths were corrected for the durable 26-member rerun.

## Exact candidate failure trace

All six failures stop at the same setup call, before a test calls
`runtime_commit`:

1. `tests/sdk/test_timeline_commit_graph_roots.py:70` already creates the
   `chapter-1` child timeline.
2. The candidate fixture wrapper in
   `tests/sdk/test_sequential_shared_item_provenance.py:59-65` loops over the
   same internal scope and calls `service.create_timeline` again with the same
   ID/key.
3. Runtime `service.py:1726-1727` routes an existing ID to
   `_adopt_empty_shell_create`.
4. The existing child was created with the registered provider, so
   `create_timeline` bootstrapped a published parent head at `service.py:1742-1746`.
   `timeline_commit_store.py:2027-2032` therefore rejects adoption with the
   internal reason `history_unavailable`.
5. `service.py:1769-1771` intentionally wraps that refusal as public
   `ConflictError: timeline already exists`.

The client/registered-provider `commitTimeline` route is not entered for any
of these six cases. No producer command, canonical document, accepted receipt,
or store CAS is reached. This is a deterministic duplicate fixture setup, not
a production CAS race. The minimum owner is the Agent test fixture change at
commit `8d43cc7c6c2` (`registered_seed`); the Runtime guard is behaving as
written and was not changed in the relevant source region between `0c62` and
`1daca`.

The old-red tuple is a confound: old Agent failures stopped on missing or
ambiguous `repeated-third` identity before this setup path, and old Runtime was
`0c62` rather than candidate `1daca`. This review therefore does not claim
isolated Agent causality. It does establish the candidate’s true first failing
boundary and the named fixture owner from source and retained stderr.

## Passing comparison

Candidate exact-time is 4/4 PASS, including the corrected `at_ms` path and the
original out-of-bounds refusal. Candidate shared-item is 16/22 PASS; all six
runtime-labelled failures are the setup group above. The local shared-birth,
consumer, identity/refusal, and no-write cases pass in the same corrected body.
The source-ready counterpart is therefore not claimed as Runtime behavior PASS.

No product, test, generated, pin, registry, or kit file was changed. No tests,
typecheck, lint, or second body were run in this review; those are outside the
read-only acceptance scope.
