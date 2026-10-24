## Result: PASS (conditional)

Standard `pip download` is an appropriate acquisition operation when run with:

- the exact filtered `bb50a43…` `requirements/proof.lock`;
- `--require-hashes --no-deps --only-binary=:all: --no-cache-dir`;
- the same `CHILD_VENV_PYTHON`/platform as the maker (`python3.13` default);
- a durable physical wheelhouse retained through request queueing and maker snapshotting.

The authentic lock hash is `236d5be9894de96ce0483894630d54ee28f65107cd44ebe845940bc68c28c778`. The exact filter preserved all 127,228 bytes and 1,550 lines because the four excluded prefixes are absent.

The requester/maker validate and snapshot the wheelhouse, but Store leases do not cover the producer directory. TMPDIR cleanup before handoff correctly causes refusal. No old child, RECORD, cache, or unverified artifact is acceptable. Bootstrap availability, unsupported `.data` layouts, missing/incompatible wheels, and hash/tag/version mismatches remain fail-closed.

Evidence: [wheel-acquisition-review.txt](</tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-OPS-wheel-acquisition-review-0747/evidence/wheel-acquisition-review.txt>)

Checks:

- Source/hash receipts: passed.
- `python3.13 -m pip download --help`: required options documented.
- Worktree: clean.
- Tests/download/network/provisioning: not run per task constraints.
- Commit message written for harness commit; `DONE` marker created.