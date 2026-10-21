# AP2-M2 parent newborn final binding and offline preflight

## Result

Bound the current parent proof to the real committed source, not report0748's illustrative pre-edit SHA:

- source/keeper: `/home/user/work/wt/ap2-m2-parent-newborn-current-proof-source-0748`
- committed HEAD: `af1605a28f31a53b5a3472251493d44941b618fe`
- committed tree: `b0cb1f973c0e1b465241ebef38bd267fd39f0434`
- source status: clean (0 entries); `node_modules -> /home/user/work/app/node_modules`
- source KEEP: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-parent-newborn-current-proof-source-0748/KEEP`, present
- source spec SHA-256: `5c12370fe8a14439f6c82ddbf088bcfcc2fcdcbfb8af90cbba4ec30e72bb1603`, byte-identical to approved 0604
- live callers: NONE; no product/source/spec/pin/assertion/option changes

The rejected report0748 illustrative values were `0c9b7bf01a694856a4a5e75a46161b115c600763` and post-edit tree `00bce13c888dda845b69a944c71aae7142e2e21e`; neither was used.

Required source ancestry is retained and checked:

- `5d36b0e53ff0d17ef045e226a6e6ca7584322858`
- `968bbad09449f419ab63782fca49cad805068333`
- `6bdb7dfadb5218d00cb04db45f67468609b0a1c6`

## Binding changes

The shared helper was mutated only after its old whole-file SHA and exact role-local collision checks passed:

- helper: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/normal014-source-common.sh`
- old whole-file SHA: `d9a691dcaafd7d544a467445a3a020a9ad3d02afc1d527870f00be6948fea848`
- new whole-file SHA: `a0ed2bd7d6688799f22bc8f17f89631c603e4e692a8d5e71f3ee3b26437b27b3`
- old `final95:parent` pair: `acb582c2c3b08481d43853b8526894ac60d074bc` / `141724b56736be40a269f60aa8bfc060914ebd29`
- new pair: `af1605a28f31a53b5a3472251493d44941b618fe` / `b0cb1f973c0e1b465241ebef38bd267fd39f0434`
- old pair occurrences before edit: exactly 1 HEAD line + 1 tree line, both inside `final95:parent`
- all other helper roles/profiles/pins/guards preserved

Reverse proof was in memory only: replacing exactly the new two-line pair with the old pair reproduced `d9a691dcaafd7d544a467445a3a020a9ad3d02afc1d527870f00be6948fea848`; the written helper was not reverted.

Copied gate (old gate remains immutable):

- new owned gate: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-parent-newborn-final-binding-preflight-0756/final-keeper-gate.sh`
- new gate SHA-256: `cbf3bca135919ab43f3e6a02f1906df150448cd992e7501a7436cc4d68440270`
- immutable 0617 gate SHA-256: `515931b8700aba3bf7b1a98e5013ecbe3c5769925b9ce21e44f4fb03b1a4a1e5`
- unchanged promoted driver: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-parent-current-driver-durable-promotion-0535/run-parent-manual-drop-evidence.sh`
- driver SHA-256: `34ee03d1ea6f25ae4f68b8965f5c9b050d8892214416ec3bf551dfa81b17a2d2`

The new gate diff against the old gate is exactly four binding edits: KEEPER path, FINAL_HEAD, FINAL_TREE, and HELPER_SHA. It retains captured service-tree checking, separate keeper HEAD/tree/clean/KEEP checking, ancestry, graph/artifact/schema checks, exact argv and one-test list, child/zero-test/refusal guards, and wrong captured-tree, wrong keeper, wrong helper, and wrong argv controls.

## Offline preflight

Exact command:

```sh
env NORMAL014_PROFILE=final95 NORMAL014_APP_SOURCE=parent NORMAL014_USE_BASE_PYTHON=1 \
  sh /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-parent-newborn-final-binding-preflight-0756/final-keeper-gate.sh preflight
```

Result: PASS, exit 0.

Observed:

