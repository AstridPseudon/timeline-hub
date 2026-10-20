# Corrected 697px partial-mouth terminal-result audit

## Verdict

**APPROVE conditionally for the one manager-granted central capture, after the
clean-source check.** The rehydrated Agent checkout is present at
`/home/user/work/wt/vw-m3-mouth697-clean-source-descendant`, clean, and at
`ef4ebb23ded522c41569eb2355ee7f4a465aa4cd` (tree
`604e4c1b808e395bde56b1068f4460774942425e`). No grant or capture was created
by this audit. The terminal result is still pending the manager's fresh grant
and queued run.

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

No browser, render, network, install, socket, grant, or test was run by this
worker. The central result, exported flat PNG/metrics and optional small TGZ
SHA remain **unverified/pending**. If the manager-run capture fails, preserve
the failure and actual cause; do not retry under this audit or change the
source, matrix, denominator, threshold, or controller.
