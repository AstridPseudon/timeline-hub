# Served PCM guard-fix report

## Result

Prepared a review-only flat handoff for the two defects identified in the
served-PCM controller review. No tracked repository files changed.

Frozen artifact hashes are recorded in READY.md:

```text
controller.py  72f5c85e73082e068b2898e62ce33ce3bb6733129f929eb9333e8de734f63c3e
fixture.py     2298b10a512fe5b32a6ba20ed5b806a189ed4e6a065f125833bc91709b734ba8
regressions.py d7aa4ee955aca24bc72f48ff2a0cb805e4df41f97c88fd853a3575135c9f17d5
```

### Controller

- Added `git status --porcelain=v1 --untracked-files=all` source cleanliness
  enforcement, closing the untracked-import gap while retaining the tracked
  diff check and exact approved source tree check.
- Added a `run_test` finally path that repeats `preflight` after pytest. This
  revalidates source tree/status, normal producer presence, all three helper
  bytes, the immutable release12 archive SHA and exact 77-member installed
  package graph, peer versions, Node version, and the inherited environment
  projection.
- Postflight failures are printed explicitly. A successful pytest becomes
  failure on postflight drift; a nonzero pytest return code is preserved.
- Updated the controller prefix and temporary owner path to this new flat
  handoff. The entry point now propagates `main()`'s return code.

### Fixture

- Added `_validate_invocation_url(url, expected_port)` and made `_get` require
  the expected port.
- Passed `server.port` for original URL reads, prepared URL reads, cleanup
  404 reads, interrupted-consumption reads, and the two ordinary RED phase
  tests.
- Existing positive/nativebytes/forgery/doubleapply/cleanup assertions and
  ordinary RED expectations remain; no product protocol or source authority
  was introduced.

### Pure regressions

`handoff-vw-m3-served-pcm-guard-fix-guard-regressions.py` contains four pure
tests: tracked-only RED versus untracked-aware GREEN, no-finally RED versus
postflight-drift GREEN, arbitrary-loopback-port RED versus live-port GREEN,
and pytest nonzero return-code preservation. It imports only the flat guard
modules, uses a temporary local Git repository, and opens no HTTP listener.

## Evidence

- `ruff check` on the three flat Python artifacts: **PASS**.
- `pytest -q ... handoff-vw-m3-served-pcm-guard-fix-guard-regressions.py`:
  **4 passed in 0.35s** (final run).
- Python compilation of the controller and fixture: **PASS**.
- No browser, socket/listener, full suite, install, central request, or grant
  was run, as required.

## Handoff limits

The seven real served-PCM module cases remain unexecuted here because they are
listener-backed and central-only. The two window/layer cases remain ordinary
RED until the source-owner original-phase join described by the review report.
Manager must freeze the three flat artifact hashes, substitute the final
producer SHA and approved public12 project, register the named suite, and make
at most one central `whole` request.
