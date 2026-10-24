# Farm Codex handoff: OPS-farm-agent-full-v2

Source review only; this author pass authorizes no live operation. A packet
PASS is not Farm READY. The 0555 checkpoint remains Agent `9cd3dbe8` / tree
`57f0231d`, Runtime `45c3`: 288 failed, 17,335 passed, 187 setup errors,
4 skipped, no JUnit. Only 281 failed node lines exist; seven are unaccounted.

After independent source review, the normal Farm Codex installer must obtain
these **actual inputs** before the command below:

- Current registry bytes/hash, the existing single `agent full-farm` row and
  original `agent full` row; current Store owner/index and managed registration.
  The 0423 baseline is historical, never a replacement for current bytes.
- Normal checkout receipts: tested Agent `9cd3dbe865a941c052bda04ae0d61306d18f8f26`
  / tree `57f0231da0d7904ecd8778169973d6384e0ae141`, and clean Runtime
  `1d9ddba546f8fb1300f55ff62607ed492719cbaa` / tree
  `f56c396c4495547680b46e832565278d2c375e69`. Verify actual SHA/tree/clean
  status with read-only Git commands. Runtime `45c3` lacks D40; do not use it.
- Normal maker receipt for `agent-remotion-farm-v2-9cd`: exact requested Agent
  and Runtime SHAs, build origin, managed entry/key/path, approved
  `remotion-env-nodes` template, verified graph, lock, Node v20.19.4/npm 10.8.2.
  Authentic reuse is allowed. No invented path, legacy adoption, source overlay,
  tuple adoption, manual maker, or reinitialization. README has the supported
  later requests. Receipt facts are still missing; refuse publication until supplied.
- Preserve the Agent's declared `45c3` lock and all four canonical client hashes
  in `runtime-source-selection.json`. Selecting existing reviewed Runtime code
  does not change that declaration. Require actual subprocess module origins.

The single installer command below renders literal authenticated paths and
replaces one existing row. Fill its two angle-bracket arguments only from
those verified inputs. `pre-full-farm.suites.conf` must be a private copy of the
**fresh post-maker** registry, reviewed against the pre-maker snapshot; only
normal maker projections may have changed. Use private `$TMPDIR` for backups.
Verify `sha256sum -c ops-handoff/farm-agent-full-v2/MANIFEST.sha256` from the
packet checkout before invoking it. No helper is installed.

