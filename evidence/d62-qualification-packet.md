# R-D62 integrated-proof preparation packet (corrected)

Preparation only. This worker ran no test body, HTTP route, browser, full suite,
gate, or central proof. No source, test, generated, pin, kit, or suite file was
changed. The packet is a read-only correction of the prior readonly1512 packet.

## Authority and provenance

The current integrated tuple is the existing Runtime/Agent home pair:

| authority | full HEAD | full tree | status |
| --- | --- | --- | --- |
| Runtime producer (`R_HEAD`) | `e68cf231641db98a72805a586b51ab5c4fae2c16` | `a2cbedd185c7e576e20ed060d993deba17111b78` | `/home/user/work/runtime`, clean |
| Agent consumer (`A_HEAD`) | `68e82c0c2ce621f43ae73aa05fce0d1d0f47a677` | `aa62e96c1231de41cee32c5388592c99ae04345f` | `/home/user/work/agent`, clean |

The Agent lock is legitimate for this current tuple because its
`runtime.lock.json` `source_commit` is the Runtime producer `R_HEAD`
`e68cf231641db98a72805a586b51ab5c4fae2c16`. The lock check is against
`R_HEAD`, never `A_HEAD`.

The committed D62 candidate being prepared for future normal adoption is:

| candidate | full HEAD | full tree | parent |
| --- | --- | --- | --- |
| joined Runtime producer | `e02f3e3d9d972be74450536ec0ee49e8bc51c2ec` | `a095ecbe8b01b0ff0a7825c4c19bbf41120ec3ed` | `6e8ae0142655eb7a6d10083d2d3ae5d434b5c94e` |
| candidate base | `6e8ae0142655eb7a6d10083d2d3ae5d434b5c94e` | `bb35f386027336cbd1ae9baed9f4aa2f04369441` | — |

After normal Agent adoption, the same preflight must set `R_HEAD` to the
documented adopted Runtime producer (normally
`e02f3e3d9d972be74450536ec0ee49e8bc51c2ec`) and require the adopted Agent
lock's `source_commit == R_HEAD`. If a tree-equivalent merge commit is used,
record that documented producer and both full head/tree pairs explicitly; do
not substitute `A_HEAD`.

The candidate is not a current integration defect. Its source union depends on
the exact Agent consumer `9460a44336643291f2ab4d5d5085e7cfc391c495` until
normal home/vendor adoption. The current e68/68e82 pair remains the current
integrated authority while that adoption is pending.

## Correct producer-lock and import-origin preflight

This is the exact current-tuple preflight. It deliberately compares the Agent
lock with Runtime `R_HEAD` and runs from `/tmp` so the shell's current
directory cannot shadow either checkout:

```bash
R=/home/user/work/runtime
A=/home/user/work/agent
R_HEAD=e68cf231641db98a72805a586b51ab5c4fae2c16
R_TREE=a2cbedd185c7e576e20ed060d993deba17111b78
A_HEAD=68e82c0c2ce621f43ae73aa05fce0d1d0f47a677
A_TREE=aa62e96c1231de41cee32c5388592c99ae04345f
test "$(git -C "$R" rev-parse HEAD)" = "$R_HEAD"
test "$(git -C "$R" rev-parse HEAD^{tree})" = "$R_TREE"
test "$(git -C "$A" rev-parse HEAD)" = "$A_HEAD"
test "$(git -C "$A" rev-parse HEAD^{tree})" = "$A_TREE"
test -z "$(git -C "$R" status --porcelain)"
test -z "$(git -C "$A" status --porcelain)"
test "$(git -C "$R" remote get-url origin)" = https://github.com/banodoco/banodoco-workspace-runtime
test "$(git -C "$A" remote get-url origin)" = https://github.com/peteromallet/astrid-agent
cd /tmp
PYTHONDONTWRITEBYTECODE=1 ASTRID_RUNTIME_CHECKOUT="$R" ASTRID_CHECKOUT="$A" \
  R_HEAD="$R_HEAD" PYTHONPATH="$R:$A" /home/user/work/venv-runtime/bin/python -P -c '
import json
import os
import pathlib

import astrid.sdk.timeline.commit as agent_commit
import astrid_runtime_client
import astrid_runtime_client.contract_metadata as client_metadata
import runtime_protocol
import runtime_protocol.contract_metadata as runtime_metadata
from runtime_protocol.timeline_commit_types import HistoryEntry

r = pathlib.Path(os.environ["ASTRID_RUNTIME_CHECKOUT"]).resolve()
a = pathlib.Path(os.environ["ASTRID_CHECKOUT"]).resolve()
assert pathlib.Path(runtime_protocol.__file__).resolve() == r / "runtime_protocol/__init__.py"
assert pathlib.Path(astrid_runtime_client.__file__).resolve() == a / "astrid_runtime_client/__init__.py"
assert pathlib.Path(agent_commit.__file__).resolve().is_relative_to(a)
assert runtime_metadata.SCHEMA_DIGEST == "sha256:4118b1e26d30be43cb1a01649df0065fed6e55a528b8956364df8f4eedb413d2"
assert client_metadata.SCHEMA_DIGEST == runtime_metadata.SCHEMA_DIGEST
lock = json.loads((a / "runtime.lock.json").read_text())
assert lock["source_commit"] == os.environ["R_HEAD"]
assert "recorder_abi" not in HistoryEntry.__annotations__
print("current Runtime/Agent import origins, digest, and Runtime-producer lock PASS")
'
```

