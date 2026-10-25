# D139/D139a corrected source-packet brief

Status: `SOURCE_PACKET_QUALIFIED`, actual request: `NOT_READY`.

This is a source preparation packet for a future Codex worker using the
existing normal tools. It is not a controller implementation, state machine,
new policy, executable launcher, or approval gate. The companion
`controller-command.sh` is explicitly inert and exits before any reference
command can run. No child request, import, preflight, Store operation,
registry action, launcher, helper, or core service was run while preparing this
packet.

## Settled source tuple

The four existing integration checkouts are the only physical source checkouts
in scope. Their exact identities, parents, origins, and clean states remain
unchanged from the retained 2254 packet:

| role | checkout | commit | tree | parents | state |
|---|---|---|---|---|---|
| Agent | `/home/user/work/agent` | `41ad656529fa8489829de9078b1b6e157c7433c8` | `d29e47fe7be6e55940b42fa1477a23e7925f62fa` | `cd63be424d62226e3ee5c26fc5ce03227f5394a5`, `4fec53e0b14aea355e51c96c883fd75eef67a17c` | clean, physical |
| Runtime | `/home/user/work/runtime` | `f103bb46866999c961a8865636f2e66d544e0c9b` | `5d0cedf2e5134acf895e8d43191cc5fdc09f9883` | `cf0b82dd47452a7a34fc63eb233e9b1dc0532806`, `0bb3bc45cef22bc317398d79e1617da3eb430df2` | clean, physical |
| App | `/home/user/work/app` | `5696769dca056676cde1ab46d8bc94354b3a44a` | `0748df404125114a0f68b701fa76f43abd3fc79a` | `b5c9eadfa1950f46feac50d7d6a89c47f27f4881`, `79699d23f0cabef17eaa68463618132556c47902` | clean, physical |
| Composition | `/home/user/work/composition` | `635f4de06fda22a85fc2e4cfc764d0153a4c9f40` | `5ab5191a296980a0a6bcd1178ab6902d6478a148` | `7a95a40b07ea0d273e17afb69dbc3456b603f2bc`, `c05fdb171fe37c1d5817a060ecb716a329ee821a` | clean, physical |

The frozen R4 refs remain reference-only and are never retargeted. The
verified future tuple is Agent `41ad6565`, Runtime `f103bb46`, App `5696769d`,
Composition `635f4de0`; no old `f07`, `a4e`, `5e9ad`, or frozen tuple may be
used as a current binding.

At dispatch, the future worker must re-read each actual checkout's HEAD, tree,
parents, origin, physical non-symlink path, and clean status, and compare them
to this tuple and the fresh source manifest. This comparison covers the
entire merged tuple, not only Agent and Runtime. Any mismatch is a stop.

## Finite finding dispositions

1. **D139-SRC-001 — two core sites: fixed in this packet.** There is no
   `CORE_COMMAND`, no direct core body, and no explicit launcher execution in
   the inert reference. The only future core execution is the one named
   `request-test <worker-name> agent-core-full` call followed by its matching
   `wait-test`. The existing `p4-d73-pinned-launch.sh` is a normal-service
   input row owned by that service; it is not a second manual run.

2. **D139-SRC-002 — queued child request: fixed in this packet.** The
   existing requester API is retained exactly. A future worker may issue one
   request only after all guards bind, then must wait on the same request key:
   `queue/done/childvenv-$N` or `queue/refused/childvenv-$N`. Requester exit 0
   is queue admission only, never completion. A done result must include the
   genuine Store child and the maker's authentic `.provision-report`, with
   actual installed inventory and module-origin checks. A refused result
   preserves the exact queue row, private request/stage bytes and hashes, and
   authentic stage stderr or `EXACTMISSING`, then stops before import or
   manifest. No fallback, retry, alternate name, rename, or fabricated receipt
   is allowed.

3. **D139-SRC-003 — disk admission: fixed in this packet.** The child is
   dispatched once only with the manager's `5905580032`-byte child admission
   and no other heavy work (`D89c`). The core-start check is a separate,
   one-time `4700000000`-byte guard. The ongoing stop guard is
   `4000000000` bytes. The source-preparation floor remains `4600000000`
   bytes. The worker does not re-require the child floor after its own
   preparation; it does retain the core-start and ongoing-stop guards.

