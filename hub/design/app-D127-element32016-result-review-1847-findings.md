# D127 independent result review

## Verdict

FAIL, scoped to the retained actual normal result `app-pin-d5a1d1ab-d73-p2-element-d5a1d1ab-submit-1025184016-32016`.

This is a behavioral FAIL, not a refusal and not UNKNOWN: the one original element test has a JUnit failure and service exit 1. Source/preflight/readiness are separate PASS results. The normal run had one readiness test pass and one original element test fail; no retry or resubmission occurred.

## Exact gate and first predicate

- Preflight `app-pin-d5a1d1ab-d73-p2-element-d5a1d1ab-submit-preflight-1025183946-29958`: PASS, exit 0.
- Same normal plan SHA: `21c1e9471c61d3e7925062f3e0a0bf3b943d988dad200d789dcb4018bd1b403c`.
- Original selector: `p2-element`, count 1, source `tests/e2e/local/three-products.p2-elements-assets.spec.ts`.
- Readiness: `three-products.mounted-readiness.spec.ts`, one test PASS, exit 0.
- Actual first failed predicate: `three-products.p2-elements-assets.spec.ts:1052`, unchanged 5,000 ms wait for `dialog.getByRole('status')` to contain `applied`; the status locator was not found.
- The following `page.waitForResponse` page/context/browser-closed error is secondary teardown evidence.
- The original body tail (params patch, canonical/history checks, reload, two guarded Undo operations, and final reload) was not reached. It is UNKNOWN/unexecuted, not a refusal and not a pass.

The source bytes and blob SHA256s are unchanged from App d5a1d1ab: p2-element 78,876 bytes / `7cca78274f96c9466d82bea3108f6f8a447462c9cd722c078ab958bc3578d637`; readiness 18,101 bytes / `2b9723db262978ebbb410d5925163fe61c4a83f05f3b44fbbd524bc9df301593`. The source contains the original full request assertions, canonical/history/reload/guardedUndo checks, and zero-legacy assertions; source PASS does not establish behavior.

## Request binding and runtime profile

The retained private helper capture binds the current request as POST against the canonical timeline-commit route, request ordinal 1, PID 18571, birth ticks 20416744, namespace `pid-18571-birth-20416744-capture-1`, and UTC `2026-10-25T18:42:58.224Z`. The browser diagnostic independently reports the Idempotency-Key as present; the private capture retains only its UTF-8 SHA256 `18ac05fb924bc2495b6ba84917f2936d6308317cd66cd585e5a5bca227ebb4f9`.

Runtime lifecycle is completed with dispatch queue 0.901 ms, handler 21,740.631 ms, provider phase 13,780.929 ms, HTTP response write 3.44 ms, and dispatch wall denominator 21,741.532 ms. Arrival, request-body receive, exact lock wait, and caller receipt are unsupported/outside the Runtime process. Runtime observed HTTP 200 twice at its response boundary, but the browser/app response, provider result, and caller receipt are UNKNOWN; no response body or commit receipt is inferred.

Bounded sampler data: 828 samples at 20 ms, 15 lost samples, 877.038 ms capture-wide observer CPU, no sampler errors, 57 retained events of 57 seen, 19,005 bytes of 65,536, no truncation, and no capacity drops. Sample shares are reported separately from measured wall shares. The complete ten-entry inclusive and ten-entry leaf lists are in `safe-profile.json`; outer routing frames are not cost attribution. The only product-specific leaf observed is Runtime `timeline_commit_validation.py:reuse` at lines 120 (27 samples) and 116 (24 samples), not a dominant operation and not an optimization author.

## Custody and privacy

The four exact genuine checkouts and trees match the preflight and normal manifests: App d5a1d1ab, Agent 070dfc, Runtime ab1e4f, Composition 635f. The plan SHA, normal manifest/XML hashes, and helper SHA were independently rechecked. The helper is the canonical regular non-symlink `p2_commit_phase_capture.py`, mode 0600, SHA256 `4ee0424b63f1f9847995a605dc1050ad7cb8ca75f4d64b8c36d851cfe723f41e`.

Public output is safe projection only: no raw payload/key/auth/private URL/headers/exception text/locals/raw stacks. The raw JSONL and stack artifacts remain in the private result directory with mode 0600; no private export was made. The retained source/service artifacts survive independent worker autorecycle at their absolute paths. No tests, browser, service, profile, collector, acquisition, source, product, generated, schema, pin, Git, or upstream writes were performed by this reviewer.

## Acceptance commands

Read-only checks performed:

- `jq` JSON parses of producer facts, source custody, submission, safe profile, plan, and both manifests: PASS.
- JUnit/XML inspection of retained `readiness.xml` and `p2-element.xml`: PASS parse; counts are readiness 1/0/0/0 and original 1/1/0/0 (tests/failures/skips/errors).
- SHA256/Git exact-source checks for App source files, four pinned heads/trees, plan, manifests, XML, and helper: PASS.
- Git clean check on this review worktree: PASS; no source changes made.
- Retained actual service result/status: PASS custody; normal service exit/status is exit 1 / FAIL, readiness exit 0 / PASS.

No pytest, Vitest, tsc, lint, browser, service, profile, native replay, collector, acquisition, full suite, family/core/tour, new request, or test rerun was performed.
