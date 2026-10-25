# D73 exact-node route candidate

Status: `CANDIDATE_NOT_INSTALLED` / `NOT_READY`.

This is a private receiving recipe for the normal central test service. It does
not modify the central dispatcher, `request-test`, `test-run`, `suites.conf`,
an Agent test, a Runtime source, or an installed environment. The owner may
render the two rows below only after normal checkout receipts provide every
placeholder value. The selected4 and fork rows are deliberately separate:
their Agent sources are different immutable origins and must not be merged into
one snapshot or replaced with a whole file.

The actual entrypoint selected by the reviewed D73 source is
`tools/p4-d73-pinned-launch.sh`, taken from the Agent checkout named by the
rendered manifest. The reviewed launcher source is the `d70bb370…` source
under independent review `375c773…`; this recipe assumes neither an installed
home nor a moving `/home/user/work/agent` path.

## Candidate suite rows

The normal suite installer should render the placeholders from a fresh,
receipt-backed four-repository manifest and install these rows in the Agent
service registry. The command intentionally has no test selectors: the normal
`request-test … --files` argument is appended by the existing runner to the
launcher body command.

```text
agent d73-ab1e-selected4-exact-nodes env -i HOME=/root LANG=C.UTF-8 LC_ALL=C.UTF-8 PYTHONDONTWRITEBYTECODE=1 P4_D73_MANIFEST=__P4_D73_MANIFEST__ P4_D73_EVIDENCE=__P4_D73_EVIDENCE__ P4_D73_REQUEST_ID=d73-ab1e-selected4-exact-nodes __P4_D73_AGENT_PATH__/tools/p4-d73-pinned-launch.sh __P4_D73_MANIFEST__ run -- -o addopts= -m integration -p no:cacheprovider --timeout=45 --junitxml=__P4_D73_EVIDENCE__/d73-ab1e-selected4-exact-nodes.xml
agent d73-ab1e-fork-exact-nodes env -i HOME=/root LANG=C.UTF-8 LC_ALL=C.UTF-8 PYTHONDONTWRITEBYTECODE=1 P4_D73_MANIFEST=__P4_D73_MANIFEST__ P4_D73_EVIDENCE=__P4_D73_EVIDENCE__ P4_D73_REQUEST_ID=d73-ab1e-fork-exact-nodes __P4_D73_AGENT_PATH__/tools/p4-d73-pinned-launch.sh __P4_D73_MANIFEST__ run -- -o addopts= -m integration -p no:cacheprovider --timeout=45 --junitxml=__P4_D73_EVIDENCE__/d73-ab1e-fork-exact-nodes.xml
```

`__P4_D73_AGENT_PATH__`, `__P4_D73_MANIFEST__`, and
`__P4_D73_EVIDENCE__` are render-time values, not paths to guess. In
particular, the Runtime value in the manifest must be the existing checkout
receipt for `ab1e4f6141987706132916e2da16477f5a019464`, whose observed path is
`/home/user/work/wt/rt-pin-ab1e4f61` and whose tree is
`7d8e77b2f5a4af79305c9212ce5174d3ea9fd657`.

## Exact requests

The selected4 request uses the reviewed Agent source at commit
`4073fb0f84a9d0afbcba61b9406748a09d9c3c62` (tree
`8c3a6c64b2ed467e185e6c3fef366e9063525653`). The independent fork request
uses commit `8c41696560fd278705751febdcd32527bc2cdf07` (tree
`b3638fbf9edb2b2104a89a7e7e4400cac707e471`). In each command, `<worker>`
must be the normal worker whose snapshot receipt names that exact Agent source;
do not substitute `integration:agent` or an old worker home.

```bash
R=$("$ORCH/bin/request-test" <selected4-worker> d73-ab1e-selected4-exact-nodes \
  --files "tests/sdk/test_timeline_selected_schema_runtime.py::test_native_rebase_after_v2_and_selection_removal_uses_original_object tests/sdk/test_timeline_selected_schema_runtime.py::test_native_reselection_conflicts_while_disjoint_peer_and_exact_retry_survive[pin] tests/sdk/test_timeline_selected_schema_runtime.py::test_native_reselection_conflicts_while_disjoint_peer_and_exact_retry_survive[element] tests/sdk/test_timeline_selected_schema_runtime.py::test_http_attached_selected_param_retains_original_pin_after_v2_removal_restart") && \
  "$ORCH/bin/wait-test" "$R"

R=$("$ORCH/bin/request-test" <fork-worker> d73-ab1e-fork-exact-nodes \
  --files "tests/editing_conformance/test_occurrence_fork_source_baseline.py::test_current_runtime_retained_fork_then_emitter") && \
  "$ORCH/bin/wait-test" "$R"
```

The first request is exactly three selected local nodes plus one selected HTTP
node. The second request is exactly the separate fork node. The runner must
retain its XML, raw log, source-bound manifest, preflight/body exit files,
receipt, records, bindings, effects, dependencies, history, and undo-step
artifacts per ID. No whole-file selector, fallback, `--runxfail`, filter,
retry, or broader family is part of this candidate.

## Admission and non-claims

The D73 launcher preflight must keep the existing positive/poison controls:
the positive bounded stub exits `17` after exactly one call; a manifest with a
poisoned Agent SHA exits nonzero before the stub and records zero calls. This
candidate does not run either test body. It only records the retained bounded
control evidence and checks that source receipts, required manifest keys,
launcher identity, and exact selectors are available for a later owner run.

The candidate is not ready because the exact selected4 and fork Agent checkout
receipts are not currently available to this worker, the rendered four-repo
D73 manifest is not installed, and neither candidate suite row is present in
the read-only central `suites.conf`. The old `*-nodes` rows remain
unsupported for this tuple: they bind `/home/user/work/runtime` or the frozen
`33fc…` Runtime and their generic defaults do not provide the required cleared
addopts/integration selection. Do not retarget the frozen `a4e016b6…` /
`5e9ad1c6…` tuple or request `18455`.
