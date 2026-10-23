# R2 registry presence seam — agt-R2-registry-presence-sol-1617

Proposed source-only seam: inverse.coalesce.value_address must retain an explicitly authored parent.registry address in the physical parent object. logical_address currently maps it into config.registry, even when a complete accepted config write proves that mirror absent. Coalescing storage values must preserve this distinction; history conflict overlap continues using logical aliases. No forward or recording guard change is proposed.

Base 6aec04e8bdbdcbcca7e6ee7d979c105618357f87 retains predecessor 1603. Full immutable 320-event packet read and payload/dedup hashes verified: 7ab92b619cbe6466b782852afd63c46309722d6d65d88f8fbb8c1e93111a6c15. Events 154/264/266 supply exact accepted before/after canonical documents, immediate undo history entry, head and redo request. Event312 proves the only extra expected config key is registry:{}; actual config has no registry. Source subset: workers/agt-R2-registry-presence-sol-1617/captured-input.json. This is offline evidence, no body execution.

Validation pending. Distinct nested and shot-id causes are not reclassified. No public redo or G5 deletion qualification is claimed.
