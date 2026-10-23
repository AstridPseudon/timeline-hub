# P1/P2/P3 service readiness — PASS, static scope only

All THREE existing original suite rows are static READY on selected sources. Native seed GREEN / browser journeys / original bodies: **NOTRUN**. No test-service requests were submitted. This is harness qualification, no product behavior credit and no P1 GO.

Only `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/tests/suites.conf` rows `full-e2e-three-products`, `ap2-P3-gate5-h6-0348`, and `ap2-P1-chain-h6` changed. App worktree remains clean at merged `4c4c9c77c96fab70c4efef09db9a3bc456b0d803`, tree `2652d85a0ab40bcf0e88443f721dc4b868eeb743`; no source, test, fixture, pin, dependency, generated file, launcher, process file, new row or Git ref changed. Worker tmpdir is the harness-provided pointer file to `/tmp/w-565a500dea`; all scratch artifacts are there.

## Decisions and repairs

- Read PLAN §3, C0 §§1–5, BOARD D21/D24, 1615 report/handoff/brief, independent 1603 and App owner merged receipt. Owner receipt is complete: own `0b3cef4d21610031049b2c8809089a730d0abfbe` was merged as `4c4c9c77c...` with the ENTIRE reviewed tree. Historic pending-owner language was wrong.
- Recomputed actual P1 blob `38ada64bb2596254472e93974a44893987a87db1`, full-file SHA256 `5b3bcc0bf55f55236d0bb738bc66d69c4c8a963698952ff5c0f65f73829d014c`, and first-test-through-EOF SHA256 `582dc8fbc3cdf1991b981dce969e3981b63484b70aaeb70f331d907f5b2fc9bd`. Refreshed stale daa50e/098d guards and added both reviewed diagnostic-file SHA guards; original test suffix unchanged.
- Refreshed P1/P3 stale Agent/Runtime tree guards and the older tuple buried in P3's full tail. App guards select the actual merged source. P3 retains all original source/ancestry/body checks (55 static `test` guards before graph mounting), all pass.
- Preserved lossless `shlex.quote` nested programs and assignment `&& eval &&` fail-fast chains. Extracted real outer-shell arguments, asserted nonempty exact bytes, and parsed both shell levels.
- Existing P2/P3 seed probes did invoke the public helper containing all 21 original Python assertion nodes, including raw closure/receipt/request hash/canonical digest/manifest validation. They did NOT check history, used the ordinary preliminary initialization, and erroneously required nonexistent `seed.projectId`. They now call the same public `startDirectHarness({ deferTimelineInitialization: true })` used by Gate 5, then unchanged `seedThreeProducts()`. The project check uses `harness.seed.projectId`. No replacement fixture, private bootstrap, extra publication or fields-merge fallback.
- In the same inline native preflight, reused original `/commits` history expectations against the helper's retained accepted packet: authoritative head/publication, receipt, previous pin, records/steps/commands/reads, attribution, merge and label. This invokes no new test file. `timeout 300s` bounds the native stage; its failure prevents the original journey. Only successful execution emits the explicit native-seed GREEN marker. That execution has NOT occurred here.
- P3's original vendor guard must use frozen producer `/home/user/work/wt/rt-pin-34eac004`, as `runtime.lock.json` pins `34eac0041b0891e9011966b39bcbd26053fde5bc`. Checking that lock against execution Runtime259 correctly refused; changing the producer argument preserves the existing guard and frozen pins. The old prebuild-unavailable assertion occurred AFTER global setup had built dist; it now requires actual availability (`null`) there. No guard was removed.
- Export the already selected Remotion directory and approved Node toolchain into both preflight and original-body environment with shell `%q` round-tripping. Body invocation tails remain intact. No shared install writes.

## Selected scope and limits

| Repo | Selected source | Tree |
|---|---|---|
| App | 4c4c9c77c96fab70c4efef09db9a3bc456b0d803 | 2652d85a0ab40bcf0e88443f721dc4b868eeb743 |
| Agent | 98ef2f9c95fd43d88cca2909d8d1518302e3050c | ed007d6efc06135b5978d8a11a71609b0f476f14 |
| Runtime | 2593942dfbbbe1d70bb6e776f811285deb2ab18b | 3bd06dc517f347976541ae4dde3caf3d29d03419 |

