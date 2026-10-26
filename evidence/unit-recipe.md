# D141p new-head/pristine unit recipe

This is the unit-service receiving route carried from full controller 0043 and the Node phase brief. It is source preparation only; no unit, Vitest, Node, or browser command was run here.

## Two required full runs

After the qualified freeze-2 App head is known, run exactly one new full on each source kind:

1. **New App head:** use the existing central `request-test` worker-metadata route for the clean qualified App worker checkout, with `repo=app`, the exact new App commit/tree, and the existing registered `full` suite. The accepted command remains `npm test -- --maxWorkers=3`; follow the returned ID with `wait-test`.
2. **Pristine freeze-2 upstream:** use the existing pristine receiver route from controller 0043, pinned to the exact `d822d2f5d2bd05187b4ff5b6071c3e13945d4747` / `2af40a015057779ceb4e4b37cad62e1469aa7e36` checkout and clean status. Do not use `request-test integration:app` as a substitute for pristine. Use the same registered `npm test -- --maxWorkers=3` suite family and retain separate raw `KEEP` evidence.

The receiving commands remain the existing service commands, with the source-owned worker names supplied only after the new receipts exist:

```text
R=$(/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/request-test <qualified-new-app-worker> full)
/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/wait-test "$R"

R=$(/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/request-test <pristine-d822-receiver> full)
/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/wait-test "$R"
```

The new-head worker metadata must identify `repo=app`, the clean final App checkout, and its full head/tree. The pristine receiver must identify the exact d822 commit/tree and clean status before the service accepts it. Each run retains its own request/status/exit/summary/log/D66 artifacts.

The two runs are separate source/environment kinds. Parse Vitest and Node reports separately; never add their counts. If a pristine failure is environment-sensitive, establish matching environment kind before calling it REG or nonREG. Controller 0043 owns the per-ID join: candidate versus pristine, source/guard custody, and `REG` only when the same root is proven on both comparable environments. No REG author is dispatched before that join.

## Exact Node phase

Both package scripts are known from the retained phase brief:

```text
test="npm run test:app && npm run test:node"
npm test -- --maxWorkers=3
```

If Vitest fails or short-circuits `npm test`, run the exact standalone Node phase `npm run test:node` separately on the new head and on pristine, through the existing test service/receiving route. Do not invent a Node-only row, alter the script, or infer REG0 from a Vitest-only result. Keep each head’s Node result separately identified and reconciled with its own full run.

The phase order is: new-head/pristine full pair → P2 placement-first D66 reproof controller and remaining P2/P1/P3 bodies → exact standalone Node phase on both heads when needed. D141l requires one new full on each head; no unchanged full rerun is substituted.

## Environment and stop rules

Use supported Node 20 only, the existing service’s private result/cache/temp paths, and the existing `npm` script. Keep all raw/private modes. The paired D141g-a body controller owns the 4.6 GB admission, continuous 5-second trace, 4 GB stop, and one-heavy rule; the unit recipe does not relax those controls or add a second floor gate. Missing installed paired API means ordinary 5 GB admission and `WAIT`.

Unit status for this packet: `NOTRUN`. The existing 0043 historical results are not silently reused as freeze-2 results.
