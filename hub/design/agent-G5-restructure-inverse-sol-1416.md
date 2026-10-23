# R2/G5 inverse investigation 1416 — BLOCKED; diagnosis premise disproved

**G5 DRAFT ONLY; P1 NO-GO. Do not merge this diagnostic branch.** No product
repair is justified by the retained input. The proposed Agent orientation
failure is not present. Both the lossless offline replay and the ONE unchanged
original body on Agent91ac / Runtimecfa fail at the FOURTH native write,
`parent/occurrences`, because Runtime observes physical `shot_revision_id`
pins while Agent's native order captures contain authored rows without those
pins. The first three writes, including `parent/config`, pass the unchanged
sequential before check. Historical503 remains unknown.

## Ownership and changes

Published ownership early: only `inverse.py:apply_inverse/_restore_write`,
`_root_inverse.py` inverse preparation helpers, or `_commit_patch.py` inverse
record construction if causally required, plus a focused new regression.
No product edit was made. `commit.py` (R1 worker1403 execution and redo1404
historical compiler source), every inverse product module, native_restructure,
Runtime, fixtures of the original test, schema, clients, pins and dependencies
are unchanged. No overlapping hunk with redo1404 was taken.

Added only:

- `tests/sdk/fixtures/g5_inverse_retained.json` (377,565 bytes): exact extracted
  request/context, accepted source, predecessor, complete accepted source
  history and refused prepared candidate from immutable packet1358. Original
  event indices: context115, source117, history119, predecessor129, prepared158.
  No fields were projected out of those retained objects.
- `tests/sdk/test_timeline_restructure_inverse_retained.py`: a passing offline
  recorder-orientation reconstruction and an intended-success authentication
  regression that remains RED. It does not assert that refusal is desired.

Harness tmpdir was a pointer file to `/tmp/w-08581704c3`; used that private
scratch path without replacing it (D18 setup interpretation). No Git writes,
shared dependency writes, new executor, root restoration shortcut, source
substitution, pin ignore, fabricated history, guard exception or Runtime change.

## Exact causal correction to 1358 / independent1406

Read PLAN, C0 request/inverse contract, diagnosis1358, review1406 and the
Runtime1406 leaf/redo handoffs. The original packet SHA-256 matches
`01ccdec35f2a8f3e72e99541092f99ec20bda2de036adc6fe77d7f773157aaeb`.

| Actual immutable boundary | Occurrences | Config SHA-256 |
| --- | ---: | --- |
| Previous flat revision `a58d0cd6...` (event129) | 1 | `3261318905a6bb014857b56b1705960454c99ae9b3e7266dd898cb4867f56115` |
| Accepted split revision `caa332cc...` (event117) | 3 | `e6d3e22782252ab1f325c0013214ad30cd9669bcae8b7502321717371fbff4a9` |

The reports had the digest labels reversed and treated the inverse's prepared
OUTPUT `a58d...` as its accepted INPUT. The full-v2 inverse request and
`prepared.expected_head` both name accepted split `caa332...` / `txn-17252...`.
Re-executing the existing Agent with accepted source history reproduces ALL
native writes and complete authoritative steps exactly, including first write
`e6d3 -> 3261`. No orientation swap is needed.

Offline tracing of Runtime859 and Runtimecfa, and the actual new original-body
run on cfa, locate the same failure at native index3 `parent/occurrences`.
The observed physical rows and claimed authored rows are byte-for-byte equal
after removing ONLY each observed `shot_revision_id`; ordering, membership,
ownership and every other field are equal. This is not a config guard failure.

Precise ownership boundary requiring manager coordination:

- Runtimecfa `runtime_protocol/timeline_commit_auth.py:734–738`
  `_inverse_stage_state` returns the physical aggregate directly;
  `_inverse_stage_boundaries:970–972` compares it to native authored rows.
- Agent `_command_state.py:290–292` reads its authored placement list;
  `:369–379` only permits order writes preserving every authored row;
  `validate_root:282–286` rejects revision fields on native occurrence roots.

Adding physical pins to the native recorder alone would violate the existing
Agent state/order contract and contaminate later inverse reconstruction. A
swap would make the first currently-valid config check fail. Neither is a
bounded causal repair inside the allowed inverse-construction scope. Coordinate
an authenticated native/physical observation representation with Runtime's owner;
keep the sequential before check and all source-pin/identity proofs. No claim
is made that a particular Runtime patch is already approved.

## Offline isolation controls — diagnostic, NOT product acceptance

The exact retained Runtime.validate call is RED on859 andcfa. A scratch-only
control adds the exact existing input `shot_revision_id` to the native order
capture's before/after rows, retaining every authored byte and each side's
original order. The unchanged Runtime validator is then GREEN on both versions.
This control changes prepared record bytes; it is **not** a provider repair,
receipt, production candidate or undo/redo proof, and never enters product code.

Starting from that positive diagnostic control, 13 narrowly focused controls
refuse: native-before, native-after, effect-before, effect-after, publication,
step, ordinal, digest, foreign root, membership, order, native sequence, and
Agent's actual intervening-write A→B→A scan. Full refusal messages and inputs
are in each offline packet. These scratch controls are causal diagnostics,
not credit for passing main-suite production behavior.

## Actual original-body run and origin/closure evidence

Agent parent `91ac58a9fc6f1f752be16c0e4b8a1bf17095acee`, tree
`ac1251cdc911b99d690d303cdd777fe14643bdb1`; Runtime
`cfa0af0d476e6954df041c08d7ef378fd6782932`, tree
`3675f446c82c455ef5635ae725409eb6076a4f83`.

