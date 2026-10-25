# D73 receiving-input packet

Status: **NOT_READY**. This is a finite source-bound packet for the existing
private earlier-owner route. The reviewed Composition source is
`afda6c66a11608d8cb012df1a54bf2489d8c20b3` / tree
`67bd2d4ee1d50bd95ebb8b0de55d4d1ed1e3e87f`, and the independent Runtime source
review `rt-D73-source-review-2209` is PASS7. Its seven-control qualification is
preserved and not rerun here.

The route remains the immutable Agent `2eca9a1d…` + Runtime `ab1e4f61…`
own-node route. It is not D139’s merged `cd63/f103` child/core. No source was
substituted, no receipt was fabricated, and no product pin or DTO was changed.

The source objects and private recipe rows are present, but receiving inputs are
not. In particular, the exact Agent checkout/receipt is absent, no D73 App
receipt exists, no afda Composition receipt exists, the genuine newline
`key=value` manifest is absent, both central rows are uninstalled, and neither
central ID has fresh preflight/body/XML/raw/disk evidence. Interpreter,
schema, profile and Node origin/dependency qualification is also absent; that
recipe remains owned by Runtime D139 child-imports-2153 / maker2212 security.

`missing-inputs.json` is the complete field-level handoff. For App and
Composition it asks for commit, tree, parents, absolute clean path, origin,
receipt path/content/hash rather than guessing values from unrelated pins.

The production caller remains the reviewed static route only after those gates:

```text
$ORCH/bin/request-test integration:agent d73-ab1e-selected4-exact-nodes --no-cache --files '<four exact selectors>'
$ORCH/bin/request-test integration:agent d73-ab1e-fork-exact-nodes --no-cache --files '<one exact selector>'
```

Each row must continue to invoke the supported pinned launcher with
`run -- -m pytest -q -o addopts= -m integration -p no:cacheprovider --timeout=45`
and bind `P4_D73_REQUEST_ID`/`P4_D73_EVIDENCE` to its own central ID. C0’s
request/reply field set is recorded in `receiving-inputs.json`; this packet
makes no DTO change.
