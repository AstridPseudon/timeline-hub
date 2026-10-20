# vw-m3-cache-default-off-final-gate

## Verdict

Approve the owner-held optional seam only; narrowly reject default production activation and any D09 deletion/rollout claim.

Reviewed Agent branch `tl/vw-m3-cache-default-off-source-unit` at `c54433b28`, over mechanics-approved `17a13fcfc`.

## Review findings

- The delta is exactly three Agent files: `composed_frame.py` plus its two focused tests. The Composition worktree stayed clean at `5a4e9b72f`.
- `cache=None` now selects the established PNG-only path (`_cache_scene_payloads = False`). The normal `filmstrip_execution.py` caller omits `cache=`, so its first write has no ancillary public-row payload.
- The new normal regression proves the second normal provider reuses byte-identical PNG bytes without recapture or `host_frames_at` query, and retains the existing address-label fallback. The explicit-cache-owner path remains opt-in and can mint rows only through the existing fresh callback/capture flow.
- The prior owner-memory guards remain unchanged: exact cache key, Root-source digest, original PNG digest, full-entry owner digest, source/basis/address/frame validation, and fresh successful callback. A new owner/process with only the persisted payload still misses.
- No D09 private fallback was cut. No durable store, signature, certificate, journal, receipt, or new state authority was added.
- Practical qualification bound: there is still no normal public-row caller or physical pixel-parity evidence. Do not roll this out by default and do not claim deletion of the private fallback.

## Tests

Private overlay assembled from only the exact candidate rendering/test files and read-only symlinks to existing Agent sources; shared venv was read-only. Final targeted command:

`PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$O" /home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider "$O/tests/packs/rendering/test_scene_cache_payload.py" -k 'test_default_provider_keeps_png_only_cache_reusable_across_owners or test_new_provider_reuses_rows_without_query_or_private_visibility or test_planted_stale_or_forged_entry_renders_fresh'`

Result: **11 passed, 27 deselected** (2 requested normal regressions plus the 10 parametrized stale/forged cases).

Also ran `git diff --check 17a13fcfc..c54433b28`: passed.

The previously reported 95 + 58 targeted results and prior `17a13fcfc` stale/forged evidence were not rerun, per the narrow brief; this delta leaves those tests unchanged. No full suite, browser, renderer, listener, network, install, or shared dependency/cache write was run.

## Recommended next step

Keep the seam owner-gated and default-off. A future default activation needs a retained normal cache owner, a normal public-row positive, cross-owner/process negatives, and physical parity evidence before any rollout or fallback deletion claim.
