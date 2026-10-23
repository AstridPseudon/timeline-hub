# P1 D21 bench portability handoff

The source-persistence issue is confirmed: sync restored the old authoritative
hubkit builder bytes. Main/Codex owns publication; this worker did not edit
hubkit, hub-sync, dispatcher, queue state, or any repo.

Use the exact packet files beside this handoff:

- `handoff-ap2-P1-bench-portability-1303-make-child-venv.sh`
  SHA-256 `f5d14c6e62e6c07fd644438c903c933cbc74bc462ea314a798bd01c029fbc03`
- `handoff-ap2-P1-bench-portability-1303-make-runtime.sh`
  SHA-256 `fd2c6bfa12e591c7ead38ab340f3e3cec2663e3ae731261b43ce34a974ce5c5e`
- `handoff-ap2-P1-bench-portability-1303-node-bootstrap.sh`
  SHA-256 `436361860c19fdacda0d301e2e606935a72bc291a900871fdc63baae601cdf8`
- `handoff-ap2-P1-bench-portability-1303-authoritative.patch`
  SHA-256 `941b293dc3b3bede894f59c3ce88768e9a04ae65e4cc9b4a5c64398f8ec02aa`

Inputs retained exactly: Agent `5b1b4db8253f46e0e085908e79f309d492877386`,
Runtime `3b926efab2eed122d374540baee297d4cdcec62a`, Agent proof lock
`236d5be9894de96ce0483894630d54ee28f65107cd44ebe845940bc68c28c778`, and
Remotion lock `f4fc0a32a8822e956dfa21ff35d19c0c83d147c754cdb3546f91c84e330be18d`.

Host state is NOT READY: current Node is `v20.20.0`/npm `10.8.2`; required is
Node `v20.19.4`/npm `10.8.2`. The bootstrap selects an already-exact path or
verifies the canonical staged archive SHA-256
`7a488a09e2fc02fbd1bc4ae084bea8a589314f741c182fc02c5f3f07c79a29d4`; it does
not download. Fresh immutable names and the unchanged queue → dispatcher →
builder route are required after host readiness.

See the worker [report](../workers/ap2-P1-bench-portability-1303/report.md) for
exact probes, prior P1/P3 body hashes, limitations, and the recorded
authoritative-original hashes.
