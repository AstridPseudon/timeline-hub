# Runtime normal settled speech source

Date: 2026-10-20T16:33:37Z (UTC)

## Result

One fresh normal Runtime task was admitted, claimed, and settled through the
real `RuntimeService.create_task` → `claim_next` → `settle_attempt` path. The
worker output was a valid 8 kHz mono PCM WAV fixture, not a speech-model call.
No SQL history was fabricated and no client-supplied duration was sent.

The settlement succeeded (`state=succeeded` / terminal task `status=completed`)
and produced a durable Runtime catalog entry:

| field | value |
|---|---|
| capability | `generation.generate_speech` |
| task | `e3b0e58e9b334b12998b58fe89432ea1` |
| attempt | `8677abd18ada44c7bb30c56528740996` |
| fence / epoch | `1 / 1` |
| settle receipt | `txn-5b1f90b9acfa4bbe8df0d7facfef15d4` |
| receipt command / key | `attempt.settle` / `speech-settle` |
| CAS object | `sha256:cfd5e274b487194a82a5b3cf87b679d541baf0132027f978bac070fde8e31276` |
| CAS size / media type | `8044` / `audio/wav` |
| generation | `generation-da70e2f5ad5d3665864e37802070e3935d29778d4a335c488520f5bd9a2ea09f` |
| variant | `variant-4764f12cc706145502b2f941ff16b7fe382ae724e5a4f0b3e0c2320dd9fb9ba8` |
| managed association | `managed-output-2d68868643d51a3dee23b277c8575cfeb0ff819557de2f630ac22e59a28eded1` |
| association lifecycle | `available`, version `1` |

The CAS descriptor read back as `audio/wav`, 8044 bytes, and the CAS bytes
rehash to the exact output digest. The managed association provenance is
attempt-bound and includes `task_id`, `attempt_id`, `capability_id`,
`executor_id=speech-fixture-worker`, `fence=1`, and `runtime_epoch=1`.

## Intent and result trace

Admission carried the existing opaque `generation_intent` envelope:

```json
{
  "version": 1,
  "modality": "audio",
  "partial_success_policy": "reject",
  "groups": [{
    "group_key": "main",
    "selectors": [{"selector": "speech", "ordinal": 0, "variant_key": "original"}]
  }],
  "metadata": {
    "content_type": "audio",
    "voice": "fixture",
    "text_sha256": "sha256:e782a8b395c60b1382510a72064d5e244135e3f593754d59285a5b1d55491d51"
  }
}
```

The admitted effect was the existing `generation.publish_v1` effect with one
declared `audio/main/original/0` selector. The terminal result contains the
same intent, the expected effect, and this publication:

```json
{
  "effect_type": "generation.publish_v1",
  "publications": [{
    "group_key": "main",
    "missing_selectors": [],
    "variants": [{
      "generation_id": "generation-da70e2f5ad5d3665864e37802070e3935d29778d4a335c488520f5bd9a2ea09f",
      "variant_id": "variant-4764f12cc706145502b2f941ff16b7fe382ae724e5a4f0b3e0c2320dd9fb9ba8",
      "variant_key": "original",
      "object_id": "sha256:cfd5e274b487194a82a5b3cf87b679d541baf0132027f978bac070fde8e31276",
      "output_port": "audio",
      "ordinal": 0
    }]
  }]
}
```

The settled output descriptor carried `producer.kind=generation.generate_speech`,
`producer.provider=fixture`, and producer provenance for the source/text hash
and voice. Runtime added the attempt identity to the durable variant and
managed-output provenance.

## MediaSelection boundary

There is no valid five-field `MediaSelection` for this exact settled output on
the current Runtime. Calling the existing association selector with
`association_id`, the exact object digest, and lifecycle `version=1` joined the
real association → generation → variant → CAS records, then failed closed with:

```text
ValidationError: invalid selected media metadata
```

The underlying reason is Runtime's existing audio/video rule: neither the
generation metadata nor variant metadata contains intrinsic
`duration_seconds`. The output descriptor deliberately did not inject a
client duration. Consequently the verified-media read was not attempted; the
five-field selection was not returned.

This is not a raw-object-only result. The object is settled, CAS-authoritative,
and associated with a completed generation/variant and attempt-bound managed
output. It is also not an acceptable selection: no raw object, old generation,
latest/gallery primary, or client duration should be substituted.

## Bounded Agent recommendation

Before any Agent implementation, use the existing carriers only:

1. Keep the existing producer attempt identity (`task_id`, `attempt_id`,
   `executor_id`, `fence`, `runtime_epoch`) and managed output association as
   the provenance carrier.
2. Once Runtime has authoritative settled intrinsic metadata, obtain and carry
   the existing exact five-field `MediaSelection` (`asset`, `generation_id`,
   `variant_id`, `object_id`, `catalog_digest`). Do not add a speech-specific
   DTO, raw-object adoption path, latest/gallery lookup, or inline client
   duration.
3. Until that selection exists, preserve the existing visible refusal/held
   proposal behavior. The original voiceover/RIPPLE/readable-audio positive
   remains OPEN; this probe does not convert it into a refusal or
   `proposal_open` success.

The narrow missing seam is authoritative settled intrinsic audio metadata, not
task lifecycle, CAS custody, generation association, or producer provenance.

## Evidence

Direct normal-flow probe (run from Runtime worktree, no model call):

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD" \
  /home/user/work/venv-runtime/bin/python - <<'PY'
# fresh RealmStore + RuntimeService; register executor; create project/task
# with generation_intent + generation.publish_v1; claim; settle valid WAV;
# read task/receipt/CAS/association/generation/variant/selection
PY
```

Targeted Runtime tests:

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD" \
  /home/user/work/venv-runtime/bin/python -m pytest -q -p no:cacheprovider \
  tests/test_generation_publish_v1_settlement.py \
  tests/test_imported_media_catalog.py \
  tests/test_timeline_media_selection.py
```

Result: **30 passed in 8.95s**.

No package install, speech model call, render, full suite, or Agent edit was
performed. No Runtime product source/schema/DTO/endpoint change is proposed by
this report.
