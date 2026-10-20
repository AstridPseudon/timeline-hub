# vw-m3-cache-payload-final-gate

## Decision

**Narrow reject of default production activation; approve the bounded mechanics
only as an owner-gated optional seam.**

The Agent commit `17a13fcfc` is appropriately bounded for an existing cache
entry payload when the same `FrameCaptureCache` object remains the trusted
owner. It does not qualify cross-owner, process-restart, or durable persisted
row reuse. No signing key, certificate, journal, receipt, or new authority was
introduced, and none should be added.

The normal production caller is not a qualifying positive caller today:
`astrid/packs/rendering/actions/timeline_visualize/filmstrip_execution.py:1771`
constructs `RemotionFrameProvider` without `cache=`, so
`composed_frame.py:646` creates a new `FrameCaptureCache` owner for each
filmstrip invocation; the provider is closed after the one pack build at
`:1849-1852`. A payload minted by one invocation is therefore untrusted to the
next provider or process and causes a fresh render. The implementation's
same-owner positive is real, but currently test/explicit-caller scope only.

This also means the default path pays to append and parse payloads without a
normal production reuse benefit. A later provider/process sees the payload,
has no matching `_scene_digests` entry, and deliberately misses; this is the
requested trust boundary but is a regression relative to reusable PNG-only
cache entries if payload writing is enabled by default. Therefore do not
qualify the current default activation as a production performance win.

Recommended owner action: either (a) explicitly provide and retain one shared
`FrameCaptureCache` owner in the normal caller and add a normal-caller positive
plus cross-owner/restart negative proof, or (b) make payload minting opt-in and
leave the normal caller on the existing PNG-only cache path until (a) is
qualified. Keep the old PNG-only fallback, bounds fresh-capture behavior, and
all D09/private fallback holds. Do not delete `visible_at`/private geometry or
invent durable trust.

## Scope verified

- `17a13fcfc` touches only the existing Agent cache/provider and two Agent test
  files: `composed_frame.py`, `test_scene_cache_payload.py`, and the existing
  `test_scene_source_carry.py` proof. The Composition worktree is unchanged.
- Fresh payload minting occurs after all requested fresh PNGs are copied and
  after the successful callback retention. The payload binds the existing
  cache key, original PNG SHA-256, source identity, Root basis, address map,
  frame answer, and Root-props digest. Publication remains one existing
  atomic `os.replace`; the whole entry counts toward existing caps.
- The same-owner cache-hit path returns the original PNG bytes without
  re-encoding and restores labels through the public captured rows. Cached
  observations remain separate from `scene_capture`/`fresh_scene_frames`.
- Key/source/Root/basis/address/frame/PNG/row-shape mismatch, malformed data,
  stale/forged rows, changed renderer/input, incomplete batch, and cap
  overflow all miss or refuse as expected. An attacker able to replace both
  disk payload and the owner's in-memory digest is outside the stated bound.
- No Composition evaluator duplication, SDK save-path change, private fallback
  deletion, D09 deletion, or fresh-only scene-capture-fact change was found.

## Tests

Prior worker evidence for the exact Agent candidate: **212 targeted tests
passed**, Ruff passed, `git diff --check` passed, and focused mypy reproduced
the same five pre-existing errors on untouched HEAD. No full suite, browser,
real Remotion render, localhost, network, install, or shared dependency/cache
write was run.

Independent isolated reruns from an archive of `17a13fcfc`:

- `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$scratch" /home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider "$scratch/tests/packs/rendering/test_scene_cache_payload.py" -k 'planted_stale_or_forged_entry_renders_fresh or payload_bindings_checked_after_owner_integrity or failed_batch_never_mints_cache_payload or payload_counts_toward_existing_cache_caps'`
  — **22 passed, 15 deselected**.
- `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$scratch" /home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider "$scratch/tests/packs/rendering/test_scene_source_carry.py" -k 'mixed_cached_and_fresh_batch_has_facts_only_for_observed_frames and transport'`
  — **1 passed, 58 deselected**.

An initial unscoped neighbor selection also attempted the native parametrized
case and errored because the isolated environment intentionally had no
provisioned Remotion Node peers; the transport-only rerun above is the valid
non-browser result. Native, browser, and full lanes remain unverified.

## Unqualified boundary

Cross-owner cache reuse and process-restart reuse are **UNQUALIFIED**. The
Composition evaluator/package is not part of this candidate and was read only
for seam confirmation; no Composition test or package change is claimed.
