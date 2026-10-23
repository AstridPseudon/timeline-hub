# A3 shared popup handoff

The resumed `4157ffb1a` WIP retains the existing A2 durable save path. When
the selected occurrence and another original occurrence share the verified
child root, popup ADD/SWAP produces `occurrence.fork` first and then the
existing occurrence-owned media command. SWAP reads the old selection from the
pre-edit canonical registry; ADD/SWAP use the authenticated Runtime selection
carrier already supplied to the provider. No duplicate occurrence, guessed
physical successor, managed-edge patch, TypeScript executor, or new route was
added.

Changed product files are limited to:

- `src/tools/travel-between-images/components/shotTimelineDataProvider.ts`
- `src/tools/travel-between-images/components/shotTimelineDataProvider.a3.test.ts`

Evidence: A3 target 23/23; combined A3/popup/element targeted run 64/65 with
the one inherited popup opaque-`__proto__` failure at
`ShotTimelinePreview.test.ts:716`; TypeScript, scoped ESLint, diff check, and
normal Runtime producer lock all pass. The exact private Composition graph
(`819acf…`, `0.0.14`) was used through `NODE_PATH` without touching shared
`node_modules`.

Live Runtime admission, browser/journey, full-suite, and HTTP-body evidence
remain intentionally unverified. Independent Luna review and App-home
merge-forward are next.
