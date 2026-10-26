# D141 REG upgrade independent review findings

## Verdict

FAIL for the exact requested target identity; PASS for the actual checked-out author source.

The brief names immutable commit `012889c1b0bbfe5f290f757cb6d31dd7d995ccc6`. That object is absent. The worktree HEAD is `012889c1b0bbfe5f290f757cb6d31dd7d995ccc7`, with the expected Runtime6a parent, subject, tree, and one-file delta. This is the only blocking finding.

## D141-REG-IDENTITY-001 — blocking, reproduced

`git cat-file -e 012889c1b0bbfe5f290f757cb6d31dd7d995ccc6^{commit}` fails. `git rev-parse HEAD` returns `012889c1b0bbfe5f290f757cb6d31dd7d995ccc7`. The review therefore cannot truthfully certify c6. The orchestrator should confirm/correct the intended hash and rerun only the identity check if c7 is intended.

## Actual c7 source review — no source finding

The actual commit changes only `runtime_protocol/upgrade.py`: it imports `threading`, assigns the staged inspector `db_path` to `root / "realm.sqlite3"`, and assigns a fresh `threading.RLock()`. Those fields match `RealmStore.__init__` and the existing staged-inspector construction in `RealmStore.inspect_realm`. `_integrity_report` still performs quick SQLite, foreign-key, schema-v32, realm identity, CAS, event, relational and timeline-history checks; WAL checkpoint, activation, and rollback code are unchanged.

The production operator caller invokes `upgrade_realm` for v23 realms. The retained P5 commit/crash path invokes `migrate_canonical_to_current`, which does not call `_validate_candidate`; no P5 receipt was retargeted and no new-head P5 proof is claimed.

The full C0v2 wire surface (base pair, commands, label, steps/per-step patch, reads, fields/atomic merge, idempotency, dry-run/source; accepted/merged/conflict/invalid/preview replies; canonical closure, authenticated receipt bindings/effects/dependencies/history/guarded undo; conflict reason/head; invalid code/path/hint/suggested command; preview no mutation) is unchanged because all contract, client, metadata, conformance, and test blobs outside the prescribed source file match Runtime6a011d58.

