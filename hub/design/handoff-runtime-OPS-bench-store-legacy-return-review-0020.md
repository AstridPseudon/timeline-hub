## Verdict

- Bounded recovery source: **PASS, bounded/source-only qualification**.
- Actual legacy readiness: **FAIL/BLOCKED/0 GB**. No legacy cleanup or adoption occurred.

## Evidence

Reviewed cumulative `f21dc5fe8cc0435cb5519d41398b90f309984023`, parent `d0324cde63543f065eceb2829539a50469c33869`, tree `92c6c69ef6762b9b677c17e3ba879b5c9aecc75b`.

The production route is proven in normal and `env -i` fixtures:

`request-runtime --recover-store` → `BENCHRECOVER` → sourced production `dispatch_request()` → `Store.recover()`.

No target, force, adoption, cutover, or ownership-stamping input was added.

Residual unqualified safety limits remain:

- Victim-name replacement immediately before final `rmdir` can delete the replacement and return success.
- Replacement after revalidation can cause refusal after projection/index writes.
- Pending-queue directory substitution can redirect the requester write through a symlink.

These are explicit counterexamples in the fixture, not weakened expectations.

## Tests

- `PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-runtime/bin/python ops-bench-store-legacy/test_legacy.py` — **21 passed**: 14 existing plus 7 new adversarial tests.
- Ruff — **passed**.
- In-memory compile — **passed**, 2 Python files.
- `bash -n` requester/dispatcher — **passed**.
- Private baseline patch dry-run, apply, and `cmp` — **passed**, all 3 source files.
- Pyright 1.1.414 — baseline and candidate each retain the same 1 pre-existing diagnostic; **zero new diagnostic identities**.
- `git diff --check` — **passed**.

## Legacy disposition

The exact seven targets remain outside Store ownership:

- Five retain current suite/provision references.
- Both partial runtimes only contain `verify-installed` failure metadata.
- All seven lack authoritative Store ownership/history.
- Existing Store recovery cannot adopt or unregister them.

Missing markers, age, byte matches, empty queues, or flock state do not establish historical quiescence. No supported caller dependency-retirement/admission path exists.

## Integrity

Runtime remains clean at `abd47e68de6d7a36bec8ac4f0f6e0bc01d98d14e`. Installed kit hashes, dispatcher, frozen C0v2/schema/client/pins remain unchanged. Packet hashes:

```text
bench_store.py  630870208ecccf7c0f841483b58fc74bbbbfbbcefec47ca3195092f2d7eba531
test_legacy.py  24aadb004653fb7ae28d4d74d424b95b9ec3b1dc656d656087199638eb2b8fd8
source.patch    f46eb2da7a444cabc79c5bae5ba2e6d7cfa4523ca81c618c8feb4bfde61a8928
```

No tracked files were changed by this review.