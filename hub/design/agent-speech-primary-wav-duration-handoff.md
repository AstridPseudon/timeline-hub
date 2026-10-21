# Agent handoff: speech primary WAV duration

Runtime ordinary-compatible source now supports the existing header fallback
for the normal declared `generation.generate_speech` primary output port:

```diff
-and output.get("output_port") == "audio"
+and output.get("output_port") in {"audio", "speech"}
```

Apply this narrow change, with its settlement regressions, only to a NEW
compatible descendant of private C3d. Do not mutate C3d, relabel ordinary
Runtime 0.2.14, or treat an ordinary server as a private pair.

The change uses the already settled generation/variant/managed association and
the existing verified CAS descriptor/header reader. It fills
`duration_seconds` only when absent; explicit value/null and exact accepted
replay semantics remain unchanged. The real 03:31 C3d observation was a
32,044-byte `audio/wav` primary on output port `speech`; the auxiliary sidecar
duration was not used.

Validated on the ordinary source:

- local non-socket neighbors: 36 passed, 1 deselected;
- central `tests/test_generation_publish_v1_settlement.py`: 16 passed;
- no API/schema/DTO/client/catalog/receipt changes.

The outer voiceover/requester/native qualification remains separate and
unclaimed.
