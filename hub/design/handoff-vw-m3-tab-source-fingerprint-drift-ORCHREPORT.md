# Handoff — tab source fingerprint drift

At exact source `1b584fb0b249922564f7958aa6b97a2e79c2c0a4`, central preflight
fails before capture because the App's read-only `playwright-core` tree is
version 1.60.0 with 106 entries but hashes to
`caa2b3e5a8d3fbd17d768645b0eae10447319508015f5dbe7368e77d7edf2d93`, not the
frozen `6a78060c81886b7ba6f631d5b1193d50f0362c779f5b2dff2d784a31a6acc46d`.
Complete current path/hash evidence is in the adjacent flat JSON manifest.
The same tree/hash appears in all available App installs. No frozen per-entry
manifest was retained in available ORCH artifacts; the frozen aggregate/count
was not replaced.

The controller also had a real path defect in the six-file Remotion/Player
check: it joined from `node_modules/@remotion` instead of `node_modules`.
The patch corrects that root and adds a six-hash regression. Those six hashes
match the frozen values. The strict Playwright guard and all Chrome/React/
Remotion/Composition/Node/source checks remain intact.

Do not request source READY or browser capture until the manager grants the
repaired qualified environment. No install/shared edit is recommended from
this worker; restore exact frozen Playwright bytes/kinds first.

Patch: `handoff-vw-m3-tab-source-fingerprint-drift-controller.patch`
