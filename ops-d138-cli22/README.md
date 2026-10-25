# D138 CLI22 current-merged-source service recipe

This is a private source recipe. It adds one named row for the existing
central `request-test`/`test-run` parser:

```text
agent d138-cli22-current-merged-exact22 ... p4-d73-pinned-launch.sh ...
```

The row passes all 22 exact selectors from `test_native_batch_ingress.py`
with `-m integration`, `-p no:cacheprovider`, a 180-second timeout, and a
JUnit path derived from the central request ID. The row is submitted with
`request-test integration:agent d138-cli22-current-merged-exact22 --no-cache
--files '<22 selectors>'`; the central service supplies the per-ID output
directory. It deliberately excludes the parser-only
`test_file_parser_requires_both_original_pins_and_describes_registry` case.

The intended source tuple is current Agent `cd63be424d62226e3ee5c26fc5ce03227f5394a5`
and normal Runtime `f103bb46866999c961a8865636f2e66d544e0c9b`. The Agent
runtime lock remains the observed `ab1e4f6141987706132916e2da16477f5a019464`;
it is recorded as lock provenance, not relabelled as normal Runtime adoption.
App and Composition identities are recorded in the rendered manifest too.

The existing launcher is used unchanged, including its preflight. A finite
receiving seam remains: this launcher directly requires `runtime_sha` to
equal `runtime.lock.json.source_commit`, so it cannot preflight the intended
normal Runtime `f103…` while the Agent lock honestly remains `ab1e…`. The
recipe does not add a launcher or bypass that guard. The source check reports
this as `NOT_READY`; the private controls still exercise the unmodified
launcher’s run-mode success (exit 17, one body call) and poisoned-identity
refusal (zero body calls).

The review is fail-closed on two additional operational facts: the migrated
fixture’s `use_runtime(vendored_runtime_commit())` follows the preserved Agent
lock rather than the manifest Runtime, and the unchanged launcher accepts
duplicate manifest keys last-write-wins. The private controls record both
findings; they do not retarget the candidate or claim original behavior.

No central registry row, manifest, receipt, checkout, dependency, schema
carrier, install, product test, or 22-case body run is created here.
