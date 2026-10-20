# Runtime union613 generator readiness

Date: 2026-10-20
Worker: `rt-m2-union613-generator-readiness`
Base: `e2db1e8cc7c176fafa1e4e651da3639b6e3a89dd`

## Result

Source-only technical review: **APPROVE for the compatibility gate; not ready
for normal generation/adoption**. No Runtime schema, generated artifact,
package version, consumer pin, or release metadata was changed.

The immutable Agent source at
`357230816c86da65d5f8cc92b10a3a90d29874e0`,
`astrid/core/timeline/schema/edit-command.schema.json`, is the expected shape:

- raw SHA-256: `613123b2760150f9f33e23485516d757359c3eaebfe02d552bc97155309aaad3`
- 55 `$defs`, 29 operation conditionals
- 13 source-bound operations with closed v1/v2 conditional branches
- the source's ordinary projection reproduces floor `6ba7b51e9518e7fb08b27ad5b7225855276b657d0adebf704dd853f699768f2d`

The existing generator can render the 55 source definitions in an isolated
scratch directory, but it currently flattens `EditCommand` to an open
`op: string`, `version: string`, `args: dict`/`Record` shape. It therefore does
not yet preserve the source's per-operation closed v1+v2 union in generated
Python/TypeScript. The current public-export template also predates the seven
new source DTO exports: `AssembledTargetArgs`, `ClipAddMediaArgs`,
`ClipAnchorArgs`, `OccurrenceCreateArgs`, `TimelineInitArgs`,
`TextBindingSetArgs`, and `WordAnchor`. These are freeze-dependent generation
work, not Runtime artifact changes for this task.

## Bounded change landed

Updated `generators/command_schema_compatibility.py` to carry the reviewed 622
repair:

- prove the five historical 0.2.2 regex widenings by constructing an
  intermediate widened previous schema and checking full containment into the
  candidate;
- retain complete old operation branches when the candidate adds a union;
- distinguish an absent schema keyword from a present keyword whose value is
  JSON `null`;
- do not rewrite or weaken the candidate during compatibility checking.

Added one small regression test proving that an unknown keyword with a null
value is rejected by both compatibility paths. The base does not contain the
later 0147 export-fix candidate (`a0dca16`); no generated export file was
rewritten here, and that fix must remain in the post-freeze adoption delta.

## Exact evidence

Source and floor audit (read-only source checkout plus in-memory comparison):

```text
git -C /home/user/peteromallet/astrid-agent show 357230816c86da65d5f8cc92b10a3a90d29874e0:astrid/core/timeline/schema/edit-command.schema.json
```

The source passed `compatibility_errors` against `runtime-0.2.3.json`,
`runtime-0.2.10.json`, `agent-0a0ac7ba.json`, and `agent-26ef2bbb.json`, and
passed `legacy_022_compatibility_errors` against `runtime-0.2.2.json`; each
returned zero errors. The ordinary projection digest was independently
`6ba7b51e...f2d`, as above.

Normal CLI check:

```text
PYTHONDONTWRITEBYTECODE=1 python generators/generate.py --check
```

Result: exit 0. It wrote no files.

Targeted tests:

```text
PYTHONDONTWRITEBYTECODE=1 python -m pytest -q tests/test_command_schema_compatibility.py
```

Result: 131 passed, 1 pytest warning (`timeout` config option unknown in this
environment), 45.61s.

```text
PYTHONDONTWRITEBYTECODE=1 python -m pytest -q tests/test_timeline_commit_type_generator.py tests/test_timeline_current_union_contract.py
```

Result: 69 passed, 1 pytest warning, 8.78s.

An earlier combined targeted run of the compatibility, DTO generator, current
union, client parity/release, and Python public API tests also passed: 205
passed, 1 warning, 54.43s. No full suite or live/browser suite was run.

## Minimal remaining delta after freeze

1. Add an explicit, read-only source-schema input to the normal generation
   path (or an equivalent manager-approved source projection), with fail-closed
   provenance and the 6ba ordinary floor. Do not replace the Runtime schema
   from an arbitrary path.
2. Teach the DTO renderer to emit a closed per-operation `EditCommand` union,
   retaining v1 and v2 branches for exactly the reviewed 13 operations while
   preserving the other 16 operation clauses.
3. Generate and test all 55 source definitions and restore the seven public
   DTO exports, including package-root Python exports and the TypeScript
   package barrel as appropriate.
4. Only after manager freeze/version approval, regenerate the Runtime bundle,
   clients, metadata, artifact manifest, and consumer pins in the coordinated
   release step.

No blocker was found in historical compatibility after the 622 repair. The
remaining blocker is procedural and architectural: source-bound DTO union
generation and public artifact adoption require the manager's freeze/version
decision, which this task explicitly did not make.
