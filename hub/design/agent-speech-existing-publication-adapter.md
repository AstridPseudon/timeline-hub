# Agent M2 speech existing-publication adapter

The narrow adapter is limited to the existing `generation.generate_speech`
capability. `runtime_synthesizer` keeps the caller's exact text and settings,
reuses its existing idempotency context, and supplies the existing v1 audio
intent only for the speech path: one `main` group with selector `speech`,
`variant_key=original`, and `ordinal=0`. An explicitly supplied caller intent
wins unchanged.

The SDK invocation helper recognizes that capability as audio only when an
explicit `generation_intent` is present. It then uses the existing
`_kernel_invoke` admission path, which produces the matching
`generation.publish_v1` effect. No other capability gets broadened and no DTO,
endpoint, schema, producer pin, or worker commit is added.

The synthesizer retains terminal task/attempt IDs, the managed output row and
association, and terminal `generation_publish_v1` context alongside the old
readable-audio result. It does not derive a generation, variant, catalog
digest, selection, or duration from latest/gallery/CAS/client input. The
existing publisher and readable-audio/RIPPLE path remain unchanged; exact
generation/variant/catalog selection and verified duration remain Runtime's
counterpart work.