4. **D139-SRC-004 — custody and freshness: fixed in this packet.** The
   complete pending-input inventory is named once in `required-inputs.json`,
   `tuple.json`, and `findings-map.json`. Every unpublished final field stays
   `UNBOUND`, and therefore blocks any external invocation. The final worker
   must bind and compare, from actual owners only: API and source freshness;
   regular non-symlink `0755` received-kit mode and actual received hash; CAS,
   independent review, protected helper, inventory, seal, source
   registration, child registration, Runtime client identity, installed module
   origins, proof lock, dependency receipt, and input receipt. It must also
   retain the actual requester/provisioning report, check-only identity, and
   durable evidence custody paths. No guessed API, fake receipt, future hash,
   old receipt, overlay, or new approval gate is valid.

## Required future order

1. Verify all source, API, dependency, custody, disk, and no-other-heavy
   guards. The child request is not ready until every unpublished field binds.
2. Use the existing `request-child-venv` interface once with the exact
   source-carrier arguments. Preserve the authentic requester stdout/stderr,
   queue row, request hash, and provision stage hashes privately. Wait for the
   same key's terminal done/refused record and genuine provision report.
3. Only after a genuine in-child complete check passes, make one fresh normal
   supported full-tuple manifest. The complete check is in-child only and is
   not a new preflight or replacement state machine.
4. Run the existing D73 positive report-all control once with 17 positive
   calls, then the poison control with zero calls. Any failed control stops.
5. After a fresh manifest and all source checks, enforce the one-time
   `4700000000` core-start guard and ongoing `4000000000` stop guard, then
   submit one named `request-test ... agent-core-full` service. The manager
   owns the dispatch; the launcher row is service input only. Preserve the
   exact 22 roots and argv from the retained packet:

   `-m pytest -q -n 3 -o addopts= -p no:cacheprovider --timeout=45`

   The exact 22 selectors are retained in `required-inputs.json` and
   `source-manifest.json`; no `-k`, skip, xfail, or fail-fast option is
   permitted.

6. Keep the same service ID across any restart; never resubmit. Before harness
   cleanup, retain durable raw XML, runner log, per-ID record, start/stop disk
   record, and every `tests/<ID>/KEEP` marker with private `0600` custody.

The future worker must stop on the first refusal or guard mismatch. It must
not re-run the child admission after its own preparation, and must not claim
request readiness from source qualification alone.

## D139a installed schema boundary

The only permitted installed schema input remains `banodoco-timeline-schema`
0.0.2 from `https://github.com/banodoco/ArtAgents.git`, revision
`242f9c4306bf3b501222cb041a9eb246ef47bc85`, subdirectory
`packages/timeline-schema/python`. The authenticated installed evidence has 18
RECORD rows: 12 hashed and six named unhashed; direct URL SHA-256
`b7a0a4f90218d54bc1fb118609d40a381f5762650f8e5863ec39098ec269165e`; RECORD
SHA-256 `50be781bec3546ca9995ce2f0aaa1284fa68198735866c0f00a601bb3ce9c3a1`.
The physical schema carrier remains unavailable. No broad overlay, acquisition,
403 retry, archive, or source regeneration is permitted.

## C0 wire inventory retained without DTO changes

The production caller continues to use the existing C0 request fields:
`api_version`, `project_id`, `timeline_id`, `base_revision_id`,
`base_publication_id`, `commands[{schema_version,op,version,select,args}]`,
`label`, `steps[{id,label,intent,tags,command_ordinals,patch,reads?}]`,
`merge`, `reads`, `idempotency`, `dry_run`, `source`, `rationale`, and
`group_id`. Accepted/merged replies retain `canonical`, `base`, `landing`,
`receipt`, `records`, `bindings`, `effects`, `dependencies`, `history`, and
`undo_steps`; conflict retains `reason` and `head`; invalid retains `code`,
`path`, `hint`, and `suggested_command`; preview retains `would_status`,
`receipt: null`, and `writes: null`. No DTO, Git, hub, credential, product,
test, or pin change is part of this packet.
