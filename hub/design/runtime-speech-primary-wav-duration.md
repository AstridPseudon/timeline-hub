# Runtime speech primary WAV duration handoff

## Result

On ordinary Runtime source `30413e3c3e6db027f450e864ea9cb4a07446475b`
(tree `2c5a5088c90cddfb38fba6dadcad899b28fb2c59`), the existing settlement
fallback now accepts the declared `speech` output port in addition to the
existing `audio` port. All existing capability, WAV MIME, absent-duration,
explicit-metadata, and verified-CAS guards remain unchanged.

The 2026-10-21 03:31 Agent handoff identified the exact C3d gap: normal
`generation.generate_speech` settled generation
`generation-f80323996714689c49fcfebc583537fc564cd86a24cdbb2168c2393a95def92c`,
variant `variant-b760f65d00fe17a3ee7be802a349e46a32eb857ee48514cfd52fd79a20fc6a18`,
and managed association
`managed-output-8621dca1745d66d930ce6ce9bfd7be234bdb9b63d5b5f3064a907fb181abdb0b`.
Its declared primary WAV was `audio/wav`, 32,044 bytes, while the auxiliary
sidecar's `duration_seconds: 4.0` was explicitly not authoritative. The
existing `output_port == "audio"` condition therefore left the exact
five-field selection unavailable.

## Source change

`runtime_protocol/store.py` changes only:

```diff
-and output.get("output_port") == "audio"
+and output.get("output_port") in {"audio", "speech"}
```

`tests/test_generation_publish_v1_settlement.py` now models the real declared
`speech` selector and retains coverage for:

- normal task/attempt settlement of a WAV with initially absent duration,
  exact five-field selection, verified media read, CAS identity, and no
  canonical timeline writes;
- malformed WAV and invalid/unknown duration refusal;
- explicit metadata/value and explicit null preservation;
- exact accepted replay returning the original result without a second
  generation;
- the authenticated verified-media neighbor.

No sidecar, source window, raw object, latest/gallery lookup, client duration,
DTO/schema/API/client/version, catalog normalization, receipt rewrite, or
canonical timeline write was added. C3d was not modified, and no integration
merge or pin was performed. This ordinary-compatible patch is intended for
identical application to a NEW compatible descendant of private C3d.

## Evidence

Local targeted command:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD" \
  /home/user/work/venv-runtime/bin/python -m pytest -q -p no:cacheprovider \
  tests/test_generation_publish_v1_settlement.py -k 'not authenticated_http' \
  tests/test_imported_media_catalog.py tests/test_timeline_media_selection.py
36 passed, 1 deselected
```

Central socket-capable targeted command:

```text
request-test rt-m2-speech-primary-wav-duration-0336 targeted \
  --files "tests/test_generation_publish_v1_settlement.py"
16 passed in 2.34s
```

`git diff --check` passed. No full, render, browser, model, TLS, or old-root
rerun was requested.
