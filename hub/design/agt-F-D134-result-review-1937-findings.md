# Findings

## Verdict

FAIL for independent final review. The durable log agrees with the operator summary, but actual 18455 XML/raw runner receipt were cleaned before review; final custody and XML-level reconciliation cannot PASS. No ship, custody, release, or retirement credit.

## Controls

The packet binds the frozen tuple and recipe controls: 22 roots, `-n3`, empty addopts, no-cache, timeout45, ordinary preflight 0, one accepted body. 29996 was setup-only exit126; 18455 is sole actual body. `integration:agent` does not itself prove runtime sources; snapshot and recipe/source receipts stay distinct. No guard refusal, acquisition, selector, skip, assertion weakening, fallback, retry, or alternate route is reported.

## Classification

The accepted summary is 8926 passed, 190 failed, 180 errors, 0 skipped, 173 subtests passed; 370 unique bad IDs. Baseline pairs are `error/error=180`, `failed/error=36`, `failed/failed=111`, `failed/passed=43`. Upstream status matches are `failed/failed=16`, `failed/passed=2`; status matching is not causal proof.

D54a classifies 344 bad IDs as `OURS_NEW_FILE` (absent at named `08e6b905`). Fourteen exact D118 REG14 IDs are current FAIL, so REG14 remains open. The first host-bootstrap node and 11 others remain UNKNOWN. No pre-existing/environment classification is manufactured. `core_open_n=UNKNOWN`, `reg_open_n=UNKNOWN`, retirement=0.

The exact REG14 records preserve the original pristine `26621` and independent `1307` comparisons; closure still requires all 14 to be PASS in this actual run, and all 14 are FAIL. The D134 START NOW receipt is recorded by the operator. C0 caller-contract behavior is not independently evidenced by a retained request/response packet, so it receives no behavior credit.

## Custody

Actual XML, raw runner receipt, and start/stop disk witness are unavailable. Final source custody is NOT PASS; XML duplicate/collection/subtest checks are UNKNOWN.
