# Runtime parent-clip native media-swap path

## Result

The remaining `test_native_parent_clip_swap_route_replaces_parent_media`
strict xfail is a genuine current-pair contract gap. No supported command
sequence in Runtime/Agent integration replaces media on an existing raw parent
clip while retaining its clip ID, opaque fields, track and authored timing.
The xfail stays; no Runtime schema, Agent product, endpoint, DTO, or frozen
reference was changed.

## Evidence and current carrier inventory

The focused test already constructs the intended real path: Runtime creates the
project and timeline, imports old/new real MP4 media, obtains each exact
five-field media selection plus `VerifiedMedia`, bootstraps a parent clip, and
captures a parent swap through the Agent provider. The request is rejected
before acceptance by the current Runtime validator:

```text
invalid CommitRequest: 'parent' is not one of ['shared', 'occurrence']
```

The exact rejection is at `tests/test_timeline_clip_replacement.py:294-300`.
The current Runtime command schema has `occurrence.swap-media` at
`contract/schemas/edit-command.json:1104-1135`, with an occurrence-only
selector and `ownership: occurrence`; it has no `clip.swap-media` case.

The current Agent integration is equally missing the carrier:

- `astrid/sdk/timeline/commands.py:29-72` registers `occurrence.add-media`
  and `occurrence.swap-media`, but no parent swap operation.
- `astrid/sdk/timeline/_clip_commands.py:16-30` explicitly refuses media
  `clip.add` rows, so add-then-delete cannot preserve the original identity.
- `astrid/sdk/timeline/_clip_scalar_commands.py:108-110` exposes `clip.set`
  capture, whose asset operation is an explicit clear; it does not assign a
  replacement media selection. The current generated `Intent` type also only
  permits `shared | occurrence` ownership.
- The old direct `replace_timeline_clip` route is intentionally retired and
  remains under the original strict xfails at the bottom of the target test;
  restoring it would violate the one-command-path decision.

The closest existing positive is the occurrence-native route in
`test_native_clip_swap_is_atomic_cas_and_exactly_replayable` and its neighbors.
It proves real media/provider acceptance, CAS/idempotency, cross-project and
timing refusals, reopen retry, and inverse-relevant guards for an occurrence
clip. It cannot target `parent/clip:<id>` without changing ownership semantics.

## Candidate carrier and exact missing Agent request

The normal Agent 310 source snapshot `310e54840fa5fb8eb7e51bb64ed2c34b7a1063b3`
already contains the minimal bounded carrier (also isolated in Agent branch
`7afcd2dabfe5015ef1bbc9c9fa4e399f2107f90d`,
`tl/agt-m2-parent-media-swap-native`):
`capture_parent_swap_media` emits `clip.swap-media` v1 with
`select=parent/clip:<raw-id>`, exact `old_media`/`media` selections, and
`intent.ownership=parent`. Its handler reuses the media-swap checks, reads the
raw parent row and registry, writes only the asset leaf/new exact registry
binding, and retains the raw clip identity, opaque fields, track and timing.
The reviewed candidate also has guarded inverse behavior for the old/new
selection and target writes. This is source evidence only; it is not the
current public Agent/Runtime pair and was not imported here.

The current integration Agent tree is older than that normal 310 snapshot and
does not carry the operation. The missing current-pair handoff is therefore
precise: retain/carry that already-reviewed bounded `clip.swap-media` operation
into the current Agent successor through the normal command registry/schema
generation and provider path, preserving the existing occurrence operation and
original replacement-positive expectations.
Do not widen `clip.set` to arbitrary asset assignment, make `clip.add` a media
birth workaround, or create a new endpoint/DTO. Runtime can consume the normal
generated schema/pin only after that Agent handoff is paired and qualified.

## Test evidence

- `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD/packages/python" /home/user/work/venv-runtime/bin/python -m pytest -p no:cacheprovider tests/test_timeline_clip_replacement.py -q -m integration -k 'native and not public_http'`
  — **10 passed, 11 deselected, 1 xfailed** (the parent schema gap).
- The same parent test with `--runxfail` — **1 failed**, at request
  validation with the exact enum error above. This confirms the xfail is not
  vacuous.
- Central targeted file run `rt-m2-parent-clip-native-path-targeted-1020155846-15998`
  — **pass**, but its default filter selected only the ten retired-writer
  xfails (`12 deselected, 10 xfailed`), so it is not evidence for the marked
  native lane.
- A direct unfiltered local file run attempted the HTTP test and hit the
  sandbox's socket permission error; no local socket result is claimed. No
  full suite was run.

## Limits

No parent-swap positive was added because the current command/schema carrier
does not exist. No existing inverse path can be qualified for this missing
operation. The Agent owner must provide the normal generated successor and
paired Runtime qualification before this xfail can become a positive; the
original direct-writer tests and expectations remain untouched.
