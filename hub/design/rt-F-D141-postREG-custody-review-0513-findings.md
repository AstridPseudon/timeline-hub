# D141 final integrated findings

All findings are one-pass and closed.

1. Exact-15 REG source custody: PASS. The retained integrated run is the requested Runtime head and Agent checkout, with 15 collected/passed and no failure/error/skip/xfail. The two source files and the original 38 “bad” cases were not changed. The integrated Runtime delta is exactly the reviewed three blobs: the two TypeScript outputs and `runtime_protocol/upgrade.py`. No full-suite approval follows.

2. P5 applicability: PASS. The original `runtime-d141-p5-cut-1026013331-6934` receipt remains a valid 38/38 proof for the retained P5 scope. The independent path challenge found no changed Agent path at an executed P5 boundary. Runtime’s `tests/conftest.py` and `tests/lanes.py` are the actual collection/lanes modules; Agent’s same-named changed files are not loaded. The only changed Runtime module imported by P5 is `runtime_protocol/upgrade.py`, and its changed `_validate_candidate` hunk is outside the P5 migration caller path. No reproof, new body receipt, or automatic retarget is authorized. App P4 obligations do not change.

3. Producer mapping correction: PASS. The prior `canonical15_artifact_hashes` claim is not a 15-client mapping; it is a REG test-body hash map. The corrected receipt uses the actual 15 entries in Agent `runtime.lock.json`, with every source hash matching the live Runtime manifest and source bytes, and with the manifest byte-identical to Runtime 6a. App’s Runtime lock is a separate 14-entry consumer lock; its overlap and four App-only sources are disclosed. No release/tag/fabricated pin is claimed.

4. C0v2 production caller contract: unchanged and accepted as a documentation/control requirement. The normal caller must supply `api_version`, project, timeline, base pair, command labels, step ordinals, per-step patches and reads, merge fields/atomicity, declared reads, idempotency, `dry_run`, source, rationale, and group. Accepted/merged responses must retain canonical closure, authenticated receipt bindings, effects, dependencies, history, and guarded undo. Conflict must expose reason and head; invalid requests must expose code/path/hint/suggested command; preview must not mutate. The reviewed handoff makes no product, test, fixture, DTO, generated, pin, package, environment, network, Store, cleanup/delete, Git, D130, build/ZIP, or credential change.

## Deferred obligations

Agent full/P4 and any central full-suite decision remain outside this review. The evidence is a custody/applicability finding only; it is not a release or full-suite GO.
