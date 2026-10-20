# Runtime private 357/613 consumer probes

Date: 2026-10-20 UTC

Status: **prepared; intentionally unexecuted**. The normal private generator
worker owns the product generator and generated artifacts. These are external
consumer probes only and do not change that work-in-progress.

## Pinned input

- Agent source commit: `357230816c86da65d5f8cc92b10a3a90d29874e0`
- Agent source tree: `94692ec85167d5c606626c4ec678fe2a63ee0aa5`
- canonical schema: 55 `$defs`, 29 operation clauses, 13 v2-capable operations
- canonical schema SHA-256: `613123b2760150f9f33e23485516d757359c3eaebfe02d552bc97155309aaad3`
- source schema input: materialize from the immutable Agent commit at probe
  execution time; no checked-in JSON snapshot is used

The Python probe must be given an exact source-schema file materialized from
the pinned Agent commit. It fails closed on any other digest. A private
temporary copy is sufficient and is deleted after the probe.

## Probe files

- `workers/rt-m2-private613-client-probes/probes/typescript_consumer_probe.mts`
  is a tiny external TypeScript consumer. Replace its two placeholders with
  absolute candidate source paths ending in `.js`, then run strict NodeNext
  type-checking. It imports all 55 source definitions through the package
  barrel, directly checks the timeline DTO too, checks the seven new public
  Args/`WordAnchor` exports, accepts `clip.move` v2, and expects compile errors
  for `producer.guard` v2, unsupported `clip.move` versions, and typed fields
  accidentally degraded to `any`.
- `workers/rt-m2-private613-client-probes/probes/python_reflection_probe.py`
  loads the candidate Python DTO by path. It checks the closed `EditCommand`
  discriminant pairs, all 55 source definitions, absence of `typing.Any` in
  those source definitions, package-root exports/`__all__`, the
  `tuple[int, int]` receipt sequence, and unchanged old public schema floors.

No JSON snapshot, generated matrix, provider, health, schema override, native
pair, or full-suite machinery is involved.

## Execution after the final commit only

From the orchestrator scratch root, after the generator worker has committed a
candidate and supplied its exact path/tree, first materialize the pinned source
schema into a private temporary directory:

```sh
ORCH=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a
tmp=$(mktemp -d)
git -C /home/user/peteromallet/astrid-agent show \
  357230816c86da65d5f8cc92b10a3a90d29874e0:astrid/core/timeline/schema/edit-command.schema.json \
  > "$tmp/edit-command-357.json"
python probes/python_reflection_probe.py \
  /path/to/final-runtime-candidate \
  "$tmp/edit-command-357.json"
```

For TypeScript, make a private temporary copy of the fixture, replacing
`__CANDIDATE_INDEX__` with
`/path/to/final-runtime-candidate/packages/typescript/src/index.js` and
`__CANDIDATE_TYPES__` with
`/path/to/final-runtime-candidate/packages/typescript/src/timeline-commit-types.js`,
then run:

```sh
tsc --noEmit --strict --module NodeNext --moduleResolution NodeNext \
  --target ES2022 /private/tmp/typescript_consumer_probe.mts
```

The source tree must be the generator worker's final committed candidate, not
the mutable WIP path. Do not report these as green until both commands have
run against that exact candidate.

## Expected evidence

The probes cover the generated consumer surface only. They do not qualify the
old public v1 103-read/3-selection native behavior. The Python check preserves
the three published old schema floor bytes and OpenAPI receipt provenance; the
TypeScript check preserves the main `MutationReceipt` alias and the direct
timeline DTO alias with `[number, number]`. Native 103/3 behavior remains a
separate held gate and must be reported unexecuted here.
