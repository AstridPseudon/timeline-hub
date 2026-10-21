# Runtime ordinary-only transition source review — public018

Date: 2026-10-21 UTC

## Verdict

**SOURCE ACK — bounded ordinary-only source/tree/schema review.**

The exact committed Agent source `47b716d001b45d38805e03b1a254c3353b5968e9`
(`tree bbb5ffa28eaadcc521ebc85e115f56e7edf3b1ca`, parent current
`b3c96a758`) is accepted as the ordinary source input for the owner-authorized
public018 transition + derived-digest successor track. This is not a
version/publication, freeze/pin, generation, activation, native, HTTP, or
Runtime schema-acceptance claim.

The owner 09:18/09:44 rule remains in force: private017 may join the containing
successor only if independently ready within the same one-hour inclusion
window; no private017 materialization is included or claimed here.

## Exact inventory

| Item | Identity |
| --- | --- |
| Agent commit/tree | `47b716d001b45d38805e03b1a254c3353b5968e9` / `bbb5ffa28eaadcc521ebc85e115f56e7edf3b1ca` |
| Agent parent/current | `b3c96a758c1cfa2a609d1498e0e9ee401b32cc40` / `3467b7bffb0fe6edf9178c9a9de4d446c8ab8857` |
| Complete schema raw/canonical | `9397d5faf66776c0a27d3611def6af42d9526dd965ad60eef11dc52bd3dd3e3a` / same |
| Complete schema inventory | 55 `$defs`, 29 `EditCommand` clauses |
| Ordinary-only floor | `6ba7b51e9518e7fb08b27ad5b7225855276b657d0adebf704dd853f699768f2d`, 55 `$defs`, 29 clauses |
| Runtime read-only base/tree | `b92d3e7a05eec65c142294ef4873edd059e9b31d` / `6abc2f117391de8e7e35c0283f575a002199894d` |
| Runtime ordinary schema | `6ba7b51e9518e7fb08b27ad5b7225855276b657d0adebf704dd853f699768f2d` |
| Runtime bundle schema | `6d707cb84a232f6ecd7e17c09c8722a379bb76b6a9d2869efea691d6bd8366e3` |
| Normal lock | `920f4a3edf3d0e5ce9df5a0b2749f7b02bc2ea7db6fef2ec70db8d02b65be8e7` |
| Normal lock source/producer | `95bd3c5f6d00e9bc8cc8cbe5ef510b68ed660f3c` / `sha256:54205b3ecb55038e416b31af936c9af26afa30dc1b05da16157ee4d861fe05ac` |
| Normal generated client | `astrid_runtime_client/generated.py` = `e2e66babca52a7ff95b8387dd6b36a5e46b4a4085bc9082ea664ab8d054bd468`; `timeline_commit_types.py` = `4b23c46311210f5fa3a5684eceeab2772b30c40b61c623eacf0fcd1183d45457` |
| Agent `artifacts.json` (unchanged) | `81ed2cbfa5ccd16be5b97708052a32c6a2967d6556411a2a8e3d5e483f823ada` |
| Runtime `contract/artifacts.json` | `a902387c6a2315374f7e73511feea47da30191aba831b48820b3864b773a532d` |

The candidate `runtime.lock.json` contains 15 entries. Every candidate locked
byte is exactly equal to the corresponding Runtime b92 producer byte:

