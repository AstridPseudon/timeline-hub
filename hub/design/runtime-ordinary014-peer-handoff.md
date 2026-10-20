# Runtime ordinary014 peer handoff

Prepared for coordinated Agent/App qualification, not public release.

Use only Runtime commit `a0dca16975dfe8f5e762703b99d9791a16cf7fd7`, tree `4b7dd0fe44be973c344bab3de568eaf0bdd28476`, package `0.2.14` (unpublished). It is the corrected, independently approved candidate from `workers/rt-m2-ordinary014-corrected-final-review/report.md`; source provenance is frozen Agent `310e54840fa5fb8eb7e51bb64ed2c34b7a1063b3`, raw schema `sha256:6ba7b51e9518e7fb08b27ad5b7225855276b657d0adebf704dd853f699768f2d`. Candidate wire digest is `sha256:ce3781c282564b650890456f6c257f3faabe2de3898a84363fecd47e48b30d59`; corrected artifact version is `sha256:f021e7714c1b40011b69ba624d288c217749d58013b8adf0352d283854f20fa0` (75 artifacts, 133 unique HTTP operations; 55 definitions / 29 command operations).

Evidence: current union 64, independent generated client 73, central commit 9, central TypeScript 61, and frozen Agent native 11 all passed. The seven public DTO exports are restored and identity-checked. Rejected artifact `sha256:8023c665f0e32835cf06b793c6f5ffa0a278a7ca5aadbfe971d52d163d66c7a3` / rejected parent `806636baf42e9ed1e4c7f9fe76c3e14d7330fcc1` is not consumable.

Current public 0.2.13 producer `2c4ac180c2220bdad966bc01e95ad230e99ce26a` remains immutable. Agent consumer qualification must compose current Agent `8130a401` P1/WC4/Scene over frozen source `310e5484`; carrier excluded. App and Agent must pin and prove this exact candidate as one normal-owned cohort. No integration pin, release, or Runtime bump before gates and owner release confirmation. Coordinate through the active `agt-review-ordinary014-corrected-exports` review; no duplicate review.
