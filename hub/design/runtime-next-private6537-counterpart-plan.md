# Runtime complete65/37 private-counterpart prerequisite proposal

Status: source ACK and allocation proposal only. This is not generation, freezing,
pinning, publication, or consumer adoption.

## Decision

Use Runtime commit `b92d3e7a05eec65c142294ef4873edd059e9b31d` (tree
`6abc2f117391de8e7e35c0283f575a002199894d`) as the source base. Pair it with
the exact Agent source commit `10226a7f08a739ba3e41f8e91de6971eed63aa9d`
(tree `e2c08fbe9b21a3082db7bcf62d9677babfc15e98`, parent
`9502e3ebdf43c9759fe1445a91d32599822cc1d0`) and the canonical Agent schema
hash `322733a57e781847e50228f91b6c6a9237ad2237406a188515c8f9da5e554bcc`
(raw SHA-256 `9cb9597a618f51949fe9ec35686e544dca812b8b252a96a4cff1f686afdfb3ec`).

The source review found no schema or carrier incompatibility requiring a new
DTO, endpoint, store, wire field, or authority. The concrete prerequisite is
that the later private Runtime candidate port the already-approved custody,
projection, and materialization joins below. Current `b92d3e7` does not yet
contain those RT03/RT08 source files, so it is a base proposal, not a claim
that the current checkout already accepts the complete65/37 source.

The Agent commit changes only the final blank line in the transcript
conformance test. It does not change product, schema, generated, lock, or
client bytes. The schema adds the retained transcript successor surface over
raw OLD: 65 definitions and 37 closed EditCommand clauses versus 64/36 for
raw OLD. The new operation is `transcript.associate@1`, with
`TranscriptAssociateArgs` and the existing `DocumentPin`/document carrier
shapes.

## Exact source allowlist

The later candidate should be assembled as minimal hunks on the `b92d3e7`
base. Do not replace whole Runtime files with an older branch.

1. Port only the approved RT08 materialization join from Runtime commit
   `83a982eb1185477e50817e10b8c61212c43c8e03`, tree
   `becc776a4f0c88ae2f4c8ba9350116a040d223c7`:

   - add `runtime_protocol/timeline_materialization.py` from that commit
     (Git blob `bfb1217ed19d6071ecafc2b4941f38fdfabeef6d`, SHA-256
     `92ec9b...` in the RT08 review);
   - port only the materialization validation/invocation hunks in
     `runtime_protocol/timeline_commit_port.py` (blob
     `99a075befe009d05d11cfef4ecb3a96e6e0b48fa`) and
     `runtime_protocol/timeline_commit_store.py` (blob
     `d9781479f92360fa5899d9b14b0aa38f6e78caa6`);
   - retain current b92 history, retry, source, and transcript guards around
     those hunks. In particular, the 83a982 port version removes
     `TRANSCRIPT_KIND` from its source allowlist; that is an old-branch
     regression and must not be copied. Keep the current
     `PROJECT_PACK_KIND, TRANSCRIPT_KIND` import and allowlist.

   The join must remain read-only and exact: project/timeline, content digest,
   shot/internal/item membership, parent/source pins, bindings, no created
   IDs, source owner/provenance, inverse support, and the existing
   `materialization.source:`/`materialization.owner:` identity edges. Keep the
   current request/port/store authority checks; do not introduce an authority
   or alternate identity source.

2. Port the approved RT03 raw-media custody hunks from
   `f53bf588bf70b090ce8e0bed5ccb7d91157771b6`, tree
   `d82f37052847949e77c12e1704c3f27c6dd56a46`:

   - `runtime_protocol/timeline_commit.py`, Git blob
     `e7364e401a...`, raw SHA-256 `9de452...`;
   - `runtime_protocol/timeline_commit_port.py`, Git blob
     `a2e0d0ec...`, raw SHA-256 `26c179...`;
   - retain the reviewed custody tests from `tests/test_timeline_raw_capture.py`,
     Git blob `07fb3ae...`, raw SHA-256 `374a...`, for the later candidate.

   Preserve the exact existing `MediaManifestEntry` carrier
   (`media_id` and equal `content_digest`, each `sha256:` plus 64 lowercase
   hex), command-scoped `raw_media_info(pin)`, managed-project ownership,
   single CAS descriptor, regular-file identity, size/full-SHA/stable
   descriptor checks, declaration/acceptance revalidation, ledger-first
   replay, and no-write refusal on missing, foreign, tampered, or mismatched
   media. No caller catalog, public object, or fallback source is permitted.

