# M4 delivery gate-results inputs — current 0408 proposal

**Status: DRAFT / BLOCKED.** This is a proposed replacement for the
owner-controlled input at
`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/delivery/gate-results.md`.
It was not copied into that file because the 0408 delivery rehearsal had
already snapshotted its inputs in
`delivery/build-20261021T040409Z/README.md`. The next authorized
`delivery-build` run may use this proposal after reviewing it.
The shared `delivery/gate-results.md` and that completed snapshot were not modified by this worker.

This is gate-results data only. It is not a README, packer change, release
result, final ZIP, foundation-complete claim, or all-gates-green claim.

## Builder input authority and source boundary

The existing builder is
`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/delivery-build`.
Its `GATE_RESULTS` constant reads the shared `delivery/gate-results.md` file
when rendering a README. The current carrier SHA-256 is
`3dfd5c28a9be9ab809e6c1fe1e9a83fbf8417ea888afc1b10eec5f751023e990`.

Published014 remains the normal Runtime producer and lock authority:

- Runtime producer: `95bd3c5f6d00e9bc8cc8cbe5ef510b68ed660f3c`, tree
  `d3a290b407fa61e6ab2d476f50c068073f70df00`, protocol/client `0.2.14`.
- Published artifact producer/version SHA-256:
  `54205b3ecb55038e416b31af936c9af26afa30dc1b05da16157ee4d861fe05ac`.
- Current compatible Runtime server: `b92d3e7a05eec65c142294ef4873edd059e9b31d`,
  tree `6abc2f117391de8e7e35c0283f575a002199894d`. This is a descendant
  server source, not a new publication and not a replacement producer.
- Adopted normal consumer pins: Agent
  `091aa23ec83ea05ffd3b0115a640230d51c8c429`, tree
  `e3ae90fe482ba6cad6c3f94069127faf76ebceb6`; App
  `3be3c116610c4ffdf019cba447464280fd7b8e06`, tree
  `d030e4b8b41a1d5ec46de1c0c245111cafa7e98a`; Composition13
  `7bb54bbd64107e5090643ecca1e4d33164173e85`, tree
  `20467712e66dbadff4d562c0d5baae22b8c077a7`.

The completed 0408 rehearsal used current integration descendants, not the
short adoption refs above: Agent `7ab6cbae273f133b3adf2a7bae9f2439f02ce71e`
(tree `075339b2c6d5e57c1b0e76754457d053b51edf2c`), Runtime `b92d3e7a…`
(tree `6abc2f117391de8e7e35c0283f575a002199894d`), App
`1557c312b999ddc0a21c1728acbc64052ef6491f` (tree
`cf94daef960fe1426f6f50e4000b00c0fc42867e`), and Composition13
`7bb54bbd64107e5090643ecca1e4d33164173e85` (tree
`20467712e66dbadff4d562c0d5baae22b8c077a7`). The rehearsal's source
identities and target trees are recorded separately from the immutable
producer and consumer pin authority; a synthetic `git am` commit must never
be called producer `95bd…`.

The published Runtime bundle or the clean producer checkout
`/home/user/work/wt/rt-pin-95bd3c5f` remains the source-authority route for
the normal consumer byte check. Do not rewrite locks or copy generated
artifacts by hand. The neutral Runtime `runtime_protocol` path remains
provider-free; the installed normal product path remains the existing
private Runtime/client/Agent carrier with `astrid-runtime up --profile
astrid`.

## Evidence retained for this input refresh

### Current compatible-server full run

The exact current full result is:

```text
runtime-full-retained-owned-temp-integration-1021035028-28646
Runtime source b92d3e7a05eec65c142294ef4873edd059e9b31d
Runtime tree 6abc2f117391de8e7e35c0283f575a002199894d
6002 passed, 26 skipped, 15 xfailed, 12 warnings; exit 0
298.37 seconds; no failures
```

Exact command:

```sh
env ASTRID_CHECKOUT=/home/user/work/agent \
PYTHONPATH=$PWD:/home/user/work/agent \
/home/user/work/venv-runtime/bin/python \
/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-m4-full-temp-retain-all-final/runtime-full-retained-temp.py \
-- /home/user/work/venv-runtime/bin/python -m pytest -q -n 3
```

The 26 skips are Windows-native API cases. The 15 xfails are the held RT02 /
D04 legacy timeline-writer and clip-replacement cases. The 12 warnings are
Python 3.13 fork deprecations (10 from
`tests/test_realm_admission_hardening.py`, 2 from
`tests/test_t4_replacement_foundation.py`). This full result is Runtime
compatible-server evidence; it does not prove a coordinated consumer
journey, browser/native bootstrap, renderer, physical parity, owner-film
viewing, Gate 7, or ZIP completion.

