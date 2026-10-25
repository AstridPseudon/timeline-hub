# D77/D117a stage-return decision

Status: blocked before acquisition.

The latest free-space sample is `5,958,463,488` bytes. The strict heavy-start
gate (`>5,200,000,000`) passes. The prior known-only additive is
`1,358,509,601` bytes, leaving `4,599,953,887` bytes. This is only
`99,953,887` above the unchanged `4,500,000,000` inter-phase floor and is not
a complete peak estimate.

The prior actual run reached the ordinary installer path and measured a
`1,168,669,468`-byte private stage root, but stopped before OMP source/native
materialization and Remotion `npm ci`. Those phases have no retained peak
sample. Their archive/extraction, Bun/native, cache, temporary and Remotion
`node_modules` allocation is therefore an explicit unknown. Shared dependency
directories were measured read-only but are not counted as private reuse.

Decision: do not acquire or reconstruct source, do not fetch OMP, and do not
invoke `Installer.run` / `Backend.stage` until a complete finite phase bound
exists. Durable exact custody remains the retained D108 Agent/Runtime patches
and manifest; the worker KEEP note records those paths. No profile, schema,
service argv, installed origin or seven-key claim is made.
