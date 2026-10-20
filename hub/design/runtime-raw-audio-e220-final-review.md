# Runtime raw-audio e220 exact review

## Decision

**APPROVE** for the exact immutable e220 commit.

Reviewed commit `e220670e40e196fb8f37dd8ce5d558fe0f6adf1c`, tree
`6f802e315a7a447fa8d8245bf6f30963da6bb4f2`. This is the requested e220
tree, not `89fb7dcd113023d7e1e044d537202caca509830a` and not a mutable branch
checkout. The e220 parent is `89fb7dc`; the current review base is
`6ab3243972f8dc49105819e6d7ba7aef1a2888b8`.

The earlier `runtime-raw-audio-single-fd-final-review.md` rejected `89fb`
because it still verified one descriptor and reopened the CAS pathname for
WAV parsing. That rejection is valid for `89fb`, but is explicitly not proof
against, or a review of, the e220 fix.

## Findings

- `MediaReads.media_info` now opens the CAS object once, calls the existing
  bounded `_verify_open_file` helper on that descriptor, rewinds the same
  descriptor, and parses the WAV header from it. It then verifies the same
  descriptor again in `finally`, so a parse failure cannot bypass the
  post-parse integrity check.
- `_verify_open_file` checks regular-file status, catalog size, chunked SHA-256,
  and before/after descriptor identity (`st_dev`, `st_ino`, `st_size`,
  `st_mtime_ns`, `st_ctime_ns`). It does not reopen the pathname or use a
  whole-file memory buffer.
- Atomic pathname replacement after the first verification leaves the already
  opened original inode authoritative; the post-parse check deliberately does
  not compare the pathname's ctime. Same-inode/in-place mutation changes the
  descriptor hash or identity and raises `ConflictError` before metadata is
  returned.
- The request-scoped `media_info` memo remains unchanged: exact base-closure
  pin validation precedes memo lookup, and acceptance rechecks every consumed
  raw-media capture. The accepted-retry path remains ledger-first and avoids
  invoking `media_info` again.
- The e220 diff from `89fb` is limited to
  `runtime_protocol/timeline_commit_port.py` and
  `tests/test_timeline_raw_audio_port.py`. No public route, generated DTO,
  schema/manifest, ABI/version, or inline duration/table contract changed.

## Decisive race evidence

The old `89fb` tree was archived into a private temporary directory and probed
without changing its source. A hook called the real
`_verify_child_object_bytes`, then atomically replaced the CAS pathname with a
two-second WAV before the old `cas.open` call. The old tree returned
`old_tree_observed_duration=2.0`, reproducing the rejected pathname-reopen
race.

The e220 race test calls the real `_verify_open_file` before injecting the
storage change, so it is not a hash shim. Its two cases pass: rename returns
the original one-second duration from the already-open descriptor; in-place
same-size header corruption raises the expected hash/size conflict.

## Tests

All commands below ran against a temporary `git archive` of the exact e220
commit, using `/home/user/work/venv-runtime`; no source files in this review
worktree were modified. The `target=$(mktemp ...)` setup was repeated for
each lane, with the archive removed afterward:

```text
target=$(mktemp -d /tmp/runtime-e220-review.XXXXXX)
git archive e220670e40e196fb8f37dd8ce5d558fe0f6adf1c | tar -x -C "$target"
cd "$target"
PYTHONPATH="$target" /home/user/work/venv-runtime/bin/python -m pytest -q tests/test_timeline_raw_audio_port.py
```

Result: **7 passed**.

```text
PYTHONPATH="$target" /home/user/work/venv-runtime/bin/python -m pytest -q tests/test_timeline_raw_audio_port.py -k storage_race
```

Result: **2 passed, 5 deselected**.

```text
PYTHONPATH="$target" /home/user/work/venv-runtime/bin/python -m pytest -q tests/test_timeline_commit_port.py
```

Result: **35 passed**.

```text
PYTHONPATH="$target" /home/user/work/venv-runtime/bin/python -m pytest -q tests/test_timeline_raw_audio_port.py tests/test_timeline_commit_contract.py
```

Result: **36 passed**.

- The 35 commit-port tests plus the 36 raw-audio/contract tests provide the requested **71 neighboring tests** (the raw-audio file is intentionally included in the second lane).
- `PYTHONPATH="$target" /home/user/work/venv-runtime/bin/python -m py_compile runtime_protocol/timeline_commit.py runtime_protocol/timeline_commit_port.py tests/test_timeline_raw_audio_port.py` — **passed**.
- `git diff --check 89fb7dcd113023d7e1e044d537202caca509830a e220670e40e196fb8f37dd8ce5d558fe0f6adf1c` — **passed**.

No full, broad, browser, live-socket, or central test suite was run. Native
legacy-trim qualification against the actual paired Agent/Runtime remains
open and is outside this Runtime-only review.

## Private Agent handoff remains unchanged

```text
RequestCommitPort.media_info(pin: {
  "media_id": "sha256:<64 lowercase hex>",
  "content_digest": "sha256:<same digest>"
}) -> {
  "object_id": "sha256:<same digest>",
  "media_type": <managed object media type>,
  "size": <catalog byte size>,
  "duration_seconds": <finite positive WAV-header duration, omitted when unsupported>
}
```

The Agent adapter must call this only for an exact base-closure `MediaPin`,
preserve visible refusal when the private method is unavailable or metadata is
unsupported, and never forward or persist a caller-supplied duration. No
public contract or ABI change is approved by this review.
