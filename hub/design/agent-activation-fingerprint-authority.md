# Agent activation fingerprint authority

Status: read-only investigation. No Agent source, schema, DTO, ABI, pin, or test was changed.

## Finding

The normal activation refusal is a real cross-repo lexical mismatch for the same live child, not a PID-reuse finding. Agent's local activation authority is the existing `process_group.process_birth_identity()` helper. On Linux it returns:

```text
<kernel boot UUID>:<decimal /proc/<pid>/stat starttime ticks>
```

There is no literal `boot-id:` prefix; “boot-id:N” here means the boot UUID followed by `:` and the decimal tick value. Runtime currently sends `proc-start-ticks:<decimal ticks>`. The tick suffixes agree, but strict string equality correctly rejects the different encodings.

The Runtime worker's central diagnostic `17275` recorded the same live child as, for example, `proc-start-ticks:7027515` on the Runtime side and `b38142f7-84c5-487d-95a4-8180cbff3972:7027515` on the Agent side. The second child showed the same pattern with tick value `7027562`. See the existing Runtime result report at `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-m2-activation-child-diagnostics-final/report.md` and its `source-identities.json`.

## Agent authority and inputs

- `astrid/core/execution/process_group.py:191-216` is the canonical helper. Linux reads `/proc/<pid>/stat`, splits after the final `)`, rejects `Z` and `X`, reads `/proc/sys/kernel/random/boot_id`, takes `stat_fields[19]`, requires nonempty boot ID and decimal ticks, and returns `boot_id + ":" + start_ticks`. Read/parse failures return the empty token.
- `astrid/core/execution/process_group.py:219-237` builds the exact same token for an unreaped Linux zombie; it is not a relaxed alternate format.
- `astrid/core/execution/process_group.py:72-128` puts that token into the Linux process census. `astrid/sdk/host_bootstrap.py:282-294` obtains the parked-host token from that census, and `astrid/core/execution/generic_host.py:4121-4123` re-exports the same helper.
- The actual activation check is `astrid/core/execution/generic_host.py:13137-13183`: it computes the local token, requires a `{pid,birth_id}` host object, requires the PID to be the current process, and requires exact `host["birth_id"] == actual_birth`. This is the same-incarnation gate; it must remain strict.
- Agent's independent custody observation is deliberately a different seam: `astrid/core/execution/custody_broker.py:1561-1596` uses Darwin native identity or Linux `ps -ww ... lstart`, yielding `ps-lstart:...` on Linux. That observer is not an activation-format fallback and must not be used to make the activation comparison permissive.

## Activation ABI/version

The existing Agent activation envelope remains `v1`:

- `astrid/core/execution/generic_host.py:235-240` defines `runtime.local-worker-activation/v1`, `astrid.local-worker-activation-accepted/v1`, `astrid.local-worker-activation-request/v1`, and `runtime.local-worker-activation-recorded/v1`.
- `astrid/core/execution/generic_host.py:13147-13212` validates those frame versions and carries the host identity as `{pid,birth_id}`. No nested fingerprint version or manifest field exists.
- Direct activation authority tests are in `tests/core/execution/test_generic_host_activation.py:21-75` (same-token request/receipt/ACK) and `:306-336` (wrong birth/PID/version and other stale grants refuse without an ACK).

Runtime's corresponding `v1` path is `runtime_protocol/local_worker.py:31-36`, `runtime_protocol/local_execution_supervisor.py:20-32,1070-1114`, and `runtime_protocol/local_worker_composition.py:184-193,573-616`. Its Linux identity source is `runtime_protocol/platform.py:415-471`: it reads the same `/proc/<pid>/stat` field 19, but formats it as `proc-start-ticks:<ticks>` and does not include `/proc/sys/kernel/random/boot_id`. The activation sender then forwards that exact value at `runtime_protocol/local_execution_supervisor.py:1079-1089` (and the relay path's equivalent). This is the disagreeing side.

## Main/current comparison

