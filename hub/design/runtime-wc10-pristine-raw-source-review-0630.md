# Runtime WC10 pristine raw source review

Date: 2026-10-21

## Disposition

**SOURCE ACK (bounded), with activation held.** Runtime’s existing
provider-backed `/v1` commit carrier can carry Agent’s proposed
`timeline.init@2` raw `parent.config` without a Runtime DTO, port, endpoint, or
provider-ABI change. This does not approve Agent schema registration, a
generated artifact/pin, an App caller, the remote creator, or legacy-route
retirement.

## Reviewed source

The original positive is the raw `theme_overrides.visual.canvas` config in
`/home/user/work/agent/tests/v10/test_timelines_create.py:24-29`.
Main constructs it at
`/home/user/work/agent/astrid/packs/timeline/cli.py:175-192`; Main’s
`RemoteTimelines.create_empty` places the caller mapping unchanged at
`parent_composition.config` at
`/home/user/work/agent/astrid/sdk/remote.py:482-552`. The source plan records
that this is a raw-config roundtrip and must not be normalized to `output` at
`design/agent-wc10-custom-output-existing-recipe-plan.md:10-41`.

The exact proposal is `design/agent-wc10-pristine-raw-init-proposal.md`:

- closed `timeline.init@2` envelope and open `args.config` subtree: `:11-51`;
- ordinal-zero, exact bootstrap, empty placement/shot, and absent name/slug
  guards: `:53-64`;
- only scoped config/name/slug writes, with no root replacement, registry
  injection, or output projection: `:66-85`;
- recorder/inverse controls are explicitly not Runtime acceptance evidence:
  `:87-103`;
- future schema/registry and paired-proof requirements, with v1 unchanged:
  `:105-133`.

## Runtime carrier and guards

`runtime_protocol/service.py:1697-1743` creates the identity shell and calls
the provider’s `commits.bootstrap(...)`. The fixed bootstrap document is
defined at `runtime_protocol/timeline_commit_baseline.py:416-423`; the store
checks membership and refuses an already headed/unpublished state before
persisting the initial immutable publication at
`runtime_protocol/timeline_commit_store.py:994-1026`.

The old raw carrier is not available as an unrecorded escape hatch:
`runtime_protocol/service.py:2779-2807` refuses a tracked publication with
`timeline_commit_required`.

Agent v1 remains unchanged and output-only at
`/home/user/work/agent/astrid/sdk/timeline/native_initialize.py:7-22`.
Provider-side initialization admission requires the original bootstrap history
edge and exact base head at
`/home/user/work/agent/astrid/sdk/timeline/commit.py:923-933`.

## Why no Runtime DTO/port change is needed

The existing `RuntimeCommitPort` only exposes canonical reads plus
`preview(prepared)`/`accept(prepared)` at `runtime_protocol/timeline_commit.py:31-55`.
The coordinator passes detached context to the provider and checks invocation
identity at `runtime_protocol/timeline_commit_execution.py:69-115`.
The raw config is already inside the `PreparedCommit.canonical_document`, not a
new Runtime field.

The Runtime schema explicitly allows this carrier:

- `ParentComposition.config` is `RawTimelinePayload` and is described as exact
  authored data at `runtime_protocol/schemas/timeline-commit-bundle.json:3077-3110`;
- `RawTimelinePayload` is an open object at
  `runtime_protocol/schemas/timeline-commit-bundle.json:3180-3230`;
- structural validation only applies the existing parent/config clip check at
  `runtime_protocol/timeline_commit_store.py:437-446` and
  `runtime_protocol/visual_seam.py:78-90`.

Thus `theme_overrides`, opaque siblings, explicit nulls, absent keys, and list
ordering remain JSON values. The Agent codec opens and reconstitutes the same
immutable Runtime document at
`/home/user/work/agent/astrid/sdk/timeline/commit.py:75-161` and `:281-390`.
Runtime persists the parent payload and digest at
`runtime_protocol/timeline_commit_store.py:834-865`, and reloads/revalidates it
at `:288-319`.

## History, publication, retry, inverse, placement, identity

Runtime checks project/timeline membership, invocation/base-history identity,
and the exact expected head in `runtime_protocol/timeline_commit_store.py:691-741`.
It records the accepted command records, previous head pair, publication, and
CAS head update in `:884-910`. Exact retry is ledger-first: changed request
hashes are refused and an identical key returns the verified original envelope
at `runtime_protocol/timeline_commit_store.py:115-149`.

The proposed Agent guard owns ordinal/placement/shot and later inverse refusal;
its exact intended boundary is recorded in
`design/agent-wc10-pristine-raw-init-proposal.md:53-85`. Runtime need only
preserve the accepted records and immutable parent payload. The existing old
publication route remains refused, so no tracked legacy publication is
re-enabled.

## Concrete boundary

No Runtime semantic counterexample was found for JSON values, explicit
null-versus-absence, opaque siblings, or array order. One textual limitation is
material: `runtime_protocol/util.py:24-25` uses sorted-key `canonical_json`, and
the parent payload is stored in that canonical form at
`runtime_protocol/timeline_commit_store.py:863-865`. Therefore the ACK means
semantic raw JSON preservation, not preservation of textual JSON object-member
order. If object-member byte order is a hard requirement, this is a concrete
HOLD requiring a different codec; under the settled plan’s semantic raw-config
contract, it is not a blocker.

## Evidence boundary and next step

No tests were run. This was the requested source-only review; no product
implementation, generation, full/socket/browser/renderer/install run, or
route-retirement claim was made. Future activation requires the paired proof of
the original custom canvas positive, exact retry/restart, inverse, and
later-edit refusal, with v1 unchanged and no `publish_parent_composition`
escape hatch.