```text
astrid/core/timeline/schema/timeline-config.schema.json  f52b82024ecd44a5e6c9c68d5cb326d50d70efe9aaad6f8ac6352ea1c87b97b1
astrid_runtime_client/__init__.py                       78a69901f7c68d67b152410732f1c42dd30954ca07e7b4b9a319d4ddbd9035e6
astrid_runtime_client/contract_metadata.py              cdedeb72880102ff6557320d908eac9068470b5088256c4441514e9d7db40514
astrid_runtime_client/generated.py                     e2e66babca52a7ff95b8387dd6b36a5e46b4a4085bc9082ea664ab8d054bd468
astrid_runtime_client/timeline_commit_types.py         4b23c46311210f5fa3a5684eceeab2772b30c40b61c623eacf0fcd1183d45457
tests/fixtures/runtime-responses/events_page_1_200.json 6aaaabe512589beddddd5ef64f2307c39d365a99565c5a3291a15933a114be0d
tests/fixtures/runtime-responses/events_page_2_200.json d5bffdc93e9939779c92a18c047e70df21711f12e16c345f43f3cbdec5b27eb2
tests/fixtures/runtime-responses/invalid_cursor_400.json 16a1db399e06b8d059472f567a091b4bd579d13d8885595376f61835646bfbff
tests/fixtures/runtime-responses/managed_outputs_200.json 6bcef19aca4ad8d574c60d738b54ba57fce6a3a9d4e1481c6f8f088dd460858d
tests/fixtures/runtime-responses/not_found_404.json 4a40fedbeccd345f24944e4af368c50430593d976a923c12af93ba21faa21af6
tests/fixtures/runtime-responses/publish_conflict_409.json 19d664d035691202da03b22b858456c49983e253c7485a6347baa1cf350eea57
tests/fixtures/runtime-responses/task_admission_201.json 108559a92c9e681e3ade37fa6b567e1eaac3edce221665a07a81c2c2c06bb48c
tests/fixtures/runtime-responses/task_read_200.json cc590c4f7d34820382b684d737f1cdb45eebeb20fbad2d5edda2dadac8ab2829
tests/fixtures/runtime-responses/validation_error_422.json 2a02a9147bc0a8b74727d9c577803b0aca333bd0dd035602dafcf2503b00ff1a
tests/fixtures/visual-boundary-v1.json                 1fc778b42f7a5ef91a1fd8620fd92417131e44f97dd5c6a238c78f13bcabfc55
```

## Bounded delta and semantic comparison

The committed parent-to-candidate allowlist is exactly these eight paths:

```text
astrid/core/timeline/schema/edit-command.schema.json
astrid/sdk/timeline/_clip_scalar_commands.py
astrid/sdk/timeline/_collections.py
astrid/sdk/timeline/_recording.py
astrid/sdk/timeline/_selected_param_authority.py
astrid/sdk/timeline/commit.py
tests/sdk/test_timeline_current_union_schema.py
tests/sdk/test_timeline_transition_schema.py
```

The transition implementation is contract-compatible with approved `1acc` and
the reviewed transition portion of `fcf8`:

- `_transition_set` is AST-identical to approved `1acc`.
- Incoming predecessor selection records same-track membership/order and the
  track boundary; authored seconds and shortest-neighbor-fit checks remain
  unchanged.
- Selected transition IDs and revisions are literal; raw key presence and
  revision identity remain guarded, including no-reference legacy identity.
- `params` remains presence-sensitive; literal null is allowed only when it
  does not destructively remove an existing non-empty/non-null value.
- `clip.set` selected-pack authority retains the reviewed original-P1 and exact
  `schema_source` behavior. Paired `transition` + `elementRef` clear retains
  exact identity checks; transition-only clear preserves unrelated references.
- `_collections.selection_overlap`, `_recording.selection`, selected-P1
  handling, and commit hydration/resolution provide the needed ordinary
  helpers. No helper is missing and no guard is broadened.

The current `b3c` context contributes only preserved current behavior in the
candidate (including current safety/tests); the transition-specific differences
from approved `1acc` are limited to equivalent formatting/docstring wording and
current-context integration. No stale current-file overwrite was found. Added
lines contain no private017 materialization, insertion-order/group, rawOLD,
transcript, or other private feature dependency.

Schema stripping removed only `ClipSetArgs.values.transition`,
`ClipSetArgs.values.elementRef`, the `elementRef` clear enum entry,
`ClipSetArgs.schema_source`, and the transition-specific description. The
reconstructed bytes are exactly ordinary6ba; no unrelated definitions or
operations were removed.

## Evidence and limits

Read-only pure probe passed:

```text
candidate identity/allowlist/schema/floor/15-file normal lock parity/transition helper parity
git diff --check b3c96a758..47b716d001b45d38805e03b1a254c3353b5968e9: passed
```

Reused, without replaying broad tests, the source-window evidence in
`agent-m2-transition-ordinary-complete-source-window-1043-REPORT.md`, Runtime
feature ACK `runtime-transition-1acc-reciprocal-source-1038.md`, and complete
source ACK `runtime-transition-complete-fcf8-reciprocal-1105.md`.

No Runtime pytest, full suite, HTTP/socket, browser, renderer, native,
generation, install, version, pin, publication, or activation run was made.
The current Runtime hold-only carrier remains an activation/publication boundary
and is intentionally not overridden by this source ACK.

