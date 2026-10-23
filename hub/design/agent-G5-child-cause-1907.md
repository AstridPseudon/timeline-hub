# G5 first-return diagnosis — 1907

## Result

No production repair was made. The qualified Agent source remains exactly
`89c38c9355f5d4bcc68597ec74e4729435a7a07a` in the worktree; `git status
--short` and `git diff --stat` were empty.

The prior 1902 `internal_error` was caused by the observer, not Runtime:
`g5_preflight_observer.py:410` called `_event(service, project, timeline,
request=body)` without the required `name` argument. The actual Runtime
server traceback captured before public error conversion is:

```text
TypeError: _event() missing 1 required positional argument: 'name'
  ... g5_preflight_observer.py:410 in service_commit
  ... runtime_protocol/server.py:311 in _timeline_commit
```

The causal owner is the 1848/1902 observational harness. Runtime never
reached the provider/commit path for that request; assigning that failure to
Runtime would be incorrect.

I isolated the compatibility fix in my own external shim
(`evidence/g5_corrected_observer.py`), leaving the other worker's observer
untouched. The child hook also received a final nonsemantic guard for a
module-level `__qualname__` lookup; no product or test file was changed.

## One bounded corrected run

The permitted single node was run once, with the unchanged test body and
exact Runtime/source/archive requested by the brief:

```text
HOOK=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-G5-child-cause-1907/evidence/hook
OBS=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-G5-four-preflight-1848/evidence
EVID=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-G5-child-cause-1907/evidence
RTPIN=/home/user/work/wt/rt-pin-2a9e347f
ARCH=/home/user/timeline-hub/hub/design/g5-sdk-authentic-capture-20261023-b6069d1d.tar.gz
env PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 \
ASTRID_RUNTIME_CHECKOUT="$RTPIN" ASTRID_AUTHENTIC_LEGACY_ARCHIVE="$ARCH" \
G5_AGENT_ROOT="$PWD" G5_EVIDENCE_ROOT="$EVID" \
G5_CHILD_OBSERVER_LOG="$EVID/original-corrected.jsonl" \
G5_EXPECTED_AGENT_COMMIT=89c38c9355f5d4bcc68597ec74e4729435a7a07a \
G5_EXPECTED_RUNTIME_COMMIT=d9e2a71e87c827290a3ff58a94f6fb8b4bc11e0b \
PYTHONPATH="$HOOK:$EVID:$OBS:$PWD:$RTPIN" \
/usr/bin/timeout -k 15 720 /home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider \
-p g5_corrected_observer -m integration \
tests/sdk/test_timeline_checkout_history_runtime.py::test_checkout_reload_undo_cli_redo_uses_retained_history
```

Result: **1 failed in 20.73s**, at the first post-commit assertion:

```text
tests/sdk/test_timeline_checkout_history_runtime.py:148
assert restored_basis is not None
```

Both ordinary `TimelineSession.move` commits were accepted. The corrected
capture recorded no seam exception and no `runtime.server.error`; Runtime
provider, port, store, coordinator, and Agent provider entry/exit packets all
completed. Thus this run does **not** reproduce a Runtime `internal_error`.
The next owner boundary is Agent's retained-basis lookup in
`astrid/sdk/timeline_sheet.py:find_version`: the historical lookup returns no
sheet whose `sheet_version` matches the original. This is an Agent history /
historical-basis mismatch to dispatch separately; it is not evidence of a
new Runtime commit bug. No retry, FOUR rerun, undo/redo continuation, or
source repair was made.

## Actual process and source proof

The hook was loaded in the actual Runtime daemon process, not merely the
pytest parent. The corrected durable log records `(pid, ppid) = (3, 2)` and
`argv` inherited from pytest. The hook wrote and fsynced the boot packet
before any test seam packet. Target module origins were the requested Agent
worktree and Runtime checkout; the target source hashes matched their
configured commits in the running process:

| module | origin | source hash matched |
|---|---|---|
| `astrid.sdk.timeline.commit` | `/home/user/work/wt/agt-G5-child-cause-1907/astrid/sdk/timeline/commit.py` | `f777ad0f…` = Agent `89c…` |
| `runtime_protocol.server` | `/home/user/work/wt/rt-pin-2a9e347f/runtime_protocol/server.py` | `aa82d81b…` = Runtime `d9e2…` |
| `runtime_protocol.service` | same Runtime checkout | `267bec1a…` |
| `runtime_protocol.timeline_commit_execution` | same Runtime checkout | `2b0c2567…` |
| `runtime_protocol.timeline_commit_port` | same Runtime checkout | `0d44b5a5…` |
| `runtime_protocol.timeline_commit_provider` | same Runtime checkout | `2dff389a…` |
| `runtime_protocol.timeline_commit_store` | same Runtime checkout | `b1cfdce…` |

The valid log contains 37 rows: one durable `child-boot`, nine wrapper
installations, thirteen seam entries, and thirteen seam exits. The provider
loader's install event was itself lost to the old observer's module
`__qualname__` logging defect, but its `runtime.provider.load` entry/exit
proves the wrapper was installed and reached. The final external hook fixes
that logging-only defect; the bounded test was not rerun.

## Evidence manifest

Evidence is under the worker-owned external directory:

```text
/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-G5-child-cause-1907/evidence/
```

It is 14 MiB, below the 50 MiB limit. `original-valid-node.jsonl` contains the
complete old-observer traceback and source proof. `original-corrected.jsonl`
contains the corrected run. `cases/001..010` plus two validation packets
retain the complete request, prepared availability facts, private original /
landing/history/native/effect/bindings/dependency views where available,
heads, SQL before/after, public replies, and guard state; unavailable fields
remain explicitly marked unavailable. No capped log was substituted for the
case packets.

Important hashes:

```text
archive 2915bd4ac0d46954d19c30f87a517b82074218699978e650fab03fcba81b72d3
corrected durable log 0a5ea1a3bc7c8f7ce78921c1c240e42221f1a6b71141236ca06fd3c1bd74a57a
final child hook faf11c99a22fd6e804806c2892adeac0539bd81a8cd7764ce823433d84da9ef1
```

Credential scan: **0 findings** (`report-all.json` and observer boot).

The exact bounded request, C0 shape/fields, and retained C0 response keys
were not changed: `api_version`, scope/base pair, commands, label, steps,
declared reads, key/idempotency, `dry_run`, source/rationale/group id, and
canonical accepted/merged/full-receipt records remain as in the qualified
source. No Git writes, activation, deletion, pin/schema/environment change,
new seed, DB injection, cache injection, or guard waiver was used.

## Checks

```text
python3 -m py_compile <external hook and corrected observer>  PASS
AST parse of both external observer files                    PASS
git diff --check                                              PASS
git status --short / git diff --stat                          clean
body-lock report-all.json                                     all_match=true
archive SHA256 and credential scan                            PASS / 0 findings
```

No full suite or ratchet was run, per the brief. The 1738 historical
`2 PASS / 2 FAIL` and 1902 historical `1 PASS / 3 FAIL` remain qualified only
as actually observed. The 1902 private capture is not recovered and is not
claimed as recovered here.

## Next step

Dispatch the Agent owner for the `find_version` / retained historical-basis
mismatch using this packet. Keep source `89c…` as draft and keep P1 NO-GO;
do not assign the former `internal_error` to Runtime or activate/merge this
candidate from this report alone.
