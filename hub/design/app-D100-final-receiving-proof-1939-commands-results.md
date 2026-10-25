# D100 final receiving results

## Receiving identity

- Main source: `42040a9c05ae7105cf88459cad5f0b8b9bf56fd1`, tree `66c0215955332af8ed32ae7d4c17d4f71ccb17d4`.
- Product SHA-256: `018f174004bf9b9c275aa23ef6ceb432ce9d7294d71e3024f96353c25fa808a3` (64 characters).
- D100 test SHA-256: `fcd5f187e185faa2222fb23c69827bd6d8bcbb710fdad131f649973f95e6de37` (64 characters).
- Corrected derivative differs from source1914 in exactly `agent.protected_product.sha256` and `agent.protected_product.required_exact_blob`; original source1914 remains untouched.
- Source-purpose/static review1919 and product-security review1803 are reused exactly as allowed; no semantic review or product repair was performed.

## Candidate27

Exact command:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=/home/user/work/wt/app-D100-final-receiving-proof-1939:/home/user/work/wt/rt-pin-ab1e4f61 ASTRID_RUNTIME_CHECKOUT=/home/user/work/wt/rt-pin-ab1e4f61 /home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider --timeout=45 --junitxml=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-D100-final-receiving-proof-1939/private/candidate27.xml tests/sdk/test_d100_item_birth_boundary.py
```

Result: **PASS**, `27 passed in 2.86s`, exit 0. Runtime was the exact immutable `ab1e4f6141987706132916e2da16477f5a019464` / `7d8e77b2f5a4af79305c9212ce5174d3ea9fd657`; the registered provider route was used.

## Projection receiving delta

After candidate27 PASS, received only `tests/sdk/test_timeline_capture_projection.py` from approved commit `f53b016900c99e46998268e36c7c431ac0eec61e`.

- Byte-exact SHA-256: `6e41a5bba04666275b9e252d7aeb30247a145207da3f9ed14f06b338563a1436`.
- Scoped AST check: PASS, 11 test functions.
- `git diff --check`: PASS.
- Product and D100 test hashes remained exact; only the approved projection file is dirty.

## Own9 projection selectors

Admission at start: `5113278464` free bytes (above the 5,000,000,000-byte floor).

Exact nine-selector command used the same immutable Runtime and provider recipe and wrote only the private XML at `private/own9.xml`.

Result: **FAIL**, exit 1; XML parses as 9 tests, 9 errors, 0 failures, 0 skipped, 27.585s.

All nine selectors failed during setup at the same genuine Runtime/provider seam:

```text
candidate.parent.config.theme_overrides.visual.canvas.fps: must be a finite number
```

This is a setup failure for the exact approved projection source against the mandated Runtime pin, not a passing projection result. No adaptation, retry, alternate pin, browser/native/full suite, or broader test was run.

## Source/caller custody

- Agent provider origin: `astrid/sdk/timeline/commit.py`.
- Registered provider test: `tests/sdk/test_capture_source_runtime.py` registers `load_timeline_commit_provider("astrid")` and calls `service.commit_timeline`.
- Runtime route: `RuntimeService.commit_timeline` through the startup-selected Astrid provider.
- Mounted App route retained from the approved review: `localSaveSession` durable outbox to `DataProvider.commitTimeline`.
- D66 is not relevant to this physical-item custody assertion and receives no credit.
