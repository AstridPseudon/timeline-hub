# D140 whole-path receipt investigation

Verdict: `FAIL_SOURCE`; whole-path qualification is `NOT_READY`.

This is an independent, read-only source investigation at Composition HEAD
`d7727b99fb9cb063d4c0ee73fdfa54d752666135` (tree
`222476a7f8eea57f46402ab4fefabce4e2b8a703`). No Farm admission, child
provisioning, request, queue, Store, core, package installation, or live input
was used.

## Exact source identity

The source tuple required by the D140 receiver is:

| component | required commit | required tree | required origin |
|---|---|---|---|
| Agent | `41ad656529fa8489829de9078b1b6e157c7433c8` | `d29e47fe7be6e55940b42fa1477a23e7925f62fa` | `https://github.com/peteromallet/astrid-agent` |
| Runtime | `f103bb46866999c961a8865636f2e66d544e0c9b` | `5d0cedf2e5134acf895e8d43191cc5fdc09f9883` | `https://github.com/banodoco/banodoco-workspace-runtime` |
| App | `5696769dfca056676cde1ab46d8bc94354b3a44a` | `0748df404125114a0f68b701fa76f43abd3fc79a` | `https://github.com/banodoco/reigh-app` |
| Composition | `635f4de06fda22a85fc2e4cfc764d0153a4c9f40` | `5ab5191a296980a0a6bcd1178ab6902d6478a148` | `https://github.com/peteromallet/timeline-composition` |

Read-only `rev-parse HEAD`/`HEAD^{tree}`, origin, and clean-worktree checks on
`/home/user/work/{agent,runtime,app,composition}` found Agent at
`547e10456250c1b5bcf63b44a50c90ff0563ce1e`/tree
`68df11fad2b082fa12d99ca20404e1e40e350cd7`, Runtime at
`0ca306dfd3cf4e21976271cc4b2e779b10e025b0`/tree
`37cfcd4f6108c1fdda401e563e3674503bc328ef`, and App/Composition at the
required identities. Therefore the current source checkouts are not a
qualified four-checkout tuple. The required Agent and Runtime objects and
source blobs are present in the repositories, but that does not create a
qualified Farm receipt. The four frozen R4 references were inspected with
`git show` only; they are not substitutes for the required tuple.

## Producer-to-receiver trace

### Source and D73

`ops-d140-farm/receive-farm.sh:238-294` accepts a physical JSON file if it has
a broad status allowlist, a `timeline.*` schema prefix, any recursively found
commit/agent/runtime SHA and tree value matching the expected values, any
recursively found repository path, and a local Git checkout whose HEAD/tree
matches. This is not an authenticated producer/source closure. A producer-free
JSON object containing the expected strings can satisfy the check; the prior
final2332 private control reproduced that synthetic attack with
`schema=timeline.synthetic-forged/v1`, `status=passed`, `producer=untrusted`,
and `receipt.FARM_CURRENT_AGENT_RECEIPT`.

The genuine D73 producer is the pinned Agent launcher
`tools/p4-d73-pinned-launch.sh` (source SHA
`9f668e398b1ea4cce48a6c610102723e0a3dab27a764be4191015aa7fc4110cd`). It
renders a `p4-d73-v1` key/value manifest after the four normal request
checkout receipts have been validated, checks exact commits/trees/paths and
clean Git state, then copies the manifest to
`$P4_D73_EVIDENCE/$P4_D73_REQUEST_ID.manifest` and writes a runmanifest. The
current receiver’s byte comparison to the positive manifest is directionally
aligned, but `check_d73_receipt` (`receive-farm.sh:419-429`) does not bind the
receipt path to the evidence copy or verify the producer/runmanifest digest.
No live positive D73 manifest/evidence copy was available for this review.

### Installed kit / D139a input

The genuine source-only Farm input producer is
`/home/user/timeline-hub/hub/kit/bin/verify_farm_distribution_inputs.py`.
Its canonical JSON is `schema=timeline.farm-distribution-inputs.v1`, with
`roles`, `lock`, `distributions`, `ownership`, and a `component_identity`
digest over the validated result. Schema-source validation binds the exact
Agent Git root, commit/tree, clean state, source bytes, and custody metadata.
`verify_dependency_seed.py` retains these canonical bytes as
`<child-root>/.farm-receipt.json` mode `0400` and revalidates raw byte equality
and component identity before reuse.

The receiver’s `check_farm_kit_receipt` (`receive-farm.sh:355-417`) instead
expects `timeline.ops.*`/`installed-kit` JSON (or an unrelated flat fallback)
and checks selected fields. That is not the current Farm input format. A
historical D139 installed-kit JSON exists in prior evidence, but it is not a
current live input and must not be promoted to one. The current Farm kit
receipt and exact schema-source carrier are missing/unbound.