3. Port the approved RT03 reference projection from
   `449d13d291cc3b62ebbdd780d38d8c58732e4e1b`, tree
   `47d5f06...`:

   - add `runtime_protocol/timeline_commit_reference_projection.py`, Git blob
     `4863b98da154...`, raw SHA-256 `db8a6d...`;
   - port its minimal store hook and retain its reviewed tests (test blob
     `81d0c542...`, raw SHA-256 `cf03...`).

   Keep the exact closed-v1 parent carrier
   `config.app.astrid.timeline_references`, lowercase-equal media/content
   digest, exactly one manifest entry, global active/archived occupancy,
   prior-carrier/live-row ownership, transactionally coupled closure/
   publication/head/version, and ledger-first retry. Do not add a catalog,
   placement writer, or new projection authority.

4. Do not re-port the retained transcript or Speech changes. They are already
   present in b92 and are current guards:

   - transcript source-document boundary test, Git blob
     `49af86fadbf8692d43e412dbd5e0c9bb939545e8`;
   - Speech-compatible `runtime_protocol/store.py`, Git blob
     `5415a62fbc4692c110017245ceda12260e25629b`;
   - settlement test, Git blob
     `a5317ce82f008cc4cfd8d86f73e5c95e50a567dd`.

   Keep the existing verified `media.transcript` carrier, exact input pin,
   retained-after-removal/restart behavior, and rational-compatible source
   fix. Do not add a transcript endpoint, new DTO, or command registration.

## Current guard and contract bytes to retain

These are the b92 Git blobs that must remain the surrounding source/test
anchors while the donor hunks are applied:

| path | b92 Git blob |
| --- | --- |
| `runtime_protocol/timeline_commit.py` | `464e5a3490af5d67390168fe74c5ff910f718005` |
| `runtime_protocol/timeline_commit_port.py` | `07883e592e1349263adc7e7f5cefc89e6c985c9c` |
| `runtime_protocol/timeline_commit_store.py` | `be6708a65b11456151f55be29e47697d54f3f888` |
| `runtime_protocol/store.py` | `5415a62fbc4692c110017245ceda12260e25629b` |
| `tests/test_timeline_source_document_boundary.py` | `49af86fadbf8692d43e412dbd5e0c9bb939545e8` |
| `tests/test_generation_publish_v1_settlement.py` | `a5317ce82f008cc4cfd8d86f73e5c95e50a567dd` |
| `tests/test_timeline_raw_payload_contract.py` | `aebd268dd485f694e38540255d0b4f3aa5c96c2a` |
| `tests/test_timeline_projection_occupancy.py` | `b820a45ab80bcce10eb377a5e3f4e6e12876851d` |
| `tests/test_timeline_current_union_contract.py` | `0c72f5934770aae9017a3c38017561e4ce72b05a` |
| `tests/test_command_schema_compatibility.py` | `107cbb690c031b2486af36a2137e720c2a4f1026` |
| `tests/test_timeline_commit_type_generator.py` | `cc2ee25f73d3dabbc807902afbf25f09272e7b37` |

Retain current generator/template anchors as well:
`generators/generate.py` (`2cd404db443059d8cc5789771880cf6f1897d5da`),
`generators/python_client_init_template.py`
(`f1b00f9920b31e0a8eab08e71750f4a2cf74df25`), and
`generators/timeline_commit_types.py`
(`bd338a197f95072140f38e92c2a6ecd8018eb650`). Existing public contract
fixtures, artifact manifests, lock bytes, and public validation remain
unchanged. The current ordinary schema floor is canonical SHA-256
`6ba7b51e9518e7fb08b27ad5b7225855276b657d0adebf704dd853f699768f2d`.

## Later private generation and package roots

Generation is deliberately not performed in this task. Once the reciprocal
source review passes and the manager authorizes a private candidate:

