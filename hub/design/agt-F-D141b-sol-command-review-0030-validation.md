# F/D141b independent corrected-command validation

Disposition: `PASS_COMMAND`; no production body was run.

## Reviewed source and exact outputs

- Sol0019 branch `tl/agt-F-D141b-command-sol-0019`: commit
  `0710897c87834550d1ee68b3f120405a9c81fe8f`, tree
  `1861d3e9f3b6fa5cc87660952add8042cabc3227`; clean worktree.
- Exact absolute author publication root:
  `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-F-D141b-command-sol-0019/evidence`.
- `command.sh` SHA-256:
  `db0c2f366597cba1e4a4a067366fda38049fdcb15640d82a26b4dbac41d1043e`.
- `service-row.txt` SHA-256:
  `c3ef3edaaf5250bbe14fa94a7625a5bb17154f82d01a14d9a80f479bae474fd7`.
- Both absolute outputs compare byte-for-byte with the committed Sol0019
  blobs. The source branch delta from wholepath0019 is limited to seven
  evidence files; no product source changed.

## Exact checks run

- `bash -n <absolute command.sh>` — PASS.
- `jq empty <absolute admission.json> <absolute source-manifest.json> <absolute findings-map.json>` — PASS.
- `sha256sum` over command, row, author manifest, admission, findings map,
  and validation — PASS; hashes are recorded in source-manifest.json.
- `cmp` of absolute command/row against `git show` of Sol0019 — PASS.
- `git diff --check` over the Sol0019 evidence delta — PASS.
- Direct read-only source tuple observations — PASS: all four exact paths,
  commits, trees, and clean states match the author packet.
- `realpath /home/user/work/venv-agent/bin/python` —
  `/usr/bin/python3.13`.
- `/home/user/work/venv-agent/bin/python --version` — `Python 3.13.16`.
- Comparator run root and both body gates — absent; no run root or gate was
  created by this review.

## Static path review

The corrected command independently satisfies the requested path properties.
`capture_sources` runs all four repository probes after any individual
failure. The EXIT/INT/TERM traps precede source probes, run-root creation,
lock acquisition, and witness initialization. If the output root cannot be
owned, witness contents are attempted on service stderr, the return remains
nonzero, and the terminal classification is NOTRUN with no durable-path
claim.

All durable witness classes are checked: body and monitor exits are retained
separately; raw streams are opened before body announcement; combined log,
JUnit freshness/nonemptiness, disk, source, and terminal writes are checked.
Evidence failure replaces only a zero return. Missing/empty XML cannot yield
PASS.

The monitor stops only the `setsid --wait`-owned body process group before
failure witness logging for unreadable, low-floor, disk-write, and sleep
failures. Terminal handling stops and waits for the owned group/direct
wrapper and monitor before source-after and log capture; a remaining group
sets a nonzero cleanup result and prevents PASS. No unrelated process or
cleanup target is introduced.

The command still dispatches the existing plain command using the exact
venv-agent interpreter, pristine Agent/Runtime paths, the recorded App and
Composition provenance, 17 roots, `-n 3`, cleared addopts, no cache provider,
timeout 45, durable JUnit, one heavy-body lock, and decimal 4.6/4.7/4.0 GB
thresholds. The service row remains the supported existing normal request-test
/test-run publication path; no unsupported self-location or extra comparator
GO gate was added.

The author packet’s tiny operational smoke reports 7/7 PASS and its static
validator reports PASS; those reports were reviewed, not rerun here because
the exact temporary smoke scripts were not available in the allowed inputs.
No pytest, import, collection, provider, browser, socket, suite install,
service submission, body, or test investigation occurred.

This review is source/command qualification only. It does not establish
behavior PASS, REG0, or ship credit. The manager may record the independent
review marker and, after the ordinary U2 freeze marker, send the one existing
normal service controller.
