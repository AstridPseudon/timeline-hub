# Exact source-bound materialization implementation coordination

Agent worker agt-m2-materialization-map-impl; Runtime peer rt-m2-materialization-own-slot.
Both manager ACKs are in commit-contract.md (Agent 01:22, Runtime 01:18).
Before wiring: implementing the exact existing flat map, binding and dependency contract; no Runtime files, generated artifacts or pins changed here. Runtime must keep actual coupled acceptance held until normal paired schema generation.

Planned exports: Plan.id_map; records[].bindings fixed source entries keyed shot:D and shot:D/item:J plus materialization.owner:shot:D; records[].dependencies materialization.source:shot:D, entity/exact, pin {parent: ORIGINAL base_parent, source: ORIGINAL source_mapping.shots[D]}. command.bindings retains all these refs before sealing. Result/prepared.id_map copies Plan.id_map. Rebase retains original records/pins and consumes D/J across a sibling-first head.

Canonical source: astrid/core/timeline/schema/edit-command.schema.json, four patterns ScopedId, EntityRef, TargetKey, AnchorIdentity add closed shot-owned item refs. interface_version stays 1. No args.materialization or physical created facts.

Budget assessment before implementation: the sibling-first counterexample needs original-source installation before claim verification, while accepted reload inverse needs a read-only source resolver separate from writable State. These are independent of schema/codec/map capture and SDK ACK verification. The 150–220 line target may be exceeded to preserve all of those checks rather than bypassing source or ACK validation; final diff and evidence will be reported here.