- captured service TREE: `b0cb1f973c0e1b465241ebef38bd267fd39f0434`
- separate keeper HEAD/TREE: `af1605a28f31a53b5a3472251493d44941b618fe` / `b0cb1f973c0e1b465241ebef38bd267fd39f0434`, clean, KEEP present
- Agent: `6efc81500a0e0688c2bb41e736503f0fc3e04abb` / tree `2ed2b8a12b5b3391ca221ba6ff05390f71a73556`
- Runtime/producer: `95bd3c5f6d00e9bc8cc8cbe5ef510b68ed660f3c` / tree `d3a290b407fa61e6ab2d476f50c068073f70df00`
- artifacts: `76`, manifest `a902387c6a2315374f7e73511feea47da30191aba831b48820b3864b773a532d`, artifact version `sha256:54205b3ecb55038e416b31af936c9af26afa30dc1b05da16157ee4d861fe05ac`, schema `6ba7b51e9518e7fb08b27ad5b7225855276b657d0adebf704dd853f699768f2d`
- unchanged App pin hashes from the bound helper: `runtime.lock.json` `770352eaf1d015e90fca0ed2f1893749b73b69356ca82a7223b2573276fe485e`; generated metadata `4cd934d868eafd5ab82578da2232f1ee13f04d83c9314b3473b75bd951570044`; generated client `c575f183b6486dd07e8ec798f5a46bff4c9ffc0918892b189c1a433b9f80762d`; timeline types `f8cbbbbc48713a308c2ac2e2e977d08525c4280ef4dc93cd3e8d842245394564`; schema `f52b82024ecd44a5e6c9c68d5cb326d50d70efe9aaad6f8ac6352ea1c87b97b1`
- locked graph: Node v22.22.0, Vite 5.4.21, Playwright 1.60.0
- Composition 0.0.13 archive: outer `895c628ab0727c8975247310fd0319b0f546a8d032a57072c9e364e20965ca30`; embedded package `9412ae25c306d5118241f4d631e8eecc6eef9b2fb5a98302d40938e9f6d54738`; embedded member count 77
- exact collection: 1 test, `three-products.spec.ts:1440`, title `M2 real mounted manual video drop: Runtime selection refusal is closed, native ADD recovers exactly, and undo preserves opaque data`
- negative controls: all 4 refused — wrong-captured-tree, wrong-keeper, wrong-helper-hash, wrong-argv
- shell syntax: `sh -n` passed for helper, owned gate, and promoted driver
- source preflight output: `verified artifacts=76`; native marker collection and locked graph checks passed

Local resource checks:

```sh
flock -n /home/user/work/.app-m1-browser.lock true
df -Pk /tmp
find /tmp -maxdepth 1 -type d -name 'timeline-normal014-parent.*'
find /tmp -maxdepth 1 -type d -name 'timeline-parent-*'
find /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-parent-newborn-final-binding-preflight-0756 -type d -name 'private-node-modules'
```

Result: browser lock available; `15036164` KiB available on `/tmp` (above 10 GiB); orphan normal014 temp roots 0; orphan parent-negative roots 0; worker private graph directories 0. Shared node_modules and locked graph were read-only; no install, build, daemon, browser, localhost/live socket, full suite, or actual was run.

## Proposed central registrations (not submitted)

These are the literal rows to register after independent custody review; no row was added to `suites.conf`, and no actual was submitted.

```text
app ap2-m2-parent-newborn-final-binding-preflight-0756-preflight test "$(sha256sum -- '/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-parent-newborn-final-binding-preflight-0756/final-keeper-gate.sh' | cut -d' ' -f1)" = 'cbf3bca135919ab43f3e6a02f1906df150448cd992e7501a7436cc4d68440270' && test "$(sha256sum -- '/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-parent-current-driver-durable-promotion-0535/run-parent-manual-drop-evidence.sh' | cut -d' ' -f1)" = '34ee03d1ea6f25ae4f68b8965f5c9b050d8892214416ec3bf551dfa81b17a2d2' && env NORMAL014_PROFILE=final95 NORMAL014_APP_SOURCE=parent NORMAL014_USE_BASE_PYTHON=1 sh '/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-parent-newborn-final-binding-preflight-0756/final-keeper-gate.sh' preflight
app ap2-m2-parent-newborn-final-binding-preflight-0756-actual test "$(sha256sum -- '/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-parent-newborn-final-binding-preflight-0756/final-keeper-gate.sh' | cut -d' ' -f1)" = 'cbf3bca135919ab43f3e6a02f1906df150448cd992e7501a7436cc4d68440270' && test "$(sha256sum -- '/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-parent-current-driver-durable-promotion-0535/run-parent-manual-drop-evidence.sh' | cut -d' ' -f1)" = '34ee03d1ea6f25ae4f68b8965f5c9b050d8892214416ec3bf551dfa81b17a2d2' && env NORMAL014_PROFILE=final95 NORMAL014_APP_SOURCE=parent NORMAL014_USE_BASE_PYTHON=1 sh '/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-parent-newborn-final-binding-preflight-0756/final-keeper-gate.sh' run
```

The registered actual, if later authorized, remains the one parent mounted ADD journey; it is not a result here.

## Verification boundary

No actual suite result, browser replay, build, full suite, install, or writer-deletion claim is made. This task only rebounded custody and completed offline preflight. Independent final custody review remains the next step.

