# AP2-M2 bootstrap fresh-capture parity — current-root sequence

Base: `hub/timeline/app/tl/integration` at `ea38656fe62950440b36cafee780698cff2c3f9c`

The approved source sequence was reviewed as the strict real-transport handoff
`9c6e05abd9cb330edce41e7d717aad43189ce81bc87c3fb4da02ba291867c59` plus
transport assertion repair `f5ae641574b45b7e9733b2ef6ffd5955a27888c0b1c1d3467b4e0121cc8e0fd6`.
The new current-root packet below is the applicable linear result; it does not
apply either old-base patch directly.

```sh
git apply --check handoff-ap2-m2-bootstrap-fresh-capture-parity-currentroot.patch
git apply handoff-ap2-m2-bootstrap-fresh-capture-parity-currentroot.patch
```

Packet SHA256:

`511ec8c038fdf5f5c6291e535ab64ae2a92ffe640bcb07d7e0f4486ed4c1f2d1`

The packet contains the real App create/init path, strict native transport
test, durable outbox reservation/recovery tests, the fresh TS capture, and its
consumed parity fixture. It makes no schema, version, generated-client,
dependency, pin, ledger, or legacy-route activation change.

## Fresh TS → Agent 4296 parity

Agent source: `4296a7091d30543d3839fe703c0f0626f9882ebe`

The App capture emits three commands and three records. The exact initializer
read list is:

```text
parent/config.output   ABSENT
parent/name            ABSENT
parent/slug            ABSENT
parent/registry.assets ABSENT
```

The raw pristine parent check remains outside recording: non-empty parent,
placements, or shots still refuse capture. The consumed packet records these
hashes over canonical JSON:

```text
commands       sha256:6276c0a9665c78c9f06c726e42b24bf7d538c6e383e851f9b13c1aa21be03493
records        sha256:4d1dc12e6be3c15e980ffecebb493cfc8baf50572a3e9e5a103ff9108142bcad
bundle         sha256:eff04f641966266d39e857de094f61e114c1074d1e4558df85adcfa041760d6e
after_bundle   sha256:e65c02cdec14937885da35b66fbe326cfaf0c677feaa7ed2f8b16e6d75a56447
inverse        sha256:37eeec535cdd8601be2c5feef99a13cab5d8c5e098e5f5d6ca63673bf813e159
redo           sha256:5a64c18f56e97e25c1eb3c435a29aa8b2203f69b7d9c301b18a1263d8927ef5b
```

Full JSON is in `ap2-m2-bootstrap-fresh-capture-parity-currentroot-packet.json`.
