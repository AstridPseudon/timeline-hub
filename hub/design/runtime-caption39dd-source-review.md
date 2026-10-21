# Runtime peer source review: generated-only Main captions

## Disposition

**SOURCE ACK — bounded scope.** Agent resolve commit
`39dd47c67351cc6d1a3f0a0fb39c495b680e9b54` is source-safe for the repaired
generated-only ownership branch and fits the existing generic Runtime carrier.
No Runtime consumer, route, DTO, semantic writer, or caller activation is
recommended by this review.

This ACK is limited to the repaired branch and envelope-level Runtime fit. It
is not a full source/schema, native, HTTP, browser, render, install, pin, or
public-surface qualification.

## Exact sources and reviewed blobs

- Agent resolve: commit
  `39dd47c67351cc6d1a3f0a0fb39c495b680e9b54`, tree
  `4b250c136557ced7c4ecff9e647acf8a63f85d69`.
  - `astrid/sdk/timeline/_clip_scalar_commands.py`, blob
    `406b8d76c1ea92ecc5fc26168d11601c1dbaacd6` (lines 59–102, 209–213).
  - `tests/editing_conformance/test_recipe_producer_clip_set.py`, blob
    `c89af2628b7ac330cd22023c8b46c756094785a5` (lines 107–180 and the
    existing-owned controls at 77–105, 183–215).
- Rejected prior Agent source: `e96eeb5e5` (tree
  `a679331c961d35bdb49d7c80115d9e5d66412672`). Its generated-only branch
  lacked the incoming-owner refusal.
- Main witness source identity: commit
  `860d43b331fb4422b16bc0dbd7b08666a0c766a0`, tree
  `ea4eabb8eb469df63fd1d515f84982d85b2f14cc`, from
  `ap2-m2-fresh-caption-main-joint-case-handoff-0447.json`.
- Runtime peer source: integration commit
  `b92d3e7a05eec65c142294ef4873edd059e9b31d`, tree
  `6abc2f117391de8e7e35c0283f575a002199894d`.
  - `runtime_protocol/timeline_commit_validation.py`, blob
    `a50d811c4deecd99e2ff5979950c82838a1126bf`.
  - `runtime_protocol/timeline_commit_provider.py`, blob
    `a05812e82ee2930f29e277f260f3329855378932`.
  - `runtime_protocol/timeline_commit_port.py`, blob
    `07883e592e1349263adc7e7f5cefc89e6c985c9c`.
  - `runtime_protocol/timeline_commit_store.py`, blob
    `be6708a65b11456151f55be29e47697d54f3f888`.
  - `runtime_protocol/schemas/timeline-commit-bundle.json`, blob
    `cf5dfbda604f7337f8fc155f811cb67fbfa4dfc9`.

## Review result

The repair closes the prior hole at `_producer_app` before any incoming app
leaf is written:

1. For an established generated carrier with no persisted `managedBy`, any
   incoming `managedBy` now refuses with `unsupported_ownership`, including a
   foreign owner and the matching generated extension. `clip_set` therefore
   cannot synthesize ownership, and the capture/execute path remains atomic.
2. The same established generated-only row still accepts a refresh that carries
   `__generated__` but omits `managedBy`; the fallback to the established
   extension is comparison-only and is never materialized.
3. Existing owned clips retain the prior owner match, generated identity and
   fixed identity-field checks, and malformed/missing carriers still refuse.
4. The existing clip-set path continues to preserve unmentioned text/app
   siblings and inverse round trips; timing/geometry are handled by the same
   bounded source recipe and are not rewritten by this repair.

### Actual Main witness mapping

The witness builder/compiler path is recorded as
`extension.ts:288-476,754-774` and
`timeline-patch.ts:1012-1029,1098-1183,1207-1316,1936-1978`. It emits a
`clip.add` followed by `clip.update` for
`transcript-caption-ca055bff87805488`. The persisted row has:

- `at=1`, `hold=1`, `x=128`, `y=418`, `width=1024`, `height=101`;
- text `Zażółć 🌍` and the witness label/style values;
- `app.__generated__` with extension
  `haus.astrid.transcript-lane`, contribution
  `transcript-caption-foundry`, source schema
  `astrid.transcript_segment/v1`, generator `1.3.0`, and
  `preserve-output` provenance;
- `managedBy` absent in both operations and in the persisted row; and
- the same row projected through both `parent_composition.config.clips[0]`
  and `parent_composition.clips[0]`, with opaque siblings and ordering
  retained.

The Agent source controls use the same generated-only birth/refresh boundary
and the same identity/provenance shape. The witness remains a source handoff;
it does not authorize routing the currently mixed Main batch through a legacy
snapshot writer.

### Prior-hole disposition

The rejected `e96eeb5e5` behavior allowed `_producer_app` to use the established
extension as a comparison fallback while still writing every incoming app
leaf. Consequently, a generated-only refresh could add either a foreign
`managedBy` or the matching extension. Commit `39dd47c67` adds the explicit
no-owner/incoming-owner refusal and permanent controls for both values. The
prior finding is resolved for this branch.

## Generic Runtime carrier fit

Runtime's generic path is compatible at the reviewed boundary: finite JSON is
validated and detached, the request context is passed unchanged to the
installed provider, and the commit store records provider-produced commands
and writes. These Runtime layers do not infer ownership or rewrite nested
`app` values. Thus the repaired Agent rule remains the authority: absent
`managedBy` stays absent, and an incoming owner is refused atomically before
the provider produces a mutation.

Operation-schema/digest parity and native consumer qualification are outside
this bounded review and remain separate integration work. No Runtime source,
schema, route, DTO, endpoint, or semantic writer was changed; live callers
changed: **NONE**.

## Bounded recommendation

Carry the Main generated-only refresh through the existing `clip.set` command
carrier only after the normal Agent/Runtime operation-schema pin is qualified.
Keep `managedBy` omitted for generated-only births and refreshes, preserve the
existing `__generated__` identity/provenance guard and all recorded reads/
expectations, and leave the legacy mixed-batch refusal and consumer activation
closed until that qualification is complete.
