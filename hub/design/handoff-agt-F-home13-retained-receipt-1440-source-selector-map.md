# F/R2 retained evidence map

This is a custody record for existing material only. No test or product source
was executed by F/R2. The prior worker's retained log is copied verbatim as
`prior-worker-log.txt`; the three XML files below are exact contiguous lines
from that log, including their terminating newline. They are
**transcript-retained XML**, not original-file custody.

## Prior worker and raw transcript

| Item | Value |
| --- | --- |
| Prior worker | `agt-R2-legacy-inverse-home-1435` |
| Prior Agent head | `68e82c0c2ce621f43ae73aa05fce0d1d0f47a677` |
| Prior Agent tree | `aa62e96c1231de41cee32c5388592c99ae04345f` |
| Runtime fixture | `e68cf231641db98a72805a586b51ab5c4fae2c16` |
| Raw source log | `prior-worker-log.txt` |
| Raw source log SHA256 | `fd9f638b86ab7ca0759e204137bac0c438c0c78063dc9becbbda3f059acfa52f` |

The finalizer record shows that `/tmp/w-bda7eb9404` was removed during
cleanup. The original XML files, lane logs, `hashes-pre.txt`,
`hashes-post.txt`, and `final-verification.log` are therefore absent. Only the
transcript lines and the copied prior worker records are retained here.

## XML byte ranges and outcomes

Offsets are zero-based byte offsets in `prior-worker-log.txt`; lengths are the
exact XML byte lengths (the source XML had no terminating newline). The `line`
is the source log line containing the contiguous XML payload; the following
path label on that transcript line is excluded from the retained XML bytes.

| Retained file | Source log line | Start byte | Length | SHA256 | Outcome |
| --- | ---: | ---: | ---: | --- | --- |
| `transcript-neighbors.xml` | 4011 | 397515 | 1295 | `56f79ece7619cf4116e76c608759a8b6014bbb455a2e9d38b0383a83659d023e` | 6 tests, 0 failures, 0 errors, 0 skipped |
| `transcript-new-legacy-bindings.xml` | 4012 | 398888 | 1280 | `2a8f0b9bc6a9c815734edc8425c52f832a84db2a63346aeddc53433dad0c12c2` | 6 tests, 0 failures, 0 errors, 0 skipped |
| `transcript-original-settled-numeric.xml` | 4013 | 400251 | 400 | `20b2184abadf536394cae074e3bab35b12fb26db44933aab5760a7e7bf0e9f50` | 1 test, 0 failures, 0 errors, 0 skipped |

The 13 recoverable names are:

- `tests/sdk/test_timeline_legacy_inverse_bindings.py:40` — `test_legacy_producer_forward_inverse_and_redo_bind_every_stage_effect` — PASS.
- `tests/sdk/test_timeline_legacy_inverse_bindings.py:76` — `test_legacy_inverse_rejects_incomplete_or_misattributed_effect_binding[missing]`, `[duplicate]`, `[wrongside]`, `[wrongeffect]`, `[wrongphysicalsource]` — PASS (five cases).
- `tests/sdk/test_timeline_producer_guard_runtime.py:149` — `test_settled_numeric_proposal_accepts_retries_after_restart_and_undoes` — PASS.
- `tests/sdk/test_timeline_producer_guard_runtime.py:184` — `test_settled_artifact_mutation_refuses_without_history_or_head_changes[number]`, `[boolean]`, `[reason]`, `[digest]` — PASS (four cases).
- `tests/sdk/test_timeline_producer_guard_runtime.py:204` — `test_settled_proposal_queue_refuses_tampering_preserves_draft_then_accepts_fresh_request[digest]`, `[target]` — PASS (two cases).

## Source and caller map

These are read-only related source paths, with SHA256 values matching the
prior transcript. They are not regenerated or re-proven by F/R2.

| Role | Path | SHA256 |
| --- | --- | --- |
| Agent inverse implementation | `astrid/sdk/timeline/_commit_patch.py` | `05a1ebc6b251c75f4d5dc272598adc295ce5bf5a8c4596ad08497de6676264be` |
| New binding test | `tests/sdk/test_timeline_legacy_inverse_bindings.py` | `877d5b86f132befe12b210396ebc52a777e54970ab9557f06aae327fa15b46e5` |
| Original producer test | `tests/sdk/test_timeline_producer_guard_runtime.py` | `7b23a57e20f123c99c933c7558f8f68cc4c209d22b823f87873ddc1aaa8a6471` |
| Commit service caller | `astrid/sdk/timeline/commit.py` | `4a8c5ffa54d1d76a08d0bc928a37c514ae871e401604ec235aae166ce6728896` |
| Producer batch caller | `astrid/sdk/timeline/producer.py` | `420d44af09fef5f793d34fa0eeddb111bc94b750f58c7466f4d28690268be32f` |
| Queue/flush caller | `astrid/sdk/timeline/sync.py` | `44ace78aa0b38b1c501291ebe27c2e37b6d3afb7018be8c2d33379b4f1f955e8` |
| Runtime auth | `/home/user/work/runtime/runtime_protocol/timeline_commit_auth.py` | `e172f8c56d81e8039570ba5a07fc7121fba623b305e7c7a0b529d90c5dcccb70` |
| Runtime port | `/home/user/work/runtime/runtime_protocol/timeline_commit_port.py` | `0d44b5a5e1e0374239df461cb5094ff4fe5bb70761233efd4e3a65c2b29b0859` |
| Runtime store | `/home/user/work/runtime/runtime_protocol/timeline_commit_store.py` | `4d975505c876731eefafc5c8bf8bb79783c2d5c151392163406b1e971004be99` |

The prior report records the production caller as:
`queue_proposal → flush → producer batch → RuntimeCommitService → inverse validation`.
The read-only source selectors are `astrid/sdk/timeline/sync.py:271,483`,
`astrid/sdk/timeline/producer.py:47`, and
`astrid/sdk/timeline/commit.py:938`.

## Copied-record digests

| File | SHA256 |
| --- | --- |
| `prior-worker-finalize.log` | `09e66b9937054d52480991665d14fea4655c78fc8a5e333678c884685198b5ed` |
| `prior-worker-log.txt` | `fd9f638b86ab7ca0759e204137bac0c438c0c78063dc9becbbda3f059acfa52f` |
| `prior-worker-meta` | `6661ca2306da7ba260e70742007428422ad1642e5ede221f4abf9dd0a1344edf` |
| `prior-worker-report.md` | `8aba0c3bc96e4f9abc0e54803cab6bb4187eb058269b7eac5c72dbc2a652716c` |

