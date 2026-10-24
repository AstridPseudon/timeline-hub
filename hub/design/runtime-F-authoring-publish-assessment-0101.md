Blocked by the fixture scope; no product or test changes made.

The production helper delegates to the retired route. Its callers include `astrid/sdk/authoring_remote.py:310` and `astrid/sdk/remote.py:1536`. The preserved roundtrip fixture cannot exercise v2 because:

- Its `Transport` exposes only `publish_parent_composition` for writing.
- Its `RuntimeService` has no registered commit provider; new v2 commits require startup registration.

Your brief permits “ONLY the two approved fixture setup lines.” **May that allowance expand to register the existing provider and add existing authenticated v2 read/commit delegations to this Transport, preserving every original edit and assertion?** No new Runtime API is proposed.

Evidence:

- Agent commit: `b61cebe8e0d6e062f15da922f3812d7b6718f12e`; tree: `c8b86f253be7ae46a299c1a7e79ac1aaa2b6b8bb`.
- Changed paths: none. Both original test functions remain byte-for-byte unchanged.
- Runtime: `458595850c354f4403dabc58a72b98bebbc2c3a3`, origin `banodoco/banodoco-workspace-runtime`. Compared with qualified `abd47e68de6d7a36bec8ac4f0f6e0bc01d98d14e`, only the client-init generator and generated public exports differ; authentication code is unchanged.
- Frozen R4 refs resolved to Agent `11caf1d9de29`, Runtime `31c7ac3a00f7`, App `8f0c2484463e`, Composition `c82eb7c459d0`.

Checks:

- `PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-agent/bin/python scripts/vendor_lock.py check runtime.lock.json` — passed.
- `PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-agent/bin/python scripts/artifact_manifest.py --check` — passed.
- `git diff --check` — passed.
- Producer-qualified vendor check using `--producer runtime-producer` failed because that checkout is absent.
- No pytest bodies rerun; prior 0048 RED retained. Retry/stale/foreign/forged/modified-candidate controls remain unverified. Lint/type comparison is inapplicable without changes.

Wrote `BLOCKED` and the requested `commit-msg`; no `DONE`. Recommend resolving the fixture allowance before implementation.