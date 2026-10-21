# AP2-M2 parent projection custody one original 0900

## Verdict

**HOLD — exact process-custody mismatch before execution.** The single
central submission reached neither the keeper gate nor the parent browser
journey. The registered gate SHA was malformed/truncated (62 characters),
while the actual gate file has a different, valid 64-character SHA-256. Per
the brief's “no reviewer repair” rule, I did not edit the proposal or rerun.
This is not a product-safety verdict; the historical `31285` failure remains
historical and was not repeated.

## Source and custody review

The independent changed-binding verdict before submission was **APPROVE**:

- Live service source: `/home/user/work/wt/ap2-m2-parent-projection-custody-one-original-0900`
  - `HEAD=8eb4d08e60f434b938ea885c8cadca4bd87151b3`
  - `TREE=ea317333400d1a342f2520556eef8ce9399666c1`
  - clean status; `node_modules` resolves to `/home/user/work/app/node_modules`
- Restored private protected keeper (verified separately before cleanup):
  `/home/user/work/wt/ap2-m2-parent-projection-final-owned-binding-0855`
  - `HEAD=8eb4d08e60f434b938ea885c8cadca4bd87151b3`
  - `TREE=ea317333400d1a342f2520556eef8ce9399666c1`
  - clean status; same shared `node_modules` symlink; required `KEEP` marker present
- Original proof spec SHA-256:
  `5c12370fe8a14439f6c82ddbf088bcfcc2fcdcbfb8af90cbba4ec30e72bb1603`
- Approved projection blobs remained exact:
  - `drop-position.ts`: `c634ede997c8ca9c197fcf17d84fcf2630c69889`
  - `drop-position.test.ts`: `4ed1d4cde67f32f1b573baafea400ae58bc4dd22`
- HOME App `e465af770be78adfca3a5e92a0d587b20ba74a77` / tree
  `aa659245db3e58c2cf592e4437316aeb1454f38f` has matching projection blobs.
- The helper had only the authorized `final95:parent` binding:
  `96969ce9ff43b676abb4616009fd1112e93020065483b2a8ae0afac7245ba109`;
  old pair counts were `0/0`, new pair counts `1/1`, and reverse substitution
  reproduced `a0ed2bd7d6688799f22bc8f17f89631c603e4e692a8d5e71f3ee3b26437b27b3`.
- Gate actual SHA-256:
  `45b10f9bbae7d33030be1166d7447090d6a9fc98e9b08c041d13b69a022bd1`
  (64 characters).
- Driver SHA-256:
  `34ee03d1ea6f25ae4f68b8965f5c9b050d8892214416ec3bf551dfa81b17a2d2`.

Bounded prerequisites passed before registration: shell syntax checks, source
and keeper identity/cleanliness, projection identity, helper binding counts
and reverse proof, browser lock free, and `13,222,104 KiB` available on `/tmp`
(over the required 10 GiB). Two exact normal source copies were present at
most: the live service source and the private keeper.

## Central registration and first failure

Registered exactly once under:

`ap2-m2-parent-projection-custody-one-original-0900-actual`

The registered command was syntax-checked and submitted once with
`request-test ... --no-cache`:

```text
request-test ap2-m2-parent-projection-custody-one-original-0900 ap2-m2-parent-projection-custody-one-original-0900-actual --no-cache
```

Run ID:

`ap2-m2-parent-projection-custody-one-original-0900-ap2-m2-parent-projection-custody-one-original-0900-actual-1021085956-24727`

Result: **fail exit 1 in 2s**, with service tree `ea317333400d1a342f2520556eef8ce9399666c1`.

First real failure: the first registered precondition
`test sha256(gate) = expected` failed. The registered expected gate value was
the malformed 62-character string
`45b10f9bbae7d33030be1166d7447090d6a9fc98e9b08c041d13b69a022bd1`, whereas
the actual gate file was the valid 64-character value recorded above. The
driver hash precondition was not reached. No `final-keeper-gate.sh` output,
source preflight, browser lock acquisition by the run, browser, socket,
build, install, or actual test execution occurred.

## Durable evidence manifest

The central service retained these files before cleanup:

- Request and no-cache registration: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/tests/ap2-m2-parent-projection-custody-one-original-0900-ap2-m2-parent-projection-custody-one-original-0900-actual-1021085956-24727/request`
- Snapshot/source identity: same directory `/snap` (`tree=ea317333...`, target worktree recorded)
- Durable failure summary and exact command: same directory `/summary`
- Runner tail: same directory `/runner.log` (empty because the precondition failed before the gate)
- Service command log: same directory `/log.txt` (empty; no gate/driver process reached)
- `exit=1` and `status=fail`: same directory `/exit` and `/status`
- No trace, error-context, request/response summary, or browser evidence was
  created because the run stopped before the driver; this is explicitly an
  unexecuted-precondition failure, not missing retained actual evidence.

No source/spec/helper/gate/driver repair or second submission was made. No
writer cut is authorized.
