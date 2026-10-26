# F/D141b operational correction validation

Disposition: `PASS_SOURCE_READY_REVIEW_PENDING`; production body `NOTRUN`.
Authoring base: `a8118e9a51ccb629e88cb6dcde981b22ba448b98`.

Read PLAN section 3 F/C0, original0003, final0014 and the finite independent
wholepath0019 packet. All four residual findings plus its additional
`D141B-LIFETIME-010` are addressed together in findings-map.json. Wholepath0019
reviewed the prior command; it does not approve these corrected bytes.

Exact commands run from the assigned worktree:

- `bash -n evidence/command.sh` — PASS.
- `git diff --check` — PASS.
- `jq empty evidence/admission.json evidence/source-manifest.json evidence/findings-map.json` — PASS.
- `python3 -I "$TMPDIR/d141b-operational-smoke/run-smokes.py"` — 7/7 PASS.
- `python3 -I "$TMPDIR/d141b-operational-smoke/validate-static.py"` — PASS:
  JSON parse, absolute publication bytes/hashes, four exact frozen SHA/tree/
  path/origin/clean states and existing receipt hashes, 17 roots and five absent
  roots, D134 root comparison, preserved production environment/pytest arguments,
  early trap/lock, fresh XML, interpreter/disk constants, absent approval gates,
  and no candidate row installed in suites.conf.
- `realpath /home/user/work/venv-agent/bin/python` — `/usr/bin/python3.13`.
- `/home/user/work/venv-agent/bin/python --version` — `Python 3.13.16`.
- `df -B1 --output=avail /home/user` — read-only observation only; not a body
  admission receipt. The three command thresholds remain decimal
  4600000000 / 4700000000 / 4000000000 bytes.

The operational smoke loads the actual shell function text and unchanged frozen
checkout/interpreter/threshold constants from command.sh. Only evidence outputs
are routed into `$TMPDIR`; no source/interpreter/disk/gate input is substituted,
no production command is dispatched, and no approval marker is created. Its
stub is a tiny shell printf/exit or sleep process group. The nonempty stub
artifact is explicitly labeled operational stub, never presented as pytest XML
or product evidence. The exact production env and all 17 pytest root arguments
are compared byte-for-byte with return0008 by the static check.

The first static-inspector run misinterpreted the inherited inventory hash as
the 17 root names. It hashes the expanded `git ls-tree -r --name-only` file
inventory. Correcting that inspector interpretation yielded PASS; the inherited
hash and approved roots are unchanged. The manifest now states its hash format.

| Case | Actual wrapper exit | Result |
| --- | ---: | --- |
| Shell stub success | 0 | PASS, body/monitor exits 0, four before/after rows |
| Shell stub exit 23 | 23 | FAIL, actual body exit preserved |
| Body exit witness `/dev/full` | 1 | FAIL, body exit 0 retained on stderr; no false PASS |
| Monitor witness `/dev/full` | 1 | FAIL, owned group stopped, body 143 / monitor 1 |
| TERM wrapper with live shell group | 143 | FAIL, body and monitor reaped before final capture |
| Missing body artifact | 98 | NOTRUN, no behavioral credit |
| Initialization beneath regular file | 1 | NOTRUN, all four before/after records on stderr |

Every dispatched smoke group is checked absent afterward. For real disk-read
failure and low-floor branches, static inspection verifies stop_body precedes
failure logging. These branches are not dynamically forced: doing so would
change guard inputs. Source mismatch/unreadable cases are likewise inspected
for independent per-field probes and all-four aggregation; the frozen checkouts
are never altered to make them fail.

Return semantics: keep a nonzero entry/signal return; on normal completion use a
nonzero monitor exit before a body exit. Preserve both actual exits separately.
Custody, cleanup, XML/log/exit/status failure can replace only zero. No pre-body
failure is a behavioral FAIL: status is NOTRUN. Missing/empty XML is also NOTRUN.
If the output root is unavailable, durable evidence is impossible: write
all-four custody and attempted witnesses to service stderr, return nonzero,
and explicitly mark durable status UNWRITABLE. A controller must reject stale
fixed-path files on that attempt. A lock contender cannot overwrite the active
run's witnesses. A still-present owned process group prevents clean/PASS credit.

Normal service comparison: request-test resolves one registered repo/suite row;
test-run snapshots the target and executes its command through bash. This row
uses the same absolute command hash/existence/exec pattern. Its wrapper selects
the frozen sources rather than the service snapshot. D134's settings/root
inventory are preserved after exactly the five approved absent roots are
removed. D134's historical D73 launcher/control bindings are not revived.
No normal service request, suite installation, kit, acquisition, product body,
pytest, collection, product import, browser or socket ran. C0 production request
and reply shapes and all product/test code are unchanged.

Durable publication, byte-identical to the worktree's seven owned files:
`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-F-D141b-command-sol-0019/evidence`.

- command SHA-256: `db0c2f366597cba1e4a4a067366fda38049fdcb15640d82a26b4dbac41d1043e`
- service-row SHA-256: `c3ef3edaaf5250bbe14fa94a7625a5bb17154f82d01a14d9a80f479bae474fd7`

The row path and hashes exist outside this recyclable worktree. Independent
review of this corrected command must PASS before controller installation or
submission; final U2 freeze must PASS before the one heavy body. No body result,
REG or ship credit is claimed. Remaining gates are controller/reviewer work,
not authority granted by source validation.
