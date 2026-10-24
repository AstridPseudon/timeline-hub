Blocked on product media admission; the fixture-plumbing authorisation is clear.

- `publish_authoring_candidate` still calls the retired publisher. Production callers are `sdk/authoring_remote.py:310` and the reserved `sdk/remote.py:1536`.
- `doc.patch` admits media from the authenticated base or `ctx.verified_media` (`_doc_patch.py:310–314`). Existing occurrence media commands require translation-only timing, and `_media_inputs.py:15` rejects audio.
- Runtime’s existing `raw_media_info` requires an exact pin already declared in commands. I found no registered operation that supplies this admission while preserving the required scenario.

**Decision needed:** identify an existing admissible operation, or explicitly authorise a narrow media-input admission operation using the existing authenticated Runtime port. Provider capture would require coordination around the reserved `commit.py:961–988` hunk. I added no API or authority workaround.

Source remains `b61cebe8e0d6e062f15da922f3812d7b6718f12e`, tree `c8b86f253be7ae46a299c1a7e79ac1aaa2b6b8bb`. Changed paths: none. Both original tests remain byte-for-byte unchanged; file SHA-256: `a64ada1d453602527d0a778b5a0e5aab0dda044c70c8eec40ae58f0df6ea8b00`.

Checks passed:

- `PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-agent/bin/python scripts/vendor_lock.py check runtime.lock.json`
- `PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-agent/bin/python scripts/artifact_manifest.py --check`
- `git diff --check`

Runtime is `458595850c354f4403dabc58a72b98bebbc2c3a3`, origin `banodoco/banodoco-workspace-runtime`. Service, commit port, coordinator and store bytes match qualified `abd47e68…`. Frozen R4 refs remain Agent `11caf1d9de29`, Runtime `31c7ac3a00f7`, App `8f0c2484463e`, Composition `c82eb7c459d0`.

Prior 0048 RED retained; no pytest bodies rerun. Retry/stale/foreign/forged/modified-candidate controls remain unverified. Lint/type comparison is inapplicable without changes. Discovery caveat: the artifact script treats `--help` as generation; it rewrote identical bytes, leaving no diff.

Wrote `BLOCKED` and `commit-msg`; no `DONE`.