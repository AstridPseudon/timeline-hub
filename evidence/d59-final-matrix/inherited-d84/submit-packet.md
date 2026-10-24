# D84 private submit packet

Status: PRIVATE PREPARATION ONLY. No installation, registry mutation, source Git write,
request-checkout, request-test, service, P5 body, Composition body, full/core/gate run,
build, ZIP, network fetch, package acquisition, or child was performed.

## Candidate

Successor to reviewed ed39ab99cb6f5026be58cd4d18191d6e87fcd2e2, based on the current
tl/integration Runtime worktree. Durable candidate root:

/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-F-final-D84-core-prep-2207/evidence/candidate

| artifact | SHA-256 |
|---|---|
| submit-final.py | 345c8663dde1379264f913e0b72657dbe0d326aac13571dd5cc1e0700087bcca |
| acceptance-d73.py | 08d69d10a58c8b65ded99165054e6f11e42fcaf9c9c9471b57cdaa2d2d81d8f8 |
| run-final-services.py | 05c5662aa14c3bb288f672421d448335a0b10df659fd58439e6abd296c4c3a97 |
| run-final-delivery.py | cf714b7d6105ddf1bd752f311bb2982896e5b67e4988b4096417e6b30f8237f8 |
| install-final-services.py | 6e7eafca3f31c559e07d85a69ef9ac1f785679f727dad831b005a9cb9c6e01f1 |
| runtime-final-service-rows.txt | be2572c2b4ea888237a8696c15e68505010da4453df93aba9ff876b724e2553a |
| core-inventory.json | 9705979776ebb9182d986e9364a29911fafd04227e817f5f19346e8fd116bb97 |

The reviewed D68 wrapper remains
bae840fad6ea496457a3d6138609ce9d89b0b10825827c94f855257bce6c6779; the installed
delivery builder remains f25dfab13bbfb090bf26cf97a85e59bd4818859f5b974dac94aae7e6f2272708.
The three existing rows remain the only candidate rows; their original P5 14+24 bodies and
Composition 86 membership are unchanged.

## Current read-only inventory (not the final tuple)

At the D73 predecessor source capture, the integration heads were:

| repo | commit | tree |
|---|---|---|
| Agent | 8a2f5bb4f87d299bf418c5dc88bf8d32ee165451 | e2a2a7159b7b535c63ab4583fb1492aa0b8e1c97 |
| Runtime | 327da207ed30880fe2ae0cd0b116722bb2c6f7a6 | 0140a9ab2bf8582c4712dbf84498a6d5dcb132cf |
| App | 281c9f1cf98a50e9c0a37e53a47b81e4f0aded77 | 82f8438a5348b6b2e06c318617325cb716174fdb |
| Composition | 635f4de06fda22a85fc2e4cfc764d0153a4c9f40 | 5ab5191a296980a0a6bcd1178ab6902d6478a148 |

These are observation-only facts, not a submitted or qualified final tuple. The future
source and gate tuple files intentionally remain absent; row markers remain
FINAL_TUPLE_SHA256_PENDING and GATE_TUPLE_SHA256_PENDING.

For this D84 inventory-only refresh, the Runtime worktree is now:

| repo | commit | tree |
|---|---|---|
| Runtime | 732c48c6f5a9441a65c61b24595d454a1cd3e180 | 7ed0559c6f0a05954427cc668e303b6cd2f51586 |

This single-repo observation does not capture or select a four-repository final tuple; Agent,
App, and Composition remain the predecessor originals above until the later one-time cut.

## D73 wire, retained unchanged

The production handoff is submit-final.py:

1. Read each of the four /home/user/work/{agent,runtime,app,composition} integration SHAs
   and trees once, with clean-status checks.
2. Queue exactly request-checkout REPO SHA "reason" using the installed helper.
3. Wait for queue/done/checkout-REPO-SHA and verify the receipt path, selected checkout
   HEAD, tree, and clean status.
4. Write the source tuple using those receipt paths and the already-captured SHA/tree values.
5. Only then invoke the installed syntax request-test TARGET SUITE [--files "..."] [--no-cache].
   No current home is resolved after capture. The service runner validates and runs from
   the selected Runtime checkout, so a newer home arriving during the run cannot replace
   the captured tuple; a selected checkout/tree/hash drift is refused.

Normal service-cwd invocation shape after the tuple is selected:

    python3 <candidate>/submit-final.py
      --tuple <candidate>/final-source-tuple.json
      --receipt <private-submit-receipt.json>
      --target integration:runtime
      --suite core-v2-final-integration --no-cache

The generated request is the existing request-test integration:runtime
core-v2-final-integration --no-cache route. Delivery rows retain the reviewed
D68 wrapper and owner extras. No new custody framework or registry route was added.

## Inventory and qualified sources

The successor preserves the old 84 Python selector plus its TypeScript command and the D73
three-file expansion as 87 Python targets. It adds every top-level core test file actually
added to Runtime since the D73 source snapshot, for 92 Python targets total:

- tests/test_timeline_capture_projection.py
- tests/test_timeline_popup_fork_owner_projection.py
- tests/test_timeline_validation_walk.py
- tests/test_timeline_request_verification.py
- tests/test_timeline_lock_placement_limits.py

The last two are the named D84a core tests. The old selector digest is
80ca4630aa83be4e1570074e76dd0be0c701d2d3e02586359592eebc000b618d; the predecessor 87-target
selector and all predecessor source-input bodies remain byte-for-byte unchanged.
The new popup source body is unchanged (SHA-256
16dc1297695bf9203601ff1063953b71c19728c15843c62274f3827683492468).

The two refreshed source inputs are retained verbatim under source-inputs/:

