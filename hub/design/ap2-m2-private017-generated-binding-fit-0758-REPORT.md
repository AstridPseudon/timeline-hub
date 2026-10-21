# App2 PRIVATE017 generated-binding fit

## Outcome

**ACK — bounded generated-carrier fit; downstream HOLD remains.**

The exact normally generated PRIVATE017 carrier is compatible with the App2
recorder boundary: `AgentWrite.insertion_order` is an optional string array,
and `CommandRecord.writes` remains an array of `AgentWrite`. It is omitted for
ordinary writes and is not a command argument, metadata alias, filtered write,
normalizer, or second carrier.

This ACK does not qualify the current App public014 binding, a private Agent
pin, adoption, activation, native/RT03/outer execution, release, or the
dormant project-data-remove consumer. Current App sources and all live callers
remain unchanged.

## Exact inspected identities

- Runtime: `42a7203f49bb89f299ec854cfbf2b1444e815a7c`, tree `1f220b3d3a27e8eb061b15c944bad784c8fdb82e`.
- Agent source: `ed5fd33c4a7fa9956178f9b24eb127415eaca9e6`, tree `f4a632e4f627499e0b15d8477db9aaab78ebb3d2`.
- Agent raw schema: `sha256:6dd2b082ebdb630b4fc8ec3eeeea3b40c1eebe910c84557e45ab8fab05322b16`.
- Agent canonical schema: `sha256:9f5612ff34a5758ecacae948d5c0bfb1acc867d6ecb7a6af037bf8e3974fd9d6`.
- Schema inventory: 65 definitions / 37 EditCommand clauses.
- Runtime package: `0.2.17`.
- Runtime health/schema: `sha256:a8fad23f5b46636fe219b6219bdfdeb143ee42937e2e72996c90c947e92905fd`.
- Runtime raw bundle: `sha256:e6fb80e7961b3e9eb34908b532a042a9f024e52b5178cd906d9c1d45a18a5f8f`.
- Component manifest: `sha256:1ad76db27c1d9716bb234f811bf63e1f5898cb3d5f9b835a821765e6cad895e5`.
- Artifact manifest version: `sha256:a0dc430a146f4093f64da29c1bbda32ebf25c3a1565eee2bb7860c3ec00298b0`.
- Artifact manifest file: `sha256:0c0e3379302f5ded0bef96d9a5c7d7e72a29962d83bbb5b1500c0cfd7344e06f`.
- Artifacts: 76.
- App snapshot inspected: `07d86990c65f1663529c19dc41eaf52460f58a61`, tree `757ff3e20c344afd87b15d1bcea273738011987c`.

The Runtime handoff and artifact review were read using the committed
identities above; no pre-harness identity wording was used.

## Focused fit evidence

The exact Runtime generated projections contain:

```text
TypeScript: AgentWrite = { ref; path; before; after; insertion_order?: Array<string> }
           CommandRecord.writes: Array<AgentWrite>
Python:     insertion_order: NotRequired[list[str]]
           CommandRecord.writes: list['AgentWrite']
```

The generated bundle schema has `AgentWrite.additionalProperties: false`,
requires only `ref`, `path`, `before`, and `after`, and defines
`insertion_order` as `array`/`string` items. Its `CommandRecord.writes` items
reference `#/$defs/AgentWrite`. Therefore absent ordinary writes remain valid;
`null`, null members, non-string members, and unknown keys are refused by the
same closed generated schema. No App-side type or alias was added.

The current dormant App path remains replace-only at
`src/tools/video-editor/commands/projectDataMember.ts:23-39,111-145,316-329`.
It records ordinary writes through the existing `MoveRecording` path and does
not manufacture or strip `insertion_order`. The current App generated
`AgentWrite` at `src/integrations/runtime/timeline-commit-types.ts:15` is the
unchanged public014 shape, so this worker did not edit it or the lock files.
The field is consequently a compatible generated successor boundary, not an
already-adopted App type.

Existing App `projectDataMember.test.ts` was run directly: **1 file, 9 tests
passed**. Those tests cover ordered command serialization/replay, exact
replace/merge lowering, null and opaque values, malformed namespace/key
refusal, same-leaf guards, and atomic mixed-batch refusal. They do not prove
project-data-remove or ordered inverse execution; those remain downstream
qualification work.

## Reused evidence and limits

Reused without replaying broad lanes:

- `design/ap2-m2-ed5-ordered-carrier-source-review-0748-REPORT.md`: Agent
  source ACK and the existing six-test source/schema evidence.
- `design/runtime-ed5-ordered-record-source-review.md`: reciprocal source
  compatibility, existing recorder/state/inverse binding, and refusal
  semantics.
- `design/peer-runtime-to-agent-app2-20261021T0749-private017-exact-artifact-review.md`:
  committed Runtime artifact identity and reported 252 focused + 6 raw + 1
  source ordered-semantic checks, including Python/TypeScript projection.
- `design/runtime-private017-ordered-artifact-handoff.md`: exact 76-artifact
  preservation boundary and ordinary source semantic evidence.

Local focused commands and results:

```text
npx vitest run --no-cache --config config/testing/vitest.config.ts \
  src/tools/video-editor/commands/projectDataMember.test.ts
=> 1 file passed; 9 tests passed

git diff --check
=> passed
```

No full suite, browser, HTTP/live socket, daemon, renderer, install, generated
App type refresh, private pin, native/RT03/outer execution, adoption, release,
or Runtime byte modification was performed. The Runtime/Agent broad counts
above are reused evidence, not new local claims.

## Next step

Keep current published014 and all callers unchanged. A later authorized
matched consumer change may refresh App’s generated types and add the dormant
remove carrier using the exact generated field; it must retain absent-versus-
null behavior, sibling order, malformed refusal, and serialized inverse/redo
proof. Until then, the bounded carrier ACK should not be read as App activation
or remove qualification.
