# Runtime project-data contract review

Date: 2026-10-20 UTC

## Decision

**BOUNDED SEMANTIC ACK for the Agent project-data shape; current Runtime
qualification is held on an explicit pairing prerequisite.**

Reviewed Agent commit `0a774e4968f5a9728c4ee6b5bbbfe286e26f29a3`, tree
`2f3eee4e9a7d37db80374b5e98d16f1e08082a35`, schema
`89ed90ce0a4a95559a6d086d57f851fbcc6d224c9e7658f41467dfa9280eb0c3`.
The independent Agent review's successor verdict was APPROVE for this private
source slice (`209 + 17` focused checks, `83` additions and `0` removals).
This ACK does not authorize freeze, generation, release, pin, integration, or
App cutover.

## Contract findings

- The command is closed to `schema_version: 1`, `op: project-data.write`,
  `version: "1"`, `select: "parent"`, and args exactly
  `{target, key, value, mode: "replace"}`. Unknown args and other modes are
  refused.
- The semantic write is exactly the existing authored path
  `parent.config.app[extension_id][key]`. It preserves other extension keys,
  other `config.app` extensions, and all timeline fields. Project catalog or
  unplaced-project state is not reachable from this operation.
- Agent validates the existing extension-ID grammar and the main key rules:
  non-empty and already trimmed, at most 256 UTF-8 bytes, and exact rejection
  of outer `__proto__`, `constructor`, and `prototype`. Entry, extension-total,
  and per-extension entry-count limits are enforced by the semantic handler.
  Arbitrary nested JSON object keys, including those names, remain ordinary
  opaque data.
- Missing, null, and empty containers remain distinct. The successor's
  container-claim handling permits disjoint-key rebases through a concurrently
  born absent/null/empty namespace, while malformed shapes still refuse.
  Exact leaf recording, inverse, dependent-write, and A-to-B-to-A guards remain
  authoritative. No whole-parent replacement or caller-supplied container
  adoption was introduced.
- The compiler-canary source and source-map members remain one ordered command
  batch. An unsupported member in a mixed batch refuses the complete batch
  before any supported member is applied; the original draft remains intact.
  Runtime must preserve that all-or-nothing behavior at its existing `/v1`
  commit transaction boundary.

## Runtime compatibility boundary

Runtime has one semantic owner: `runtime_protocol/timeline_commit_provider.py`
loads the trusted Agent factory `astrid.sdk.timeline.commit.create_runtime_commit_service`
and checks the existing provider ABI and contract digest. The execution path
calls only `provider.commit(context, port)` in
`runtime_protocol/timeline_commit_execution.py`. Source inspection found no
Runtime project-data handler, second writer, project-data store/table, new
endpoint, or project-data DTO. A future generated `ProjectDataWriteArgs` type
is only a schema projection; it must not become a second semantic implementation.

The current reviewed Runtime tree is not the requested ordinary candidate:

| source | definitions | operation clauses | schema SHA-256 |
| --- | ---: | ---: | --- |
| current Runtime `contract/schemas/edit-command.json` | 48 | 22 | `a6f1aaa9dfcc31828bd04c908158fd7fd9a825df6c9f88f79b81779273a190ef` |
| Agent private candidate | 56 | 30 | `89ed90ce0a4a95559a6d086d57f851fbcc6d224c9e7658f41467dfa9280eb0c3` |

The current Runtime pin lacks the candidate's eight additional operation
clauses, including `project-data.write`; therefore a live/current Runtime
qualification would be a concrete false claim. The executable next step is a
separate authorized Runtime pairing that imports the exact Agent schema,
updates the existing bundled resource/generated projections through the normal
generator, checks the provider contract digest, and then proves the existing
`/v1` atomic/idempotent path with the mixed unsupported-batch refusal. No new
Runtime writer, store, endpoint, or public DTO should be added.

The candidate schema's `maxLength: 256` is a conservative schema-level
character bound; Agent's handler is the authority for the stricter 256 UTF-8
byte rule. A Runtime projection must not introduce a looser semantic writer or
silently normalize a rejected key.

## Separate 357/613 composition requirement

This review is only for the project-data candidate above. It must not replace
or be casually merged into the separately reviewed full carrier source:

- Agent source commit `357230816c86da65d5f8cc92b10a3a90d29874e0`;
- actual source tree `94692ec85167d5c606626c4ec678fe2a63ee0aa6`;
- private schema SHA-256
  `613123b2760150f9f33e23485516d757359c3eaebfe02d552bc97155309aaad3`.

The 357/613 source is a separate 55-definition/29-operation carrier. If the
project-data operation is later composed into that source, it needs a new
reviewed successor and an exact Runtime counterpart generated from the agreed
combined source. Preserve the current Runtime CAS/text/promotion/catalog-head,
global-item, headless, and strict-marker protections; do not use this
56/30 candidate as a substitute for 357/613, and do not infer a native pair or
release from either source review.

## Focused evidence

One in-memory compatibility probe, run from this Runtime worktree, passed:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=. /home/user/work/venv-runtime/bin/python - <<'PY' ...
candidate schema positive + closed-negative validation: PASS
candidate/current compatibility errors: []
timeline commit Python/TypeScript DTO generator with candidate schema: PASS
PY
```

The probe accepted a valid nested opaque JSON value, rejected wrong scope,
wrong mode, unknown args, reserved key, and leading-space key, verified
containment of the current Runtime schema in the candidate, and rendered
`ProjectDataWriteArgs` into both Runtime DTO outputs using a private temporary
directory. No repository files were changed.

Not run: Runtime full suite, live HTTP/socket suite, Agent tests (the supplied
Agent and independent reports were read rather than duplicated), App/browser
journeys, generation/freeze/release/pin/integration, or native qualification.
