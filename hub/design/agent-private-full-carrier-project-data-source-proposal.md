# Agent private full-carrier + project-data source proposal

Status: proposal published for Runtime and App2 agreement; no generated client,
pin, release, integration, or native-pair change is included.

## Exact source boundary

- Agent repository: `/home/user/work/wt/agt-m2-full-carrier-projectdata-source`
- Base/private pin: `a53703ce` (`Agent357/613` with the private Runtime952 client)
- Frozen source/schema references remain unchanged: `0a774e4968f5a9728c4ee6b5bbbfe286e26f29a3` / `89ed90ce...` is not this source, and `a53703ce` / `613123b2...` is not relabeled.
- Proposed changed paths only:
  - `astrid/core/timeline/schema/edit-command.schema.json`
  - `astrid/sdk/timeline/_project_data_commands.py`
  - `astrid/sdk/timeline/commands.py`
  - `tests/editing_conformance/test_recipe_m2_project_data.py`
  - the two existing carrier-union tests, updated only for the additive 56/30 inventory and hash proof

## New schema proposal

The proposal preserves all 55 existing definitions, all 29 existing operation
clauses, all 613 carrier branches and the 12 explicit v2 branches. It appends
exactly one v1 operation and one closed definition:

- operation: `project-data.write`
- version: `"1"`
- select: exactly `"parent"`
- args: `ProjectDataWriteArgs` with exactly `target`, `key`, `value`, `mode`
- mode: exactly `"replace"`
- target: extension identifier, max 128 characters
- key: 1–256 characters, non-whitespace at both ends, excluding
  `__proto__`, `constructor`, and `prototype`
- value: finite JSON, retained opaquely
- no `TargetKey`, store, endpoint, DTO, group, or transition addition

Canonical proposed schema bytes:

`39211e63a50b9fb495fdf3feb5beaf0e4d0b4eab9a7e13f4d5f769e0d317429d`

Source-file SHA-256 values for the executable proposal are:

- `_project_data_commands.py`: `aef03cf2bf36a3f18f72cbbb4e0b009f849c9693b40e598f6664a111110e73e0`
- `commands.py`: `302f8ab7130dd618e93d4e8aaab6164f26f5e3d43c961d52ba9ddbc68be0f3cf`

Removing only `ProjectDataWriteArgs` and the `project-data.write` conditional
from this proposal reconstructs the private carrier exactly:

`613123b2760150f9f33e23485516d757359c3eaebfe02d552bc97155309aaad3`

The ordinary/public-v1 reconstruction remains:

`6ba7b51e9518e7fb08b27ad5b7225855276b657d0adebf704dd853f699768f2d`

## Runtime/App2 semantic floor

The operation writes one leaf under `parent.config.app[target]`. Existing
namespace members and unknown nested keys/values are not normalized. Absent,
null, empty, and present values remain distinct for inverse and guards. Disjoint
keys may rebase through a missing/null/empty namespace; same-key ABA, malformed
namespace shapes, dependent later writes, and strict inverse/later dependencies
remain refusals.

The Agent-side limits are: 256 UTF-8 bytes per key, 64 KiB per entry, 128
entries per extension, and 1 MiB total encoded values per extension. App2 keeps
its narrower nested-key and noncanonical-input preflight; native acceptance does
not broaden App behavior.

## Agreement gate

Runtime and App2: please ACK this exact operation/schema/semantic floor before
any normal generation, private pin, or native pair is created. This file is a
proposal only; it records no peer ACK and authorizes no downstream artifact.
