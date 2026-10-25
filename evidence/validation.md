# F/D134 validation and disposition

## Source conservation

- The four frozen checkouts are clean and match the bound SHA, tree, parents,
  and official origin recorded in `source-review.json`.
- The normal D73 maker is the unchanged Agent
  `tests/suites.conf.candidate.request.md`; the pinned launcher is the
  unchanged `tools/p4-d73-pinned-launch.sh`. Their Git blob and SHA-256
  witnesses are recorded in `source-review.json`.
- The generated positive manifest binds Agent `a4e016b6`, Runtime `5e9ad1c6`,
  App `d8a1cd40`, Composition `635f4de0`, existing `venv-agent`, the exact
  profile/schema, and Node `v20.19.4`. The poison copy changes only
  `agent_sha`; `manifest-diff.json` records the parsed comparison.
- The existing 0811/2234 positive stub was independently hashed in full as
  `38afc8a5b177801f86f33b0166c8ecd4489ee997629e91b336b9c248ca360ad0`.
- The old 070dfc/f4d6 manifests were not reused. No package, profile, child,
  kit, suite, product, or test change was made.

## Recipe conservation

`evidence/measurement-command.sh` retains the canonical 22 selector roots,
`-n 3`, cleared `addopts`, `-p no:cacheprovider`, and `--timeout=45`. This
worker did not run that body, request-test, collection, provider, or suite.

## Authorized DRY controls

The ordinary launcher was run exactly twice in `dry` mode. The positive path
passed launcher preflight (`preflight_exit=0`), reached the existing stub,
returned 17, and recorded one call. The poison path stopped at the deliberate
`D73 launcher: agent SHA mismatch` guard with exit 1 and zero calls. Raw
stdout/stderr and launcher records remain in the private scratch directory;
only hashes and safe outcomes are published in `preflight.json`.

## Validation commands

```text
bash -n evidence/measurement-command.sh evidence/preflight-command.sh
python3.11 -m json.tool evidence/source-review.json
python3.11 -m json.tool evidence/source-manifest.json
python3.11 -m json.tool evidence/manifest-diff.json
python3.11 -m json.tool evidence/preflight.json
python3.11 -m json.tool evidence/readiness.json
python3.11 -m json.tool evidence/missing-inputs.json
git diff --check
```

All commands above are source/evidence checks only; no full suite or body was
requested. No own Python, TypeScript, or production code was added, so compile,
Ruff, and typecheck lanes are not applicable.

## Gate disposition

D128's child-maker custody refusal remains immutable and is not a route for this
worker. The dry controls are accepted only for the exact positive/poison
preflight assertions; they provide no full-body, behavior, or ship-grade
custody credit.

## Independent D134 review

The accepted service `agent-agent-core-full-1025191128-18455` is terminal exit 1, preflight exit 0, with one body. Operator packet commit/tree: `abf555e3638955ae90f796815fd66ed6d6e95e91` / `2b46e9b653479acc9d77029ac552e2c88743b7a4`.

The durable service log SHA-256 is `65def166348d4ffde949d530bff1a7bcba820ad674ca85b8ccc3e708c781ae8e`; safe short-summary parsing found 190 FAILED, 180 ERROR, 370 unique bad IDs, and no duplicates. In-place baseline 30693 parsing reproduced `error/error=180`, `failed/error=36`, `failed/failed=111`, `failed/passed=43`. In-place upstream 9244377 parsing reproduced `failed/failed=16`, `failed/passed=2`, `error/missing=180`, `failed/missing=172`.

Named `08e6b905` source checks resolved all current bad-ID source blobs at current `a4e016b6`; 344 files were absent and 26 present at the named tip. Fourteen retained D118 REG14 IDs are preserved in `per-id.tsv` and all are current FAIL.

The retained REG14 evidence preserves the original pristine `26621` and independent `1307` comparisons; this actual run does not close REG14. The operator's D134 START NOW receipt is present. No independent C0 request/response packet was retained for caller-contract behavior validation.

Actual XML, raw runner receipt, and start/stop disk witness were unavailable after finalization. XML-level duplicate/collection/subtest checks and final source custody are therefore UNKNOWN/NOT PASS. No product/pristine tests, body, collection, dry run, retry, or alternate route was executed.
