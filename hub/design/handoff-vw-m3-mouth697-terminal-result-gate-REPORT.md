# Corrected 697px partial-mouth terminal-result audit

## Verdict

**APPROVE the component-level result.** The rehydrated Agent checkout is present at
`/home/user/work/wt/vw-m3-mouth697-clean-source-descendant`, clean, and at
`ef4ebb23ded522c41569eb2355ee7f4a465aa4cd` (tree
`604e4c1b808e395bde56b1068f4460774942425e`). No grant or capture was created
by this audit. The manager supplied the fresh grant and queued exactly one
central run; its terminal result is PASS.

## Source and scope audit

- The descendant of `ee71010a0947edcbbacbf8178e5fee11ab6bab3d` adds exactly five
  test files: the partial capture/test and its three capture helpers.
- Presenter product blobs are unchanged between the base and `ef4ebb23`.
- The corrected controller SHA256 is
  `005b01bc3ed95a7da5ee5f6e5035fda27db30d66357d90ee5eafd38c813a84fb`.
- The manifest SHA256 is
  `8d3d3d2842b88516725a799ea5a8a10f4c178f86ffaf205857769686eea9694a`.
- The reviewed patch SHA256 is
  `9624922e36ff9668d2458704368a16ea87d4e82551959e46d9e0b197ca122d5c`.
- The exact `ef4ebb23` source SHA256s are: presenter `component.tsx`
  `b1dea928a4c709e1148525ceb88c704952b93fdf6f2b89c49e6e668afb7e84cc`,
  `motion.ts` `00b60482093b5f5ead7179bd81689afcc671502f40f38059432d5087634c7701`,
  `scene.ts` `4cde365dd358ac02eafca9a59f565a96fe8e204f68b955b51c6b260441e46e50`,
  and `element.yaml`
  `7bbcb59775818bda4d0cdc58e364256139d904901ce87bcc7263c8ee80afe156`.
- The five added test SHA256s are: `presenter_crop_capture.mjs`
  `43e25df018d921c23762e67cb7ffc73facece9089826432bfabd14a24d10255e`,
  `presenter_crop_capture.py`
  `93879653a8de7ef68f0d46b029b0a148846f2e89a5f25d9c4cc530ea71ec1d9e`,
  `presenter_crop_entry.mjs`
  `5223ef4ecf007124920773bef10a9f543749cd07c943e5143720837f18e29947`,
  `presenter_crop_partial_capture.mjs`
  `ef567b58087484a210b7562f2c1745b476147bd1eccb4ef639284d455624e535`,
  and `test_presenter_crop_partial_physical.py`
  `3915572204a2e8f3ba6247d0115c6b0ce7a6163870eae882809dcbc7a1d7e3b7`.

The future run is limited to the registered presenter component and the two
actual frames `[0, 3]`. Its only positive input is raw `mouth: {x: 151,
y: 104}` with width omitted. The private and public compatibility crops must
both be `(298, 202, 339, 219)`, area 697, byte-identical on both PNGs, and
produce identical unchanged statistics. A fresh 20-pixel planted mismatch
must be `20 / 697 > 0.02` for both crops. Default and malformed inputs remain
source-only unknown/no-inspection controls; they are not fabricated PNG
positives. The prior partial-input 799px controller remains rejected and
unused. The original explicit-width 799px/erase-387px four-still proof is not
replaced or broadened.

## Runtime guards reviewed

The controller binds the exact source revision, source/test hashes, controller,
manifest and patch; checks clean status before `RUN_STARTED`; requires the
fresh manager `REVIEW.md`/`READY_GRANTED`; and performs one-shot pre/post
source, dependency, browser and tool checks with private 0700 temporary cleanup.
The pinned environment is Node `v20.19.4` (SHA256
`43d6cf63f2a460b463eba6b19df5e9a259771c56f11b5130e04178a15bb99490`), graph
`f8164bef…` with 21,488 entries and six peer hashes, public12 with 77 files,
and Chrome `155.0.8059.84-1` with the recorded 255-entry tree. The run must
refuse if normal admission requires stale-root artifact regeneration; this is
component-level evidence only, not Runtime, normal-host, whole-player Gate 6,
root-manifest, deletion, or full-suite qualification.

## Evidence

Manager-run central evidence:

- Test ID: `vw-m3-mouth697-clean-source-descendant-e2e-viewing-mouth697-component-frame-pixels-1020151035-26769`.
- Exact source tree: `604e4c1b808e395bde56b1068f4460774942425e`; source revision:
  `ef4ebb23ded522c41569eb2355ee7f4a465aa4cd`.
- Exact command:

  ```sh
  env -u PYTHONOPTIMIZE PYTHONDONTWRITEBYTECODE=1 ASTRID_CHECKOUT=/home/user/work/wt/vw-m3-mouth697-clean-source-descendant VIEWING_CROP_REVISION=ef4ebb23ded522c41569eb2355ee7f4a465aa4cd VIEWING_CROP_ARTIFACT=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/artifacts/banodoco-timeline-composition-0.0.12.tgz VIEWING_CROP_CENTRAL=1 VIEWING_BROWSER_FLOCK_HELD=1 ASTRID_REMOTION_BROWSER_EXECUTABLE=/opt/google/chrome/chrome flock -x /tmp/timeline-viewing-browser.lock /usr/bin/python3 /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-vw-m3-mouth697-clean-source-descendant-controller.py
  ```

  This was executed through the corrected controller with the fresh
  `REVIEW.md` and `READY_GRANTED`.
- Result: `1 passed in 12.26s`, suite exit 0, controller exit 0, and
  `POSTFLIGHT_OK` contains the exact source SHA.
- The controller's private PNG/metrics scratch was cleaned after postflight;
  no giant raw-RGB/log copy was retained. The existing small explicit-mouth
  archive remains available at
  `viewing-mouth-legacy-public-four-stills-v1.tgz` (10,319 bytes, SHA256
  `e7f32e40aa1aa25d81f30d05fd5ccb83a8a19cd8ce4a5a560e9fd93dc73d7c39`).

This proves only the requested component pixel ROI. It does not qualify root
manifest freshness, normal host admission, Runtime, whole-player Gate 6,
deletion, selected-cut aggregate callers, or a full suite. Do not retry under
this audit or change the source, matrix, denominator, threshold, or controller.
