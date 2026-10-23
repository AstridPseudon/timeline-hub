# Runtime OPS-retire-venv-v2 — staged guarded retirement extension

Status: **PASS for staged private qualification; not installed or published.**

This packet extends the existing `request-retire-venv` → `RETIREVENV` FIFO
dispatcher branch → `retire-child-venv` route. The installed request and
dispatcher remain untouched; the staged dispatcher is byte-identical to the
previous packet. No Runtime source, product test, schema, generated file, pin,
daemon, production venv, or remote/main path was modified.

## Staged files

All staged artifacts are under:

`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-OPS-retire-venv-v2-1722/`

- `evidence/kit/retire-child-venv` — extended handler.
- `evidence/kit/request-retire-venv` — accepts completed names and explicit
  `.partial.*`/source leftover names; queue payload remains `RETIREVENV NAME`.
- `evidence/kit/dispatcher-daemon` — unchanged FIFO branch.
- `fixtures/test_retire_guard_v2.py` — private fixture-only acceptance cases.
- `evidence/retire-child-venv.patch` — flat handler delta from the reviewed
  `a5beb33d` packet.
- `evidence/hashmanifest.txt` — exact staged hashes.
- `evidence/{prior37guard,prior7unit,callshape,private-fixture}.log` — test
  outputs.

Staged hashes:

```text
f18bc20b23010dc47a6891d4ef7a357da5991a620b83b5cdc67e0c8741892c15  dispatcher-daemon
6430c093cb219fb1d20dfc22cc34e96fb86d3031152fabf14c24962332fffa1d  request-retire-venv
a72acde6dd440d2e196a29f109bd532c4c00d3dd713680393ad18bb181583b8b  retire-child-venv
```

## Settled behavior implemented

- A completed owned name can retire itself and stale associated
  `NAME.partial.*` and `.child-venv-source-NAME-*` directories. Old stale
  sources are retired; source existence alone is not considered active
  custody. A young partial remains a fail-closed builder/live-window refusal;
  a young source is observed and retained. An explicit partial request must
  itself be older than one hour.
- An explicit partial name is supported by the same request shape. Source
  names use the maker's exact timestamp/random form when directly addressed;
  ambiguous broad source names are refused unless a unique direct owned base
  resolves them. Malformed, foreign, symlinked, non-directory, and escaping
  candidates refuse.
- Completed venvs with both valid tuple markers retain the existing identity
  checks. Markerless old venvs are eligible only when their exact
  `venv-agent-child-[a-z0-9][a-z0-9-]*` grammar matches. If either marker is
  present, both must be readable lowercase-hex identities; incomplete or
  corrupt pairs refuse.
- Current suites/env files, pending requests, running worker metadata/brief/env,
  and every target/associated candidate are scanned for both literal and
  canonical references. Process scans cover cmdline, exe, cwd, and fd paths.
  An unreadable cmdline refuses; a nonempty cmdline with unreadable exe
  refuses. A verified empty cmdline plus unreadable exe is treated as a
  non-user kernel thread. No zombie/PID guess is used, and no argv/key data is
  printed.
- Age and all candidate fingerprints are checked twice, with final canonical
  containment/inode/mtime/size checks before bounded removal. The private
  process-table seam defaults to `/proc` and is only used by fixtures.
- Logs include each candidate's exact name, case, and disposition without
  printing process arguments or secret data.

## Evidence

Commands and exits:

```text
bash -n evidence/kit/dispatcher-daemon evidence/kit/request-retire-venv evidence/kit/retire-child-venv — 0
prior independent guard matrix (37 cases) — 0, pass=37 fail=0
prior Python guard controls (7 tests) — 0, 7 passed
private fixture matrix — 0, 13 passed
request → actual dispatcher branch → handler shape controls — 0, pass=3 fail=0
git diff --check (Runtime worktree) — 0; worktree remained clean
```

The prior 37-case fixture uses a young source custody directory; under the
settled ruling it remains retained while the old completed target retires.
Its young partial case still refuses. The new fixture covers stale partial and
source positives, young/live builder, reference, private cwd/fd, pending and
running negatives, empty-cmdline/unreadable-exe positive, nonempty and
unreadable-cmdline negatives, markerless old positive, wrong-name/corrupt
marker negatives, source-before-partial live window, symlink refusal, bounded
race controls, and real request/dispatcher smoke using throwaway names.

Not run: production cleanup, daemon invocation, provisioning, host install,
atomic publication, normal publish, full Runtime suite, or any live/remote
cleanup. Independent Luna review and host-owned installation/smoke remain
separate gates.
