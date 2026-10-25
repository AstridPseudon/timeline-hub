# D100 independent result-review findings

## Verdict

FAIL — D104 authored-input STOP. Candidate27 is independently qualified, but the exact nine projection selectors all stop at the same provider-validation boundary, so projection acceptance is not run or claimed.

## Decisive boundary

The approved projection fixture authors `parent.config.theme_overrides.visual.canvas.fps` as the two-number array `[30000, 1001]` at source lines 418–420. C0 permits unknown/open document fields to remain preserved, but this is a known FPS parameter. The Agent validator reads it through `_fps_values` and `_fps`; `_fps` accepts a positive finite scalar or the typed rational object with integer `numerator` and `denominator`, not an array. The exact source seam is `astrid/sdk/timeline/validation.py`, and the Runtime only reports that provider rejection.

This makes the value typed and predicate-relevant, not opaque producer decoration. Converting it to a number or rational object would alter authored input and could alter protected purpose, so no conversion, approximation, or fixture edit was made. Causal owner is the Agent/provider final-candidate validator. D104 source-owner direction is required before any rerun.

## Actual results

- Corrected identity: qualified PASS. Only `agent.protected_product.sha256` and `agent.protected_product.required_exact_blob` differ from the original 1914 manifest derivative; both now contain the exact 64-character product hash. The original manifest and original 1919 FAIL remain preserved.
- Candidate27: qualified PASS, 27/27 in 2.860s, exit 0. The private XML has zero errors, failures, and skips. The source log records a real 5 GB admission gate immediately before launch; the manager’s 19:40:44Z cleanup receipt recorded 5,280,329,728 free bytes before this run. This qualification does not rely on the later own9 check.
- Projection source receive: qualified PASS. The sole changed file is the byte-exact approved f53b0169 fixture, SHA-256 `6e41a5bba04666275b9e252d7aeb30247a145207da3f9ed14f06b338563a1436`.
- Own9: NO-GO. 9/9 setup errors, 0 pass, 0 fail, 0 skip, 27.585s, exit 1. First common seam is the FPS validation error above.
- Projection acceptance: NOTRUN. No whole-candidate, release, or core credit follows.

## Caller/custody boundary

The frozen qualified App source proves the mounted route as durable persistence → `RuntimeDataProvider.saveTimelineAtHead`/`saveCommitAtHead` → `client.commitTimeline`. The Runtime source proves startup provider loading/registration and `RuntimeService.commit_timeline` dispatch into the registered provider. The Agent registered-provider test supplies the actual `load_timeline_commit_provider("astrid")` registration and `service.commit_timeline` call. The ordinary D66 diagnostic hook is not relevant to this physical-item custody claim and receives no credit.

## Held scope

No product, fixture, Runtime pin, manifest, source body, kit, or upstream file was edited by this review. No pytest, collection, socket, provider, body, full, browser, native, TEN, P4, D130, acquisition, repeat, or guard-writer action was run by this reviewer. The source remains HELD; all prior results remain historical inputs.
