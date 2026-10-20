# Agent review of Runtime carrier 83fe

Date: 2026-10-20 UTC

## Decision

**APPROVE — bounded internal source review only.** Runtime commit
`83fe4a1cc8e79ba6db2f06271097a96ff2e7c59a`, tree
`2d9d740ef22eea3b9ec4899bb8e400251bd6d444`, is acceptable as the corrected
private carrier composition against Runtime `16acbb6ef94a6d8e226ccdc351ba0d96e0b09ea5`.
This is not approval to publish, pin, merge, activate, release, or claim the
native Agent/Runtime pair.

The exact Agent counterpart is commit
`3730d0bd51686a1692450359482205df64dcc839`, tree
`3892a10bcffa9bf520b4c79591637cf3259d6724`, with private schema SHA-256
`f80215f272bc2cf302d772d619cb8248108eb597a654e01ab89c3a332204d94f`.
The public `agent-26ef2bbb` floor remains immutable at SHA-256
`a6f1aaa9dfcc31828bd04c908158fd7fd9a825df6c9f88f79b81779273a190ef`.

## Source and boundary review

- The candidate has 16 changed tracked paths relative to `16acbb6`; the
  declared 17-path allowlist is respected.
- An independent blob audit compared every tracked path outside that
  allowlist: **414 paths, 0 mismatches** against `16acbb6`.
- `tests/test_door_transport.py` is byte-identical to `16acbb6`.
- No added xfail, skip, TODO, or HACK marker was found in the candidate diff.
- The generated changes are the private command schema/artifact digests and
  their generated metadata; there is no new HTTP route, DTO, endpoint, ID
  seed, or authority field. Existing `EditCommand.version` carries the
  v1/v2 boundary.

The Runtime carrier checks source-bound materialization as authenticated,
read-only provenance: exact parent/source/owner joins, closure digests,
source membership and item maps, sealed bindings, and request-private
captures are required. `id_map` is checked against the derived join; it is not
an authority source. Native semantic births remain separately recorded and
reserved, while derived allocations have no fake `created` facts. Occupied
shot/item destinations, cross-project identity, archived reservations,
accepted own-slot reuse, and corrupt/missing accepted history remain guarded.
Accepted ledger lookup is first in the normal retry path, before head,
projection, or provider validation.

The Agent counterpart preserves complete public S2 v1 captures (including the
103-read/3-selection placement case), refuses an obsolete private v1 sealed
capture without silently refreshing claims, and succeeds only after explicit
current v2 re-authoring. Existing accepted v1 history retains ledger-first
retry and inverse/redo/restore behavior. The source-bound v2 tests keep the
seven capture facts and reject missing proof, legacy bundles, forged maps,
and semantic-birth conflation.

## Evidence

Executed for this review:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=<private Runtime archive> \
  /home/user/work/venv-runtime/bin/python -B generators/generate.py
  PASS

PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=<private Runtime archive> \
  /home/user/work/venv-runtime/bin/python -B generators/generate.py --check
  PASS

PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=<private Runtime archive> \
  /home/user/work/venv-runtime/bin/python -B scripts/artifact_manifest.py --check
  PASS; bundle SHA-256 3b17151af11c35460aa54d9732f3235bd136dfa7622b795a68a9da622dfb4425;
  manifest SHA-256 9e5915b912b4fb49ff7cca2bc4d43c25473a55a9a5198b562f5276058032dc62

PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=<private Runtime archive> \
  /home/user/work/venv-runtime/bin/python -B -m pytest -q -p no:cacheprovider \
  --basetemp=<private temp> tests/test_timeline_projection_ownership.py \
  -k 'frozen_artifact or current_typed_item_creation_claim_is_accepted_and_reserved'
  PASS: 2 passed, 52 deselected

/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/request-test \
  integration:runtime targeted --files \
  'tests/test_door_transport.py::test_admission_order_host_origin_and_route'
  PASS: 1 passed in 2.35s on current integration Runtime tree
  c431abc5025bcadae5355da8229289af797187ec
```

The private archive was overlaid only with the exact Agent f802 schema; no
repository or shared dependency was modified. The central host check ran on
the current integration tree because live-socket tests must use the central
service; its door-test blob is identical to the candidate/base blob.

Reviewed but deliberately **not rerun** here: the candidate's inherited
carrier-focused result (195 passed, 19 deselected), neighboring socket lane
(209 passed, 11 deselected), and compatibility lane (169 passed). No full
suite, duplicate 195/209 lane, native pair, or native-artifact duplicate was
run.

## Required hold and next steps

Final adoption stays held. Current Runtime `c45cbc6ba3772ac2cebb5a5c94f91be24231e2d5`
adds the 125-line `tests/test_render_native_historical_retry.py` native
historical retry test after `16acbb6`; it must survive composition and be
requalified. The upcoming catalog-promotion source `4c1a1a30a6dfed4b1d0c7674fe6f8bfc23aab15f`
adds the newer-catalog-head prewrite protection (and its positive/negative
tests); the carrier merge must preserve that protection and requalify it
afterward. Do not call this report public/final clearance until that merged
tree is qualified.

The actual Agent `3730` native pair and one matched normal artifact remain a
separate gate. Next: compose 83fe with the current c45 and catalog-fence
changes, run the bounded post-merge checks once, obtain the coordinated
native pair, then request the final public decision.

