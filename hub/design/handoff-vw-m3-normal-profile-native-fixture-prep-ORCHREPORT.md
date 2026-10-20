# Separate normal-profile native1920 proposal — prepared, not authorized to run

Base verified: `1e13eadfc6ba5f96a1cd570893bd3743fed5f666` (completed headers worker, exit0). Nine NEW test/proposal files only. Original 640 fixture, media generator, comparator, four cases, diagnostics, `allHeaders()` observer, existing config and seven final fda6 product paths are byte-identical. No product change, replacement of a passing behavior, skipped test, install, network, browser/socket/service/render/full/central request, controller or grant. Absolute manager QUIET was absent before CPU batches. No repo REPORT or git mutation.

## Authority and mismatch

Retained central `vw-m3-render-download-blob-proof-e2e-viewing-render-download-blob-diagnostic-1020043712-5716`: exit1, **1 pass / 3 fail**. Codec triage's three saved MP4s are identical `sha256:ba653c490689847a31033babc48dba64f6322549fa2b98b12e615ea58658bbc9`, 1,109,353 bytes, 1920x1080; no new FFmpeg/render/decode was needed. Native MediaError4 remains unresolved. This is **leased b70/9f9/installed8 DIAGNOSTIC**, never current-tuple or M3 evidence.

`profile-authority.py` reads each trace internally and emits only safe projections in `profile-authority.json`; no raw task, token, request headers or snapshot payload is printed/persisted. For EACH export case:

1. The real App POST selects `rendering.remotion`, with output policy `{format: mp4, destination: download, filename: ...}`. No caller inputs/profile/review override. The succeeded admitted spec also has no profile/review override.
2. Read that case's ACTUAL retained parent/shot/internal revision responses, check all payload digests and project identities, and materialize with the exact frozen Runtime `admit_closure`. Apply the existing `store.py:1905` managed registry projection. The resulting canonical `{config, registry}` hash equals BOTH the admitted CAS snapshot reference and authority snapshot digest. The snapshot HTTP body itself was not retained; exact digest reconstruction is the evidence. Initial audit development assumptions about the task envelope and retained body were corrected; no identity expectation was weakened.
3. Snapshot `config.output.resolution` is **640x360**, with no theme override. Run the real unmodified Agent `resolve_render_profile(config, registry)` AND the backend `_canonical_profile(timeline_path, registry, None)` entry: **1920x1080, 30/1**, identical profiles. Python import locations are checked against the exact leased files; no source alias/fallback or stub resolver.
4. Changing ONLY the copied config.output.resolution to 1920x1080 returns the SAME normal profile. A separate resolver control with the existing explicit theme canvas640 resolves640, demonstrating the actual canvas authority; this control is NOT added to the proposed authored fixture or export request. Source heads/file hashes are equal pre/post.

Source path (all read-only): App `useRenderState.ts:889/980` → `renderRouter.ts:959/984/996` reference-only catalog-backed admission → frozen Runtime `store.py:1692/1794/1853/1905/1967` closure/materialized binding snapshot → Agent `core/execution/generic_host.py:6648/6711` snapshot hydration to attempt-local inputs → existing `packs/rendering/actions/render/run.py:413/473` RenderRequest with absent profile → Remotion backend `run.py:1663/1674` `_canonical_profile` / `request.profile or canonical` → shared backend `__init__.py:235` `resolve_render_profile` → `core/rendering/profile.py:99/221/248` theme override canvas, runtime/built-in theme canvas, 1920x1080 defaults. `remotion/src/Root.tsx:122/124/149` selects the same canvas. Existing `tests/core/rendering/test_profile.py:164` expressly names the intentional default1920 (source read, not a new pytest run).

**Decision boundary:** the existing normal default1080 is established; therefore a SEPARATE matching fixture is justified as a proposal. This does NOT demonstrate that the old explicit output640 request is honored. It is demonstrably ignored by this profile authority; the old expectation stays intact. If the manager considers config.output640 a required export-size contract, this fixture must not be accepted as its fix; resolve that product-contract question with the renderer owner first. No settled plan decision was changed here, and no cross-owner product fix is smuggled into the fixture.