Immutable child `venv-agent-child-ap2-current-98ef-259-1606` and Remotion `agent-remotion-ap2-current-98ef-259-1608` SUCCESS receipts/installed markers verified; no rebuild/provisioning. Actual installed imports, PEP610 metadata and freeze exactly match the selected provisioning report. **Count discrepancy:** receipt says 92 pins, but both original report and current freeze contain 70 `==` version pins plus two source distributions (72 lines); filtered requirements file has 74 version lines. Do not describe this as 92 installed distributions. Freeze SHA256 `ebe66eb17e7caa945e5e59cf85e809bd39017fb86264a13e7d889f08405a31b7`.

The unchanged Remotion env metadata also names `/home/user/work/venv-agent/lib/python3.13/site-packages`, which does not exist; no directory/dependency was created or env receipt rewritten. Installed schema-package import is unverified/unavailable in that child; native provider retains its vendored JSON schema. Static readiness verifies the selected metadata/guards, not schema execution or seed acceptance. Service-owned seed preflight must decide that capability honestly.

Runtime home had moved to `d9e2a71e87c827290a3ff58a94f6fb8b4bc11e0b` / tree `9b07545cac9a8bbafb16246aaa6f72050ef7cffe` when observed. These rows intentionally exercise selected259, not integrated-current Runtime. Final P1 GO still needs integrated-current proof. Full v2 wire/request/reply/history/undo/preview behavior and mounted persisted save source are untouched and unexecuted here.

The actual 1366 log `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/tests/ap2-P1-P2-P3-atomic-current-OPS-1610-full-e2e-three-products-1023161042-1366/log.txt` contains the nested unexpected EOF near `cut -d`; its zero service summary is rejected as proof. No seed GREEN inferred.

## Exact commands and results

Run from `/home/user/work/wt/ap2-P1-P2-P3-OPS-sol-1625` unless stated:

```sh
/home/user/work/runtimes/agent-remotion-ap2-current-98ef-259-1608/.toolchain/node-v20.19.4-linux-x64/bin/node --import tsx --test tests/e2e/local/p1-diagnostic-safety.test.ts
python /tmp/w-565a500dea/verify.py
python /tmp/w-565a500dea/final-audit.py
env -u PYTHONPATH PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-agent-child-ap2-current-98ef-259-1606/bin/python -B -P /tmp/w-565a500dea/installed-verify.py
node --check /tmp/w-565a500dea/native-preflight.mjs
node scripts/vendor-lock.mjs check runtime.lock.json --producer /home/user/work/wt/rt-pin-34eac004
git diff --check
git status --porcelain=v1 --untracked-files=all
```

- Actual Node20 safety tests: **6 passed, 0 failed, 0 skipped**, run ONCE; TAP duration 395.420498 ms. Node v20.19.4/npm 10.8.2 verified by all static prefixes. No Vitest/cache writes.
- Final `verify.py`: PASS, **3/3 actual static prefixes**, **9/9 negative source/tree/body controls REFUSE exit2**, **6/6 outer+inner bash-n**, **3/3 nonempty exact shell extraction**, **9/9 exact-row fail-fast controls** (nonzero17, inner parse2, eval parse2 for each). No body marker reached by any negative control.
- `final-audit.py`: PASS, **3/3 positive assignment/eval/body-marker controls**, **3/3 selected toolchain-export roundtrips**, all **55 P3 pre-mount static tail guards**, all three complete journey invocations, outside identity, P1 original suffix and clean App source.
- Installed verification PASS (actual count caveat above); native inline JS syntax PASS; frozen vendor check PASS; diff check PASS; status empty. Initial exploratory checks expecting literal 92 installed pins or an existing optional schema env directory failed and are disclosed, not relabeled as passes.
- Existing private graph public effects/animations/transitions exports resolve under its `dist/` with Node20: PASS. No mounting or mutation performed here.
- No global setup, hosted/native build, native seed, browser/list/body/full suite or service request executed. No safety denial occurred.

## Identity audit

