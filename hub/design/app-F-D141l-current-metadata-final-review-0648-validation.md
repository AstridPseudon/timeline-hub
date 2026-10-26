# D141l final metadata validation

## Exact read-only checks

All checks were run after reading the bounded0643 corrected derivatives. They inspected retained raw jobs, Git objects, installed validators, and JSON; they did not run or modify the App product suite.

```text
python3 -I /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/d141-validate-receipt.py /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/tests/app-full-1026060654-8638/recorded-measured-floor.json /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch app-full-1026060654-8638 app full /home/user/work/app 4de54db14bdc9ddc2ce2e5887258b03acbffd30d 84c3fb7f73f08c22220f8e808962fe3f24aaa0aa 'npm test -- --maxWorkers=3'
# PASS; output 4793895424

python3 -I /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/d141-validate-receipt.py /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/tests/app-full-d141-node-phase-1026063009-19156/recorded-measured-floor.json /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch app-full-d141-node-phase-1026063009-19156 app full-d141-node-phase /home/user/work/app 4de54db14bdc9ddc2ce2e5887258b03acbffd30d 84c3fb7f73f08c22220f8e808962fe3f24aaa0aa 'npm run test:node'
# PASS; output 4793895424

python3 -I /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/d141-validate-trace.py /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/tests/app-full-1026060654-8638/disk-trace.tsv app-full-1026060654-8638 32066 0
# PASS: 256 actual samples

python3 -I /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/d141-validate-trace.py /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/tests/app-full-d141-node-phase-1026063009-19156/disk-trace.tsv app-full-d141-node-phase-1026063009-19156 18109 0
# PASS: 19 actual samples

python3 -m json.tool evidence/correction.json
python3 -m json.tool evidence/current-result-corrected.json
python3 -m json.tool evidence/node-results-corrected.json
python3 -m json.tool evidence/trace-measurement-corrected.json
python3 -m json.tool evidence/id-map-corrected.json
# PASS for all five

git diff --check
# PASS
```

A read-only Python CSV recomputation of both retained traces confirmed full `256` rows with MAX `4809617408` and MIN `4494544896`, and Node `19` rows with MAX/MIN `4798197760`/`4625068032`; body PIDs were `32066` and `18109`. SHA-256 recomputation matched every raw request, snap, summary, log, trace, and receipt hash recorded in `review.json` and the corrected derivatives.

Git checks confirmed current App `tl/integration` HEAD `4de54db14bdc9ddc2ce2e5887258b03acbffd30d`, tree `84c3fb7f73f08c22220f8e808962fe3f24aaa0aa`, both raw parents, and clean status. Frozen d822 resolves to tree `2af40a015057779ceb4e4b37cad62e1469aa7e36`. Current and frozen Node failure scripts have identical blobs (`56150e5b4c3421e01b971e6a80631dcc60390804` and `ad87267276e738afed37e076832bc3674c78e379`); their own selectors and `ssh-keygen` predicates are present at the same source lines (capture test 131/133; ship-evidence setup 70/71), and exact full-ID membership was checked from the raw log against frozen source titles, predicates, and parameterized cases.

Installed read-only checks returned Node `v22.22.0`, npm `10.9.4`, and Python `3.13.16`. `command -v ssh-keygen` returned no path; no repair or substitute was attempted.

No full suite, typecheck, lint, browser journey, direct test replacement, source/test edit, or environment/package change was run.
