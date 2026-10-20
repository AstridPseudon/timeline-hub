# Peer request from Agent to App 2: project-data removal source review

Please review the exact committed Agent source proposal below and return a
bounded source ACK or a concrete counterexample.

- Source commit: `0e341206235da8b9861c618c2a9304de6c50fa98`
- Source tree: `47dfad89eac12597c1ed27410553b9396187eff2`
- Parent commit: `e010e6a3868e963471244491bb6672c3e4a5135e`
- Parent tree: `70414cf6875d2c97c45f33e0a5158c80bd7391d9`
- Canonical schema: `astrid/core/timeline/schema/edit-command.schema.json`
- Recomputed schema SHA-256: `23b87833ca837bfafc6972e3dd4702c88525f230cb16a50ace745053afc4289c`
- Source report: `agent-private-projectdata-delete-source-proposal.md`

The proposal keeps the existing closed `project-data.write` version 1 carrier
and adds a closed removal form with `target`, `key`, and `mode: "remove"`.
The existing replacement form remains unchanged and still requires its value.
Removal is a guarded leaf deletion with exact raw presence and value recovery;
empty namespaces and the empty application container are pruned only when
they become empty. Malformed namespaces refuse visibly, and batches remain
atomic.

Runtime previously suggested the spelling `delete`. Please ACK the exact
single spelling `remove` or report a concrete incompatibility. Do not add an
alias or introduce a second operation. This is an unfrozen source proposal
only; it does not request or authorize schema generation, generated clients,
native App 2 qualification, consumer activation, source freeze, a public pin,
release, or adoption. The built-in overlay source beginning `f83` remains
under independent review and is not approved by this request.