For the future candidate tuple, retain the same assertions but use
`R_HEAD=e02f3e3d9d972be74450536ec0ee49e8bc51c2ec`,
`R_TREE=a095ecbe8b01b0ff0a7825c4c19bbf41120ec3ed`, the exact post-adoption
Agent head/tree, candidate digest
`sha256:867f3553ac0ff264300e5a2596b363cdb4c071842eb6570ad461c093d351708b`,
and assert `HistoryEntry.__annotations__["recorder_abi"]` is the optional
`Literal[1, 2]` field. The future Agent lock still compares to Runtime
`R_HEAD`.

The command above was inspected, not executed as a proof. The read-only origin
check used the suite-equivalent `PYTHONPATH="$R:$A"` and observed:

```text
current Runtime: runtime_protocol=/home/user/work/runtime/runtime_protocol/__init__.py
current Agent:   astrid_runtime_client=/home/user/work/agent/astrid_runtime_client/__init__.py
current Agent:   astrid.sdk.timeline.commit=/home/user/work/agent/astrid/sdk/timeline/commit.py
current digest:  sha256:4118b1e26d30be43cb1a01649df0065fed6e55a528b8956364df8f4eedb413d2
candidate Runtime: runtime_protocol=/home/user/work/wt/rt-R-D62-proof-return-1517/runtime_protocol/__init__.py
candidate digest:  sha256:867f3553ac0ff264300e5a2596b363cdb4c071842eb6570ad461c093d351708b
candidate + current Agent: Agent client remains /home/user/work/agent/... and digest 4118...
```

## Direct canonical-15 byte inspection

These are direct `git show REV:path | sha256sum` results, not imported-module
claims. The first column is current Runtime e68 and the second is candidate
base 6e8 / committed candidate e02; 6e8 and e02 are byte-identical for every
listed canonical path. The three overlapping generated Python client files in
Agent 68e82 match the current e68 bytes; Runtime-only canonical paths are not
claimed as Agent files.