```bash
python3 -B -I - "$ORCH" /home/user/work/bench-store \
  "$PWD/ops-handoff/farm-agent-full-v2" \
  '<receipt-managed-profile>' '<authenticated-Runtime-checkout>' \
  "$TMPDIR/pre-full-farm.suites.conf" "$TMPDIR" <<'PY'
from datetime import datetime, timezone
import hashlib
import importlib.util
import os
from pathlib import Path
import re
import sys

orch, root, packet, profile, runtime, baseline_file, backups = map(Path, sys.argv[1:])
source = orch / 'bin/bench_store.py'
assert hashlib.sha256(source.read_bytes()).hexdigest() == '6d9368207947aa316e1ed6486c5fa7ef843a84f50163114bb958011b538712a8', 'Store source drift'
spec = importlib.util.spec_from_file_location('bench_store', source)
api = importlib.util.module_from_spec(spec)
spec.loader.exec_module(api)
# Open only. A missing, partial, replaced or symlinked Store is a refusal.
store = api.Store(root, orch / 'tests')
name = 'agent-remotion-farm-v2-9cd'
assert store.registered(name), 'normal managed registration missing'
entries = store.registration_entries(name)
for path in (profile, runtime):
    assert re.fullmatch(r'/[A-Za-z0-9_./-]+', str(path)) and path == path.resolve() and path.is_dir(), 'physical receipt path required'
assert any(Path(e['path']) == profile and e['component'] == 'runtime' for e in entries), 'profile differs from managed entry'
assert hashlib.sha256((runtime / 'runtime_protocol/external_pack_sources.py').read_bytes()).hexdigest() == '8931d2ae530ff1d6eccbb28dadec4349641fd4e1c19f231dba2616b93be2234e', 'Runtime D40 source mismatch'
row = (packet / 'registration-row.txt').read_text()
assert row.endswith('\n') and row.count('\n') == 1
row = row.replace('@MANAGED_PROFILE@', str(profile)).replace('@RUNTIME_CHECKOUT@', str(runtime))
assert '@MANAGED_PROFILE@' not in row and '@RUNTIME_CHECKOUT@' not in row
candidate = row.encode()
baseline = baseline_file.read_bytes()
full = b'agent       full              /home/user/work/venv-agent/bin/python -m pytest -q -n 3\n'
rows = baseline.splitlines(keepends=True)
assert rows.count(full) == 1, 'original agent full changed'
old = [r for r in rows if r.split(None, 2)[:2] == [b'agent', b'full-farm']]
assert len(old) == 1 and old[0].endswith(b'\n'), 'exactly one full-farm row required'
position = rows.index(old[0])
prefix, suffix = b''.join(rows[:position]), b''.join(rows[position + 1:])
post = prefix + candidate + suffix
assert baseline == prefix + old[0] + suffix
suites = orch / 'tests/suites.conf'
backup = backups / ('suites-' + datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S.%fZ') + '.conf')
with store.mutex():
    assert suites.read_bytes() == baseline, 'registry drift'
    with backup.open('xb') as stream:
        stream.write(baseline)
        stream.flush()
        os.fsync(stream.fileno())
    api.sync_dir(backups)
    try:
        api.atomic(suites, post.decode())
        assert suites.read_bytes() == post, 'atomic replacement differs'
    except BaseException:
        if suites.read_bytes() == post:
            api.atomic(suites, baseline.decode())
        raise
try:
    assert store.registered(name)
    assert store.registration_entries(name) == entries
    raw = candidate.decode().split(None, 2)[2].rstrip('\n')
    assert name in store.names_for_suite('agent', 'full-farm', raw)
except BaseException:
    with store.mutex():
        if suites.read_bytes() == post:
            api.atomic(suites, baseline.decode())
    raise
print('backup=' + str(backup))
print('pre_sha256=' + hashlib.sha256(baseline).hexdigest())
print('post_sha256=' + hashlib.sha256(post).hexdigest())
print('replaced=' + repr(old[0]))
print('row=' + repr(candidate))
print('outside_bytes=unchanged; source packet installed, Farm preflight still required')
PY
```

The rendered row carries `PATH`, `ASTRID_REMOTION_PROJECT_DIR`,
`ASTRID_TEST_NODE_MODULES=<managed-profile>/node_modules`,
`ASTRID_NODE_EXECUTABLE`, `ASTRID_TIMELINE_SCHEMA_PYTHONPATH`,
`ASTRID_RUNTIME_CHECKOUT`, and `PYTHONPATH="$PWD:<Runtime-checkout>"`, plus
HOME/LANG/LC_ALL/PYTHONDONTWRITEBYTECODE. `$PWD` is the production Agent
snapshot, not an ambient source fallback. There is no receipt environment
variable to inject into the service. `env -i` discards inherited overrides.
Before pytest it checks actual Node/npm versions, profile peer files and Node
imports, Python imports/origins, D40 source bytes, declared lock and client
hashes. Normal maker authentication remains required for the complete graph.

Return exact rendered row and pre/post hashes, backup, outside-byte comparison,
Store public validation, normal receipts and actual sources/origins. Stop on
any refusal or permission denial. Rollback restores only this row replacement
and only while registry bytes still equal this command's post-image; concurrent
changes must be returned for recovery, never overwritten. Do not restore
owner/index or initialize a Store. No full suite is authorized by this brief.

The production caller is installed `ORCH/bin/test-run`, invoked by the normal
dispatcher. It selects `agent full-farm` with its line-15 awk command, then
`Store.names_for_suite` and `Store.acquire` (lines 66, 70–73); the unmanaged
row leases all normal registrations. It runs the row from the Agent snapshot.
Only later, after genuine Farm preflight, may the manager request the one
checkpoint through the existing service. No alternate wrapper or ledger.
