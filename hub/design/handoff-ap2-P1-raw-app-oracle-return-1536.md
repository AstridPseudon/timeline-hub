# Handoff: P1 raw App oracle correction

PASS. In `/home/user/work/wt/ap2-P1-raw-app-oracle-return-1536/tests/e2e/local/three-products.p1-chain.spec.ts`, changed only line 824 from the unsupported `app` absence expectation to whole-object equality with authentic `originalClip.app`:

```ts
expect(mergedDocument.clips[1].app).toEqual(originalClip.app);
```

This follows the independently reviewed 1531 handoff and `current16398` FAIL2/415s evidence: the numeric-held accepted split preserves the authored App object, and C0 preserves unspecified raw keys. All other bytes/assertions/fixtures/helpers remain unchanged.

PASS: root/app/node TypeScript no-emit checks, ESLint for the touched file, exact Playwright list (2 tests only), and `git diff --check`. No live body/full suite was run. The second-case no-POST issue remains separate and untouched.
