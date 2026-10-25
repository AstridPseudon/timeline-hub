# D73 own-node exact service recipe (candidate)

`CANDIDATE_NOT_INSTALLED`; receiving status `NOT_READY`; product bodies and
real interpreter preflight `NOTRUN`. This directory is private source for the
normal service owner to review and install. Nothing here installs a suite,
acquires a dependency, mutates a child, or requests a run.

D139 ends the freeze and supersedes frozen-core attempts. This recipe is the
separate **own-node Runtime ab1e** route. It is not the future merged-tuple
child/core recipe, and must not retarget frozen `a4e016b6…`/`5e9ad1c6…`, request
`18455`, or their receipts. D139 worker `rt-OPS-D139-child-imports-2153` exclusively
owns the child schema/distribution recipe. Missing genuine interpreter/schema
source is a finite prerequisite, never grounds to borrow Main's site-packages,
change guards, or construct an old-venv overlay. Agent 2136's frozen-tuple schema
binding evidence is input to that owner, not admission for this route.

## Exact eligible source

The existing receipt
`$ORCH/queue/done/checkout-agent-2eca9a1da94eb35bb969540e150192ff920ce326`
records `/home/user/work/wt/agt-pin-2eca9a1d`, commit
`2eca9a1da94eb35bb969540e150192ff920ce326`, tree
`888c16e3dbbff2d6827e7ffcfea64208b0e2a5e4`, origin
`https://github.com/peteromallet/astrid-agent`. This is an immutable older
snapshot, **not current merged Agent home**. Both independent exact requests
use this eligible combined source receipt while retaining their separate test
origins and results. No file overlay or alternate operational launcher is used.

The launcher is that checkout's `tools/p4-d73-pinned-launch.sh`, SHA-256
`9f668e398b1ea4cce48a6c610102723e0a3dab27a764be4191015aa7fc4110cd`, from
`d70bb370f396f137933d3b8ae3b194588e96e2b1`, reviewed at
`375c773449b1c6b477f10c1daff1d9f4704208a2`. The selected-file SHA-256 is
`8243f3b9fe71b218b3b6a402c10d099e15c848b91b82770383e91a2dd3a72b86`
(selected source previously observed at `27140eaafa748eb1d7c0789c8150b5872d1c07ad`).
The fork-file SHA-256 is
`3fef15b5862e044942f2d0164b37f6f9281f86d378345d8a0b262c64870af8a4`
(fork origin `8c41696560fd278705751febdcd32527bc2cdf07`, reviewed 2042).
The immutable focused-control SHA-256 is
`0c2c70bd5e26598beebd31f4c7a0a3c1bf48bdc5e9f32ff93c6b54bf15b4b600`.

Runtime is receipt-backed `/home/user/work/wt/rt-pin-ab1e4f61`, commit
`ab1e4f6141987706132916e2da16477f5a019464`, tree
`7d8e77b2f5a4af79305c9212ce5174d3ea9fd657`, origin
`https://github.com/banodoco/banodoco-workspace-runtime`. Its receipt is
`$ORCH/queue/done/checkout-runtime-ab1e4f6141987706132916e2da16477f5a019464`.
The Agent runtime lock binds this commit and all 15 vendored files.

Current `/home/user/work/agent` was observed at `547e10456250c1b5bcf63b44a50c90ff0563ce1e`
(tree `68df11fad2b082fa12d99ca20404e1e40e350cd7`). Its launcher is `cec561…`,
selected source `6d7ba762…`, and fork source `cd921e3f…`; it is ineligible for
this own-node recipe. A future merged tuple requires its own review/receipts.

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
central registry format. Render `__P4_D73_AGENT_PATH__` to the exact eligible
Agent path above and `__P4_D73_MANIFEST__` to the genuine manifest's absolute
path; shell-quote render values if needed. There is no central installation in
this change. Only the normal owner install after independent review may add
these rows to `$ORCH/tests/suites.conf`.

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
"$ORCH/bin/request-test" integration:agent d73-ab1e-selected4-exact-nodes --no-cache --files 'tests/sdk/test_timeline_selected_schema_runtime.py::test_native_rebase_after_v2_and_selection_removal_uses_original_object tests/sdk/test_timeline_selected_schema_runtime.py::test_native_reselection_conflicts_while_disjoint_peer_and_exact_retry_survive[pin] tests/sdk/test_timeline_selected_schema_runtime.py::test_native_reselection_conflicts_while_disjoint_peer_and_exact_retry_survive[element] tests/sdk/test_timeline_selected_schema_runtime.py::test_http_attached_selected_param_retains_original_pin_after_v2_removal_restart'
"$ORCH/bin/request-test" integration:agent d73-ab1e-fork-exact-nodes --no-cache --files 'tests/editing_conformance/test_occurrence_fork_source_baseline.py::test_current_runtime_retained_fork_then_emitter'
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
and source guards identify the older tested own-node source. They must remain
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
inputs, all-missing census, absent schema and multiple missing paths, and refusal
of an old frozen tuple. `--source-check` prints every source error and receiving
need together. Without a manifest it reports every required key, both absent
central rows, both missing fresh result sets and unqualified interpreter/schema
readiness. With complete valid source inputs it can report `source_ready: true`;
receiving status remains `NOT_READY` until normal receiving evidence is reviewed.

No product, test-provider, central registry, dependency install, generated file,
pin, contract, or protected assertion is changed. All C0 request/reply fields and
save behavior remain unchanged and functionally unverified by this source task.