The frozen diagnostic Runtime still has its existing materializer; this offline audit calls it to reconstruct that historical run, not a new projector or an endorsement of that path on the awaited current tuple.

## Proposal

Review `tests/e2e/timeline/viewing-parity/normal-profile-native1920.manifest.json` and the nine-file `proposal.patch` in this ORCH directory. `player-export-normal-profile-native1920.proposal.ts` is deliberately NOT a `.spec.ts`: it is not automatically substituted for the four existing cases. Future name is `player-export-normal-profile-native1920.spec.ts`, pending manager decision.

The manifest explicitly enumerates every adaptation: separately authored parent output1920; native Player host/screenshot/raw RGB capacity/dimension guards1920x1080; negative denominator2073600; 2000x1200 host viewport (32px margin, DPR1); and direct source-marker coordinate sampling in native1920 RGB. No compared frame is resized. Input VP8/WebM remains640x360/45frames/1.5s from the ORIGINAL generator; audio source remains44.1kHz WAV. No change to clips, holds, timing, occurrences, gains/fades, media selectors/digests, canonical/task/version guards, admission, host, provenance, source package/browser/codec pins or policies.

The separate fixture/comparator/frame/diagnostics/spec copies intentionally preserve the old files byte-for-byte. A main-suite-style Node test enforces EXACT equality to the originals after ONLY the manifest's enumerated replacements; this makes the review a bounded dimension/import diff rather than divergent test logic. Harness extends the original source/browser/host guards, overriding fixture and viewport only. The original config and all original tests remain executable.

Preserved controls: all FOUR cases; twelve frames `[0,37,44,45,52,89,90,120,121,135,143,164]`; RGB channel2/255 and outside fraction0.001; all12 baseline comparisons BEFORE the frame52 picture-only intervention; unchanged export/task/media/revision checks; source marker readiness, actual Player scale1/DPR1; AAC48kHz/stereo metadata and strict media/auth/abort failures. No tolerance widening or codec/browser/profile selection.

**Audio precision:** these four frame cases have audio metadata assertions, not an independent PCM/negative-audio parity journey. All existing diagnostic wrong codec/rate/channels/missing-audio negatives are preserved and passed against the1920 metadata proof. Do not promote these to an audio waveform parity claim.

## Commands and results

All commands ran in `/home/user/work/wt/vw-m3-normal-profile-native-fixture-prep`. Paths:

```sh
NODE=/tmp/vw-m3-agent-gate-node20.19.4/bin/node
OWN=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-normal-profile-native-fixture-prep

PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=/home/user/work/wt/vw-m3-host-agent-source:/home/user/work/wt/vw-m3-runtime-source-lease2 /home/user/work/venv-agent/bin/python "$OWN/profile-authority.py"
# PASS exit0: all3 exact retained snapshot hashes; both real resolvers; pre/post unchanged.

"$NODE" --import tsx tests/e2e/timeline/viewing-parity/normal-profile-native1920.test.ts
# PASS exit0, 8/8. normal-fixture.log
"$NODE" --import tsx "$OWN/normal-profile-native1920.diagnostics.test.ts"
# PASS exit0, 141/141. normal-diagnostics.log
"$NODE" --import tsx tests/e2e/timeline/viewing-parity/download.test.ts
# PASS exit0, original 58/58. download.log
"$NODE" --import tsx tests/e2e/timeline/viewing-parity/diagnostics.test.ts
# PASS exit0, original 141/141. diagnostics.log
"$NODE" --import tsx --test tests/e2e/timeline/viewing-parity/normal-profile-native1920.test.ts tests/e2e/timeline/viewing-parity/download.test.ts tests/e2e/timeline/viewing-parity/diagnostics.test.ts tests/e2e/timeline/viewing-parity/compare.test.ts tests/e2e/timeline/viewing-parity/authority.test.ts tests/e2e/timeline/viewing-parity/admission.test.ts tests/e2e/timeline/viewing-parity/harness.test.ts
# PASS exit0, seven file-level results. units.log; do not confuse file count with case count.

"$NODE" node_modules/eslint/bin/eslint.js tests/e2e/timeline/viewing-parity/normal-profile-native1920*.ts tests/e2e/timeline/player-export-normal-profile-native1920.proposal.ts --max-warnings 0
# PASS exit0. Initial regex-spaces lint issue fixed without a suppression.
"$NODE" node_modules/typescript/bin/tsc --project "$OWN/typecheck.json" --noEmit
# Exit2: ONLY unchanged tests/e2e/local/support/harness.ts:630 TS2352 clips/never[].
cmp -s "$OWN/typecheck.log" "$OWN/../vw-m3-download-complete-headers-fix/typecheck.log"
# PASS exit0, diagnostics byte-identical to completed predecessor; no new TS error.

"$NODE" node_modules/playwright/cli.js test --config "$OWN/collection.config.mjs" --list
# PASS exit0, four proposal cases, no execution.
"$NODE" node_modules/playwright/cli.js test --config "$OWN/future-collection.config.mjs" --list
# PASS exit0, four cases under exact FUTURE .spec.ts name. future-collection.log.
# The latter used an exclusive, temporary byte-identical copy of .proposal.ts;
# try/finally removed it immediately. No future .spec.ts is left active.

ASTRID_CHECKOUT=/home/user/work/wt/vw-m3-host-agent-source ASTRID_RUNTIME_CHECKOUT=/home/user/work/wt/vw-m3-runtime-source-lease2 TIMELINE_COMPOSITION_CHECKOUT=/home/user/work/composition ASTRID_REMOTION_PROJECT_DIR=/home/user/work/wt/vw-m1-ssr-snapshot/remotion ASTRID_REMOTION_BROWSER_EXECUTABLE=/opt/pw-browsers/chromium_headless_shell-1194/chrome-linux/headless_shell "$NODE" --import tsx "$OWN/verify-sources.mjs"
# PASS exit0: original sourceVersions; both exact77-member Composition8 installs,
# six Remotion/Player targets per consumer, exact leased Agent/Runtime roots/heads,
# original/product/proposal file hashes, identical pre/post. No launch method called.

git diff --check
git diff --exit-code HEAD -- src tests/e2e/timeline/player-export-frame-parity.spec.ts tests/e2e/timeline/viewing-parity/fixture.ts tests/e2e/timeline/viewing-parity/media.ts tests/e2e/timeline/viewing-parity/compare.ts tests/e2e/timeline/viewing-parity/download.ts tests/e2e/timeline/viewing-parity/diagnostics.ts
# PASS exit0, no tracked original/product changes; new-file whitespace also checked separately.
```

`normal-profile-native1920.diagnostics.test.ts` in ORCH is an exact copy of the original diagnostic test source with ONLY the new compare/diagnostics imports, valid native dimension/buffer constants, and absolute import resolution into this worktree changed. All141 original test names/expectations remain, including strict audio negatives. It uses the original mocked Page/EventEmitter unit pattern; no browser or Runtime is started.

## Holds and next steps

No implementation block for the bounded preparation. Actual run remains UNGRANTED. Manager must decide whether to accept this separately named normal-profile fixture and explicitly resolve the output640 contract interpretation, then separately review the codec triage's unresolved native decoding cause. Current source tuple remains awaited; installed8 diagnostic proof cannot stand in for it. After those decisions, manager alone prepares the reviewed combined source, updates an explicit source freeze, re-collects four cases and uses central scheduling if authorized. No controller/grant was created by this worker. No native preview, new saved MP4, frame comparison, PCM comparison, current-tuple/gate6/M3 pass is claimed. DONE means proposal/preparation complete only.