Observer records actual loaded module paths/hashes before/after, complete
requests/keys/replies/history/canonical output, provider contexts and prepared
records. Caller closure preflight retained full local/base/state, `local==base`
and `passed=true`. Original function source SHA-256 before AND after is
`c2711a2d10765828694ee1906d75bdf62a91ed6ac0bbef8e4cb0d823e48ec30d`.
Actual refusal is `validation_error / invalid_records`, mapped to CommitConflict
by TimelineSession.undo, at the first undo. Redo and later overlap portion
were not reached. No new preview, merged-reply, retry or historical503 proof.

## Exact commands and results

Run from `/home/user/work/wt/agt-G5-restructure-inverse-sol-1416`.

ONE original-body invocation, together with new focused tests:

```sh
PYTHONDONTWRITEBYTECODE=1 ASTRID_RUNTIME_CHECKOUT=/home/user/work/wt/rt-pin-cfa0af0d PYTHONPATH=.:/home/user/work/wt/rt-pin-cfa0af0d:/tmp/w-08581704c3 TMPDIR=/tmp/w-08581704c3 /home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -o tmp_path_retention_policy=all -p no:cacheprovider -p g5_observer --timeout=40 --basetemp=/tmp/w-08581704c3/pytest-original tests/sdk/test_timeline_restructure_inverse_retained.py tests/sdk/test_timeline_restructure_guarded_runtime.py::test_restructure_whole_inverse_redo_and_intervening_overlap_refusal
```

Exit1: **2 failed, 1 passed in22.07s**. Original body fails with the actual
native order mismatch. The newly added success regression initially used
strict xfail; the repo's lane guard converted that to a failure (`an xfail hides
the result`). Removed only that NEW marker, preserving the success expectation,
and reran only the new focused file:

```sh
PYTHONDONTWRITEBYTECODE=1 ASTRID_RUNTIME_CHECKOUT=/home/user/work/wt/rt-pin-cfa0af0d PYTHONPATH=.:/home/user/work/wt/rt-pin-cfa0af0d TMPDIR=/tmp/w-08581704c3 /home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider --timeout=40 --basetemp=/tmp/w-08581704c3/pytest-focused tests/sdk/test_timeline_restructure_inverse_retained.py
```

Exit1: **1 failed, 1 passed in1.00s**. Failure is now the actual
`CommitRejected: inverse stage write differs from its sequential input`.
No passing behavior expectation was rewritten, no test skipped, no lane guard
changed, and original body was not rerun.

Offline replay commands (both exit0: actual RED, pin-lift diagnostic GREEN,
13/13 controls refused):

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.:/home/user/work/wt/rt-pin-cfa0af0d /home/user/work/venv-agent/bin/python /tmp/w-08581704c3/offline_diagnosis.py /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-G5-restructure-inverse-sol-1416/evidence/offline-cfa.json
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.:/home/user/work/wt/rt-pin-8592822f /home/user/work/venv-agent/bin/python /tmp/w-08581704c3/offline_diagnosis.py /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-G5-restructure-inverse-sol-1416/evidence/offline-859.json
```

Checks (all exit0):

```sh
PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-agent/bin/python -m ruff check --no-cache tests/sdk/test_timeline_restructure_inverse_retained.py
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=. /home/user/work/venv-agent/bin/python -m mypy --cache-dir=/tmp/w-08581704c3/mypy tests/sdk/test_timeline_restructure_inverse_retained.py
PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-agent/bin/python scripts/vendor_lock.py check runtime.lock.json --producer /home/user/work/wt/rt-pin-34eac004
PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-agent/bin/python scripts/artifact_manifest.py --check
git diff --check
git diff --exit-code 91ac58a9fc6f1f752be16c0e4b8a1bf17095acee -- astrid runtime.lock.json artifacts.json tests/sdk/test_timeline_restructure_guarded_runtime.py
```

Ruff clean. Private Mypy: no issues in1 source file, zero added error identities;
no product baseline change. Vendor lock matches frozen34e; artifacts current;
all tracked product, pins and original-body source equal parent. No full suite,
HTTP/socket/browser/P1P4/native14/V4 or broad matrix run/request was made.

## Durable publication and next step

Worker evidence: `workers/agt-G5-restructure-inverse-sol-1416/evidence/` contains
both pytest logs, observational runner, executable offline reproducer, both
full diagnostic packets, actual original-body packet and manifest. Shared
`design/agent-G5-inverse-1416.manifest.json` names the exact published flat files:

- Actual packet `agent-G5-inverse-1416-actual-a94e094388a4c315.json`, SHA
  `a94e094388a4c3159b25d2f1b2a088a15729142e54113ad01f40f0b0f3ca96c0`.
- cfa offline `agent-G5-inverse-1416-offline-cfa-a141c3702335878e.json`, SHA
  `a141c3702335878e9b964900ec2f3aed9ca5b733ddb9b44bda23389ddc4c0b7c`.
- 859 offline `agent-G5-inverse-1416-offline-859-d57677670e1a2246.json`, SHA
  `d57677670e1a22466dbd93f4e02e9d566b1333b4982e993a75e4d9b38db60e1b`.

Each file is below2MB, byte-equal to worker evidence, JSON roundtrip-equal and
credential-scan clean. Actual source/orientation correction and precise Runtime
comparison hunk are ready for manager coordination. This branch is diagnostic
and RED; no merge request, DONE, product GREEN, or P1 GO is claimed. Reassign
the native/physical observation boundary after reviewing this evidence, then
requalify the original journey on the reviewed repaired pair under a new brief.
