# Turso and remote end state: review of the 90:10 plan (§0–§4, §11–§16)

*Heads: Runtime cc7410a1f, Agent a086cc6db, App c85da5427. File:line claims are verified in code. Turso/libSQL claims are marked "inferred" and should be checked.*

## Verdict

Nothing the plan builds now would have to be removed or rebuilt for a remote Turso end state. The commit protocol it finishes is already network-shaped:
- clients generate the idempotency keys;
- a durable ledger with a primary key enforces idempotency (`canonical_schema.py:213-219`);
- rebase is optimistic, in up to 3 tries (Agent `commit.py:1023-1066`);
- the head moves only through a compare-and-set update whose row count is checked (`timeline_commit_store.py:1103-1106`);
- the outbox is IndexedDB in the browser (`commitOutbox.ts:197-202`).

What doesn't fit is the **storage layer the plan builds on**, which is mostly upstream code. Runtime holds one shared `sqlite3` connection behind an in-process lock (`store.py:745,1137-1145`). Each commit runs dozens of separate statements inside one `BEGIN IMMEDIATE`, and their number grows with the number of clips (`timeline_commit_store.py:888-940,1033-1080`). Backup, upgrade and integrity checks work on the database file.

Under reading **(a)**, a local libSQL file next to Runtime, this all works nearly as it is. Under reading **(b)**, where Runtime reaches Turso over the network, every one of those statements becomes a network round trip while the write lock is held. That needs a storage-layer redesign. An *embedded replica* sends writes to the remote primary (inferred), so for commits it behaves like (b).

The localhost door and the loopback-only rules are local by design; remote replaces them. The plan doesn't deepen either if it follows the rules below.

## Table