- Checked-in upstream Main `origin/main` (`a9a3550c`) already has the Agent helper and format at `astrid/core/execution/process_group.py:190-216`.
- Approved custody commit `19e4abb2` (`fix(execution): bind pidfd exit proof to a retained kernel watch`) and current approved `21413934` have identical `process_group.py` content for the helper (SHA-256 `1234b73f61ee47de14f9006fdd0bf7c8b958da16e9d54ea15ac7fdbe0d4321d2`). Their relevant delta is retained pidfd/epoll exit proof and reused-incarnation handling, not birth-token serialization. Activation versions remain the same `v1` values above.
- The current Agent tree `f711cbd2` differs from upstream Main in `process_group.py` only in the approved retained-pidfd exit-proof and reaped-root/reused-PID handling; the identity helper is unchanged.
- Frozen R4 candidate SDK also uses the same Linux boot-ID-plus-ticks format at `astrid/core/execution/process_group.py:181-207`; it is not the source of Runtime's `proc-start-ticks` value.

The approved kernel work therefore strengthens proof of an exact retained incarnation's exit; it does not make a readable pidfd, a changed PID, or an alternate string format sufficient evidence of that exit or identity.

## Compatibility recommendation

Runtime owns the correction. At the existing local activation `v1` seam, Runtime should emit Agent's already-established canonical token from the same child PID: read `/proc/<pid>/stat` field 19 and `/proc/sys/kernel/random/boot_id`, reject missing/malformed input, and verify the tick value remains stable across the bounded observation. Keep Agent's strict PID-and-token equality, credential/receipt ordering, retained custody, and independent peer checks unchanged. Do not add Agent acceptance of `proc-start-ticks:*`, a caller-format fallback, or a versioned dual-format union. No activation ABI/schema/pin change is justified by this diagnosis; the existing `v1` field is already the identity carrier.

If Runtime's shared `process_identity()` helper also serves its internal role custody records, the Runtime owner must reconcile those consumers in the same Runtime-owned change rather than silently translating an untrusted caller value at the Agent boundary. The required regression is one positive same child and one negative changed-birth case that still refuses before publication/credential enablement. The existing Agent custody guards remain the authority for the negative case.

## Existing custody guards consulted

- `tests/core/execution/test_process_group.py:1049-1070` refuses lost or substituted retained descriptors while the process is live.
- `tests/core/execution/test_process_group.py:1091-1135` refuses descriptor faults and then refuses a reused process identity.
- `tests/core/execution/test_process_group.py:1146-1177` refuses descriptor substitution even when the original kernel watch is ready.
- `tests/core/execution/test_process_group.py:1222-1241` verifies the retained watch closes with custody and that unavailable epoll cannot prove exit.
- `tests/core/execution/test_process_group.py:1244-1276` allows cleanup only for the exact exited descendant and rejects the wrong birth token.
- `tests/core/execution/test_process_group.py:1309-1328` fails closed without an exact zombie witness and requires the exact bound incarnation.
- `tests/core/execution/test_generic_host_activation.py:306-336` preserves the direct live/stale activation identity refusals.

## Check run

One pure, no-activation format check was run:

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=. /home/user/work/venv-agent/bin/python - <<'PY'
import os
import re
from astrid.core.execution.process_group import process_birth_identity
pid = os.getpid()
value = process_birth_identity(pid)
boot_id = open('/proc/sys/kernel/random/boot_id', encoding='ascii').read().strip()
fields = open(f'/proc/{pid}/stat', encoding='ascii').read().rsplit(')', 1)[1].split()
expected = f'{boot_id}:{fields[19]}'
assert re.fullmatch(r'[0-9a-f-]{36}:[0-9]+', value), value
assert value == expected, (value, expected)
print(f'PASS format={value.split(":", 1)[0]}:<ticks>; helper_matches_direct_proc_inputs=True')
PY
```

Result: `PASS format=b38142f7-84c5-487d-95a4-8180cbff3972:<ticks>; helper_matches_direct_proc_inputs=True`.

No real activation, browser, or full suite was run for this investigation.
