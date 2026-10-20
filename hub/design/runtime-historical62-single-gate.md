# Runtime historical-audio gate — 2026-10-20

Status: BLOCKED. The original positive historical-audio journey was not
qualified. The exact prepared sibling fails Runtime startup admission before
the SDK can call `open_bundle` and before the journey can submit its first
POST.

## Exact source tuple

- Worker source: Runtime `HEAD 62d0876a2d376d38ac08b84c7d95c8cc8d004455`,
  tree `14d28d0d1ea2505729475a9a85ca6f9d43cd4771`.
- Runtime product pin requested by the brief: `7d1cfa6b1da0c50bb8a9d3430dcaa6272b20b55e`.
- Agent: commit `27e823a5ddeb4f8995c436b44c8d42f728350919`, tree
  `7f43878c1f37abf1a8bef6d79b44df51d1ced50a`.
- Normal Runtime producer source: commit
  `a0dca16975dfe8f5e762703b99d9791a16cf7fd7`, tree
  `4b7dd0fe44be973c344bab3de568eaf0bdd28476`.
- Normal contract: client `0.2.14`, schema
  `sha256:ce3781c282564b650890456f6c257f3faabe2de3898a84363fecd47e48b30d59`,
  producer artifact `sha256:f021e7714c1b40011b69ba624d288c217749d58013b8adf0352d283854f20fa0`.

Central request:
`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/tests/rt-m2-historical62-final-single-gate-raw27-historical-only-integration-1020184457-25493/`

- requested suite: `raw27-historical-only-integration`
- requested files: `tests/test_timeline_public_s2_mixed_cli_journey.py`
- snapshot: tree `14d28d0d1ea2505729475a9a85ca6f9d43cd4771`
- external manifest: `agent=490c10ac12d55f75d698213487353a7912d33067`,
  `app=0096ba86d09560b6581f23228167777d4ec47e88`,
  `composition=5a4e9b72f1916c4da01fa370ec5fe8d46b6da8e8`

## Evidence

The fixture worker's setup smoke passed `py_compile`, `git diff --check`, and
the direct sibling normal GET/closure checks. Its old central request
`.../rt-m2-historical-pcm-scope-setup-fix-original-raw27-two-node-pair-integration-1020183610-24878`
is not evidence: it is `fail` because it referenced the recycled old
`rt-m2-original-raw27-two-node-pair` worktree.

I then checked the prepared sibling through the exact Agent SDK's normal
`client.timelines.open_bundle(...)` path. Runtime daemon startup failed first:

```text
RealmAdmissionError: realm failed startup admission
issues: ['revisions']
table: composition_revision_dependencies
identity: historical-audio-pcm-child-bootstrap-v1
reason: dependency_graph_mismatch
expected: [('media', 'sha256:71d93ef76e5ff6087d522277e83309f1d8d790e9b756324dec73d216ea57cc75', 'sha256:71d93ef76e5ff6087d522277e83309f1d8d790e9b756324dec73d216ea57cc75')]
actual: []
```

The one authorized central run completed with exit 1 in 1.90s:

```text
exact raw27 / Runtime7d product / ordinary014 a0-f021 source preflight PASS
1 failed, 1 deselected
```

The failing node was
`test_public_cli_stale_trim_rebases_label_lost_ack_restart_retry_and_undo[historical-audio]`.
It failed during `_start_door` while opening the prepared sibling realm; no
CLI POST, provider execution, capture assertion, or journey semantic step ran.
The literal control was deselected as required. No retry was submitted.

## Scope and next step

No product, Agent, schema, read, auth, health, metadata, or additional fixture
change was made in this gate. The next worker may repair only the fixture
bootstrap dependency graph (the bootstrap seed must account for the media
dependency expected by Runtime admission), then repeat the required direct
SDK `open_bundle` closure check and one historical-only central run. Until
then, the original positive remains unverified and blocked.
