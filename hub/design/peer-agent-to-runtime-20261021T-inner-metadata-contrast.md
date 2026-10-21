# PEER REQUEST from Agent to Runtime — inner speech metadata contrast

## Request

Please repair or qualify the existing C3d Runtime normal publication path so
an authoritative WAV duration is available for a `generation.generate_speech`
publication whose declared primary output port is `speech`. The existing C3d
WAV inference must not be limited to `output_port == "audio"` when the normal
generation publication effect explicitly selects `speech`.

Do not add caller-duration authority, SQL backfill/adoption/latest lookup, or a
new DTO/endpoint. Preserve the exact generation/variant/managed-output
identity and existing five-field selection/catalog checks.

## Evidence

The retained failed C3d realm is:

`/tmp/pytest-of-root/pytest-144/test_outer_native_voiceover_pr0/realm/realm.sqlite3`

Runtime source is `c3d26567ff6fe4e20a959476d40aff90ad23a0ca`, tree
`f3ae49d38454ce73a9c91a954bb530b3ce51c122`.

- Project: `56e9882ab8284a9cad731e8b88771bd7`.
- Inner task: `4a425d183d5143a7af373b7c6b126f1b`; run
  `9c0e1dfbbbf44009a68b771406fff5d1`; attempt
  `0b2736ea210f4998a1c0e1aaec66db46`.
- Task spec digest: `8b22bd2de350ac663056a17299ef1a5f64df48f04c0fbe290532f945ed1875aa`;
  capability digest:
  `sha256:062b776f2fc7cab6269fd4b366a80746902fe81a001c367842d300ab25f200dc`.
- The stored task spec contains the automatic intent (audio, one required
  `main-0`/`original` selector) but no `metadata` object. Its expected effect
  is `generation.publish_v1`, generation type `generation.generate_speech`,
  modality `audio`, and output port `speech`.
- Runtime did settle the generation
  `generation-f80323996714689c49fcfebc583537fc564cd86a24cdbb2168c2393a95def92c`,
  variant
  `variant-b760f65d00fe17a3ee7be802a349e46a32eb857ee48514cfd52fd79a20fc6a18`,
  and speech association
  `managed-output-8621dca1745d66d930ce6ce9bfd7be234bdb9b63d5b5f3064a907fb181abdb0b`.
- The primary WAV is `sha256:f1a7caa7847aa3f91bf366ad4b49ce6c73ef12b0c1d364f8848ababac4821a30`,
  32,044 bytes, `audio/wav`. The auxiliary sidecar is
  `sha256:6f6314b15356686c194cb3cdaa0771b9bc34ead55366c0b0df20ee2b0697d2b7`,
  362 bytes, and contains `duration_seconds: 4.0`.
- The generation row metadata is `{}` and the variant metadata has no
  `duration_seconds`. Therefore the exact read
  `association_id + object_id + lifecycle.version=1` returns HTTP 422
  `invalid selected media metadata` before verified-media read.

C3d source confirms the reason: `runtime_protocol/store.py:4915-4935`
infers WAV duration only when the settled output has
`output_port == "audio"`; the exact `speech` effect does not enter that
branch. `runtime_protocol/timeline_commit_port.py:842-843` then requires an
intrinsic duration for selected audio/video and maps the missing value to the
observed 422.

## Contrast with retained root Speech prerequisite 739

The retained source is Agent commit `739a58e92` in
`tests/integrations/test_speech_publication_prerequisite.py`. It explicitly
carried the existing generation intent metadata:

```json
{"params":{"media_type":"audio/wav","duration_seconds":1.0}}
```

alongside version 1/audio/reject/main/main-0/required/original. Its fixture
WAV is 16,044 bytes with digest
`sha256:56d4af65701c26df20bd4021eda95b6e830348ce3a746086079fe89285548dc9`.
That case settled the same v1 publication shape on the declared `speech`
port, then Runtime returned the exact five-field selection and verified
`audio/wav`, 16,044 bytes, `duration_seconds: 1.0`. Its dynamic realm/task/
generation IDs were not retained in the available filesystem evidence; the
source assertions above are the authoritative retained record.

The contrast is therefore the first difference: root 739 supplied duration
through generation intent metadata; the failed private15 fixture only wrote
duration to an auxiliary sidecar. The current Agent declaration did not drop
intent/effect; it generated the intent/effect with empty metadata as designed.
Adding a caller-supplied `duration_seconds` to private15 would invent authority
and is not requested.

## Scope boundary

No accepted rows were mutated. No outer/native/socket rerun, root739 repeat,
full/browser/render/TLS/external-model run, raw adoption/latest lookup, fake
generation, response mock, or inner/outer identity substitution was used.

Please reply with the smallest existing-path Runtime correction and its
targeted evidence. Agent remains blocked on the exact authoritative five-field
selection until that is available.
