# D141l corrected current-result validation

## Controlling result

The actual current App full and standalone Node tests remain `FAIL`. Custody qualification is `PASS` for documentary bindings only after the corrections in the adjacent immutable derivatives. This is not a product-test PASS, REG verdict, or global result.

The original controller and independent-review evidence remain unchanged. Their SHA-256 values are recorded in `correction.json`; the raw job directories and `KEEP` markers remain the authoritative originals:

- `tests/app-full-1026060654-8638`
- `tests/app-full-d141-node-phase-1026063009-19156`

## Corrected facts

- Full: exit 1, 4/1362 files failed, 32/19777 tests failed, Vitest `1263.40s`, service `1270s`; chained Node phase `NOTRUN`.
- Node: exit 1, 296 passed, 2 failed, 26 actual skipped tests, 324 tests, 33 suites, Node duration `79907.300109ms`, service `83s`; 27 declared skip entries remain separately named.
- Full trace: 256 rows (`1 first`, `253 periodic`, `2 final`), all-row minimum `4494544896`, raw observed maximum `4809617408` including first sample `4809617408`, final `4624244736`, periodic gaps `4.991440548s..5.008102580s`.
- Node trace: 19 rows (`1 first`, `16 periodic`, `2 final`), all-row minimum `4625068032`, raw observed maximum `4798197760`, final `4625068032`, periodic gaps `4.995830387s..5.004783044s`.
- Both receipts remain `timeline.d89d.measured-floor.v1`, floor `4793895424`, historical growth `593895424`, stop `4000000000`, margin `200000000`, bracket-only historical semantics. No lower floor is introduced.
- Both Node failures independently report `spawnSync ssh-keygen ENOENT` at their own call sites. The second is a suite-level uncaught setup failure and is not causally collapsed into the first test failure.
- The full log contains exactly 32 failed IDs plus one separate collection error. The corrected ID map compares each title/parameterized input with frozen d822 source membership. The d822 `useTimelineSave.test.tsx` file (blob `691c67745b750f06571e40530acd9005f2cc0b3b`) contains recovered-draft tests but not the current prepared-video or public-client Undo predicates; those own IDs are `N/A` pending a genuine pristine result.

## Read-only validator commands and results

These commands were run against immutable retained originals; no product suite, typecheck, lint, browser journey, source, test, fixture, pin, registry, or package install was run or changed.

```text
python3 -I /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/d141-validate-receipt.py /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/tests/app-full-1026060654-8638/recorded-measured-floor.json /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch app-full-1026060654-8638 app full /home/user/work/app 4de54db14bdc9ddc2ce2e5887258b03acbffd30d 84c3fb7f73f08c22220f8e808962fe3f24aaa0aa 'npm test -- --maxWorkers=3'
# exit 0; output 4793895424

python3 -I /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/d141-validate-receipt.py /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/tests/app-full-d141-node-phase-1026063009-19156/recorded-measured-floor.json /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch app-full-d141-node-phase-1026063009-19156 app full-d141-node-phase /home/user/work/app 4de54db14bdc9ddc2ce2e5887258b03acbffd30d 84c3fb7f73f08c22220f8e808962fe3f24aaa0aa 'npm run test:node'
# exit 0; output 4793895424

python3 -I /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/d141-validate-trace.py /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/tests/app-full-1026060654-8638/disk-trace.tsv app-full-1026060654-8638 32066 0
# exit 0; output trace PASS: 256 actual samples

python3 -I /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/d141-validate-trace.py /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/tests/app-full-d141-node-phase-1026063009-19156/disk-trace.tsv app-full-d141-node-phase-1026063009-19156 18109 0
# exit 0; output trace PASS: 19 actual samples

python3 -m json.tool evidence/correction.json
python3 -m json.tool evidence/current-result-corrected.json
python3 -m json.tool evidence/node-results-corrected.json
python3 -m json.tool evidence/trace-measurement-corrected.json
python3 -m json.tool evidence/id-map-corrected.json
# exit 0 for all five corrected JSON files
```

Read-only Git/static checks independently confirmed current App `4de54db14bdc9ddc2ce2e5887258b03acbffd30d` / tree `84c3fb7f73f08c22220f8e808962fe3f24aaa0aa`, frozen d822 `d822d2f5d2bd05187b4ff5b6071c3e13945d4747` / tree `2af40a015057779ceb4e4b37cad62e1469aa7e36`, the exact current failure-file blobs, identical Node failure-file blobs, and title-level absence of the current own predicates in frozen d822. No pristine test outcome exists, so `REG` and `nonREG` remain undetermined.
