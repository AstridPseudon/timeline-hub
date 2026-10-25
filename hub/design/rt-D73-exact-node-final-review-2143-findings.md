# D73 final independent source review

Result: `FAIL_CODE`; receiving readiness remains `NOT_READY`.

The new Agent checkout receipt is valid and clears the stale missing-Agent
input. The checkout at `/home/user/work/wt/agt-pin-2eca9a1d` is clean at
`2eca9a1da94eb35bb969540e150192ff920ce326`, tree
`888c16e3dbbff2d6827e7ffcfea64208b0e2a5e4`. The four supplied Agent hashes
match. Runtime is clean at `ab1e4f6141987706132916e2da16477f5a019464`, tree
`7d8e77b2f5a4af79305c9212ce5174d3ea9fd657`.

Two blocking candidate-code findings remain:

1. `dry-check.sh` validates `D73_MANIFEST` with `python -m json.tool`, but
   the reviewed launcher parses newline-delimited `key=value` lines. A
   key/value manifest therefore fails the advertised `--source-check` before
   source admission. This was reproduced with an existing launcher manifest.
2. The README says `--controls` exercises the launcher via production `run --`
   argv. `dry-check.sh --controls` only runs the focused pytest file, whose
   helper invokes the launcher with `dry`; no `run --` control is exercised.
   The direct focused test is useful bounded evidence, but it does not prove
   the production mode claimed by the recipe.

The central `suites.conf` has no `d73-ab1e-selected4-exact-nodes` or
`d73-ab1e-fork-exact-nodes` row. The rendered D73 manifest and fresh per-ID
results are also missing. Functional selected4/fork bodies are `NOTRUN`; no
installed route or body pass is claimed.
