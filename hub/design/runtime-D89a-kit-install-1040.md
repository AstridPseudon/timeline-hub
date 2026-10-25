# D89a MAIN kit install receipt

Installed the already worker-authored Agent `test-run` bytes at the canonical MAIN path using an exact-preimage CAS and atomic same-directory rename.

- Source: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-agt-D89a-1024-test-run.sh`, SHA256 `0be17b74ad1e324bc84e50e61e50e3e07390b262b7abe17a37ad22b9bd10d0fe`, mode `0755`, regular file.
- Canonical: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/test-run`, now the exact source bytes, mode `0755`, regular file.
- CAS preimage: exact `5df4145dfb972a0470f20a1959b470f6b17aa68d02c6478da22ed3fadbd922ea`; unexpected drift would have stopped the install.
- Backup: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/test-run.20261025T1040Z.bak`, SHA256 `5df4145dfb972a0470f20a1959b470f6b17aa68d02c6478da22ed3fadbd922ea`.

The exact semantic delta is the authored 4.7 GB inclusive floor for named `agent-core-full`; the default heavy, light, invalid-`df`, and reciprocal busy policies remain as specified.

Validation passed: `bash -n` source and canonical; source hash/mode/type; canonical hash/mode/type; source/canonical byte comparison; and eight isolated private mock controls before and after install. The mock harness stubbed `setsid` and the request/body path, so zero actual test-run body executed.

Job `30693` was not stopped, retargeted, resubmitted, or otherwise touched. No hub write was performed. The production caller remains the real normal central `test-run` named `agent-core-full` path through hub kit publication.
