# Speech generation publication eligibility

## Decision

Use the existing generation publication contract on the registered
`generation.generate_speech` pack declaration:

```yaml
generation_publication:
  version: 1
  modality: audio
  output_port: speech
```

This is sufficient because the current generic SDK and GenericPackHost already
resolve metadata-declared modality and explicit primary output ports. No SDK
special case, action whitelist, DTO, endpoint, scope, child delegation, lock,
schema, or client change is needed.

## Independent source review

The declaration matches the existing image/video/audio publication pattern and
the frozen source candidate. The `speech` output is a file with `audio` artifact
type; `speech_manifest` and `speech_words` remain auxiliary outputs. The generic
validators reject a wrong modality, version, manifest port, or ambiguous port.

## Evidence

- Targeted SDK/publication/voiceover tests: `91 passed`.
- `git diff --check`: passed.
- Only the pack declaration and direct publication tests changed.
- The separate speech-action lane was not green because the shared Runtime
  checkout exposes `runtime_protocol.platform` without `durable_replace`; this
  is an environment mismatch outside this metadata-only change.

The real Runtime claim/settlement and genuine fixture-WAV selection remain the
Runtime counterpart boundary; this change only makes normal speech admission
eligible and preserves the predeclared `generation.publish_v1` effect.
