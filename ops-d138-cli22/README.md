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

The qualified source tuple is Agent `41ad656529fa8489829de9078b1b6e157c7433c8`
and normal Runtime `f103bb46866999c961a8865636f2e66d544e0c9b`. Agent `41ad…`
has the independently reviewed `4fec…` tree exactly; its only provenance
change is the lock source moving from `ab1e…` to qualified normal Runtime
`f103…`. The canonical 15 schema/client/fixture bytes remain exact. App and
Composition identities are recorded in the rendered manifest too.

The existing launcher is used unchanged, including all of its original
preflight guards. The named row performs a private pre-dispatch check first:
it requires a complete, unambiguous key=value manifest and verifies that the
Runtime tuple and canonical-15 lock agree. Duplicate or malformed keys and
tuple-lock mismatches therefore stop before the launcher can create evidence
or body artifacts. The private controls still exercise the unmodified
launcher’s run-mode success (exit 17, one body call) and poisoned-identity
refusal (zero body calls).

The private pre-dispatch gate resolves the two prior operational findings: the
qualified Agent lock now makes `use_runtime(vendored_runtime_commit())` select
normal Runtime `f103…`, and duplicate keys are refused before the unchanged
launcher is invoked. The private controls record both attacks and do not
retarget the candidate or claim original behavior.

No central registry row, manifest, receipt, checkout, dependency, schema
carrier, install, product test, or 22-case body run is created here.
