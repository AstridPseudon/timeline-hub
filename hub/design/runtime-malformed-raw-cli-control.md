# Runtime malformed raw CLI control

## Scope

Add one Runtime integration test at `tests/test_raw_cli_malformed_source.py`.
It uses the original `film` fixture from `test_timeline_commit_integration`,
whose retained `music-bed` object is exactly the 19-byte
`b"synthetic-music-bed"` payload. The authored registry asset has no duration.
The test does not use `historical_audio_fixture.prepare_pcm_historical_audio_film`
or create a sibling timeline/publication.

## Exact source pair

- Agent: `27e823a5ddeb4f8995c436b44c8d42f728350919`, tree
  `7f43878c1f37abf1a8bef6d79b44df51d1ced50a`.
- Runtime candidate: the task base `8455378325dd3593cc84d489e79859ed4d58ca9d`,
  carrying Runtime `7d1cfa6b` behavior.
- Normal Runtime/client source: `a0dca16975dfe8f5e762703b99d9791a16cf7fd7`,
  artifact `sha256:f021e7714c1b40011b69ba624d288c217749d58013b8adf0352d283854f20fa0`.

## Control and assertions

The test invokes the ordinary `astrid timelines edit ... --clip
parent/clip:music-bed --trim-out 4 --idempotency-key ... --json` parser and
handler. It observes final timeline-commit HTTP sends if any occur. With this
Agent pair, the normal CLI's non-authoritative WAV preflight cannot derive
duration, so capture refuses before HTTP; the visible error must name both
metadata and duration. The test therefore requires no HTTP commit observation,
no receipt/accepted result, and no outbox byte change. It does not create a
replacement pending command when capture fails.

The duplicate's head, immutable closure, SQLite dump, and CAS bytes are
snapshotted after daemon startup and compared after the refusal. The original
source root digest and malformed bytes are also unchanged. No client duration,
hold inference, adoption, generation, metadata override, or health override is
used.

The test is integration-marked and must run once through the central exact-source
integration lane; no full, browser, or duplicate control suite is requested.
