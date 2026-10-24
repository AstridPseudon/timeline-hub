## PASS

The D32 package can publish official **201 closed / 66 open / 267 total** counts.

- Recomputed 267 unique nodes: 201 `proven_passed`, 66 `active_owner`.
- Active owners: Agent 60, Runtime 2, Viewing 4.
- Active family totals reconcile to 66; Rendering-missing-result is correctly 0. All six such nodes are proven passed.
- Exact 59 mapping rows reconcile with the CSV: 30 integrated, 7 H3, 22 inverse. No original mapping members dropped.
- All node and proof records are byte-for-byte unchanged from `1f929a4acb`.
- SHA-256 `05be2296…ba7e5c1` matches both the checksum file and mapping linkage.
- Historical 172/95 and 179/88 counts remain clearly historical.
- Source-copy, D40, track labels, ABA, IMAGE inverse, renderer timeout, and Farm remain uncredited/open.

Commands:

- `cd evidence && sha256sum --check agent-D32-current-node-reconciliation-H30-corrected.sha256` — **OK**
- Independent JSON/CSV/hash/count recomputation — **PASS**
- `git diff --check` and `git diff --check HEAD^ HEAD` — **PASS**
- Worktree — clean

No behavioral/full suites were run, per instructions. The package explicitly does not claim v2 production-caller or wire-contract acceptance; that remains separate follow-up work.