| canonical path | e68 / current | 6e8 = e02 / candidate |
| --- | --- | --- |
| `conformance/second-client-core-v1.yaml` | `3a0a5aff4e66435212ba567850a0a27c5555601a33ecbd3ed7e21737948662e3` | `3a0a5aff4e66435212ba567850a0a27c5555601a33ecbd3ed7e21737948662e3` |
| `packages/python/astrid_runtime_client/__init__.py` | `d095328fdfadc0883aa103147eb8be8d91f24de2f5fc81c6a9ac37be1809ecc2` | `d095328fdfadc0883aa103147eb8be8d91f24de2f5fc81c6a9ac37be1809ecc2` |
| `packages/python/astrid_runtime_client/contract_metadata.py` | `51e8ce94a7149f6b3160a6e5e66bafe17c7f94cfd3beb6733bbf8abd63125ab6` | `b42c58a36fff3e3136824492382eb05e983c247e5ca0656b35836e1a4e9ee72b` |
| `packages/python/astrid_runtime_client/generated.py` | `e3f51c05342088bc34a562e17997cbf8ff8065c3df795da1cb6cd374216b51b7` | `952fe98a54c9529af723a029957994efec52821da24a2e9c9c34a8dce99e274b` |
| `packages/python/astrid_runtime_client/timeline_commit_types.py` | `88c67d9eb650b445b8ad04c9011c1f44f1ec5e9f72a4a733050515de7ec0b616` | `6c0d21d3eb87cff2977f9e33a5b4d0da13676c4ebad0df4c935f39106a45b417` |
| `packages/python/pyproject.toml` | `6c15723214b1d240f1e9fbea6692019da4893acc486dabcb74ab28e2efaf879f` | `6c15723214b1d240f1e9fbea6692019da4893acc486dabcb74ab28e2efaf879f` |
| `packages/typescript/package-lock.json` | `bb5b79bd79ddd6c780a16e658763f7d534718a739703abcf809b75b664957d66` | `bb5b79bd79ddd6c780a16e658763f7d534718a739703abcf809b75b664957d66` |
| `packages/typescript/package.json` | `8510b0cb8e15630ef999539e697b4f480e6b640d8c9b56c121fa58b66fb451f3` | `8510b0cb8e15630ef999539e697b4f480e6b640d8c9b56c121fa58b66fb451f3` |
| `packages/typescript/src/contract-metadata.ts` | `1028aaeca1cd15f860994c1e830ba69f55405e648841877eff4d43f466f40c79` | `adedd98ba6672fc1ab7476fccb69b1380fc23f09edd42a80a9b2294182a2e15c` |
| `packages/typescript/src/generated.ts` | `7be7f351d485fdb24a7ebb0329fea7c65037675b11a96c581d33e60a14a581a4` | `7be7f351d485fdb24a7ebb0329fea7c65037675b11a96c581d33e60a14a581a4` |
| `packages/typescript/src/index.ts` | `2d23f8ee1cb38e6b1d3366663887b88a4981ec298d8c8d5a758a62a7ad8cc0e4` | `2d23f8ee1cb38e6b1d3366663887b88a4981ec298d8c8d5a758a62a7ad8cc0e4` |
| `packages/typescript/src/operation-handle.ts` | `3f8c69044a0efd5171290f925b0bc3706495c4c0da0252d0008d8056671fa460` | `3f8c69044a0efd5171290f925b0bc3706495c4c0da0252d0008d8056671fa460` |
| `packages/typescript/src/timeline-commit-types.ts` | `bf4728831e35bdfec96ffa0188feb439f3c89a2aecfa8682925019eba5855470` | `b567dcc623d3b3047b931c4337d9f6688efdfa590c9108c3406d0659fa152674` |
| `packages/typescript/tsconfig.json` | `48bc718286b70c7ff5af00d1adfea37ad7c7f8820d3050117dc9d6aea239181b` | `48bc718286b70c7ff5af00d1adfea37ad7c7f8820d3050117dc9d6aea239181b` |
| `contract/artifacts.json` | `f74b0e3041fe45422e6f4f349ee65401fe7222cacefdfa782aaac59354ff4d20` | `9bbce65e5b8dd4fd7ca1f24105ffb88d341e5d5beb10348e555dda79145c4dd3` |

The complete e68-to-e02 delta is not “no generated source change.” Direct
`git diff --name-status e68 e02` shows the additive schema/client delta plus
the two product files and two new tests:

```text
M contract/artifacts.json
M contract/schemas/timeline-commit.json
M packages/python/astrid_runtime_client/contract_metadata.py
M packages/python/astrid_runtime_client/generated.py
M packages/python/astrid_runtime_client/timeline_commit_types.py
M packages/typescript/src/contract-metadata.ts
M packages/typescript/src/timeline-commit-types.ts
M runtime_protocol/contract_metadata.py
M runtime_protocol/schemas/timeline-commit-bundle.json
M runtime_protocol/timeline_commit_auth.py
M runtime_protocol/timeline_commit_store.py
M runtime_protocol/timeline_commit_types.py
A tests/test_timeline_forward_created_authority.py
A tests/test_timeline_recorder_abi_authority.py
```

The candidate product blobs are `runtime_protocol/timeline_commit_auth.py`
SHA-256 `a0e9b4ad529b4affcbe936eb68a268a040cdb8b7988814e6e657e8ef7bfe3411`
and `runtime_protocol/timeline_commit_store.py` SHA-256
`a2db29e4dbb5ef781d818690647e888b4eb02550c93a3e3d962df161d610d4cd`.
The new test blobs are
`90bfb24667bb7b0faff78ce0cb73d8b91c940fb5e05c1835495d305ff79467bf` and
`676226476f2389aa673a66392a01f26229d5dbd0fb24d386047394d42bcb19c8`.
These are candidate evidence, not current-home adoption evidence.