- test_timeline_validation_cost.py from actual qualified 24c61fe2092bf7e40dd060fe561e9612d2978cd0,
  SHA-256 68e27d3a3b703f7c9feb29802078a29ad4840da57f40775d79bcad17e386eeb2;
- test_timeline_schema_resolution.py from actual qualified current 327da207ed30880fe2ae0cd0b116722bb2c6f7a6,
  SHA-256 2283e7169f4f82dafeec0b8d5affd9dca2bf65639dad5a46004d7db27b0d75ae.

The five added live core files are mapped to Runtime 732c48c6f5a9441a65c61b24595d454a1cd3e180
in core-inventory.json with their exact source SHA-256 values. This is an inventory/prose
refresh only; no test body was edited and no new custody or gate was introduced.

## D84a source qualification and release boundary

Runtime structural source 732c48c6f5a9441a65c61b24595d454a1cd3e180 is released and security-PASS.
The release evidence reports 243 targeted tests plus 13 final scope tests, and the corrected
lock-placement proof reports 10 passed. Agent and App remain their own predecessor originals;
this packet does not replace, adopt, or claim their originals passed. The final tuple and gate
tuple remain PENDING, and the historical Agent P4 45s result remains OPEN.

No independent security review was repeated: this change is only current-core inventory/prose
and the same already-guarded private harness. Installation, build, service bodies, P1-P5,
browser/HTTP/provider/render work, ZIP, checkout/child/runtime requests, network, source fetch,
package acquisition, and source/current-head adoption remain deferred behind the D59 cut gate.

## Full v2 request/reply shape retained

The existing request is the full v2 form: `api_version`, `project`, `timeline`,
`base_revision_id`, `base_publication_id`, ordered native or `doc.patch` `commands`, `key`,
`label`, `steps` (each with `patch`, `reads`, `intent`, and `tags`), `merge` (`fields` or
`atomic`), `declared_reads`, `dry_run`, `source`, `rationale`, and `group`. Accepted and
merged replies retain full canonical `data`, `result=data`, `commands`/`idmap`, compiler and
provider versions, steps/dependencies, publisher, base/previous/accepted heads, and the
authenticated receipt/event. Conflict, invalid, and refused replies retain `code`, `path`,
`hint`, `suggested_command`, `head`, and `conflicts`; preview retains the full candidate or a
null receipt. History ABI 1|2, the D62 submit-time gap, and every existing security/budget
predicate are unchanged. No credential, upstream push, M5, or denied-retry path is added.
E/D79 remains paused.

## Current qualification receipts (bounded scope)

The exact `24c61fe2092bf7e40dd060fe561e9612d2978cd0` source is covered by the final
independent security review at
`/home/user/timeline-hub/hub/design/rt-P4-resolver-final-review-1720.md` (1,112 bytes,
SHA-256 `9ef76940ace226b256bfc7377424bc74d02049532190cf211d9dd7c7aa627fb8`) and its
genuine receipt
`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-P4-resolver-final-review-1720/evidence/final-security.xml`
(27,863 bytes, SHA-256
`a9cbbfa209fcd6d3f75c47e79502e40eee9f01f85e7fcbdd67d75e209075efb7`). That receipt
records the targeted suite as **175 passed** in 86.19s, with the review's Ruff,
Pyright, compile, diff, capture, and isolation checks. No full suite was run.

The exact current integrated Runtime source `327da207ed30880fe2ae0cd0b116722bb2c6f7a6`
is represented by the genuine integrated handoff
`/home/user/timeline-hub/hub/design/handoff-rt-P4-resolver-integrated-1728.xml`
(6,003 bytes, SHA-256
`694a5b1e5eb74aa4d785cacede306e65c9dccafeb9e5d5e8de241e0a11a5c7e0`). Its XML
testsuite reports **35 tests, 35 PASS** (`errors=0`, `failures=0`, `skipped=0`).

These receipts establish only their named source and integrated-test scopes; they do
not infer a final gate, whole P4 outcome, or live D73/service qualification. The actual
Agent P4 45s result remains **OPEN**. The predecessor's 174-source, 30-focused, and
9-security-pass counts are historical lineage only, not current qualification. No
unsafe memo is used; the safe-phase harness remains noncore and distinct.

## Acceptance evidence

python3 acceptance-d73.py passed with private fake helpers only: one capture, four checkout
requests and four receipts before request-test; a simulated newer-home-midrun marker was
accepted; a selected-checkout/hash drift was refused before request-test.

The controlled acceptance stub passed with private fake helpers only. The preserved no-install
command was also attempted:

    PYTHONDONTWRITEBYTECODE=1 python3 install-final-services.py
      --registry <ORCH>/tests/suites.conf
      --candidate <candidate>/runtime-final-service-rows.txt
      --builder <ORCH>/bin/delivery-build

It refused before mutation because the live registry is SHA-256
`c21b1b08e1ff86037974ba7e5ceed727842a8a32334c0a8ff6f87357aaa5747a`, while the preserved
predecessor guard is `b0557c15f20fa6de47fc9202f80a4c7533d085611f05c8e1849c3e55239980d3`.
The guard was not retargeted; registry preimage validation is therefore OPEN for the later cut.
No registry bytes changed. Full normative v2 request/reply shapes, including
recorder ABI 1|2 and the D62 submit-time gap, remain inherited from design/commit-v2.md;
this packet does not add a gate or alter product bodies.

## Required next step

At the actual cut, capture the four final SHAs once, request and verify all four exact
checkouts, materialize the concrete tuple/row markers, then submit P1-P5 and Composition
through the existing service route. This packet is not live proof.

