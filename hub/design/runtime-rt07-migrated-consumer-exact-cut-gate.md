# RT07 migrated-consumer exact-cut gate

Date: 2026-10-21. Result: **BLOCKED / not qualified**.

## Runtime cut inspected

The assigned worktree is clean at Runtime `9cc544add033b7cb6c16a69f6e545053c682aa28`,
tree `e1dd72370defd74e59f021bbe60adb40693526d6`, parent
`95bd3c5f6d00e9bc8cc8cbe5ef510b68ed660f3c`, tree
`d3a290b407fa61e6ab2d476f50c068073f70df00`.

The approved cut changes only `runtime_protocol/service.py`: 53 additions and
120 removals, net -67 lines. `git diff --check` passed and
`PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-runtime/bin/python -m py_compile
runtime_protocol/service.py` passed. No source, schema, client, artifact,
public pin, release, or test changes were made by this worker.

## Dependency result

The dependency did not clear during the requested coordination wait (00:53Z
through 01:22Z):

- Current Agent integration remains `57d6635616f2982b814cfcc059b670ea1a7c9f2c`,
  tree `0174fd49bd175a726a44542d1d6e31bca13c0f02`. Its
  `astrid/core/execution/generic_host.py` still contains
  `_publish_assembled_timeline` and its invocation (observed at lines 8428 and
  9659). The last-caller migration is therefore not in the integrated source.
- Agent staged D13 source `0963d9452ec2a5720ffed834017b28b0a5413c8e`, tree
  `27e62d0797dbc74c1f1753a10b0ac3570e51be73`, removes the hook and restores an
  active native-positive assertion path, but its current central runs remain
  environment-blocked before Runtime admission. The final run
  `...-1021011225-30146` failed in the guarded registry-generator subprocess;
  the D13 report explicitly makes no native transport, Runtime admission,
  requester-outbox, render, decode, or undo claim and keeps the unit HOLD.
- App2’s exact Main014 consumer-neighbor check passed 47 tests across 4 files
  on App `10fa2ff9a8216604aa39e3584f89dc9e7a09080a`, Agent `6efc815...`, and
  Runtime `95bd...`, but it is explicitly offline adoption-only evidence. It
  does not qualify the native bootstrap/activation gate or the D13 replacement.

Consequently, the required active registered-native proof and coordinated
Agent/App/Runtime adoption are absent. The Runtime deletion must remain held;
the endpoint was not retired early.

## Tests and evidence

Run in this worker:

```text
git diff --check HEAD^ HEAD                         PASS
git diff --numstat HEAD^ HEAD -- runtime_protocol/service.py
  53  120 runtime_protocol/service.py
PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-runtime/bin/python -m py_compile runtime_protocol/service.py
  PASS
```

Not run because the migration/adoption gate was not cleared: the narrow
retirement/authentication/no-write Runtime pytest lane and the matched-Agent
replacement acceptance lane. No full suite, browser, MP4/ffprobe, or original
7012 run was repeated. Existing candidate evidence remains historical and is
not relabeled as current adoption.

## Exact next step

Agent must make the D13 native positive pass from the current source through
the existing central environment, including producer guard, requester outbox,
Runtime admission/settlement, lost-ACK/restart exact retry, revision-pinned
render, MP4/ffprobe, and guarded undo. App and Runtime then must adopt the same
cohort. Only after that should Runtime run the narrow current-source refusal,
authentication, no-write, replay, and replacement-neighbor tests, merge the
67-line cut, and let the manager mark RT07 DELETED.