The published artifact comparison remains bounded and exact: all 76 paths in
the published manifest have 0 differences, 0 missing paths, and 0 hash
mismatches between producer `95bd…` and server `b92…`. This preserves the
published artifact, schema, client, and lock facts; it does not promote the
server descendant to a new publication.

### Completed 0408 delivery rehearsal

The exact rehearsal was the existing owner-extra dry-run lane:

```sh
env GIT_CONFIG_GLOBAL=/dev/null PYTHONDONTWRITEBYTECODE=1 \
TIMELINE_DELIVERY_SCRIPT_SHA=3dfd5c28a9be9ab809e6c1fe1e9a83fbf8417ea888afc1b10eec5f751023e990 \
python3 /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/delivery-build \
--dry-run --repos "agent runtime app composition" \
--extra "extras/owner_film_cliplook_scan-v1.0.8.zip=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-vw-m4-owner-scanner-delivery-payload-scanner-v1.0.8.zip" \
--extra "extras/owner-film-differences.md=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-vw-m4-owner-scanner-delivery-payload-owner-film-differences.md"
```

Result `runtime-delivery-owner-extras-dryrun-1021040405-30942`: pass, exit
0, 97 seconds. Agent, Runtime, App, and Composition all passed patch/tree
verification; the staging directory was
`delivery/build-20261021T040409Z` with 12 files and 22.3 MiB uncompressed.
The SHA256SUMS check passed for all 11 non-self members, including the two
owner extras. It was a dry run, so no ZIP was written. This is procedure and
input alignment evidence only, not a current final delivery result.

The retained owner-extra hashes are scanner ZIP
`204a7aac78177824219954574f67fcaf4c56ac81620d533ecb376030340c93ee` and
owner instructions
`969fe3034ca1e7b7aab061ff16575fe7f7d973d9c9ec1f81c347464c4d9da220`.
They are scanner code and instructions, not an owner-film scan or viewing
result.

## Seven gates

| Gate | Current evidence | Status and limit |
| --- | --- | --- |
| 1. Lossless semantics | Bounded Agent conformance and connected occurrence/source, opaque-field, clear, reload, inverse/redo, stable-word, and rational-timing lanes remain recorded. | **OPEN.** The complete editing-conformance corpus and full CLI/Python/sheet coverage are not claimed. |
| 2. Atomic acceptance | Published014 producer evidence, compatible descendant server evidence, and the current Runtime full run are retained. | **PASS within the retained Runtime/producer scope; OPEN for the final coordinated normal pair.** The 6002 full is not a cross-product atomic-journey result. |
| 3. Renderer-independent save | Existing renderer-fenced and renderer-stopped Runtime/Agent evidence remains bounded. | **OPEN.** Cross-product coverage, live Composition parity, and physical frame/audio parity are not established. |
| 4. Transport | Published014 `0.2.14` producer/client and artifact bytes remain exact; the compatible `b92…` server and normal consumer pins are recorded. | **PASS within the retained producer/client scope; OPEN for the final coordinated `/v1` consumer result.** |
| 5. Adversarial App journey | Bounded uncertain-ACK/new-intent evidence and a journey-readiness recipe exist. | **OPEN.** No current normal-pair browser proof establishes intervening edit, lost ACK, newer local edit, exact retry, restart/reload, undo, and zero legacy snapshot traffic together. |
| 6. One writer, one viewer | Composition13 and bounded source/readiness evidence remain recorded. | **OPEN.** All-writer retirement, direct legacy-endpoint rejection, planted frame/audio mismatch detection, and physical parity remain unproven. |
| 7. Delivery | The 0408 dry run passed the established patch/bundle/tree and checksum procedure with both extras. | **OPEN.** It was not a final ZIP; fresh current-tuple delivery after source refresh, owner-film viewing, physical parity, and final ZIP verification remain outstanding. |

No current gate is recorded as a failure, and no unfinished gate is claimed
green. Historical red runs remain historical and are not reinterpreted as
current passes or current failures.

## Explicit remaining limits

Owner-film viewing is **OPEN**. macOS is **OPEN** and is never implied by
Linux evidence. Physical frame/audio parity, the global coordinated consumer
journey, the complete writer/viewer retirement proof, a fresh final-tuple
delivery build, and final ZIP verification remain required before release.

