# Farm stage metadata export 1224

Published the existing 1054 stage metadata and six exact d0a sibling source
files as nine flat regular files under the guarded absolute root:

`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/`

The publication-root assertion passed before writing. The worker report has
the complete source-to-destination map, original SHA-256 values, modes, byte
counts, and verification details:

`/home/user/work/wt/vw-m3-farm-stage-metadata-export-1224/report.md`

Published files:

- `handoff-vw-m3-farm-stage-metadata-export-1224-stage-complete-runtime.sh`
  — SHA-256 `24cc758029518075f671b06dffc75582b772f2fc52a5e4b57450b46c08a0c66c`,
  mode `0755`.
- `handoff-vw-m3-farm-stage-metadata-export-1224-stage-manifest.tsv`
  — SHA-256 `b349c5344ec607bc32b0e4711adf317aacd984ce98d3e5a316ba726079bb37ac`,
  mode `0644`.
- `handoff-vw-m3-farm-stage-metadata-export-1224-node-graph-manifest.tsv`
  — SHA-256 `0d9da325991bfed2fda247284adb37885d118a08f5f4fc655128f6b7481c04de`,
  mode `0644`.
- `handoff-vw-m3-farm-stage-metadata-export-1224-d0a-{SceneSurface.tsx,authoring.ts,diagnostics.ts,extension.tsx,identity.ts,runtime.ts}`
  — exact d0a git bytes, each mode `0644`; hashes are recorded in the worker
  report.

The existing kit/lead transport method is git-backed `git archive` piped to
`tar -x` into a new immutable destination, with the existing pinned install
step where applicable. No ordinary local method was available to transport the
large original App graph/dist or retained runtime stage across the farm
boundary. Those exact external paths and hashes are listed for the farm/lead
in the worker report; none is claimed transported here. No product, stage,
shared dependency, marker, test, preflight, browser, install, or farm run was
performed.