| Item | Problem for Turso / remote | Now, avoid or later | Cost |
|---|---|---|---|
| **v32 migration (WP1)** | The step itself is plain DDL on a connection (pattern at `upgrade.py:783-796`), which is portable. The framework around it works on files: it opens `root/"realm.sqlite3"`, takes an owner-lock fence, runs `quick_check` and then `VACUUM` (`upgrade.py:948-1007,899-912`). That framework is upstream. | **Now:** write `_apply_v31_to_v32(connection)` as connection-only SQL, with no `executescript` and no file operations. | 0 h |
| **Commit route and idempotency (WP3–WP6)** | Semantics port well (ledger key, head compare-and-set, request-hash binding, `timeline_commit_store.py:33-41`). The implementation doesn't port to (b): reads, validation and per-occurrence inserts all run inside the write transaction (`:893-940,1060-1077`), with every request serialised on one connection under `_mutex`. | **Avoid:** add no new reads or checks inside `accept()`, and never let correctness depend on `_mutex` or the in-process coordinator lock (`timeline_commit_execution.py:28-55`). **Later, (b) only:** batched writes and a connection pool. | 0 h now; days later |
| **Writes a full snapshot on every commit** | Each commit copies all occurrence and dependency rows (`timeline_commit_store.py:1060-1077`) and counts all timeline events (`:1094`). Inferred: Turso bills rows written. | **Later.** WP3's "N moves in one commit" is fine. | — |
| **Restore preflight** | Every `timeline.restore` runs a whole-database `PRAGMA quick_check` with a progress handler (`timeline_commit_port.py:144-146`, `store.py:6102-6120`). Inferred: on Turso this is not available remotely, or is costly. Undo uses `timeline.inverse`, so it is unaffected. | **Avoid:** don't add `integrity_report` to undo or other commit paths. | 0 h |
| **Outbox** | None: browser IndexedDB keyed by realm, actor, project, timeline (`commitOutbox.ts:152`), relative paths, built for a failing network. | Fine | — |
| **Door** | Binds `127.0.0.1` (`door.py:403`), exact loopback `Host` (`:528`); the browser sends no credential (`:539,564`) and the door injects one shared credential from a file (`:584-600`), so all browser users are one actor. Remote needs per-user auth, which replaces the door. | **Avoid:** put WP7 refusals in Runtime handlers (`server.py`), as the plan does, and give the door no new behaviour. **Later:** an auth gateway. | 0 h now |
| **Publisher identity** | Publisher is the authenticated actor (`server.py:306`): per-user once users have their own credentials. | **Avoid:** in product code, tell App and Agent apart by commit metadata, not by a fixed actor name. Tests may use fixed names. | 0 h |
| **Live tests (WP9 tour, three-products)** | Local topology (process restart, CLI subprocess, door audit log file). Fine for development tests. | **Now:** besides §11 rule 3 (addresses come from config), make the zero-old-route proof come from browser network observation plus Runtime's `/commits`, and treat the door audit log as extra evidence. | 0–0.5 h |
| **One-writer test (WP7)** | Its database snapshot uses `iterdump()` and `total_changes` (`test_timeline_legacy_authority.py:69,141`), which only Python's built-in `sqlite3` module provides. Inferred: a libSQL client lacks them. | **Optional now:** a per-table SQL row digest (helper at `upgrade.py:274`). Otherwise later. | 0.5 h |
| **Vendoring and pins (WP2)** | Runtime imports the Agent's executor in-process (`timeline_commit_provider.py:19,70-80`); they deploy together, and pins help. | Fine | — |
| **Delivery (WP11)** | Not tied to a deployment. | Fine | — |
| **Content store and `local_path`** | Blobs on Runtime's disk (`cas.py`); Runtime returns a filesystem path (`service.py:5384`); the renderer reads local files and serves them on localhost (`assets.py:299,339,525`). Under (b), database remote, blobs local: split backups. | **Avoid:** new WP6 or D13 code reads bytes through object routes, not `local_path`. **Later:** object storage. | 0 h now |
| **Loopback-only rules** | Runtime listens only on loopback (`daemon.py:54-57`); the Agent SDK accepts only a loopback Runtime (`workspace_client.py:74-104`); App discovery is loopback-only (`workspaceRuntimeConfig.ts:33-36`), though `VITE_RUNTIME_ORIGIN` takes any origin (`connection.ts:36-48`). | **Avoid:** no new loopback checks. **Later:** relax behind auth. | — |
| **WAL, backup, upgrade, admission** | File-based: WAL required (`store.py:1148-1150`), `conn.backup` (`backup.py:693`), `VACUUM INTO`/`wal_checkpoint` (`upgrade.py:153-216`), admission copies files (`store.py:950-985`). (a) mostly works; under (b) the service's backups replace them (inferred). | **Later** (upstream code) | days, (b) only |
| **Tenancy** | One realm is one database, one content-store directory and one `owner.lock` (`store.py:739,870-880`). That matches Turso's database-per-tenant model (inferred). | Fine. Keep one realm per user per database. | — |
| **Extensions, triggers, functions, ATTACH** | None found. JSON1 functions are used; libSQL supports them (inferred). | Fine | — |

## Top recommendations

1. **Pick between (a) and (b) on paper; it costs nothing now.** The cheap end state is (a): Runtime and Agent on one remote machine, Runtime owning a local libSQL file, Turso for replication and backup. Under (b), and under embedded replicas, the per-statement round trips inside `BEGIN IMMEDIATE` force a rewrite of the storage layer. "Turso" also names the Rust rewrite, which has MVCC and `BEGIN CONCURRENT` and is still beta. Check its support for savepoints, `json_each` and pragmas before choosing it.
2. **Write the v32 step as SQL on a connection only:** no `executescript`, no file access, no `VACUUM`.
3. **Add two design rules next to §11:**
   - commit correctness comes only from the ledger primary key and the head compare-and-set, never from `_mutex` or the coordinator lock, so no new work goes inside `accept()`;
   - new code gets media bytes through object routes, never `local_path`.

   Both hold today; stating them keeps it so.
4. **Make the live suite's zero-old-route proof come from browser network observation and Runtime's `/commits`,** with the door audit log as extra evidence only. Optionally, swap `iterdump()` for a per-table row digest in the WP7 test (0.5 h).
5. **Qualify §14.** "The save design works unchanged" is true of the protocol. Under (b) it is not true of the storage layer: latency there is per SQL statement, not per request. Add this table to the separate cloud note (§16 A12) instead of the work order.
