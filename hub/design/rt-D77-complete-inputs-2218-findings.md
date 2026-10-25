# D77 findings

## Verdict: NOT_READY

The handback is complete as a source/input census and preserves the custody
boundary, but it is not a qualified Farm stage/render bundle.

The source call chain is grounded in the actual product code. The normal
entrypoint is the installed `run-astrid` launcher, which invokes
`astrid.omp_agent`; `astrid install` validates the authenticated manifest and
calls `Installer.run`/`Backend.stage`. Stage creates the Agent, Runtime and
VibeComfy source trees, uv environment and locked Python closure, installs
Bun/Node/FFmpeg/FFprobe and OMP, runs frozen Remotion `npm ci`, writes the
service declaration and profile, then the consumer uses the installed
`generic_host --service` / pack-host path. The two D13 selectors are the
preflight and genuine daemon-backed render consumers. A fixture, source
checkout, direct Backend call, or shared dependency is not an equivalent.

## Source and custody decisions

1. D139 is the current tuple. Agent `4c4ee35d…` / tree `d50fd98f…` and Runtime
   `ab1e4f6…` / tree `7d8e77…` are recorded separately from the old D77
   applied Agent `91398e9d…` / Runtime `1daca2a3…` tuple.
2. Old D77 source, child and receipts are retained as historical evidence. They
   are not relabelled as D139 qualification.
3. The guard is limited PASS: Sol1243 authored the helper and Luna1257’s
   independent review records 18 controls PASS. This does not prove live stage,
   installed custody or render.
4. The D139 source census is conditional: 38 import occurrences are not in the
   graph and the filtered scope is undocumented. No source publication or
   installed qualification is claimed beyond that boundary.

## Exact missing inputs

| Input | Missing fact | Owner / supported route |
| --- | --- | --- |
| `ASTRID_RUN` | no installed launcher on Farm | Farm normal installer route |
| `INSTALL_MANIFEST` | no authenticated manifest with exact pins | Farm control plane |
| `UV` | candidate exists but version/pin is unverified | Farm normal launcher/manifest |
| current source receipts | no D139-tied checkout/runtime/child receipt in the bundle | Farm requesters |
| installed profile and seven keys | only created after ordinary stage | Farm installer receipt |
| browser | required `85918a99…` hash has no matching browser | Farm tool/profile owner |
| FFmpeg/FFprobe | required hashes could not be verified | Farm tool/profile owner |
| private roots | program/data/run/result roots have no receipts | Farm owner |
| stage/preflight/render receipts | no stage was started; no installed render | Farm owner |
| finite peak bound | exact source/build/cache/render/backup maxima absent | installer/Farm owner; cannot be guessed |

## Footprint conclusion

The retained `1,168,669,468`-byte staging observation is not a retained peak
sample and does not say whether bytes are apparent or allocated. Exact retained
Runtime and VibeComfy tracked sizes sum to `189,840,133` bytes, yielding the
known-only planning arithmetic `1,358,509,601` bytes before Agent, OMP,
dependency, cache, backup or render quantities. Adding the exact OMP archive
would produce `1,524,776,481` only if it did not overlap the retained
observation, which is unknown. The missing quantities have no authenticated
upper bounds, so the peak remains `UNKNOWN_UNBOUNDED`.

The task’s 4.6 GB source-admission floor and 4 GB stop line are operational
gates, not a peak proof. The older D89 5.2 GB heavy gate is preserved as a
stricter historical admission rule, also not a peak proof. No piecemeal stage
or source acquisition should start while this remains unknown.

## Recommended next step

Farm should obtain one complete current-D139 receipt chain through the existing
normal path, including an authenticated manifest, launcher, runtime/child
custody, installed profile/bindings, browser/tool hashes and a phase-measured
finite peak bound. Until then, leave D77 held and report `NOT_READY`.
