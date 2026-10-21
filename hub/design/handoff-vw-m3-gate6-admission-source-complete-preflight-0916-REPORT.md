# Gate6 admission-source preflight — 0916

## Result

**FAIL CLOSED before source validation.** The one registered central
preflight ran once and stopped because the harness-committed source was not
present at the exact operational checkout path:

`/home/user/work/wt/vw-m3-gate6-admission-only-reviewed-source-0914`

The harness commit is present and verified:

- commit: `0d4323913b92c4e0e3830bf14ec7f35d981475ca`
- tree: `5a1e0e85d0f336f642426b91ccf3b3f1984ebd14`
- parent: `d00a66134f330672ea7471dc69db38c1566d94cf`
- one-line App source fingerprint: `5902` files,
  `sha256:4fb1e53b2dce325f826b6b071d0782544e5ba2c7b27418b6170f8c947c450435`

The source fingerprint was derived from the frozen d00 checkout by replacing
only `cases.ts:91`; `cases.ts:159` remained unchanged. It was not fabricated
from the old d00 fingerprint.

## Packet and command

Fresh packet:

`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-gate6-admission-source-complete-preflight-0916/packet`

The packet was copied from the immutable 0845 device/inode donor and changed
only for the new namespace `gate6-20261021T0916`, the exact 0914 source
commit/tree/fingerprint, and the admission-only approval reference. Donor
hashes and the 0845 consumed namespace were not changed.

Registered command (exact flat command, no outer flock):

```text
composition e2e-viewing-gate6-admission-source-complete-preflight-0916 bash /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-gate6-admission-source-complete-preflight-0916/packet/run.sh --preflight
```

Central request/result:

`vw-m3-gate6-admission-source-complete-preflight-0916-e2e-viewing-gate6-admission-source-complete-preflight-0916-1021091955-1898`

Result: exit `1`; `run.sh` static checks passed, then `preflight.sh` failed
at its `cd` into the missing exact App checkout. The actual central log is:

`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/tests/vw-m3-gate6-admission-source-complete-preflight-0916-e2e-viewing-gate6-admission-source-complete-preflight-0916-1021091955-1898/log.txt`

Central observed free bytes `11942588416`, above the required floor
`10737418240` and staging threshold `11320247244`; `owned_bytes=50683`.
The child short-temp root was cleaned successfully. No source ancestry,
build-input/dist provenance, GET200, case-list, graph, or source-content
assertion was claimed because the source path failed before those checks.

No physical request, issue step, token, grant, marker, Runtime, helper, or
browser was started. No retry was made.

## Static evidence

- Bash syntax, Node `--check`, Python AST parse, and packet checksum checks
  were included in the central run and passed.
- `PYTHONDONTWRITEBYTECODE=1 python3 -B packet/short-player-temp-controls.py --self-test` — PASS;
  188-byte historical witness, 107-byte short bound, inode replacement
  refusal, ownership/mode/symlink-root controls, and safe symlink-leaf cleanup.
- The central log records the exact single lock as fd9 owned by `run.sh`.
- Donor 0845 `run.sh` and `issue.mjs` hashes remain
  `7e4d5bee57d5ce68f060b0ab2d7d8485cbbc7ce6200a3a346eb88f93b75d0d1f` and
  `b95508e9dccf24bb57a6ed93b228effe392aa7db8f61d54c1e5d2f2b2802f141`.

## Blocker / next step

The exact committed source checkout must be materialized by the harness or
orchestrator at the path above (or the packet must be explicitly redirected
to an authorized exact checkout). Then a new worker authorization is needed
for any future preflight; this worker did not retry after the fail-closed
result.
