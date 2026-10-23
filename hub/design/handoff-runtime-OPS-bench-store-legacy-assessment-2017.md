# Runtime OPS-bench-store legacy assessment — exact-seven disposition

## Result

**No existing safe normal operation.** The installed store cannot own or unregister the exact seven historical App2 registrations. Keep them STOPPED; retain the P-OPS-registration `blocked:runtime` status. This is an intentional `NO legacy adoption` scope boundary, not an ordinary source defect and not a true permission/safety refusal.

The reviewed exact-seven proposal is still proposal-only:

- patch SHA-256: `5984d485a2840c780c00a6461e3d6cb98462cef21428e8a9bbc233d18bf18b6a`
- source manifest SHA-256: `acb5cf9d2e4f989650e9dfd6eba98f53e89d45db835eeafad1f693091f777678`
- flat evidence manifest SHA-256: `1669d66fd9177d45d8dd515e700c3c6f804f13eedbfc596efcdad6da6691c4ac`
- independent review: PASS for proposal scope, NO-GO for live operation; host process/daemon/lease idleness is UNKNOWN by design

## Exact rows, paths, and key collision

The target is seven `agent <name>-nodes` rows in `ORCH/tests/suites.conf` plus `ORCH/tests/<name>.env`:

| name | legacy runtime path | Agent SHA / Runtime SHA |
|---|---|---|
| `agent-remotion-ap2-p1-f611-1346` | `/home/user/work/runtimes/agent-remotion-ap2-p1-f611-1346` | `f6116e1b658514021cbbf08d5a6f16a240523f1a` / `8592822fd11275540f596562f43c715676f2bc0f` |
| `agent-remotion-ap2-current-8c355-1402` | `/home/user/work/runtimes/agent-remotion-ap2-current-8c355-1402` | `8c355a48e4cc2a8ec9d5ed6873a585d2540a2dbe` / `8592822fd11275540f596562f43c715676f2bc0f` |
| `agent-remotion-ap2-current-8c-cfa-1415` | `/home/user/work/runtimes/agent-remotion-ap2-current-8c-cfa-1415` | `8c355a48e4cc2a8ec9d5ed6873a585d2540a2dbe` / `cfa0af0d476e6954df041c08d7ef378fd6782932` |
| `agent-remotion-ap2-current-583-cfa-1451` | `/home/user/work/runtimes/agent-remotion-ap2-current-583-cfa-1451` | `58316fd6e0ce8a1fb3b2b3826ec71906d29080de` / `cfa0af0d476e6954df041c08d7ef378fd6782932` |
| `agent-remotion-ap2-current-583-9ce-1513` | `/home/user/work/runtimes/agent-remotion-ap2-current-583-9ce-1513` | `58316fd6e0ce8a1fb3b2b3826ec71906d29080de` / `9ce4242bc01f100bab9efc51032a73985cefb2b2` |
| `agent-remotion-ap2-current-98ef-259-1608` | `/home/user/work/runtimes/agent-remotion-ap2-current-98ef-259-1608` | `98ef2f9c95fd43d88cca2909d8d1518302e3050c` / `2593942dfbbbe1d70bb6e776f811285deb2ab18b` |
| `agent-remotion-ap2-current-bac-d9e-1643` | `/home/user/work/runtimes/agent-remotion-ap2-current-bac-d9e-1643` | `bac094180aef38a77b86ab165962e6159f873c60` / `d9e2a71e87c827290a3ff58a94f6fb8b4bc11e0b` |

All seven resolve to the same Remotion tree `b01dca9b3b24f54093c20b7c5657316f997725db` and therefore the same current `runtime_key`:

`5ca5c561b7be7069051ac8769432cc1edf29060bed39384cd3c4ecab1736e690`.

That collision is not an idle claim. It shows why the existing one-entry-per-key store cannot preserve seven distinct legacy paths and their historical source/report provenance as managed entries.

## Source-backed API conclusion

The installed `bench_store.py` has `Store.ensure`, `acquire`, `recover`, and automatic `_evict`; it has no registration import/unregister/adopt/migrate/retire API. `initialize` refuses existing roots; `ensure` only creates/reuses store-owned `root/entries/<key>` paths, requires the store owner marker, and projects suite/env/report bytes only for managed registrations. `_evict` removes only indexed entries after lock acquisition. The CLI is only `recover`, `key`, and `run`.

The production route is therefore creation/reuse only: request → dispatcher → `make-runtime`/`make-child-venv` → `Store.ensure`; `test-run` binds the suite command and holds `Store.acquire` locks through the command. The separate `request-retire-venv`/`retire-child-venv` route is filesystem retirement with reference, process, age, and inode guards; it does not add Store custody or unregister rows.

There is no existing transaction that can preserve all outside/current bytes and the seven exact path/env/report identities while removing only the seven rows/envs. No live operation was attempted.

## Smallest missing seam and host-only boundary

If this legacy relief is made an acceptance requirement, Runtime must own a narrow migration seam: import/adopt (or explicitly move) existing entries under Store ownership with per-target identity/path/inode, owner marker, immutable report/registration bytes, lock/lease checks, and one atomic seven-row/env projection. Fixtures must cover outside-byte preservation, same-final-path report custody, shared-key handling, foreign/symlink/race/active-lease refusal, crash recovery, and protected current `079`/P1/P2/P3/F/template bytes. This is new source/API plus fixtures and a contract/scope decision; it is not a defect in the installed creation store.

The only genuinely host-only evidence needed for any later live migration/retirement is a fresh normal activity/lease check over current suite/env bytes, pending/running worker references, process executable/cwd/open-FD references, and the exact target/store locks. The reviewed packet does not provide that authority; absence of metadata is not liveness evidence. Any unknown target remains retained.

For the installed OPS-bench-store lifecycle, this is optional legacy relief: future requests avoid the churn. It is necessary only for the separate P-OPS-registration/whole-lifecycle claim if that row is explicitly included in acceptance. C0v2 request/reply shapes and frozen `34e` remain unchanged; the protected current tuple remains untouched.

## Verification and next action

- Installed live hashes match the reviewed/install receipt: `bench_store.py` `6d936820...`, `test-run` `f599c5ad...`, `make-child-venv` `89d82618...`, `make-runtime` `99cca067...`, `request-child-venv` `72cafb3a...`, `request-runtime` `f13a1d07...`.
- Runtime head `2a9e347ff0e1df1dedff5ab7b59ddb27dfe3129d` is clean; `git diff --check` passed.
- `bash -n` passed for the live callers and retirement helpers; isolated `compile()` passed for `bench_store.py`; AST inspection confirmed the API/CLI conclusion without importing or constructing `Store`.
- No full suite, browser/HTTP run, process scan, Store construction, queue/provisioning, network, config/env/bench/store mutation, cleanup, retry, or reference removal was performed.

Runtime OPS owner should publish this disposition, keep the row blocked, and do no further broad audit/review/install. Only if acceptance is expanded should Runtime author the migration API/fixture seam, then obtain independent review and one host-authorized normal lifecycle run.
