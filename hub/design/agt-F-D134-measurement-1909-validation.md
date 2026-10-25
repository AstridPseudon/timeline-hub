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
`-n 3`, cleared `addopts`, `-p no:cacheprovider`, and `--timeout=45`. The
authorized suite row changed only the operational bindings and invoked this
byte-identical recipe through `bash`; no selector, filter, deselection,
xfail/skip, assertion, source, package, profile, or environment fallback was
introduced.

## Authorized DRY controls

The ordinary launcher was run exactly twice in `dry` mode. The positive path
passed launcher preflight (`preflight_exit=0`), reached the existing stub,
returned 17, and recorded one call. The poison path stopped at the deliberate
`D73 launcher: agent SHA mismatch` guard with exit 1 and zero calls. Raw
stdout/stderr and launcher records remain in the private scratch directory;
only hashes and safe outcomes are published in `preflight.json`.

## Measurement result

The normal service `agent-agent-core-full-1025191128-18455` admitted one body,
passed the D73 launcher preflight (`0`), and reached terminal body exit `1`.
The measured terminal summary is `8926 passed, 190 failed, 180 errors, 86
warnings, 173 subtests passed` in `1379.05s`. The raw body log and XML remain
private; safe counts, the XML digest, root inventory, and exact-node comparison
inputs are in `outcomes.json`.

The current XML has 9296 unique testcase nodeids plus 173 subtests reported by
the runner but not represented as individual XML testcase elements. Exact
status-pair comparisons against immutable 30693 and retained upstream 924 are
recorded without assigning causes to current-only nodes. Complete finite
per-node accounting is therefore not claimed: `core_open_n` and `reg_open_n`
remain `UNKNOWN` pending independent result/classification review. Retirement
is `0`; this run carries no ship, custody, or release credit.

## Validation commands

```text
bash -n evidence/measurement-command.sh evidence/preflight-command.sh
/home/user/work/venv-agent/bin/python -P -m json.tool evidence/source-review.json
/home/user/work/venv-agent/bin/python -P -m json.tool evidence/source-manifest.json
/home/user/work/venv-agent/bin/python -P -m json.tool evidence/manifest-diff.json
/home/user/work/venv-agent/bin/python -P -m json.tool evidence/preflight.json
/home/user/work/venv-agent/bin/python -P -m json.tool evidence/readiness.json
/home/user/work/venv-agent/bin/python -P -m json.tool evidence/missing-inputs.json
git diff --check
```

The source/evidence checks above passed before submission. Post-terminal JSON
validation and XML count/hash extraction also passed. No own Python,
TypeScript, or production code was added, so compile, Ruff, and typecheck lanes
are not applicable.

## Gate disposition

D128's child-maker custody refusal remains immutable and is not a route for this
worker. The measured core result is retained for independent Luna result and
classification review only; it provides no ship-grade custody or release
credit.