## Production-path selectors retained for the central proof

The proof must wait for the actual Agent home/normal vendor adoption of the
committed candidate. Running the candidate with the old current Agent would
repeat the known legacy consumer seam and is not a valid D62 integrated result.
After adoption, use these exact existing production and strict-negative
selectors:

```text
tests/test_timeline_history_boundaries.py::test_http_history_keeps_fixed_head_and_distinct_same_revision_edges
tests/test_timeline_history_boundaries.py::test_http_history_scope_auth_and_limits_refuse_without_leaking_data
tests/test_timeline_history_boundaries.py::test_http_dry_run_needs_write_scope_and_reserves_nothing
tests/test_timeline_commit_archive_replay.py::test_http_bearer_scope_and_actor_binding_survive_archived_replay
tests/test_timeline_commit_routes.py::test_commit_route_forwards_full_v2_envelope_and_reply_unchanged
tests/test_timeline_commit_routes.py::test_commit_route_rejects_path_mismatch_before_service
tests/test_timeline_commit_routes.py::test_commit_route_rejects_duplicate_fields_and_nonfinite_overflow
tests/test_timeline_commit_routes.py::test_history_route_passes_authorize_callback_and_exact_shape
tests/test_timeline_commit_routes.py::test_history_authorize_callback_rejects_actor_change
tests/test_recorded_responses.py::test_recorded_retirement_and_canonical_conflict_are_distinct
tests/test_recorded_responses.py::test_product_client_preserves_recorded_errors
tests/test_timeline_recorder_abi_authority.py
tests/test_timeline_forward_created_authority.py
tests/test_timeline_commit_authentication.py
tests/test_timeline_commit_sequential_verifier.py
tests/test_timeline_commit_port.py
tests/test_timeline_history_authenticated_read.py
```

The ordinary empty-bootstrap HTTP selector is intentionally excluded because
its module retains the known first-unsupported-wire acceptance exception; it is
not a D62 PASS selector.

## Existing central route and corrected request/wait operation

Read-only inspection of the actual service files found:

- `tests/suites.conf:34` registers `runtime restore-integration` as
  `env ASTRID_CHECKOUT=/home/user/work/agent PYTHONPATH=$PWD:/home/user/work/agent /home/user/work/venv-runtime/bin/python -m pytest -q`.
- `bin/test-run` validates each `--files` token, then appends it to that
  registered command. The validator requires the first character to be
  alphanumeric, `_`, or `.`, so `--junitxml=...` is not an allowed `--files`
  token. No suite row was changed.
- The historical D61 route at `tests/suites.conf:150` writes the historical
  `recorded-responses.xml` and must not be reused for this proof.

The following is the exact operational request command for the sufficient
existing route. It uses only allowed selectors and records the central result
in the service result directory. Do not run it until normal Agent adoption is
complete:

```bash
REQUEST_STDOUT=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-R-D62-proof-return-1517/tmpdir/d62-request.stdout
/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/request-test integration:runtime restore-integration --files "tests/test_timeline_history_boundaries.py::test_http_history_keeps_fixed_head_and_distinct_same_revision_edges tests/test_timeline_history_boundaries.py::test_http_history_scope_auth_and_limits_refuse_without_leaking_data tests/test_timeline_history_boundaries.py::test_http_dry_run_needs_write_scope_and_reserves_nothing tests/test_timeline_commit_archive_replay.py::test_http_bearer_scope_and_actor_binding_survive_archived_replay tests/test_timeline_commit_routes.py::test_commit_route_forwards_full_v2_envelope_and_reply_unchanged tests/test_timeline_commit_routes.py::test_commit_route_rejects_path_mismatch_before_service tests/test_timeline_commit_routes.py::test_commit_route_rejects_duplicate_fields_and_nonfinite_overflow tests/test_timeline_commit_routes.py::test_history_route_passes_authorize_callback_and_exact_shape tests/test_timeline_commit_routes.py::test_history_authorize_callback_rejects_actor_change tests/test_recorded_responses.py::test_recorded_retirement_and_canonical_conflict_are_distinct tests/test_recorded_responses.py::test_product_client_preserves_recorded_errors tests/test_timeline_recorder_abi_authority.py tests/test_timeline_forward_created_authority.py tests/test_timeline_commit_authentication.py tests/test_timeline_commit_sequential_verifier.py tests/test_timeline_commit_port.py tests/test_timeline_history_authenticated_read.py" >"$REQUEST_STDOUT"
cat "$REQUEST_STDOUT"
```

