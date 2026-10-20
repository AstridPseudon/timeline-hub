# Runtime ordinary014 normal candidate tuple

**Status: REVIEWED CANDIDATE / NOT CURRENT.** This is a concrete handoff for coordinated Agent/App qualification only. It is not a public release, consumer pin, integration pin, merge, or Runtime bump.

## Exact candidate and source provenance

| Field | Exact value |
| --- | --- |
| Runtime candidate commit / client producer SHA | `a0dca16975dfe8f5e762703b99d9791a16cf7fd7` |
| Runtime candidate tree | `4b7dd0fe44be973c344bab3de568eaf0bdd28476` |
| Candidate parent corrected from | `806636baf42e9ed1e4c7f9fe76c3e14d7330fcc1` |
| Corrected working patch SHA-256 | `9f19160ea6ffbd44105e615432bb9b2f44c0a258799a200ba5c362d60d58c7dc` |
| Generated client/package version | `0.2.14` (unpublished) |
| Frozen Agent source commit | `310e54840fa5fb8eb7e51bb64ed2c34b7a1063b3` |
| Frozen Agent source tree | `c5a8a3ec7e9e01c61c5ae31834da53bed4be406a` |
| Frozen Agent raw schema SHA-256 | `sha256:6ba7b51e9518e7fb08b27ad5b7225855276b657d0adebf704dd853f699768f2d` |
| Runtime wire/schema digest | `sha256:ce3781c282564b650890456f6c257f3faabe2de3898a84363fecd47e48b30d59` |
| Corrected artifact manifest version | `sha256:f021e7714c1b40011b69ba624d288c217749d58013b8adf0352d283854f20fa0` |
| `contract/artifacts.json` SHA-256 | `sha256:ecda762ebe682f266395161af055921c3db33ee9914fb00860626e7e4852d815` |
| Counts | 55 definitions, 29 command operations, 75 artifacts, 133 unique HTTP operations |
| Frozen S2 floor | `sha256:a6f1aaa9dfcc31828bd04c908158fd7fd9a825df6c9f88f79b81779273a190ef` |

The frozen Agent schema is the source authority: 55 definitions and 29 operations, with the exact raw hash above. The corrected candidate was independently approved in `workers/rt-m2-ordinary014-corrected-final-review/report.md` and by the Agent export review. The seven added public Python DTO names are:

`AssembledTargetArgs`, `ClipAddMediaArgs`, `TimelineInitArgs`, `WordAnchor`, `ClipAnchorArgs`, `OccurrenceCreateArgs`, `TextBindingSetArgs`.

The corresponding additive operation names are `timeline.assembled-target`, `clip.add-media`, `timeline.init`, `clip.anchor`, `occurrence.create`, `clip.swap-media`, and `text-binding.set`. All seven root exports identity-match their DTO definitions and appear in `__all__`.

## Normal generated paths and reproducibility

The corrected export repair changed only these intended generated/contract paths:

```text
contract/artifacts.json
generators/python_client_init_template.py
packages/python/astrid_runtime_client/__init__.py
tests/test_timeline_current_union_contract.py
```

Reproduce the normal checks from the Runtime candidate worktree:

```sh
python generators/generate.py --check
python scripts/artifact_manifest.py --check
node tools/generate_typescript_conformance.mjs \
  --contract contract/openapi/workspace-v1.yaml \
  --schema-manifest contract/manifest.json \
  --component-manifest contract/component-manifest.json \
  --check --source-root "$PWD" --fixture-root "$PWD/conformance/fixtures"
```

The checked evidence is: `tests/test_timeline_current_union_contract.py` **64 passed**; independent generated-client `test_generated_client.py` **73 passed** in the central lane; central commit integration **9 passed**; central TypeScript lane **61 passed**; and the frozen Agent native cohort **11 passed**. Generator, artifact-manifest, TypeScript reproducibility, direct export/import, floor, metadata, forbidden-surface, and diff checks also passed. The five local socket cases were covered by the independent central 73-test client lane.

## Compatibility and qualification boundary

The rejected artifact version `sha256:8023c665f0e32835cf06b793c6f5ffa0a278a7ca5aadbfe971d52d163d66c7a3` and rejected parent/candidate `806636baf42e9ed1e4c7f9fe76c3e14d7330fcc1` are **not consumable**. Do not fall back to them or describe them as ordinary014.

The current public 0.2.13 producer remains immutable: Runtime producer commit `2c4ac180c2220bdad966bc01e95ad230e99ce26a`, with the existing public consumer guard `sha256:6f000bc615a9cb24fb00cc69a97af75eae71006ebfe87e3caa272fcdbbb1af56`. Ordinary014 does not replace or mutate that public tuple.

For qualification, Agent consumer source must compose current Agent `8130a401` (P1/WC4/Scene and its current extractions) over the frozen `310e5484` source/schema. The private carrier is excluded. App and Agent must qualify their normal-owned branch pins as **one cohort** against the exact Runtime candidate above, with generated-client byte identity, package/version/digest guards, and consumer behavior proof. Do not create an integration pin, publish 0.2.14, or bump Runtime consumers until all required gates pass and the owner confirms release.

The already-active `agt-review-ordinary014-corrected-exports` review is the coordination point; do not duplicate that review. This tuple is a review handoff, not release authorization.

## Approval record copied with provenance

Source: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-m2-ordinary014-corrected-final-review/report.md`.

> ## Verdict: APPROVE
>
> Verified committed candidate:
>
> - Commit: `a0dca16975dfe8f5e762703b99d9791a16cf7fd7`
> - Tree: `4b7dd0fe44be973c344bab3de568eaf0bdd28476`
> - Parent: rejected `806636baf42e9ed1e4c7f9fe76c3e14d7330fcc1`
> - Worktree clean; no product edits made.
>
> Checks passed:
>
> - All seven DTOs publicly exported with identity and `__all__` coherence.
> - Frozen Agent schema byte match: `6ba7b51e…768f2d`; exact 55 definitions/29 operations.
> - Metadata: schema wire `ce3781c2…30d59`, artifact version `f021e771…f20fa0`, 75 artifacts, 133 unique HTTP operations.
> - S2 floor unchanged: `a6f1aaa9…a190ef`.
> - Generator/artifact/TypeScript reproducibility checks passed.
> - `tests/test_timeline_current_union_contract.py`: 64 passed.
> - Central `test_generated_client.py`: 73 passed, covering the five local sandbox socket failures.
> - Central commit lane: 9 passed.
> - Central TypeScript lane: 61 passed.
> - Frozen Agent native cohort: 11 passed.
> - Direct import/export, floor, metadata, forbidden-surface, and diff checks passed.
>
> No full suite, merge, pin, publication, or release activation was performed.
