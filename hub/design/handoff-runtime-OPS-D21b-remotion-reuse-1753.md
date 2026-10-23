# Runtime handoff: OPS-D21b Remotion reuse

Status: private staged candidate; not installed or published by this worker.

The exact candidate and unified diffs are in:

`$ORCH/workers/rt-OPS-remotion-reuse-1753/evidence/`

Files: `make-runtime.candidate`, `request-runtime.candidate`,
`make-runtime.patch`, `request-runtime.patch`, `hashmanifest.sha256`, and
`test_reuse.py`. Full commands, exits, source identities, and limits are in
the worker `report.md`.

The maker computes the authentic Agent commit's `remotion/` tree SHA and
package-lock/package/component identity before lookup/build. It accepts an
existing graph only when the graph marker, source bytes, exact Node 20.19.4 /
npm 10.8.2 markers, installed module lock/component provenance, read-only
files, and artifact manifest all match. The graph key is only the Remotion
tree. It preserves the graph's original Agent build-origin marker and creates
new requested env/suite registration metadata carrying the actual requested
Agent and Runtime checkout/SHA. Receipt fields explicitly distinguish
`requested_agent_sha` from `build_origin_agent_sha` and return the physical
reused graph path.

A missing/changed tree reaches the existing bounded build/refusal path. A
same-tree tampered, incomplete, wrong-lock/profile/engine graph or ambiguous
match refuses closed. Existing 2/3-argument and exact 7-argument request
forms remain supported. The private matrix passed offline; no real build,
network, install, provision, dispatcher/daemon, cleanup, or publication was
performed.

Required next step: independent Luna review, then lead-owned idle/smoke/
UTC-backup/atomic-install/normal-publish. Do not treat this handoff as an
installed-kit or production-graph qualification.
