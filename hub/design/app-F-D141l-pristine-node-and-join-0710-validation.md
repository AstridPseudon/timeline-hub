# D141l validation

## Exact normal-service runs

- Existing pristine full was verified terminal before continuation: `app-pin-d822d2f5-full-1026063854-17524`, status `fail`, exit `1`, command `npm test -- --maxWorkers=3`, `17,866` passed and `18` failed tests across `1,277` passed and `3` failed files; chained Node phase was explicitly `NOTRUN`.
- One and only one standalone pristine Node request was dispatched:
  `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/request-test app-pin-d822d2f5 full-d141-node-phase --no-cache`
- Same-ID wait command:
  `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/wait-test app-pin-d822d2f5-full-d141-node-phase-1026072325-11111`
- Node result: status `fail`, exit `1`, service duration `95s`, `289` passed, `2` failed, `26` actual skipped, `317` tests, `33` suites, `27` declared skip entries, `0` cancelled/todo.
- Actual Node failure IDs are the two `ssh-keygen ENOENT` callsites recorded in `pristine-node-result.json`; no environment repair or rerun was made.

## Receipt and trace controls

- Attached only the existing general `timeline.d89d.measured-floor.v1` receipt format at the actual Node ID. It uses the retained 0653 normalized DATA projections and independent 0705 qualified Node-kind floor.
- Exact read-only validator command:
  `python3 -I /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/d141-validate-receipt.py /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/tests/app-pin-d822d2f5-full-d141-node-phase-1026072325-11111/recorded-measured-floor.json /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch app-pin-d822d2f5-full-d141-node-phase-1026072325-11111 app full-d141-node-phase /home/user/work/wt/app-pin-d822d2f5 d822d2f5d2bd05187b4ff5b6071c3e13945d4747 2af40a015057779ceb4e4b37cad62e1469aa7e36 'npm run test:node'`
- Validator result: exit `0`, stdout `4600000000`; receipt hash `d0616b60bcbf6e622f812fabd765d5c4d3d0e3c208165adff7e19959d5500172`.
- Qualified arithmetic is `4814028800 - 4625068032 = 188960768`; floor is `max(4600000000, 4000000000 + 188960768 + 200000000) = 4600000000`.
- Node service trace validation: `trace PASS: 21 actual samples`; body PID `18199`; raw trace hash `6224f257c2072eab6e15a470570ec706ec42c7025c829c46c782ca326c9bebb2`; five-second sampling and unobserved inter-sample gaps are disclosed. The original qualification trace remains `b3fcb304...`, 19 samples, PID `18109`, and is explicitly derived DATA rather than original stdout.
- Raw `KEEP` markers remain present. Disk traces are mode `0600`; no source, test, generated, pin, registry, queue, validator, or Git metadata was edited.

## Static evidence checks

- All evidence JSON files parse with `jq empty`.
- `id-join.json` counts verify as `32` current full failed IDs, `18` pristine full failed IDs, and `2` standalone Node IDs.
- Worktree check: `git status --short --branch` reports only the assigned branch with no changes.

No full suite, browser journey, typecheck, lint, adapter, environment repair, or SSH repair was run by this worker. The only authorized execution was the actual normal-service pristine Node phase above.
