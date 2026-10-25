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
