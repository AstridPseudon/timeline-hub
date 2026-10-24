# A4 image evidence/cause review

Verdict: stale submitted-vs-recorded boundary, not command mutation.

Evidence verified:

- Producer input SHA: `c0a3b657…`
- App output SHA: `af1a9a845…`
- Project/timeline: `7b6f2bae…` / `film`
- Base revision/publication match exactly.
- Idempotency key matches receipt.
- Request body SHA recomputes to `sha256:d27b8f7b…`.
- Accepted receipt: `txn-15e03e4e55bf485cae9b70831ce25663`
- Status: `accepted`; `rebased_onto: null`.
- Publisher: `app-image-witness`; event `4`; project sequence `[18,18]`.

Every submitted command field is preserved exactly:

```text
schema_version: 1
op: "clip.add-media"
version: "1"
select: "parent"
args.media: exact five-field selection
args.row: exact id/track/at/asset/clipType/hold/opacity
intent: {}
created: [parent/asset:<asset>, parent/clip:clip-0]
```

The authoritative command adds:

- `authorship`: direct asset and clip writes
- `bindings`: `media.track -> parent/track:visual`
- `expect`: both created entities were absent
- `reads`: 15 read facts
- `selections`: 3 guarded collections
- `resolved: []`

Thus the minimal assertion adaptation is:

```ts
const submitted = request.commands[0]!;
const authoritative = data.commands[0]!;

// Preserve every submitted expectation; do not hand-pick fields.
for (const [field, value] of Object.entries(submitted)) {
  expect(authoritative[field], `authoritative command 0.${field}`).toEqual(value);
}

expect(authoritative).toMatchObject({
  authorship: {
    [`parent/asset:${submitted.args.media.asset}::`]: 'direct',
    'parent/clip:clip-0::': 'direct',
  },
  bindings: { 'media.track': 'parent/track:visual' },
  expect: {
    [`parent/asset:${submitted.args.media.asset}::`]: { state: 'absent' },
    'parent/clip:clip-0::': { state: 'absent' },
  },
  resolved: [],
  reads: expect.any(Array),
  selections: expect.any(Array),
});
```

The submitted step has `patch: []`; Runtime records the authoritative effects. Preserve the submitted metadata fields, then assert the recorded effects separately:

```ts
const submittedStep = request.steps[0]!;
const authoritativeStep = data.steps[0]!;

expect(submittedStep.patch).toEqual([]);
expect(authoritativeStep).toMatchObject({
  id: submittedStep.id,
  label: submittedStep.label,
  intent: submittedStep.intent,
  tags: submittedStep.tags,
  command_ordinals: submittedStep.command_ordinals,
  dependencies: expect.any(Array),
});

expect(authoritativeStep.patch).toEqual([
  expect.objectContaining({ op: 'set', ref: 'parent', path: ['config', 'clips'] }),
  expect.objectContaining({
    op: 'set',
    ref: 'parent',
    path: ['config', 'registry', 'assets', submitted.args.media.asset],
    before: { state: 'absent' },
  }),
]);
```

Observed canonical effects are exactly one new `clip-0` and one image registry entry; no child/occurrence mutation was observed.

The accepted response contains no top-level `records`, `effects`, or `history` fields. Therefore record/history readback, inverse, and refusal were not executed or verified. The receipt itself is authoritative and equals `data`; its `request_hash` differs from the App body hash by design because Runtime hashes invocation identity plus publisher/path/request, not only the JSON body.

Checks:

- `python3 scripts/artifact_manifest.py --check` — passed.
- `git diff --check` — passed.
- Offline finite-JSON, body-hash, identity, key, and submitted-field comparison — passed.
- No producer rerun, fixture recreation, Runtime call, full suite, or product/source/test edit.

Worktree is clean. Completion marker and commit message were written.