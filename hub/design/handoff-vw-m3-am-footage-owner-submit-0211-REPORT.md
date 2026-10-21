# AM-footage current-source owner submission

The current Agent integration is `4467c1c1a9ed81fa7cd1b2d7687b8ada54dc216a`.
The exact qualified owner donor is committed as
`53d1f5c7282064fcf8802646313bf31612dd8ee8`, with that current integration
head as its parent. It is not integrated yet, so this is a clean owner
handoff rather than a source-parity NOOP; there is no conflict and no source
replay was performed here.

`handoff-vw-m3-am-footage-owner-submit-0211-PATCH` is the exact eight-file
diff from the current head to the donor, and `git apply --check` passes. The
existing typed generator boundary at
`2b25a16cae6d1fdc5c3e6ab1d4883fab19bf7f90` is already in the current base and
is intentionally not duplicated. No live caller is activated or changed.

The packet preserves custom owners and immutable admissions, transparent
inset alpha as unknown, full-field missing/blank-media SLOT behavior, the
invalid legacy `x/y/scale` non-geometry behavior, and every existing
assertion. It adds no pin, DTO, route, store, release, physical run, or broad
merge.

Qualified evidence: pack validation; 5 direct scene tests; 1 volume test; 46
public13 host/scene-answer tests; 11 generator/custom-owner/refusal tests;
source-closed Root typecheck with zero diagnostics; normal catalog generation
and freshness check; Ruff; diff checks; and clean-patch application all passed.
The pinned inputs were Node 20.19.4, the read-only peer graph, and Composition
0.0.13 artifact SHA-256
`9412ae25c306d5118241f4d631e8eecc6eef9b2fb5a98302d40938e9f6d54738`.
No install, browser, physical, full-suite, or shared-dependency write is
claimed.

Apply the patch on the owner branch and run the accompanying `COMMAND`; use
normal metadata generation and do not hand-edit or replay the older packet.
