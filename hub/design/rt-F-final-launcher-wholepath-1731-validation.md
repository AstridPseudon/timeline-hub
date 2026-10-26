# Validation

All checks were read-only or source-only controls. No repository suite was run;
the brief forbids real builder, dry-run, clone, service, collection, and 33-run
operations.

1. `sha256sum` and `stat` over the candidate closure — PASS. All eleven
   manifest files matched their recorded hashes and modes; all were regular
   non-symlink files owned by UID/GID 0. Candidate rows were SHA
   `251dc228...`; caller, lifecycle, wrapper, builder and inventory pins
   matched the manifest.
2. Tuple materialization audit — PASS as an observation. Both concrete tuple
   files exist, are regular non-symlinks mode 0644, and hash to `90b9da11...`
   and `eec63978...`. Their four roots matched recorded heads and trees; all
   four source worktrees were clean at read time.
3. Actual registry audit — PASS as an observation. The file is regular,
   non-symlink, mode 0600, SHA
   `0495919f9ab694d034ca53d77877c90d5553560ac3bbcbf7e90e8b268e227e15`.
4. Read-only row parser/comparator over actual registry, 1719 successor, and
   current source11 successor — PASS; it found F1/F2 and confirmed the current
   dry-run row has all reviewed required arguments.
5. `PYTHONDONTWRITEBYTECODE=1 python3 candidate/install-final-services.py --help`
   — PASS; CLI shape was recorded without side effects.
6. Exact no-install CLI against the immutable actual registry — expected FAIL
   at the stale declared registry preimage:

   ```text
   PYTHONDONTWRITEBYTECODE=1 python3 candidate/install-final-services.py --registry /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/tests/suites.conf --candidate candidate/runtime-final-service-rows.txt --builder /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/delivery-build
   ValueError: predecessor registry hash mismatch: 0495919f... != 7b1ffdd7...
   ```

7. `PYTHONDONTWRITEBYTECODE=1 python3 candidate/receiving_controls.py` —
   expected FAIL at its first registry-hash assertion for the same stale
   installer constant; it did not reach its monkeypatched private install.
8. Real available-byte sampler — PASS: two samples five seconds apart,
   available bytes remained above 4 GiB, sampler PID 3 exited 0, and the
   owning shell waited/reaped it. Full trace is in `disk-trace.txt`.

Not run: source-positive clone harness, real builder, dry-run body, service
request, canonical installation, ZIP, product tests, full suites, or any
cleanup/repair.
