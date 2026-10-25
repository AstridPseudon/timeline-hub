# D73 own-node exact service recipe (candidate)

`CANDIDATE_NOT_INSTALLED`; receiving status `NOT_READY`; product bodies and
real interpreter preflight `NOTRUN`. This directory is private source for the
normal service owner to review and install. Nothing here installs a suite,
acquires a dependency, mutates a child, or requests a run.

D139 ends the freeze and supersedes frozen-core attempts. This recipe now binds
the **current merged Agent 41ad / Runtime f103** tuple. The historical own-node
qualification for Agent `2eca…` / Runtime `ab1e…` remains immutable evidence and
is not retargeted. This route must not use frozen `a4e016b6…`/`5e9ad1c6…`, request
`18455`, or any old receipt. D139 worker `rt-OPS-D139-child-imports-2153`
exclusively owns the child schema/distribution recipe. Missing genuine
interpreter/schema source is a finite prerequisite, never grounds to borrow
Main's site-packages, change guards, or construct an old-venv overlay.

## Exact eligible source

The current merged Agent source is `/home/user/work/agent`, commit
`41ad656529fa8489829de9078b1b6e157c7433c8`, tree
`d29e47fe7be6e55940b42fa1477a23e7925f62fa`, parents
`41ad656529fa8489829de9078b1b6e157c7433c8 cd63be424d62226e3ee5c26fc5ce03227f5394a5
4fec53e0b14aea355e51c96c883fd75eef67a17c`, origin
`https://github.com/peteromallet/astrid-agent`. It is the normal merged
checkout, not a newly created pin checkout; no receipt is invented here.

The launcher is that checkout's `tools/p4-d73-pinned-launch.sh`, SHA-256
`9f668e398b1ea4cce48a6c610102723e0a3dab27a764be4191015aa7fc4110cd`, from
blob `f1bde17ea107a8b669cb6924fbdbd2f3979da988`. The selected-file SHA-256 is
`8243f3b9fe71b218b3b6a402c10d099e15c848b91b82770383e91a2dd3a72b86`
(blob `9f75f47b5d0c927d2b758fc395702d4cc9e2b17e`).
The fork-file SHA-256 is
`3fef15b5862e044942f2d0164b37f6f9281f86d378345d8a0b262c64870af8a4`
(blob `512c806487049c1b86a9d47bcafeb3dcb0ade60c`).
The immutable focused-control SHA-256 is
`0c2c70bd5e26598beebd31f4c7a0a3c1bf48bdc5e9f32ff93c6b54bf15b4b600`
(blob `8746ff6004ce1d49efbaff4408ef37e08714bc7f`). These four files are
byte-identical to the old `2eca…` source. The only Agent source change relevant
to this tuple is the runtime-lock provenance below.

Runtime is the current normal checkout `/home/user/work/runtime`, commit
`f103bb46866999c961a8865636f2e66d544e0c9b`, tree
`5d0cedf2e5134acf895e8d43191cc5fdc09f9883`, parents
`f103bb46866999c961a8865636f2e66d544e0c9b cf0b82dd47452a7a34fc63eb233e9b1dc0532806
0bb3bc45cef22bc317398d79e1617da3eb430df2`, origin
`https://github.com/banodoco/banodoco-workspace-runtime`. No current pin receipt
is supplied. The Agent runtime lock binds this commit and all 15 canonical
vendored files; the 15 file bytes, schema/config/client/fixture mappings and
producer metadata are unchanged from the reviewed `ab1e…` adoption.

The old `2eca…` / `ab1e…` receipt-backed qualification remains preserved as
historical evidence only. Old source aliases are rejected for this new tuple.

## Manifest and suite installation handoff

The owner must supply a genuine rendered **newline `key=value`** launcher
manifest, not JSON. `check.py:REQUIRED` lists every launcher-required key.
Blank lines and `#` comments are accepted; values split only at the first `=`.
No shell evaluation occurs. Duplicate keys and malformed/missing values are
refused. Four canonical clean checkout paths, commit/tree and Agent parents,
receipt-derived App/Composition identities, existing executable Python/Node,
pinned schema source, profile lock/archive/registry hashes, composition version,
original P4 source hash, service versions and JUnit metadata are required.
Do not render guessed paths or reuse a frozen-core manifest.

[suites.conf](suites.conf) contains the two complete candidate rows in the real
central registry format, named `d73-f103-selected4-exact-nodes` and
`d73-f103-fork-exact-nodes`. Render `__P4_D73_AGENT_PATH__` to the current Agent
path above and `__P4_D73_MANIFEST__` to the genuine manifest's absolute path;
shell-quote render values if needed. There is no central installation in this
change. Only the normal owner install after independent review may add these
rows to `$ORCH/tests/suites.conf`.

The immutable launcher still enforces canonical source location, clean four-repo
commit/tree/parents, original P4 source hash, runtime lock provenance/all 15
hashes, imported module origins, client `0.2.14`, schema digest
`sha256:867f3553ac0ff264300e5a2596b363cdb4c071842eb6570ad461c093d351708b`,
profile lock/archive/registry, Node and composition versions before dispatch.
The read-only source census inspects files; it does not replace that preflight.
A schema directory alone does not prove its module can import in the actual
interpreter. Missing distributions/pinned source remain `NOT_READY` until the
D139 owner supplies a supported dependency recipe for the applicable tuple.

## Normal caller and exact selectors

After those prerequisites and normal installation, the actual caller is:

