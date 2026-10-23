# A4 integrated transcript witness

## Verdict

PASS for the requested read-only integrated witness on Agent HEAD
`14fc0740f278e13c3075fa12d5ebf975cc7044af`.

The exact transcript witness blob is identical to protected commit
`26f12b19f50021c54b2ed82bb06064749290ad22` (`c074858c073b0594985729f13bd26b633b7cd66d`),
and the prescribed pinned run passed all seven tests. No product, test, schema,
client, pin, Runtime, environment, Git, or daemon changes were made by this
worker; the worktree is clean.

## Qualification evidence

Exact command:

```text
timeout 15s env PYTHONDONTWRITEBYTECODE=1 ASTRID_RUNTIME_CHECKOUT=/home/user/work/wt/rt-pin-2a9e347f PYTHONPATH=.:/home/user/work/wt/rt-pin-2a9e347f /home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider tests/editing_conformance/test_a4_transcript_doc_patch_witness.py
```

Result: `7 passed in 1.80s` (`pytest_exit=0`). No other test suite was run.

The test environment imported Agent modules from this worktree:

- `astrid.sdk.timeline.commit` → `astrid/sdk/timeline/commit.py`
- `astrid.sdk.timeline._commit_patch` → `astrid/sdk/timeline/_commit_patch.py`
- `astrid.sdk.timeline._command_state` → `astrid/sdk/timeline/_command_state.py`
- the two provider fixture modules → this worktree's `tests/sdk/` files

Independent Runtime preflight resolves `runtime_protocol`, `runtime_protocol.platform`,
`runtime_protocol.timeline_commit`, `runtime_protocol.contract_metadata`, and
`astrid_runtime` from `/home/user/work/wt/rt-pin-2a9e347f`. The witness's
`runtime_abi` fixture intentionally supplies only the two ABI exceptions/metadata;
the command execution is Agent code against the detached in-memory port.

Target SHA-256 before and after the run was
`5181e08490658dcc97e367b38c7a54f19687e539994c3535128d08f5d085d182`.
Provider and fixture hashes were also identical before/after; see the permanent
evidence packet under the worker directory.

Protected exactness checks passed:

- current transcript witness blob == `26f` blob: `c074858c...b7cd66d`;
- current R1 product blobs == `f078d0229` blobs for `_commit_patch.py`, `commit.py`,
  and `test_commit_document_input_capture.py`;
- current registry blobs == `22f1cb169` blobs for `inverse.py` and
  `test_inverse_registry_containers.py`;
- current track witness blob == `4010f9876` blob
  `ca046a721d527a1f6bf383659b8b5bbaada4d13d`;
- all protected commits are ancestors of the integrated HEAD;
- `git diff --check 1962a2413095a2f82bf927e7c42c532072b5c812..HEAD` passed;
- changed-path scan found no vendor, node_modules, build/dist, archive, or artifact
  path;
- credential scan of the witness found no matches for the requested credential
  patterns.

Scoped Ruff and Mypy are reused from the exact reviewed witness evidence: the
reviewed body passed Ruff and Mypy, and EOF closure `1815` proved the only later
change was removal of one extra final newline while preserving all seven test
bodies/decorators/literals. They were not rerun here because this brief required
only the pinned witness test.

## Covered seam

The production seam identified by read-only App inspection is
`src/tools/video-editor/lib/project-transcript-host.ts`: transcript import calls
`input.commitData(next, { save: true, semantic: true })`, then awaits
`input.flushPendingSave()`. This Agent witness does not invoke that mounted App
path. It exercises the existing generic Agent `doc.patch` provider through
`create_runtime_commit_service().commit(...)` and `DetachedPort`, using an
App-shaped nested `parent.config.bundle` payload and the existing authenticated
transcript source-input boundary.

Concrete coverage includes nested transcript planes and opaque preservation;
explicit null versus absence; current and prior exact source pins; request
metadata (`api_version`, project/timeline, exact base pair, commands, label,
steps and patches, merge mode, reads, dry-run, source/rationale/group ID and
idempotency); preview `would_status` with null receipt; accepted canonical
document/receipt and selected records, bindings, writes, dependencies and
undo metadata; structured previous-value refusal; identity collision;
fields rebase; atomic scope refusal; and source-pin failure before nested
writes.

## Boundary and uncovered behavior

This is not transcript product semantics. It does not prove `transcript.associate`,
current mounted App/outbox/HTTP execution, reconciliation, caption ownership,
word-anchor or relational-timing behavior, open-JSON referential integrity,
exact App fixture identity parity, history-listing parity, complete effects or
authoritative attribution, whole/per-step undo, merged-reply spelling, or
Runtime service durability/idempotency across restart. The request metadata
`source.surface`/`source.via` is not production invocation proof. The old App
suite remains KEEP and was not run here.

Evidence files:

`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-A4-transcript-integrated-1823/evidence/`

No blockers. Recommended next step is normal manager merge/queue handling and
separate App/Runtime integration qualification for the uncovered boundaries.
