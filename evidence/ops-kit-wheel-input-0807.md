# OPS kit and original wheel input facts

Observed 2026-10-24 UTC, read-only. No product source, lock, wheel, hub
publication, installation, cache, process, or branch was changed.

## Received four-file kit

The normal hub manifest is
`/home/user/timeline-hub/hub/design/runtime-child-kit-live-manifest-0739.md`.
The current normal hub commit is `645ac597d0342b633952d260fb3c96a17a120d31`;
its four committed blobs match the manifest's expected SHA-256 values. The
live ORCH files are under
`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin`.

| file | bytes | SHA-256 | live/publication/HEAD | metadata |
|---|---:|---|---|---|
| `bench_store.py` | 42323 | `ba31adcf5dfbad179dfe08b048c48052cee2083026ec62790659c8cdbbc903bd` | byte-identical | regular, `0755`, uid/gid `0/0`, non-symlink |
| `verify_dependency_seed.py` | 17162 | `8f95cdaee258b87dde8e859e99fb955e9cde91dfeec9e7191f4837a5ced6714f` | byte-identical | regular, `0755`, uid/gid `0/0`, non-symlink |
| `make-child-venv` | 39611 | `6b3e34f9d8abecb7dd0a62f448e8863a76271d273815e1ec82e6c25f94665dbd` | byte-identical | regular, `0755`, uid/gid `0/0`, non-symlink |
| `request-child-venv` | 14380 | `08f1b00a716456ba328ff42ee96f3df60d0dfa5470b36eeafb5d299b3df22fde` | byte-identical | regular, `0755`, uid/gid `0/0`, non-symlink |

No kit staleness was found. This verifies receipt/publication only; it does
not claim provisioning, cache/bootstrap custody, or AgentREADY.

## Sealed lock and retained original wheel

`/home/user/work/wt/agt-OPS-kit-wheel-input-0807/requirements/proof.lock` was
127228 bytes. The before and after SHA-256 were both
`236d5be9894de96ce0483894630d54ee28f65107cd44ebe845940bc68c28c778`, and the
two byte reads were equal.

The physical owner remains
`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-F-wheelhouse-input-0733/evidence/wheelhouse`.
The one inspected archive was:

`jaraco.classes-3.4.0-py3-none-any.whl`

- Physical path: the owner path above plus that exact filename.
- `lstat`: regular non-symlink, mode `0644`, uid/gid `0/0`, 6777 bytes.
- SHA-256: `f662826b6bed8cace05e7ff873ce0f9283b5c924470fe664fff1c2f00f581790`, matching the retained input manifest and lock pin.
- ZIP integrity: `testzip()` returned no error; exactly ten required entries were present.
- Dist-info directory: `jaraco.classes-3.4.0.dist-info`.
- `METADATA`: `Name: jaraco.classes`, `Version: 3.4.0`.
- `WHEEL`: `Tag: py3-none-any`.
- Required `METADATA`, `WHEEL`, and `RECORD` paths were present under that exact dotted dist-info directory.
- `RECORD`: ten rows; every listed member's URL-safe SHA-256 and byte size matched, with the RECORD self-row correctly unhashed/un-sized.

The independently reviewed 0740 finite input report records all 67 original
archive hashes matching the sealed lock, with no missing, extra, duplicate,
version, tag, METADATA, or RECORD failures. The old live verifier's sole
refusal is the authentic dotted dist-info name versus its underscore-only
filename predicate. The corrected helper/source review is not a live
qualification receipt here, so the wheelhouse remains **unqualified** and no
AgentREADY claim is made. No helper was executed, no wheel was copied or
rewritten, and no install/request was attempted.
