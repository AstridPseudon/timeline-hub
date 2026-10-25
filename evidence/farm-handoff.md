# D140 Farm receiving handoff

Status: `SOURCE_ONLY / NOT_READY_ON_THIS_VENUE`.

This packet is the one portable receiving recipe for the merged tuple. It does
not create a child, run imports or pytest, invoke the installer, publish a
Store, touch a queue, acquire a package, or run the Agent body. Store
retirement remains deferred and the old `3e163` child/result set is retained
immutably.

## Exact source tuple

| input | commit | tree | origin | local observation |
| --- | --- | --- | --- | --- |
| Agent | `41ad656529fa8489829de9078b1b6e157c7433c8` | `d29e47fe7be6e55940b42fa1477a23e7925f62fa` | `https://github.com/peteromallet/astrid-agent` | object present in `/home/user/work/agent`; checkout is stale at `547e10456250c1b5bcf63b44a50c90ff0563ce1e` |
| Runtime | `f103bb46866999c961a8865636f2e66d544e0c9b` | `5d0cedf2e5134acf895e8d43191cc5fdc09f9883` | `https://github.com/banodoco/banodoco-workspace-runtime` | exact clean integration checkout observed |
| App | `5696769dfca056676cde1ab46d8bc94354b3a44a` | `0748df404125114a0f68b701fa76f43abd3fc79a` | `https://github.com/banodoco/reigh-app` | exact clean integration checkout observed |
| Composition | `635f4de06fda22a85fc2e4cfc764d0153a4c9f40` | `5ab5191a296980a0a6bcd1178ab6902d6478a148` | `https://github.com/peteromallet/timeline-composition` | exact clean integration checkout observed |

The stale Main Agent home is deliberately not retargeted or mutated. Farm must
receive an actual clean checkout at `41ad…` through its normal receipt route.
The old D124/1426 tuple and prior failed results remain outside this packet and
must not be rewritten as current evidence.

## Receiving gates

Run `ops-d140-farm/receive-farm.sh --check-only` with all bindings named in
`prerequisites.json`. A missing path or receipt is a finite `NOT_READY` result;
the owner and blocking input are preserved in `missing-inputs.json`. There is
no Main-only interpreter or profile fallback.

After every gate is present and re-read, use `ops-d140-farm/commands.md` in
order:

1. one normal `request-child-venv` request with the D139a installed schema
   distribution and trusted manifest pair;
2. the registered child `check-child-imports` census against the authenticated
   1,146-row canonical packet;
3. D73 positive dry control (`17`, counter `1`), then poisoned manifest
   (nonzero, counter `0`);
4. one unfiltered D124 core run with the unchanged 22 roots.

The canonical census is `4c4ee35d…/ab1e4f61…` supporting evidence only. The
current source delta is `41ad6565…/f103bb46…`; no current-tuple census hash or
import applicability claim is made. Optional/plugin misses remain diagnostic,
while unconditional-required rows remain mandatory.

The core request's production seam remains the normal C0 receiver. Its full
request fields are `api_version`, `project_id`, `timeline_id`,
`base_revision_id`, `base_publication_id`,
`commands[{schema_version,op,version,select,args}]`, `label`,
`steps[{id,label,intent,tags,command_ordinals,patch,optionalreads}]`,
`merge` (`fields|atomic`), `reads`, `Idempotency-Key`, `dry_run`, `source`,
`rationale`, and `group_id`. Accepted/merged replies retain `canonical`,
`base`, `landing`, `merge_mode`, `receipt`, `records`, `bindings`, `effects`,
`dependencies`, `history`, and `undo_steps`; conflicts retain `reason` and
`head`; invalid requests retain `code`, `path`, `hint`, and
`suggested_command`; previews retain `would_status` with a null receipt.

No product, test, pin, kit, schema, client, Store, provider, collection, or
global registry file is changed by this packet.
