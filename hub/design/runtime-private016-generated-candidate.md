# Runtime PRIVATE0.2.16 generated candidate

Status: generated private candidate; source/artifact review handoff only.

## Identity

- Runtime base: `b92d3e7a05eec65c142294ef4873edd059e9b31d`, tree `6abc2f117391de8e7e35c0283f575a002199894d`.
- Agent source: `10226a7f08a739ba3e41f8e91de6971eed63aa9d`, tree `e2c08fbe9b21a3082db7bcf62d9677babfc15e98`.
- Contract version: `0.2.16`.
- Agent schema raw: `9cb9597a618f51949fe9ec35686e544dca812b8b252a96a4cff1f686afdfb3ec`.
- Agent schema canonical: `322733a57e781847e50228f91b6c6a9237ad2237406a188515c8f9da5e554bcc`.
- Inventory: 65 definitions, 37 closed `EditCommand` clauses.
- Health/schema digest: `sha256:97724260188a1b07c06520d2233bf3cbae52370185b0c0b6e4c9f0bf2accdfdd`.
- Raw bundle: `sha256:1bbc786daab05597f7a4d910ef0f8dcda531912b2d1e37318a35544ef039d7e9`.
- Artifact manifest: `sha256:b045b4ecc9bfc026de12b64defa31b064b1187c3638554a129403e6a6356e7d5`, 76 artifacts.
- Final central snapshot tree: `0dbe6ed69c2a3d8ce8e8ad08305233c5ceb8d960`.

## Scope

The candidate composes the reviewed RT08 materialization, raw-media custody, reference-projection, and generator-support source changes. Existing transcript/Speech, rational-input, selected/base-only, catalog/C4/headless/globalitem/occupancy/exact-ledger guards remain in place. Generated outputs were produced by the normal Python/TypeScript/schema/digest/component/conformance/manifest paths. Live callers: NONE.

The compatibility checker includes one reviewed contract-positive conversion: the old `TrackSetArgs.clear.items.const = "label"` is accepted as a preserved subset of the new exact Agent `enum = ["label", "muted"]`; the old label language is retained and a muted-only old language remains rejected.

## Evidence and boundary

Passed generator/schema/artifact check-only commands, Python focused tests (`287 passed` and `136 passed`), both TypeScript `tsc --noEmit` checks, and the central socket lane (`76 passed in 17.48s`). No full suite, native/browser/render, schema pin, publication, activation, or consumer adoption was run or claimed. Stale public TrackSet shape tests and the old public 6ba/55/29 exact schema assertion remain unqualified by design and were not weakened.
