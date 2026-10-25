# D124.4 sampler handoff

Status: source-only handoff complete. No Composition product, test, generated, or pin files changed.

## Custody

The retained D111a result is byte-qualified against Runtime commit
`3c73dd148192e0eaa9cb5c7cf55ba3f62b86ac63`:

- launcher `diagnostics/measure_d111a_native_element.mjs`, SHA-256
  `7f5a9f3363beb2466f4c398a1536930cfd792798816f453a7faad5247e7f329a`;
- in-process sampler `diagnostics/sitecustomize_d111a.py`, SHA-256
  `30b345f07bec70cefdd44c9b8eb57fceda6482dd9e24b1f42df5d4f1b72a0ae7`.

The later retained custody-repair source is Runtime commit
`4b24028b405c0f18ed9f63ee240e6e252393d26e`. It adds explicit once-per-sample
recursive-frame and `deepcopy`/`finite_json` union handling, but has no matching
completed result. Do not combine its source bytes with the qualified 0827
result. Full blob IDs and hashes are in the worker evidence
`source-custody.json`.

P4's existing cross-process observer is Runtime commit `26cc08628…`, with
source hashes recorded in the same manifest. It provides the cross-process
sampling precedent and checkpoint/lost-sample controls; it is not an App
service attach helper.

## Exact supported handoff recipe

1. In the sole App worker, recover the two retained files with `git show` from
   the Runtime repository into a private, relative `diagnostics/` path inside
   that worker. Verify SHA-256 before use. For a byte-qualified replay of the
   retained result use `3c73dd148…`; for a new run requiring the repaired
   once-per-sample dedup logic use `4b24028b…` and label the result new.
2. The sampler is loaded at Python process startup as `sitecustomize.py` from
   a private per-run overlay, with its unchanged `d111a-config.json` beside it.
   Set only the existing diagnostic inputs: `D111A_PROFILE_ROOT`,
   `D111A_REQUEST_MARKER`, `D111A_RUN_ID`, `D111A_SOURCE`,
   `D111A_SAMPLING_INTERVAL=0.02`, `D111_REAL_RUNTIME`, and
   `ASTRID_CHECKOUT`. Put that overlay first on the service process's
   `PYTHONPATH`. Keep raw profile output private and mode 0600.
3. App launches the one authorized tagged tour and owns the service PID and
   lifecycle. Before the element POST, the App-owned controller writes the
   existing marker `active`; after the POST it writes `done`. Bind the profile
   to the process PID plus `/proc/<pid>/stat` birth ticks and the actual
   request boundary, not to guessed wall-clock arrival or a fabricated
   correlation. Capture the exact receipt/outcome privately; publish only safe
   hashes, counts, and timings.
4. Report the complete request aggregate: sample count, 20 ms interval, lost
   samples, observer CPU, request wall denominator, and top inclusive frames.
   Deduplicate recursive frame identity once per request-thread sample; count
   `deepcopy`/`finite_json` as a capped per-sample union; do not add inclusive
   shares or call them self CPU. If the retained aggregate cannot establish
   per-sample membership, write `EXACTMISSING` rather than inferring it.

The existing D111a launcher itself is not the actual-tour attach path: it
imports `/home/user/work/app/tests/e2e/local/support/harness.ts` and calls
`startDirectHarness`, creating a synthetic native Runtime child. It must not be
used to claim App actual-process timing. No retained helper attaches to an
already-running service PID. The App-owned process-start environment seam is
therefore the exact missing prerequisite for an actual-service run; do not
invent a launcher or retry the prior absolute-wrapper route.

## Scope and contract guard

The D111a native request used the existing whole-request `commitTimeline`
shape. The production caller remains unchanged: `api_version`, project and
timeline IDs, base revision/publication IDs, commands, label, step records
(`id`, `label`, `intent`, `tags`, `command_ordinals`, `patch`, `reads`), merge,
reads, dry-run, and `Idempotency-Key`; replies remain accepted/merged with
canonical document, receipt, head, effects, bindings and dependencies, or
conflict head/reason and invalid code/path/hint. Dry-run remains write-free.

The retained native sample measured 235 samples over 6179.286447 ms, zero lost
samples, 141.65898 ms observer CPU, and 4700 ms nominal sampled wall (76.06%
nominal coverage). These are synthetic-harness facts only. They do not identify
the App request's arrival UTC, correlation, lifecycle, or outcome, and do not
explain native 1.75 s versus actual 11251.

See `rt-D124-App-sampler-handoff-1253/evidence/` for the hash manifest,
safe summary, and validation record. No raw stacks, locals, environment,
credentials, request bodies, or private replies are exported.
