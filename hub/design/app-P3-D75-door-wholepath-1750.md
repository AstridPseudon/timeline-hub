## P3 D75 report

Verdict: proposal v2 is not ready to apply.

Findings:

- 1731’s “old URL” premise is wrong for the browser path. App requests target the stable Runtime door (`harness.ts:567–568`); `harness.runtimeUrl` is the daemon’s dynamic endpoint (`harness.ts:761`). The original passing P1 holds the stable-door route, restarts Runtime, then releases it (`three-products.p1-chain.spec.ts:1503–1554`). This does not by itself rescue v1’s lifecycle omissions.
- 1736’s `requestURL === harness.runtimeUrl` assertion is definitely wrong. The observed browser request origin is the door origin, while `harness.runtimeUrl` changes port across restart.
- The native door dispatches into the current Runtime service; its discovery record advertises the dynamic daemon endpoint separately. The standalone Node discovery proxy likewise keeps the browser URL stable and rereads discovery for forwarding.
- The smallest truthful observation is:
  1. assert the held request origin equals `new URL(harness.doorBase).origin`;
  2. after restart, use the existing `expectSameRealm` identity check to prove the door reaches the new Runtime instance;
  3. release the held route with `route.fetch({ maxRetries: 0 })`;
  4. use existing direct `harness.runtimeUrl` history assertions to prove the exact key/body was delivered to the current daemon.
- Existing v2 downstream A/B, canonical, history, legacy, and undo assertions remain structurally preserved.
- Proposal artifact diff check still fails on trailing whitespace at lines 55 and 74.

Evidence:

- Protected source SHA-256: `a6468188ff21c4fd8bd397ff242b0260ee92ab6f2f90ac94786973eaf3c1e99a`.
- No tracked source changes made.
- No browser, Runtime process, probe, collector, or test suite run, per task scope.
- Source-only command: `git show tl/app-P3-recovery-proposal-return-1736:proposed-v2.patch | git diff --no-index --check /dev/null -` — failed only for the two trailing-whitespace lines.

Next step: revise the proposal’s origin assertions to use the stable door origin, refresh evidence/hashes, and obtain another independent review before any protected-source apply or browser run.