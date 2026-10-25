# D139 private retirement candidate

The candidate is deliberately private until an independent review and an
atomic backup/CAS installation.  `retire_entry.py` is the only manager-facing
wrapper.  It accepts one exact `entry` and one owner-bound authorization JSON;
there is no force or age-only option.

Future manager shape (fixture-only until installed):

```sh
python3 ops-d131/retire_entry.py \
  --root /home/user/work/bench-store \
  --tests-dir /home/user/work/tests \
  --entry child-<64-hex-key> \
  --authorization /path/to/owner-retirement-audit.json \
  --now 2026-10-25T22:24:50Z
```

The authorization binds owner, identity, path, entry and lease in the existing
Store index, and records the one-hour `registered_at`/`not_before` guard plus
empty process, cwd, fd, command, registration, suite, worker and queue
reference sets.  Store rechecks those guards, takes the existing exclusive
lease, and uses the normal journal/projection/index/recovery route for one
victim.  No live Store, entry, suite or registration is touched by this
candidate.

`check-cas.sh` is a read-only preflight for the expected installed-source
preimage `123bb93c1f2e3d6bd23c21e50cc8445afc8853e5e659759cd30dcaa53b7adfe2`
and mode `0755`; it performs no backup, install, Store operation or cleanup.
