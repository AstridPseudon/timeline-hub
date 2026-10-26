# D141l receipt attachment validation

## Result

The existing target attachment was read and verified without overwrite. It is bound to the genuine queued Node job, unchanged request, exact d822 source head/tree, and `npm run test:node`. The supplied validator returned the exact floor `4600000000` with exit 0.

## Read-only controls

- Target receipt JSON parsed successfully; SHA-256: `d0616b60bcbf6e622f812fabd765d5c4d3d0e3c208165adff7e19959d5500172`.
- Target request SHA-256 is `7f0e9942b561dc5db0d41df2f5e2ceceb74fab22f1729c79921856073973279d`.
- `/home/user/work/wt/app-pin-d822d2f5` is clean (`git diff --quiet` exit 0), at head `d822d2f5d2bd05187b4ff5b6071c3e13945d4747`, tree `2af40a015057779ceb4e4b37cad62e1469aa7e36`.
- `package.json` is 16880 bytes; the `test:node` script value is 1666 bytes. The latter is not the package file size.
- Target status was read as `running`; `KEEP` remains present. No body was waited for or started, and no new admission/result claim was made.

## Validator command

```text
python3 -I /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/d141-validate-receipt.py /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/tests/app-pin-d822d2f5-full-d141-node-phase-1026072325-11111/recorded-measured-floor.json /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch app-pin-d822d2f5-full-d141-node-phase-1026072325-11111 app full-d141-node-phase /home/user/work/wt/app-pin-d822d2f5 d822d2f5d2bd05187b4ff5b6071c3e13945d4747 2af40a015057779ceb4e4b37cad62e1469aa7e36 'npm run test:node'
```

Result: exit `0`; stdout `4600000000`.

## Evidence boundary

The Node data is an independently reviewed derived projection, not original stdout. The start/stop values are retained same-kind data; five-second sampling gaps are disclosed, so no continuous peak is claimed. No new measurement, clock, sample, source, request, body, stop, cancel, reissue, or alternate job ID was created.