Outside-three-rows byte identity SHA256: `06a23ebe7a0ab884e31e221841049e26cd92b6d19a5b580d0018287487544cda`. Row SHA excludes the `app SUITE` prefix and newline. P1/P2 entire tails are byte-exact. P3 full tail differs for the described current source guards/frozen producer/postbuild guard; its complete original journey command, exact Gate5 grep and flags are byte-exact after selected Agent/Runtime tuple substitution. No temporary body truncation in suites.conf.

```json
{
  "outside_sha256": "06a23ebe7a0ab884e31e221841049e26cd92b6d19a5b580d0018287487544cda",
  "rows": {
    "P1": {
      "row": "b919457f55817624465b9c12f5c28f6144b2c60e719e194d20e6206d117ecf06",
      "inner": "51439672fb5c3aa728ae3f2f87b4939c787bbaf546b2ef799f1fcaf75f4abdaa",
      "tail_before": "7cc4e96afbc36fe546b34c570c7aac81ea1679b4abb7b8ef105073fd7de68190",
      "tail_after": "7cc4e96afbc36fe546b34c570c7aac81ea1679b4abb7b8ef105073fd7de68190",
      "journey": "a1e38c6b6e2986b83b9dff05e44c1f8f7b905c1802b5e0295f80e5f8b2ec918f",
      "inner_bytes": 9495
    },
    "P2": {
      "row": "2ff46c18a5e1b1e6b98dc0ebd6cba3eb77127f859c9e599f1f9e6c0c29daffb7",
      "inner": "b9117c842f32810801fe630f053cdc80028520be95cca138f832393b4765e540",
      "tail_before": "f383cfc1abbaf1e14ff9fc7f9ab6b4e0eb401f007bc979046b5e03096e8758a7",
      "tail_after": "f383cfc1abbaf1e14ff9fc7f9ab6b4e0eb401f007bc979046b5e03096e8758a7",
      "journey": "cfee3a6950b0ee6d511803a10899441647d4e177301e0dcf2227ad8e7501d93f",
      "inner_bytes": 11340
    },
    "P3": {
      "row": "a34abfe7922ebb1023d23837442848292852fc7b15b711291d35dc5d67d4ebb9",
      "inner": "b5b251c82aad3a1fea34084d863a2ec5098fda583d566867d1b09cad0401f45a",
      "tail_before": "b5fa15f8051248ad496c2c0b817c21c9f6df9a7da8f67a4d8d46a113ee6b0d35",
      "tail_after": "e202fc7a6573a92b8776bb10871b9db5b937f800259432e37756bc8a0890c3b7",
      "journey": "17726f0fed73a6b45333bf8282d0f1b934cdf0a25b7f153aaa451613823ef1cd",
      "inner_bytes": 11142
    }
  },
  "P3_tail_static_test_count": 55
}
```

All five protected spec blobs remain exact: P1 `38ada64...`, Gate5 `37caf285...`, P2 tour `45a8088...`, elements/assets `836d144...`, popup `6570c112...`. Frozen runtime34e, Composition d106 lineage and artifact SHA256819acf source files were untouched.

## Manager service order — commands only, NOT submitted

Start with original P3 (its bounded full-native seed must succeed before its original Gate5 body), then P2 original eight journeys, then the meaningfully changed original P1 diagnostic chain. Stop and route any seed refusal to its owner; never credit a zero summary without actual seed GREEN and original test counts. All are existing rows and complete bodies.

```sh
O=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch
R=$("$O/bin/request-test" ap2-P1-P2-P3-OPS-sol-1625 ap2-P3-gate5-h6-0348) && "$O/bin/wait-test" "$R"
R=$("$O/bin/request-test" ap2-P1-P2-P3-OPS-sol-1625 full-e2e-three-products) && "$O/bin/wait-test" "$R"
R=$("$O/bin/request-test" ap2-P1-P2-P3-OPS-sol-1625 ap2-P1-chain-h6) && "$O/bin/wait-test" "$R"
```

If wait returns124, wait on the same R again; do not resubmit. Commands target this unchanged merged-tree worker; integration:app is equivalent only while its exact source/tree remain the recorded merged tuple. Do not call the selected259 P1 result integrated-current GO.
