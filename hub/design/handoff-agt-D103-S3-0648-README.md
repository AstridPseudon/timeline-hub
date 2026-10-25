# F-D86 D103 + S3 source handoff

Status: **SOURCEQUALIFIED / BEHAVIORPENDING**. This is a source-only handoff
and a finite successor recipe. It is not MAIN PASS, D107 retirement closure,
or a source-delta cure claim.

## Exact integrated source

The normal Agent integration target is `dac3df399f204126e802f7888bd006c81dffa7af`,
tree `4629d906a3bfeb4566eb6cde510a2172a99f5f34`, with D103 merge
`21703579e68cfdf66218fca2c9dd2e806bb9fbde` and S3 merge
`badfe6964f7db44959bcc13d61123ad4ace8e312`.

| family | path | original-17724 blob / SHA-256 | integrated blob / SHA-256 | source receipt |
| --- | --- | --- | --- | --- |
| D103 | `tests/editing_conformance/test_cli_trim_runtime.py` | `793ab7efc71ead62c0b8e2ab827f31856a066aec` / `bd29a7a63e2213c326321ddf38bae2fe3df751c60ffa8acef1eaed46e8743868` | `9c425dea9b9aa01f6811bed76512c09b1154ad97` / `f95422aa07b917aafda4d533ddc2ff887336e2ff9e4c9d5a56f073056e41229d` | independent `A-D103.md`: `PASS_SOURCE` |
| S3 | `tests/editing_conformance/test_s3_reviewed_cohort_runtime.py` | `ab01bba8f17a2946464dc9cabdaab4fee9c03286` / `e76420c9adc51701bd2c0aff27530a84a206fe583a0215e575f4bf6c2eaf92f5` | `e754ff53b3df0f0541e5484cc38167caf3dd1844` / `b611bf469880172b725c8cf6052a1288a3d101bf65218b86f00028df4d07cafe` | protected `rt-D86-script13-protected-0629-report.md`: `PASS` |

Both integrated blobs resolve from the named target commit. The target diff
contains only these two authorized source changes: D103 adds truthful
`width=1920`, `height=1080`, `duration_seconds=42.0` to the existing
`service.import_media` call; S3 replaces the hand-built dry-run occurrence
media command with registered `capture_occurrence_add_media` and commits that
captured command. No product, Runtime, schema, generated, pin, or deletion
change is part of this handoff.

## Conservation and source basis

D103's tracked MP4 is `tests/fixtures/reshape/hype_regression/main.mp4`, Git
blob `c54c64cdc532ef4d08752ee01983966e58726531`, file SHA-256
`a13a68e512b6fae7fa4edd71b68266b33d1f7581be3fa199031809ec14d2f95e`. The
independent review tied the metadata to the genuine generator and static
ISO-BMFF facts: 1920×1080, 42.0 seconds, 30 fps. The authored source window
and timing remain `from=1`, `to=6`, `hold=5`, `speed=2`, `at=0`, and
`app.astrid.for=2.5`; the largest source endpoint is 6 and the moved
occurrence ends at 11/2. All 38 assertions, both original test functions, the
two `relevant_peer` cases, retry/lost-ack/restart, conflict/rebase, dependent
suffix, inverse/undo, refusal, and no-write guards remain.

S3 has exactly 12 assertions. Its source, timing, media pins, topology,
opaque values, command claims, refusal, retry, grouped inverse/redo, reload,
restart, ABA, and no-write guards are unchanged. The registered capture is
the same helper used by production auto-placement; no created/binding/read or
physical claim was fabricated. The remaining three ordinary-script selectors
and all six opaque selectors are unchanged-source and are excluded here.

Static verification on the integrated source: AST parse/compile PASS; D103
38 assertions and S3 12 assertions, matching original-17724; scoped Ruff
PASS; scoped mypy PASS (`Success: no issues found in 2 source files`); and
`git diff --check dac3df399f^ dac3df399f --` PASS. No pytest, collection,
fixture/helper/function/import/provider/service/probe/body/browser/render or
full suite was run for this handoff.

## Smallest successor recipe

