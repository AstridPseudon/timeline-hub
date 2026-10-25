# D73 exact-node candidate review

Result: `FAIL_SOURCE_ONLY`; candidate remains `NOT_READY`; no functional or
body qualification was performed.

## Source and receipt checks

- Composition candidate HEAD: `68343fb8e72bcdf52eddf132d2010506da9c0018`,
  tree `59cb1533b9334e5247e9b55f1ba831d9aa007fc7`.
- Runtime receipt is present and clean at `/home/user/work/wt/rt-pin-ab1e4f61`:
  commit `ab1e4f6141987706132916e2da16477f5a019464`, tree
  `7d8e77b2f5a4af79305c9212ce5174d3ea9fd657`.
- Selected4 and fork source objects are independently present and match their
  reviewed commits/trees and file hashes, but neither has a normal checkout
  receipt. No Agent source was merged or retargeted.
- Reviewed launcher blob at `375c773449…` matches the author source
  `d70bb370f396f137933d3b8ae3b194588e96e2b1` and SHA-256
  `9f668e398b1ea4cce48a6c610102723e0a3dab27a764be4191015aa7fc4110cd`.
- Both exact Agent origins contain a different launcher blob, SHA-256
  `cec561761cb90adbe94dbcc1b1f6b62afb107f1a90e079c6ce2b823405a072d1`, with
  `export PYTHONNOUSERSITE=1` rather than the reviewed source's two
  `unset PYTHONNOUSERSITE` lines. The candidate cannot claim the reviewed
  launcher while pinning those exact Agent origins.
- Read-only central input hashes match the manifest: `request-test`
  `f839c002…`, `test-run` `0be17b74…`, `suites.conf` `fecaa66d…`.

## Parser and argv checks

`request-test` requires a named suite row before queue creation and requires
`--files` for `*-nodes`. `test-run` takes the row command, appends each
space-separated `--files` token, and executes the resulting command with
`bash -c`. The candidate rows are absent from the current read-only
`suites.conf`.

The three parameterized/ordinary selector forms pass the actual `test-run`
allow-list regex, and the selected4 count is exactly four while fork is exactly
one. No whole-file selector, filter, fallback, retry, or frozen-tuple retarget
was found.

The installed body is not consumable as written:

```text
candidate after `run --`: -o addopts= -m integration -p no:cacheprovider --timeout=45 ...
reviewed launcher run branch: python -P "$@"
private probe: python3 -P -o addopts= ... -> exit 2, Unknown option: -o
```

The supported body prefix must include `-m pytest -q` before the required
`-o addopts= -m integration -p no:cacheprovider --timeout=45` options.

Even after that argv correction, the exact selected4/fork Agent checkouts carry
the old launcher blob, so the reviewed environment correction is not consumed.
Copying the reviewed launcher into either exact checkout would violate source
identity; a receipt-backed source/manifest decision is required.

The runner generates a unique ID in `request-test` but does not export that ID
to the suite command. The candidate hard-codes both `P4_D73_REQUEST_ID` and
the XML filename per suite row. Thus repeated requests overwrite launcher
evidence/XML, contrary to the candidate's per-ID retention statement. A next
installation must bind evidence and request identity through a supported
per-run value (the runner does provide `D66_OUTPUT_DIR`) or receive an
explicitly reviewed runner adapter; no such adapter was invented here.

The source-only disk admission values also do not authorize a live run:
available space was `4,816,785,408` bytes at review time, while `test-run`
uses a 5,000,000,000-byte light-run floor and rejects at or below
4,500,000,000 bytes. The prior source report's 4.6-GB floor/4-GB stop line is
therefore not a live central-run admission result.

## Controls and non-claims

- Launcher source-only controls for positive exit `17`/one call and poisoned
  Agent/zero calls are retained from the prior review, not rerun here.
- Source reviews report original selected4 and fork predicates preserved; no
  selected or fork body was run here.
- Dispatch, schema/source/origin/manifest/lock checks are present in the
  reviewed launcher source, but the four-repository manifest is not rendered
  and no live caller consumed it.
- The v2 request/reply fields (including `api_version`, project/timeline/base
  IDs, commands/select/args, steps/patch/reads, merge/idempotency/source
  fields, accepted/merged/conflict/invalid/preview forms) receive no
  functional evidence from this source-only review.

## Exact minimal supported next installation

1. Resolve the source identity blocker before installation: the frozen exact
   commits do not contain the reviewed launcher, so there is currently no
   supported checkout satisfying both requirements. Obtain an
   orchestrator-approved new receipt-backed source/manifest revision that
   carries the exact selected4/fork test origins plus the reviewed launcher,
   or explicitly revise the tuple. Keep selected4 and fork independent; do
   not copy or silently substitute a launcher.
2. Obtain/render the four-repository manifest from those receipts plus the
   existing Runtime ab1e receipt and fresh App/Composition receipts. Populate
   every launcher-required key; do not guess any path.
3. Install two rows in the central registry, correcting the launcher body to
   start `-m pytest -q`, preserving the exact four/one `--files` selectors,
   `addopts=` clearing, `integration` marker, cache-provider disable, and
   timeout `45`.
4. Bind evidence/request identity to each central run ID, then run only the
   separately authorized selected4 and fork requests. Retain XML, raw runner
   log, source-bound manifest, preflight/body exits, and all test-produced
   receipt/records/bindings/effects/dependencies/history/undo-step artifacts.
5. Recheck disk admission against the central runner before any body request;
   source-only evidence does not clear the live-run floor.

## Commands and results

```text
bash -n <(git -C /home/user/peteromallet/astrid-agent show 375c773449b1c6b477f10c1daff1d9f4704208a2:tools/p4-d73-pinned-launch.sh) — PASS
python3 -m json.tool <prior D73 route source-manifest.json> — PASS
python3 -m json.tool <prior D73 route readiness.json> — PASS
python3 -m json.tool <this review.json> — PASS (after writing)
python3 -m json.tool <this source-manifest.json> — PASS (after writing)
candidate selector regex probe — PASS (3/3)
python3 -P -o addopts= -m integration -p no:cacheprovider --timeout=45 — exit 2 as expected negative control
sha256 verification of request-test/test-run/suites.conf — PASS
sha256 verification of launcher, exact-origin launcher mismatch, and both Agent test files — PASS
git diff --check HEAD^ HEAD — PASS
```

No pytest, request-test queue, HTTP/provider, Runtime/Store, child/core/full,
fixture/profile/acquisition/socket/browser, or live suite was run.
