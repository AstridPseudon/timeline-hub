# D141w validation

## Result

The three independent 0740 findings are resolved in the documentary packet.
Pure builder binding remains PASS; the corrected packet is still prospective.
No product, test, generated-file, pin, registry, queue, hub, checkout, request,
or Git metadata was changed.

## Read-only/source checks

- `git -C /home/user/work/app status --short --branch; git -C /home/user/work/app rev-parse HEAD HEAD^{tree}` — PASS; clean `tl/integration`, App `82e9e13ddf1d7ec6c736521b2eb091dca9877598`, tree `6a6e49eb4461b5ca1a7fa1247653bc794f26d710`.
- Equivalent status and `HEAD HEAD^{tree}` checks for `/home/user/work/agent`, `/home/user/work/runtime`, and `/home/user/work/composition` — PASS; exact tuple is recorded in `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-P-D141w-ordinary-recipe-return-0747/evidence/source-manifest.json`.
- `sha256sum /home/user/work/app/scripts/testing/d66-plain-stack.mjs; git -C /home/user/work/app rev-parse HEAD:scripts/testing/d66-plain-stack.mjs; git -C /home/user/work/app cat-file -s 59b65214bc74c1ca118b097bc3b13c0ffe480a93` — PASS; unchanged genuine blob `59b65214bc74c1ca118b097bc3b13c0ffe480a93`, SHA-256 `2032f3087faab5bc1037b54faa593cb32536de15b748809601731ad5f6a7602f`, 49,914 bytes.
- Supported pure import using `/home/user/work/runtimes/agent-remotion-app-p1-787-2a9-1830/.toolchain/node-v20.19.4-linux-x64/bin/node --import tsx`, with only `buildSubmitPlan`, `serviceRecipe`, and `exactCheckoutPath` from the genuine builder — PASS; eight selectors, 16 commands, 16 one-LF rows, all hashes in `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-P-D141w-ordinary-recipe-return-0747/evidence/binding.json`.
- `python3 -m json.tool` over all JSON outputs — PASS.
- `sha256sum /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/tests/suites.conf` and prospective-name absence check — PASS; registry preimage unchanged, new names absent, no registration.
- Source inspection of builder lines 187–209, 375–395, 624–626, 638–701; `request-test`; `wait-test`; `test-run` lines 19, 30–58, 61–120; and `d141-disk-trace.py` lines 16–17 — PASS; proves explicit pins, submit ownership, full* heavy classification, strict 5.2-GB default, 4.5-GB refusal, and per-heavy-request five-second trace.
- `git -C /home/user/work/app diff --check 5344c53e3063001bb3255bd0c9cd32cc5e77967f 82e9e13ddf1d7ec6c736521b2eb091dca9877598` and Composition diff check — PASS.

## Exact command/row checks

`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-P-D141w-ordinary-recipe-return-0747/evidence/normal-command.txt` and `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-P-D141w-ordinary-recipe-return-0747/evidence/preflight-command.txt` are the genuine first-pair
0736 command bodies byte-for-byte. The 16 new registry rows retain those bodies
and change only the prospective suite names to `full-d141-<selector>-82e9e13d-submit`
and its derived `-preflight`; each row has exactly one LF and its byte count and
SHA-256 are recorded in `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-P-D141w-ordinary-recipe-return-0747/evidence/binding.json`.

## Not run by instruction

No `--submit`, checkout request, registration, `request-test`, `wait-test`, body,
full suite, browser, localhost/live socket, provider execution, test, typecheck,
lint, collector, or alternate route was run. Exact App and Agent checkouts remain
unmaterialized, so this packet does not claim operational qualification.
