# PEER REQUEST from Agent to Runtime — 2026-10-21 04:30 UTC

Owner-authorized handoff of exactly two independent joint ledger halves from
Agent base `5a625dd4c01149a085a9df85952b34cad70801f9` (the worker HEAD and
hub `tl/integration` snapshot):

- **WC1:** qualify the existing settled `authoring_proposal` /
  `producer_attempt` / first `producer.guard` / requester `TimelineSession`
  seam for the one current `publish_authoring_candidate` consumer described
  in `handoff-agent-to-runtime-wc1.md`. Preserve original target pair,
  digest, rationale, command values, exact flight/retry, restart, acceptance,
  history, and inverse; do not add a DTO, endpoint, pin, or writer.
- **WC8:** reserve the existing Runtime commit/rebase acceptance seam for a
  future detached-sheet batch only after Agent retains native basis, stable
  row intent/identity, and the original Runtime target before mutation. Keep
  the detached legacy grammar and local merge/save behavior live until that
  carrier exists; do not infer intent from snapshots or replace a positive
  with refusal.

Please ACK the two bounded Runtime halves or return a concrete existing-seam
mismatch. Runtime paths and exact positive floors are in the two handoff
notes. No `full*`, browser, renderer, live-socket, installed-launcher,
schema/generated-client/version-pin, generation, or activation work is
requested. The remote merge route, if a bounded Runtime source/test change is
needed, is `bin/request-merge-remote runtime <worker>`; no direct merge or
push is authorized.

RT03 is intentionally not included: Runtime already owns the independent
`agt-review-rt03-projection449-current` / normal reference-pair preparation;
this worker is not duplicating that scope. WC10 current native creator, WC6
current landing, D13 Runtime-origin security, raw OLD swap, and transcript /
order repair are also explicitly excluded.
