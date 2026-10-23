R2r inverse-stage correction is ready for independent review. No blockers.

Recovered the cumulative auth/store/new-test delta from `git show 430e2061c` onto
`a01e9d806e08ee4ff6d35bad18dddafa1f09f862`. No old ancestry was merged. The harness
will create the single R2r commit; this worker did not commit, merge, check out,
modify git internals, or change integration worktrees.

The regression was a representation/boundary mismatch. Real Agent move undo
removes app.astrid children before removing empty app.astrid/app ancestors; those
ancestor before-values are sequential observations, not the complete stage input.
Track undo also legitimately has no matching list item in its stage output.
Runtime now checks every native before-value in sequence and projects the complete
observed after-values with existing `native_site`, `stored_path`, and
`project_observation` logic, including the existing parent mirror mapping. It then
checks all written sites against the independently derived canonical stage image.
This projects recorded observations; it does not execute command op/args semantics.
Missing list items are allowed only in this stage-state observation; duplicate
identities still fail. Stage/effect provenance is never flattened or discarded.

The recovered guard still obtains undo sources through the actual authenticated
`TimelineCommitStore.history_entry(project, timeline, publication)` in acceptance
and `_verify_accepted` replay. Exact undo_of, selected source step, command ordinal
partition, native/effect ranges, fixed parent ref/policy/empty dependencies,
physical refs, revision/content digests and final closure equality remain checked.
No source_revision_closure, source capture/validation, port, Agent, client, schema,
pin, artifact, config, existing assertion, or fixture was edited. Only auth,
minimal store/history handoff, and the allowed new test file differ from parent.

Added three real production-Agent positive cases (move with disjoint work, track
create, and two-source-step doc.patch inverse), checking exact canonical closure,
original recorders, preview without writes/receipt, and retry without provider
execution or another write. Added six actual-Agent forgery cases: sequential
before/after, publication, step, command ordinal and stage ref. All compare the
entire durable database before/after refusal. Retained all 15 recovered real-store
cases, including the 14 forged/missing-history variants. The original three
regressing tests and their fixtures are unchanged and pass in the bounded suite.
The real-Agent tests use the repository's integration marker because they require
a second checkout; both explicitly requested commands include them.

Exact final commands (TMPDIR exported to `/tmp/w-bc9058a76a`):

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.:packages/python ASTRID_CHECKOUT=/home/user/work/agent /home/user/work/venv-runtime/bin/python -m pytest -q -o addopts= -p no:cacheprovider tests/test_timeline_inverse_stage_authentication.py tests/test_timeline_commit_authentication.py tests/test_timeline_commit_read_basis.py
# 109 passed in 27.30s
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.:packages/python:/home/user/work/agent ASTRID_CHECKOUT=/home/user/work/agent /home/user/work/venv-runtime/bin/python -m pytest -q -o addopts= -p no:cacheprovider tests/test_timeline_commit_acceptance.py tests/test_timeline_commit_integration.py -k 'inverse or history'
# 10 passed, 68 deselected in 9.67s
```

Additional evidence command:

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.:packages/python:/home/user/work/agent:/tmp/w-bc9058a76a ASTRID_CHECKOUT=/home/user/work/agent /home/user/work/venv-runtime/bin/python -m pytest -q -o addopts= -p no:cacheprovider -p capture_wire_r2r tests/test_timeline_inverse_stage_authentication.py -k current_agent
# 9 passed, 15 deselected in 13.37s; production wire and loaded modules captured
```

Actual Agent: clean `/home/user/work/agent` at
`2e21af300abbefc8afbad217189fa4715cf82616`. `loaded-modules.json` records actual paths
and source SHA256s, including Agent `_commit_patch.py`, `inverse.py`, `commit.py`
and this worktree's auth/store. `production-wire.jsonl` contains complete actual
service requests, idempotency/publisher/path, provider PreparedCommit accept/preview
values, replies/receipts and structured failures. The path exercised is
RuntimeService.commit_timeline -> coordinator -> RequestCommitPort -> installed
Astrid provider -> TimelineCommitStore; RuntimeDaemon constructs this same service
(daemon.py:244), and generated WorkspaceClient.commit_timeline is at generated.py:963.
No transport/daemon/browser qualification is claimed.

Static and preservation commands/results:

- `pyright --outputjson runtime_protocol/timeline_commit_auth.py runtime_protocol/timeline_commit_store.py`
  on current and a complete `git archive HEAD` parent snapshot: each exits 1 with
  exactly zero auth / 76 inherited store diagnostics. Complete diagnostic identity
  comparison (messages, rules, severity, start/end spans mapped through unchanged
  source) has zero added or removed identities.
- `ruff check --no-cache --output-format=json runtime_protocol/timeline_commit_auth.py runtime_protocol/timeline_commit_store.py tests/test_timeline_inverse_stage_authentication.py`
  and parent auth/store: each has the same 11 store diagnostics (5 I001, 3 BLE001,
  2 SIM102, 1 SIM118); auth and new tests are clean. `ruff check --no-cache runtime_protocol/timeline_commit_auth.py tests/test_timeline_inverse_stage_authentication.py` exits 0.
- `python /tmp/w-bc9058a76a/compare_static.py`: passes, zero added/removed Pyright
  and Ruff identities. Raw current/parent diagnostics are retained.
- `PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-runtime/bin/python /tmp/w-bc9058a76a/verify_preservation.py`:
  passes AST and py_compile for all three changed files, byte identity for all
  276 existing test files (AST identity for Python tests), all 77 frozen files
  (contract, clients, schemas, generators, TS conformance, pins/config), allowed
  file-scope check, and `git diff --check`. Compile outputs are only in scratch.

Source identity: final complete file manifest in `evidence/source-tree.json`,
manifest SHA256 `f2f816a9072129f06bb8c0ffd39dbd81f3ad6a0de17720c711a480836cbe032f`.
Exact patch, frozen manifest, preservation summary, initial two failure traces and
native/effect stage observations, final test logs, full wire capture, loaded
modules and diagnostic comparison are in this worker's `evidence/` directory.
`tmpdir` is a pointer file to `/tmp/w-bc9058a76a`, not a directory.

No full suite, broad Agent-58, native-14, crash-24/20, browser, HTTP body or P4
run was requested or run. One faithful current-Agent multi-stage positive passes;
this does not qualify the original broad 58 matrix. H3 remains NO-GO and V4 cut.
Next: independent review of this exact source tree/commit, then orchestrator's
merge queue. Broader qualification remains with its designated owner.

Evidence directory: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-R2r-inverse-stage-sol-0922/evidence`.
