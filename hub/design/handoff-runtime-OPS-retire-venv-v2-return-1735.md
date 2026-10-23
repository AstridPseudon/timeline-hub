# Runtime OPS-retire-venv-v2 return 1735

Status: **PASS — evidence-only staged repair; do not install or merge from this worker.**

The malformed source-name deletion found by independent review 1731 is fixed
in the staged handler and request writer. The actual producer is the read-only
`make-child-venv`: it emits
`.child-venv-source-N-YYYYMMDDTHHMMSSZ-PID.XXXXXX` using `date -u` and
`mktemp ...XXXXXX`. The staged validator requires that exact form, positive
decimal PID, six alphanumeric random characters, and a valid UTC timestamp.
It parses the embedded base exactly; discovered candidates must match that
same base and grammar. No broad source suffix or base-membership fallback
remains.

The exact malformed private counterexample
`.child-venv-source-venv-agent-child-fixture-EVIL` refuses in both entry
points before mutation, even with a completed base present. Valid stale source
names and explicit stale partial behavior remain positive. All prior age,
reference, process/cwd/fd, marker, canonical, fingerprint, race, and bounded
removal guards remain in the staged packet.

## Evidence

- `bash -n` all three staged scripts: exit 0.
- Private fixture: `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s fixtures -p 'test*.py' -v`: exit 0, 17/17.
- Dispatcher: staged file is byte-identical to predecessor/installed
  `f18bc20b23010dc47a6891d4ef7a357da5991a620b83b5cdc67e0c8741892c15`.
- Installed handler/request/dispatcher hashes remained respectively
  `48cac6c7`, `4713b456`, and `f18bc20b` before and after qualification.
- Runtime worktree: `git diff --check` and `git diff --quiet` exit 0; clean.
- Predecessor retained evidence: prior guard 37/37, prior unit 7/7, and
  request → dispatcher → handler 3/3. Their original private harnesses were
  not present for this return, so those logs were preserved rather than
  claimed as a fresh rerun.

## Flat exports

- `handoff-runtime-OPS-retire-venv-v2-return-1735-retire-child-venv.sh`
- `handoff-runtime-OPS-retire-venv-v2-return-1735-request-retire-venv.sh`
- `handoff-runtime-OPS-retire-venv-v2-return-1735-dispatcher-daemon.sh`
- `handoff-runtime-OPS-retire-venv-v2-return-1735-hashmanifest.txt`
- `handoff-runtime-OPS-retire-venv-v2-return-1735-retire-child-venv.patch`
- `handoff-runtime-OPS-retire-venv-v2-return-1735-request-retire-venv.patch`
- `handoff-runtime-OPS-retire-venv-v2-return-1735-dispatcher-daemon.patch` (empty; byte-identical)

The detailed worker report and private logs are under
`workers/rt-OPS-retire-venv-v2-return-1735/`. Required next gate: new
independent Luna review, then host-owned idle/smoke/timestamp-backup/
atomic-install/normal-publication. This worker performed none of those host
actions.
