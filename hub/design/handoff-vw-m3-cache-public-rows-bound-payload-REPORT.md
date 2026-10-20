# Bounded D09 cache public-row payload

Base: `4ef1391c2c104d5d11b3a27265035c51be296045`, branch `tl/vw-m3-cache-public-rows-bound-payload`, Agent repo. Ready for Agent-owner gated review; no git mutation performed. This is a bounded cache seam, not D09 deletion or a parity result.

## Implemented

- Only the existing `composed_frame.py` cache/provider and direct tests changed. Read PLAN, COMMON, current Viewing INBOX, the D09 source-witness handoff, its original ten-input/key witnesses, and the mixed PNG-only proof.
- The existing `<key>.png` optionally carries the already-public frame answer, source identity, final Root-props SHA-256, address map and Root basis in a private ancillary PNG chunk. The payload also binds the exact existing cache key and original PNG SHA-256. One existing atomic `os.replace` publishes the complete entry. PNG pixels are not re-encoded; cache reads return the original PNG bytes. The existing caps count the whole entry, including the payload; no sidecar, journal, signing key, certificate or new retention system.
- Payload minting requires the retained successful fresh observer after every requested fresh PNG was copied. Cached rows cannot mint another payload. Existing failed-render/query/missing/extra/copy protections remain. The cache owner remembers only the complete entry digest of its own successful fresh writes.
- A new provider using that same cache owner restores labels through `labels_for_scene`, without a public re-query or private `visible_at`. Cached observations are separate from `scene_capture`/`fresh_scene_frames`; mixed captures keep those facts fresh-only.
- Any changed entry bytes, stale frame, mismatched key/source/basis/address/profile, PNG substitution, malformed row, or absent trusted entry binding yields a miss and fresh capture. Public rows do not authorize a source or certify a revision/candidate.
- Existing PNG-only reads/fallback and bounds-capture bypass remain. The original mixed-cache test keeps its assertions and explicitly seeds a PNG-only entry so that it continues to qualify that separate fallback. No private visibility, geometry, crop, statistics or math was deleted.

## Exact trust bound / qualification limit

A self-contained persisted hash cannot distinguish a forged public row from a real row if a writer can replace both the row and its hash. The original source identity and final Root hash do not independently determine or authenticate the returned rows without reevaluating the scene. There is no trusted durable source-to-row binding in this scope.

The implementation therefore accepts payloads only while the SAME `FrameCaptureCache` object retains the SHA-256 of the complete entry it minted after a successful fresh callback. A new provider sharing that object can hit. A new cache object, even in the same process, and a process restart treat payload-bearing entries as untrusted and render fresh. Default provider construction currently creates a new cache object, so it does not gain cross-provider durable row reuse without explicitly sharing the existing owner. PNG-only historical entries continue to use their existing fallback.

This limit is deliberate and tested. No signature/certificate or persistent trusted ledger was invented. An attacker able to alter live Python memory is outside this bound. Removing all scene metadata from disk after owner loss leaves a PNG-only historical entry, which still carries no public rows and follows the separately preserved fallback; it cannot mint scene facts.

## Evidence

Final targeted lanes: **212 passed**, 52 unselected cases. Native-host and FFmpeg fixture-render paths were excluded; execution/capture-label selection was restricted to direct neighbours. Exact commands, counts and elapsed times are in the flat `handoff-vw-m3-cache-public-rows-bound-payload-commands.txt` alongside this report.

- Cache/provider/labels/filmstrip/SDK neighbours and new regressions: 155 passed, 3 deselected.
- Source-carry lane without native queries: 40 passed, 19 deselected.
- Filmstrip execution and pure capture-label guards: 17 passed, 30 deselected.
- Ruff and `git diff --check`: pass.
- Focused mypy: 5 errors. An identical check using `--shadow-file` on untouched HEAD reproduces all five, with matching error types and expressions; no new focused error.

The new tests cover all ten key/input dimensions: revision, candidate, compiled address map, Root profile, assets, source hash, frame, resolution, renderer environment/source, and renderer identity. They also cover same-attempt-path normalization, new-provider same-owner cache labels with a private-visibility/public-query tripwire, mixed fresh/cached separation, PNG-only compatibility via the existing mixed proof, malformed data, complete-batch minting, and the existing cache caps.

Planted controls replace an entry with another frame, change a public row while preserving key/source/PNG metadata, and substitute different valid PNG bytes while recomputing the on-disk PNG hash and chunk CRC. These all miss: the trusted complete-entry digest detects the mutation. Separate privileged test-only digest substitution isolates the remaining key/PNG/source/address/basis/frame/row-shape checks; production disk readers cannot perform that mutation.

No full suite, central test request, browser, listener, real Remotion render, package installation, network access, shared dependency/cache write, save transaction change, SDK publication change or parallel Root-prep edit. No physical pixel/audio parity claim. Native query cases and full `make check` remain unrun.

## Handoff

Flat patch: `handoff-vw-m3-cache-public-rows-bound-payload.patch`; `git apply --reverse --check` passes against the completed worktree. Commit message is in the assigned worker `commit-msg`; the harness owns the actual commit. Merge through the Agent owner's gated flow only.

Review this as same-owner cache reuse with a documented durable-trust limit. Cross-owner/process-restart public-row reuse remains unqualified until the owning source can provide a trusted source-to-row binding. Keep the PNG-only fallback and all D09 deletion holds until their separate positive qualification and physical parity are complete.
