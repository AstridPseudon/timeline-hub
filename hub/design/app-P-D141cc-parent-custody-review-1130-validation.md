# D141cc independent custody validation

## Verdict

`FAIL_CUSTODY` for `p2-parent-move@original`. The genuine service result is a body `PASS`, but custody fails F-001; no retry or rerun is authorized.

## Read-only checks performed

- Parsed the admitted worker `meta`, `ended`, `exit`, `progress.json`, `controller-receipt.json`, `results.json`, `source-manifest.json`, `trace-measurement.json`, `sampler-lifecycle.json`, `validation.md`, `handoff.md`, native stdout/stderr, and worker log.
- Parsed both genuine request/snap/status/exit/KEEP trees, `d66/manifest.json`, `collection.txt`, both XML files, summary, `ext`, and TSV traces with Python stdlib.
- Recomputed accepted Sol dispatch index 1 command and row hashes. Both preflight and normal hashes match the recipe.
- Recomputed the builder SHA-256 and Git blob; both match `2032f308…` and `59b65214…`.
- Checked all four pinned checkout HEAD/tree/status values and checkout receipt hashes; all match and are clean.
- Checked both test source SHA-256 values against the pinned App checkout; before/after manifest hashes match, and XML has one test, zero failures, zero skipped.
- Confirmed the parent-controller-next terminal-0 record is `NOTRUN_PREPARED` with no request/body/artifact and excluded it from custody.
- Ran `git status --porcelain=v1` on this Composition worktree; it is clean. No product test suite was rerun.

## Native and service custody

The worker log records one native invocation/session `59630`, exit 0, then the same authenticated normal ID was waited via session `51172`, exit 0. The raw result directory has the expected namespace, matching request/snap source tree, `ext` pins, `status=pass`, `exit=0`, and both KEEP markers. Native stdout names exactly the preflight and normal IDs. No second submit, request recreation, alternate selector, or placement rerun is present.

The accepted Sol recipe names a Sol1047 future-native root, while the admitted run used a parent1121 future-native root. The logged invocation retains the accepted production builder, selector, `--submit` argv, cwd, twelve D66 source-pin bindings, command/row bytes, and native predicates; only private operational paths were relocated.

## Independent disk trace measurements

The admitted worker trace has 72 samples from `2026-10-26T11:21:41.460949605Z` through `2026-10-26T11:27:37.407272522Z`, covering 355.946323 seconds. Gaps are 5.007251–5.027818 seconds (mean 5.013328). Free bytes range from 5,346,643,968 to 5,765,541,888; no sample reaches the 4,000,000,000 stop threshold. The raw normal-service TSV has 50 samples over 236.067 seconds, also with no 4 GB crossing.

The sampler lifecycle records an explicit Ctrl-C stop and reaped exit 1; the worker log shows the stop result followed by the inspection command. This is accepted as later sampler stop/wait/reap evidence. It does not cure F-001: the worker's first sampler tool failed at log lines 2017–2021 because `tmpdir` was a regular file, and the writing sampler began only in the second attempt at lines 2031–2032. The mandated first-tool sampler fact is therefore missing and cannot be historically backfilled.

## Scope

No wire change, source change, test change, generated change, pin change, registry/queue mutation, or merge request was made. This is a finite custody result, not an overall P2/platform GO, final-build, or ZIP claim.