`request-test` stdout is a result directory and may be accompanied by status
text in captured tool output; it is not a wait-test ID. In a separate shell
step, extract only the returned basename from the directory line and pass only
that basename to `wait-test`:

```bash
REQUEST_STDOUT=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-R-D62-proof-return-1517/tmpdir/d62-request.stdout
RUN_ID="$(sed -n 's#^.*/tests/\([^/[:space:]]*\)/[[:space:]]*$#\1#p' "$REQUEST_STDOUT" | tail -n 1)"
test -n "$RUN_ID"
/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/wait-test "$RUN_ID"
```

This deliberately does not use `R=$(request-test ...) && wait-test "$R"` and
does not pass the captured directory/status text to `wait-test`. If
`wait-test` returns 124, rerun only the wait command with the same
`RUN_ID`; never resubmit the request.

There is no sufficient current registered route for a new durable JUnit XML:
`restore-integration` is sufficient for the selected bodies but has no JUnit
option, while the only registered JUnit route is the historical D61 route at
line 150. The finite normal route proposal is therefore:

```text
UNAPPLIED proposal (do not install here):
runtime d62-integrated-proof env ASTRID_CHECKOUT=/home/user/work/agent PYTHONPATH="$PWD:/home/user/work/agent" PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-runtime/bin/python -m pytest -q -o addopts= -p no:cacheprovider --junitxml=/home/user/work/wt/rt-R-D62-proof-return-1517/evidence/d62-restore-integration-1517.xml
```

Once the owner installs that normal route, the same selector string from the
existing request command is passed with `--files`; the JUnit option remains in
the registered command, not in `--files`. No route was installed or modified by
this worker. The new XML destination is reserved at
`/home/user/work/wt/rt-R-D62-proof-return-1517/evidence/d62-restore-integration-1517.xml`.

The historical artifact remains at
`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-R0-D61-wire-review-1454/evidence/recorded-responses.xml`
with SHA-256
`b5f52c0658ac44c09b9e228cd61cccb9b2d33890e933c84e4cbf1dcc9fdf47c8` and its
recorded result was `16 passed in 2.57s`. The new D62 XML destination is
`/home/user/work/wt/rt-R-D62-proof-return-1517/evidence/d62-restore-integration-1517.xml`;
it does not exist until the deferred central run and must not replace the
historical file. The existing route is sufficient for selector execution; the
UNAPPLIED proposal is required only for durable XML capture.

## v2 request/reply acceptance checklist

The central proof must exercise the production HTTP history/commit path and
strict negatives using the existing v2 contract:

- Request: `api_version`, `project_id`, `timeline_id`, exact
  `base_revision_id` and `base_publication_id`, nonempty `commands`, nonempty
  `label`, `steps` with `id`, `label`, `intent`, `tags`,
  `command_ordinals`, `patch`, and optional `reads`; `merge`
  (`fields|atomic`), request `reads`, `dry_run`, `source`,
  `rationale`, `group_id`, and HTTP idempotency key.
- `accepted` and `merged`: canonical/full receipt, `records`,
  `steps`, dependencies, bindings, effects, history, authoritative
  actor/publisher, and undo information; merged replies include the
  landing-head canonical result.
- `preview`: `would_status` (`accepted|merged`) and `receipt: null`, with
  no durable closure, event, history, receipt, allocation, head, or idempotency
  winner.
- `conflict` and `invalid`: structured `code`, `path`, `hint`,
  `current`, and `suggested_command` in the existing error details; no
  acceptance receipt.
- The only new optional wire field is `HistoryEntry.recorder_abi`, closed to
  enum `1|2`.

## D62 boundary and known gap

The source-only security1511 union covers the candidate authority seams against
the exact reviewed Agent consumer and is not an HTTP or current-home Agent
completion result. The eventual central proof is limited to production HTTP
history/commit, strict negatives, and D62 acceptance after normal adoption.

D62 submission completeness remains a known gap: Runtime does not prove that a
v2 producer's native coverage is complete at submit. The preserved behavior is
that such omissions fail closed at fork/inverse use; no assertion is weakened
and no producer-trust failure is relabeled as PASS. The central proof must not
claim complete native submit coverage.

No new child, overlay, pin, backport, denied-source/schema access, suite
registration, or source/test mutation was made. No preparation changes were
made separately from this packet.

