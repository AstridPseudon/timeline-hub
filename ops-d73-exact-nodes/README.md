# D73 exact-node route candidate

Status: `CANDIDATE_NOT_INSTALLED` / `NOT_READY`.

This private candidate is the receiving recipe only. It does not edit the
central dispatcher, `request-test`, `test-run`, `suites.conf`, Agent tests,
Runtime source, or an installed environment. The owner may render the rows
only after a genuine four-repository receipt supplies every value. The
selected4 and fork requests remain separate exact-source requests; they must
not be combined into an overlay or whole-file replacement.

The actual entrypoint selected by the reviewed D73 source is
`tools/p4-d73-pinned-launch.sh`. Its reviewed launcher SHA-256 is
`9f668e398b1ea4cce48a6c610102723e0a3dab27a764be4191015aa7fc4110cd`; the
launcher source is the `d70bb370f396f137933d3b8ae3b194588e96e2b1` author source
reviewed at `375c773449b1c6b477f10c1daff1d9f4704208a2`. The old `cec561…`
launcher in the frozen selected/fork origins is not eligible.

## Candidate suite rows

These are direct suite commands. The existing `test-run` appends the
`request-test --files` selectors to the launcher after `run --`; therefore
`-m pytest -q` is deliberately first. `D66_OUTPUT_DIR` is the runner-provided
per-request directory. The parent basename is the actual central request ID;
no guessed request-ID environment variable or shared XML path is used.

```text
agent d73-ab1e-selected4-exact-nodes env -i HOME=/root LANG=C.UTF-8 LC_ALL=C.UTF-8 PYTHONDONTWRITEBYTECODE=1 P4_D73_MANIFEST=__P4_D73_MANIFEST__ P4_D73_EVIDENCE="$D66_OUTPUT_DIR" P4_D73_REQUEST_ID="$(basename "${D66_OUTPUT_DIR%/d66}")" __P4_D73_AGENT_PATH__/tools/p4-d73-pinned-launch.sh __P4_D73_MANIFEST__ run -- -m pytest -q -o addopts= -m integration -p no:cacheprovider --timeout=45 --junitxml="$D66_OUTPUT_DIR/$(basename "${D66_OUTPUT_DIR%/d66}").xml"
agent d73-ab1e-fork-exact-nodes env -i HOME=/root LANG=C.UTF-8 LC_ALL=C.UTF-8 PYTHONDONTWRITEBYTECODE=1 P4_D73_MANIFEST=__P4_D73_MANIFEST__ P4_D73_EVIDENCE="$D66_OUTPUT_DIR" P4_D73_REQUEST_ID="$(basename "${D66_OUTPUT_DIR%/d66}")" __P4_D73_AGENT_PATH__/tools/p4-d73-pinned-launch.sh __P4_D73_MANIFEST__ run -- -m pytest -q -o addopts= -m integration -p no:cacheprovider --timeout=45 --junitxml="$D66_OUTPUT_DIR/$(basename "${D66_OUTPUT_DIR%/d66}").xml"
```

`__P4_D73_AGENT_PATH__`, `__P4_D73_MANIFEST__`, and the evidence directory
are render-time receipt values. The Runtime receipt must name immutable commit
`ab1e4f6141987706132916e2da16477f5a019464`, tree
`7d8e77b2f5a4af79305c9212ce5174d3ea9fd657`, observed at
`/home/user/work/wt/rt-pin-ab1e4f61`.

## Exact requests and source tuple

The selected4 request is four nodes, exactly these three local selectors plus
one HTTP selector:

```text
tests/sdk/test_timeline_selected_schema_runtime.py::test_native_rebase_after_v2_and_selection_removal_uses_original_object
tests/sdk/test_timeline_selected_schema_runtime.py::test_native_reselection_conflicts_while_disjoint_peer_and_exact_retry_survive[pin]
tests/sdk/test_timeline_selected_schema_runtime.py::test_native_reselection_conflicts_while_disjoint_peer_and_exact_retry_survive[element]
tests/sdk/test_timeline_selected_schema_runtime.py::test_http_attached_selected_param_retains_original_pin_after_v2_removal_restart
```

The fork request is exactly one node:

```text
tests/editing_conformance/test_occurrence_fork_source_baseline.py::test_current_runtime_retained_fork_then_emitter
```

The source guard requires launcher SHA `9f668e…`, selected-file SHA
`8243f3b9fe71b218b3b6a402c10d099e15c848b91b82770383e91a2dd3a72b86`, and
fork-file SHA `3fef15b5862e044942f2d0164b37f6f9281f86d378345d8a0b262c64870af8a4`.
The receipt must also prove a clean canonical Agent checkout, its commit/tree,
the exact Runtime receipt, and the rendered four-repository manifest. The
normal `22bf4560…` source is not eligible by itself: its selected-file hash is
`6d7ba762…`, not the reviewed selected tuple.

## One canonical owner dry check

After the receipt and manifest exist, the owner runs the private
`dry-check.sh` with the Agent path, receipt, commit, and tree. It verifies
canonical path, clean source, launcher/test hashes, exact selectors, shell
syntax, JSON/parser inputs, and the existing normal source guards. Its
`--bind-check` mode derives two distinct synthetic central IDs from two
`.../d66` directories and proves their XML paths cannot overwrite. Its
`--controls` mode is the only control invocation: it calls the reviewed
launcher through real `run --` argv with the supported positive-17 one-call
stub and poisoned-source zero-call stub supplied by the Agent receipt. It does
not invoke a D73 body here. Historical control results from 2036/2111 are
retained as history, not claimed as fresh evidence for this candidate.

## Admission and non-claims

The candidate remains not ready. Missing inputs are: (1) one clean eligible
Agent receipt satisfying all three source hashes, (2) selected4 source/receipt
binding, (3) fork source/receipt binding, (4) the rendered four-repository
D73 manifest, (5) installation of both exact suite rows in central
`suites.conf`, and (6) fresh per-central-ID result/receipt artifacts from the
owner-run rows. The missing receipts are explicit; no executable defect is
hidden behind admission. No live service, provider, socket, install, body,
full suite, profile, acquisition, D130 path, or new framework is part of this
candidate. Do not retarget frozen `a4e016b6…`/`5e9ad1c6…` or request `18455`.