### Child provisioning and registration

The request producer (`ops-child-custody/request-child-venv:291-300`) queues a
`queue/pending/childvenv-$N` request and expects a terminal result under
`queue/done/childvenv-$N`; it does not manufacture a qualified receipt. The
maker (`ops-child-custody/make-child-venv:419-466,1022-1033,1176-1282`)
generates a fixed provision report and then a flat success line. The report
requires exact status, Agent/Runtime SHAs, requirements lock SHA, Runtime
client identity SHA, import-origin and installed-distribution sections. The
success line includes the registered entry path/key, actual source markers,
the fixed provision-report path, and its SHA.

The genuine closure therefore includes the queue/done result, registered
`bench-store/entries/child-<key>` path, child interpreter/bootstrap,
`.bench-owner.json`, `.astrid-*` source/client/schema markers,
`.astrid-import-origins`, sealed source snapshot, and exact provision-report
bytes/digest. The receiver’s `check_child_receipt`
(`receive-farm.sh:296-353`) parses loose JSON or flat key/value text, checks
only alternate SHA/lock fields and mere presence of an import-origin or
client-identity field, and does not bind those paths or bytes. It also does
not parse the genuine maker line’s `agent=`/`runtime=`/`provision_report=`
closure as the producer contract requires. Thus the current check is both
looser than the real closure and not reliably compatible with the real
success-line format.

## Comparison with the synthetic attack

The synthetic object passes the current source checker because the checker
searches arbitrary nested keys/values and independently trusts the local
checkout. It has no authenticated producer, no exact schema identity, no
receipt digest, no evidence path, no child/kit path, and no source bytes or
registration closure. A genuine child result, Farm input, and D73 manifest
each have producer-specific paths and byte/digest relationships; those
relationships are not represented by the generic recursive acceptance path.
The source-level missing-input census remains `EXACTMISSING_LIVE_VENUE_INPUTS`.

## Missing live Farm inputs

The following are still absent or unbound; this investigation did not attempt
to create them:

1. A clean current four-checkout source tuple and four genuine pre-child
   request-checkout receipts at the required Agent/Runtime/App/Composition
   identities.
2. The authenticated current D139a/Farm distribution receipt, including the
   exact schema-source carrier, canonical bytes, component identity, and
   custody/source closure.
3. A normally registered child result: queue/done result, child interpreter
   and bootstrap, registration/owner metadata, source/client/schema markers,
   import-origin report, provision report, and exact report digest.
4. A fresh positive D73 manager manifest and retained evidence copy, plus its
   runmanifest/exit evidence, produced from the same request.
5. The fresh merged-tuple D73 manifest and exact positive poison copy for the
   negative control, with durable Farm output roots and the normal service
   result/receipt path.

The shared Main venv’s installed schema distribution and the installed kit
scripts are not evidence of Farm admission, child registration, or a current
qualified receipt. No live Farm input was inferred from them.

## Smallest bounded source seam

No C0 or product/wire change is indicated. The smallest source seam is the
D140 Farm receiver’s receipt-admission boundary: replace the generic
`check_source_receipt`/kit/child acceptance with exact checks for the existing
producer formats and their already-defined paths, raw bytes, digests,
producer/status values, and source/registration closure. Unknown schema,
producer, status, path, digest, or detached tuple data must fail closed.
The D73 path should additionally bind the manager manifest to its retained
evidence copy/runmanifest. This is a bounded receiver/fixture seam; it does
not authorize inventing a new protocol, recursive-key convention, synthetic
receipt, global ledger, or acceptance of stale/currently unbound inputs.

## C0 contract check

`/home/user/timeline-hub/hub/design/commit-v2.md` and Runtime f103
`/home/user/work/runtime/contract/schemas/timeline-commit.json` were read. The request remains the
exact `CommitRequest` shape with `api_version`, project/timeline scope, base
revision/publication pair, commands, and its documented optional merge/read/
source/rationale/group fields. Accepted mutation replies remain `{data,receipt}`
with accepted/rebased/merged status, canonical document/digest and IDs;
preview replies have `receipt: null`; conflicts carry current-head/conflict
details. No C0 contract, request shape, reply shape, or wire behavior was
changed or proposed.

## Scope and validation

This was source-only as required. No test/type/lint/full-suite execution was
performed. The required JSON artifacts were parsed with Python’s standard
library; exact Git identities, source blobs, modes, and hashes were checked
read-only. Detailed commands and results are in `validation.md`; the complete
machine-readable inventory is in `findings.json` and `source-manifest.json`.