1. Carry forward the reviewed C3d generator support for
   `generators/agent-command-source.json`, `validate_command_schema(source_path)`,
   source-pin validation, and dynamic Python `*Args` root exports. Populate the
   pin only with Agent commit `10226a7f...`, tree `e2c08f...`, path
   `astrid/core/timeline/schema/edit-command.schema.json`, and raw SHA-256
   `9cb959...`; status must remain private/unpublished/no consumer adoption.
   The current b92 generator does not yet have the `--agent-command-schema`
   option, so this support is a prerequisite change, not an invocation to run
   now.
2. Later, with a private copy of the Agent schema as input, use:

   ```bash
   PYTHONDONTWRITEBYTECODE=1 python generators/generate.py \
     --agent-command-schema /path/to/private/agent/edit-command.schema.json
   node tools/generate_typescript_conformance.mjs \
     --contract contract/openapi/workspace-v1.yaml \
     --schema-manifest contract/manifest.json \
     --component-manifest contract/component-manifest.json \
     --fixture-root conformance/fixtures
   python scripts/artifact_manifest.py
   ```

   The later check-only commands are the README commands with `--check`:
   `python generators/generate.py --check`, the same TypeScript command with
   `--check`, `python scripts/artifact_manifest.py --check`, and the applicable
   targeted Runtime tests. No install or shared-dependency mutation is part of
   this proposal.
3. The Python package root must dynamically export every schema `*Args`, in
   particular `TranscriptAssociateArgs`, while retaining
   `ProjectDataWriteArgs`, `MigrateGroupsArgs`, `OccurrenceMoveArgs`, and
   `OccurrenceResizeArgs`. The TypeScript generated root must retain its
   current `generated.ts`/`timeline-commit-types.ts` export path and include
   the generated `TranscriptAssociateArgs`; do not hand-edit generated files.

## Version allocation proposal

| identity | use/status | reusable? |
| --- | --- | --- |
| `0.2.13` | historical private392 counterpart | no |
| `0.2.14` | ordinary Main014/current tuple and private613/952 history | no |
| `0.2.15` | private C3d/84fc and Speech-compatible 3e6c descendant; used staging/private identity | no |
| `0.2.16` | next unused private patch proposed for this complete65/37 candidate | proposal only |

The proposed later private package identity is therefore `0.2.16`. It must
not be treated as a release decision, normal pin, or publication until the
gates below pass. Do not reuse `0.2.15`, any withdrawn/staging identity, or
the ordinary `0.2.14` identity.

## Required gates and remaining qualification boundary

The next reciprocal review must compare the exact Agent source tuple
(`10226a7f`/`e2c08f`/raw `9cb959`/canonical `322733`) against the exact Runtime
source allowlist above, then review the later private generated schema,
package-root exports, manifest, lock/client bytes, and source/test guard
retention. Both Agent and Runtime must return an exact source/artifact ACK;
generation is not allowed before that review passes.

After that, run one normal native-pair gate: the ordinary provider/Door path,
not a prepared-provider or direct-store harness, against the generated private
65/37 candidate. The gate should use the existing commit acceptance identity,
lost-ACK retry, restart/replay, and guarded-inverse lifecycle controls, plus
the complete65/37 accepted command path, and must verify the exact source
pins/custody/projection/materialization joins. Reuse the existing counterpart
lifecycle evidence, including the existing fresh shared-occurrence retry and
historical-restore control, rather than repeating a blanket old44 matrix.

The following remain unqualified until that normal gate (and any separately
named provider/consumer review) passes: RT03 raw-media custody and reference
projection as a normal native pair; rawOLD swap-media/legacy compatibility
behavior; group migration/move and group occupancy behavior; transcript
associate/source-document successor behavior, including provider-side
caption/review reconciliation; and any native adoption or publication claim.
The historical focused reviews prove source bounds and refusal behavior only;
they do not qualify these behaviors for normal native-pair adoption.

## Verification status

No tests, generators, installers, package builds, source copies, or artifact
mutations were run. This task is read-only and produced a source-base,
allowlist, and allocation proposal. Historical reports cited above contain
their own targeted/central results; those are not new evidence from this
worker and must not be reported as qualification of the proposed candidate.
