# F D141i corrected sole measurement validation

## Gate and registration

- Independent bounded check `agt-F-D141i-terminal-final-review-0318`: terminal exit `0`, `PASS_COMMAND`, finding count `0`, on the exact 0309 packet.
- Reviewed packet hashes were read back exactly:
  - `measurement-command.sh` `cc16a840e049cfbabaa662b175cf094eba10af871bb166123a5339741adbc6d8`
  - `service-row.txt` `81ee29eebf05bb687c39449ca8551a6fde19340055d5472c54f9d493dbe3f43a`
  - `positive.manifest` `5a4d5640ff927e0c3b4d7d1ad19ecc40e77fcf6298a173d822e8b3dfe5c0d643`
  - `poison.manifest` `222693fc9fb9b8a9abc5620c6f49eb1b872dd8d42a73c38abb8a69b319d3c1fc`
- Fresh manager witness: `2026-10-26T03:21:30.916740+00:00`, `shutil.disk_usage(/home/user/work).free=4826488832`, required `4700000000`, `PASS`.
- The exact original 0249 receipt/brief arguments remain in the registered row; receipt hash `5fbdab93245696b725f7b67eca44f02d939536c8f6e5d6c6678ea628de4b5a35`, brief hash `379e1eb69b3f5e589346ac2cced4e19035ce449ce9d1075c5128be74c77137b5`.
- Suite preimage was retained at `/tmp/agt-F-D141i-corrected-controller-0321.suites.conf.preimage`: SHA `8871cb8218c828f74e2ad4a15f385df497f45ff860788b25f98a8fb111cb257d`, 161975 bytes.
- `ORCH/tests/suites.conf` was changed by one exact line only. Postimage SHA `f6996b4f1b5c697762bcad3f7cc725c555cf227460240dd0c48e105ac0a0a027`, 162265 bytes; exactly one `agent agent-core-full` match before and after; readback preserved all other bytes/rows.

## Service

- Exact command: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/request-test integration:agent agent-core-full --no-cache`.
- Request exit `0`; actual returned service ID recorded before polling: `agent-agent-core-full-1026032321-26496`.
- Exact terminal poll: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/wait-test agent-agent-core-full-1026032321-26496` → terminal `fail`, exit `1`, after `1269s`.
- Wrapper terminal: `state=FAIL`, `body_started=1`, `runner_exit=1`, `monitor_exit=0`, source-before exit `0`, source-after `clean`, finished `2026-10-26T03:44:38Z`.
- No retry, cancellation, release, retarget, local body, local collection, install, alternative environment, or second service request.

## Custody and XML

- Frozen source tuple, paths, origins, and clean guards are exact before and after. Interpreter: `/home/user/work/venv-agent/bin/python` → `/usr/bin/python3.13`, Python `3.13.16`.
- Runmanifest and JUnit binding are the exact reviewed positive-manifest paths. JUnit SHA: `7adf18d3a9cd20c2198d4cd4ccd7e0be59497e6111a73284c4977fe31b92b25d`; launcher manifest SHA matches positive manifest `5a4d5640ff927e0c3b4d7d1ad19ecc40e77fcf6298a173d822e8b3dfe5c0d643`.
- Disk trace: 254 samples, start `4692029440` bytes at `03:23:31Z`, minimum `4311924736` at `03:36:28Z`, end `4451721216` at `03:44:38Z`; continuous stop `4000000000` was never reached, monitor exit `0`.
- Stdlib `xml.etree.ElementTree` parse of durable XML: declared tests `9561`, failures `204`, errors `196`, skipped `0`; 9388 testcase elements with 8988 pass, 204 failure, 196 error, 0 skipped. Element outcomes conserve exactly (`9388 = 8988 + 204 + 196`).
- XML custody discrepancy: declared tests exceed testcase elements by `173`; the raw runner summary reports `173 subtests passed`, but no subtest IDs are present in XML and none were invented. This prevents qualification separately from the genuine outcome counts.
- Raw stdout/stderr, runner log, runner/monitor exit files, interpreter, argv, source before/after, runmanifest, launcher evidence, and XML remain in the durable 0309 runroot. The genuine service result directory remains retained with `KEEP`.

## Disposition

`MEASUREMENT` / no ship credit. No REG/nonREG conclusion. Source custody passed; genuine body outcomes are retained; qualification fails separately on XML declared-count versus testcase-element conservation. Next finite per-ID join remains the orchestrator’s step; do not rerun this unchanged result.