Use exactly the four lines in
`handoff-agt-D103-S3-0648-selectors.txt`: the three original D103 selectors
plus only the changed-source original S3 selector. The canonical overlap with
already submitted exact-source jobs remains the receiving MAIN venue's
responsibility; do not duplicate it as a new source claim. Preserve the
historical actual-17724 result unchanged: 13 selected/executed, 0 PASS,
4 FAIL, 9 ERROR (opaqueSIX 6 ERROR, ordinaryscriptFOUR 4 FAIL, D103-CLItrim
3 ERROR). No status is reclassified by this packet.

The prior identity sets remain authoritative and untouched: original550 is
the D89 rollup (`historical-original550-rollup.tsv`, SHA-256
`5fdefc7f09ec13f2cdf16f3c870a114e9c7097a224afd6127ea8b2f370d87722`), the
23 unexecuted/no-JUnit identities are `unexecuted.tsv` (SHA-256
`7f70512cfdf3d6db36c5c59106805beae7a73391803eb5d161683d8d4f98dfca`), and
the current new identity set remains the D89 `membership.tsv` / successor
packet. None is replaced, retried, retired, or inferred cured here.

The eventual MAIN caller must use the registered capture/current commit path:
read the current authenticated base, use the existing registered Agent
provider through Runtime `commitTimeline`, and preserve the exact request and
reply contract below. The source packet does not authorize execution.

## C0 v2 request shape

Mutation: HTTP `commitTimeline` with required `Idempotency-Key` and body:

```json
{
  "api_version": 1,
  "project_id": "...",
  "timeline_id": "...",
  "base_revision_id": "...",
  "base_publication_id": "...",
  "commands": [{"schema_version": 1, "op": "...", "version": "1", "select": null, "args": {}}],
  "label": "...",
  "steps": [{"id": "...", "label": "...", "intent": "...", "tags": [], "command_ordinals": [0], "patch": [], "reads": []}],
  "merge": "fields",
  "reads": [],
  "dry_run": false,
  "source": {},
  "rationale": "...",
  "group_id": "..."
}
```

`commands` may contain registered semantic commands or `doc.patch`; command
envelopes retain `schema_version/op/version/select/args`. Steps are stable,
unique, contiguous partitions with authoritative patches; request-level and
step-level reads are optional. `merge` is only `fields|atomic`. The exact
base pair, idempotency key, source/rationale/group annotations, opaque values,
guards, and all command inputs remain bound. A dry run uses the same body with
`dry_run:true` and a separate key.

## C0 v2 reply shapes

Success remains `{data, receipt}`. `data.status` is `accepted` when the landing
head equals the requested base and `merged` for a disjoint later head. Both
carry `canonical_document`, `document_digest`, normalized `commands`,
`id_map`, `provider_version`, `compiler_version`, `merge_mode`, the base and
previous head pairs, `accepted_revision_id`, authoritative `publisher`,
`steps` (patches and dependencies), `records`, `bindings`, `effects`,
`history`, `undo_steps`, plus echoed `label/source/rationale/group_id` where
provided. `receipt` is durable and its `receipt_id` is the resulting
publication; `rebased_onto` is null for `accepted` and is the landing head
for `merged`.

Conflict is HTTP 409 with the existing `{http_status, code, message, details}`
error shape. `details` has `status:"conflict"`, `reason`, structured `code`,
JSON-token `path`, `hint`, `suggested_command`, `base`, actual `current` head,
and `conflicts[]` entries containing `kind/ref/path/base/theirs/ours/choices`.
Invalid is HTTP 422 with the same outer shape and `details.status:"invalid"`,
structured `code/path/hint/suggested_command`, `base/current`, and
`conflicts:[]` where applicable. Refusal retains the existing 409
`details.status:"refused"` semantics. No failure has an acceptance receipt.

Successful dry run returns `data.status:"preview"`, `would_status:"accepted"`
or `"merged"`, `evaluated_head`, candidate `canonical_document` and digest,
normalized commands, `id_map`, complete steps and `merge_mode`, with
`receipt:null`; it creates no durable revision, allocation, history, head, or
idempotency winner.

Historical accepted `rebased` receipts remain authentic and replay unchanged;
new v2 success uses `merged`. No force/overwrite route is introduced.