```bash
"$ORCH/bin/request-test" integration:agent d73-f103-selected4-exact-nodes --no-cache --files 'tests/sdk/test_timeline_selected_schema_runtime.py::test_native_rebase_after_v2_and_selection_removal_uses_original_object tests/sdk/test_timeline_selected_schema_runtime.py::test_native_reselection_conflicts_while_disjoint_peer_and_exact_retry_survive[pin] tests/sdk/test_timeline_selected_schema_runtime.py::test_native_reselection_conflicts_while_disjoint_peer_and_exact_retry_survive[element] tests/sdk/test_timeline_selected_schema_runtime.py::test_http_attached_selected_param_retains_original_pin_after_v2_removal_restart'
"$ORCH/bin/request-test" integration:agent d73-f103-fork-exact-nodes --no-cache --files 'tests/editing_conformance/test_occurrence_fork_source_baseline.py::test_current_runtime_retained_fork_then_emitter'
```

`integration:agent` is an existing supported request target. `request-test`
resolves the Agent repo, verifies the named row, requires `--files` for
`*-nodes`, and queues a central ID. `test-run` snapshots the scheduling target,
selects the row by repo/suite with
its existing awk parser, validates and appends the exact selectors, then runs
`bash -c "$CMD"` with `D66_OUTPUT_DIR="$ORCH/tests/$ID/d66"`. The row intentionally
invokes the pinned Agent launcher rather than the disposable snapshot launcher;
the launcher checks its own location against the pinned manifest. The central
`snap` describes current merged scheduling source; the per-ID launcher manifest
and source guards identify this exact current merged source. They must remain
explicitly distinct in the result. Snapshotting does not authorize a different
product source.

Both rows pass `run -- -m pytest -q -o addopts= -m integration -p no:cacheprovider --timeout=45`
before the exact nodes. The launcher runs `manifest[python] -P` with that argv.
No whole-file, family filter, alternate targeted mode, or merged-core request is
substituted. `--no-cache` also prevents a central cached result from standing in
for fresh per-ID launcher artifacts.

The parent basename of `D66_OUTPUT_DIR` is the actual central ID. The row binds
`P4_D73_REQUEST_ID` and `--junitxml=$D66_OUTPUT_DIR/$ID.xml` to it. The launcher
writes `$ID.{manifest,request-id,runmanifest,preflight.log,preflight.exit,command,body.log,body.exit}`
in that directory; the runner retains its separate `request`, `snap`, `log.txt`,
`runner.log`, `status`, `exit`, and `summary` under `$ORCH/tests/$ID`.
`junit_paths` in the manifest is retained metadata; the executed `.command`
and actual per-ID XML prove the output path. The owner must retain genuine
submit/end disk witnesses alongside each result. None is fabricated here.
Central light-run admission currently requires 5 GB; this source task's
4.6 GB admission / 4 GB stop rule does not override it.

## Same author/reviewer source checks

```bash
# TMPDIR must be the worker's harness-cleaned private /tmp/w-* directory.
./ops-d73-exact-nodes/dry-check.sh --controls
./ops-d73-exact-nodes/dry-check.sh --bind-check "$TMPDIR/selected-ID/d66" "$TMPDIR/fork-ID/d66"
# No product imports, executable preflight, or body. Missing inputs => exit 1.
D73_MANIFEST=/absolute/receipt-rendered.manifest ./ops-d73-exact-nodes/dry-check.sh --source-check
```

`--controls` is independent of absent receiving inputs. It verifies the actual
immutable Agent identity/hashes, reuses the reviewed private fixture builder
in place, executes the **actual current** central named-row parser and node
request guard against private rows, then invokes the unchanged launcher with
**`run --`**, once per exact suite. Private Git/Python/Node stubs bound the test;
only fixture PATH and receipt placeholders are substituted in the rows.
The private Python stub accepts the exact `-P -m pytest` argv, checks private
origins/startup environment/cwd and all selectors, records exactly one dispatch,
writes explicitly bounded-stub XML, and exits **17**. Poisoning only `agent_sha`
returns nonzero with **zero additional calls**, zero preflight calls and no
body artifacts. Two separate central-ID-shaped directories prove non-overwrite.
These are source controls, not a real preflight, pytest body or schema admission.
No dry control is relabelled as production mode.

The same command also tests key/value parsing, malformed/duplicate/missing
inputs, current-tuple lock/source refusal, all-missing census, absent schema and
multiple missing paths, and refusal of the old frozen tuple. `--source-check`
prints every source error and receiving need together. Without a manifest it
reports every required key, current source receipt gaps, both absent central rows,
both missing fresh result sets and unqualified interpreter/schema readiness.
Receiving status remains `NOT_READY` until normal receiving evidence is reviewed.

The C0 wire shape is conserved: request fields are
`api_version/project_id/timeline_id/base_revision_id/base_publication_id/commands`
(`schema_version/op/version/select/args`), `label`, `steps` (`id/label/intent/tags/command_ordinals/patch/reads?`),
`merge/reads/idempotency/dry_run/source/rationale/group_id`; replies retain
`accepted/merged/canonical/base/landing/receipt/records/bindings/effects/dependencies/history/undo_steps`,
`conflict.reason/head`, `invalid.code/path/hint/suggested_command`, and
`preview.would_status/nullreceipt/no_writes`. No DTO or product behavior change is
made or claimed. All C0 save behavior remains functionally unverified by this
source task.
