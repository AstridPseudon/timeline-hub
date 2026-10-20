# Explicit Chrome155 parity environment — CONDITIONAL READY, NO GRANT

Environment-only patch against App 1e13eadfc6ba5f96a1cd570893bd3743fed5f666. Original playwright.viewing-parity.config.ts remains unchanged and defaults to Chromium141. The separate playwright.viewing-parity.native-codec.config.ts selects the named native-codec-chrome155 project through finite validated project metadata. Both collect the same four original tests; no global browser environment variable or fallback is supported.

Prepared run-native-codec-parity.mjs and setup-native-codec-parity.sh are for a future manager-only central run. No suite is registered/submitted. No grant or one-shot exists. READY means bounded preparation complete, never browser/render approval.

The controller contains an explicit frozenDimensionUnitReady=false HOLD. The current isolated candidate intentionally still has the original 640 fixture, with all native-size checks unchanged. A grant cannot override that hold. Manager must review BOTH this environment and the separately owned normal-profile-native fixture proposal, obtain the orchestrator's environment approval, combine only final reviewed patches, bind the reviewed dimension fixture/config identity in place of the hold, and freeze that exact combined candidate. Do not simply toggle the boolean to run the old 640 fixture. No adoption of a running worker branch occurred here.

After final review, update the controller's exact base/baseTree/App fingerprint and concrete final config/fixture checks, then run --freeze and --verify-sources on that reviewed combined source, inspect source-freeze.json and source-preflight.json, and collect exactly four intended cases. Freeze records complete Chrome155 directory (255 files), CPU export browser directory (12 files), Playwright directory (106 files), and full Node executable SHA256. sourceVersions verifies selected Player ELF full bytes, fixed expected version, CPU export ELF full bytes, both installed Composition77 graphs, both six-file Remotion/Player graphs and package versions. Future browser launch must report exactly 155.0.8059.84. Offline preparation reads package metadata/retained calibration identities; it does not launch the browser for --version.

Keep all selected peer sources leased/clean through finally. Controller pins b70 Agent, 9f9 Runtime, f816 Remotion donor, ff053 Composition repository provenance and installed public8 consumed artifact. This is DIAGNOSTIC, not current Runtime/public10/current tuple adoption or M3 qualification. Full browser graph/package/source checks happen before Playwright/globalSetup and again after any failure; central sourceSnapshot device/inode/.git/content must survive until foreground controller completion. No source fallback, install, retries or relaxed diagnostics.

Only after the above, with managers/viewing/QUIET.md absent, manager may create unique READY_GRANTED__vw-m3-chrome155-native-parity JSON containing nativeCodecEnvironmentApproved:true, dimensionUnitReviewed:true, combinedCandidateReviewed:true, nonempty environmentApprovalReference, profile:"native-codec-chrome155", and app equal to final source-freeze.json.app. Unique one-shot is RUN_STARTED__vw-m3-chrome155-native-parity. Previous grants/markers are not reusable.

Proposed central registration, NOT registered/run by this worker (resolve the final controller path after combining):

```sh
app e2e-viewing-native-codec-chrome155-diagnostic env VIEWING_SOURCE_IDENTITY=leased-b70-9f9-installed8-diagnostic VIEWING_BROWSER_FLOCK_HELD=1 flock -x /tmp/timeline-viewing-browser.lock bash /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-chrome155-parity-environment-prep/setup-native-codec-parity.sh
```

Manager-only future request AFTER both reviews/final freeze/registration/grant:

```sh
R=$(/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/request-test vw-m3-chrome155-parity-environment-prep e2e-viewing-native-codec-chrome155-diagnostic) && /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/wait-test "$R"
```

Require four expected passes, zero unexpected/flaky/skipped, retries0. Native actual MP4/frame positive evidence comes before the qualified negative. Calibration and unit success alone waive no native MediaError or same-case result-preview requirement. Existing task/location/full200/hash/native Blob transfer, ffprobe/full artifact, 12-frame/RGB2/.1%, negative controls and native video currentSrc/metadata/error-null proof remain strict.
