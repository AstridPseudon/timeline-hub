# Handoff: P3 checkout custody diagnosis

The P3 pre-gesture failure was an honest legacy-baseline boundary mismatch.

`seedThreeProducts()` creates the real parent/shot/internal closure through the
legacy composition publication route. Runtime does not expose a retained
`dependency_manifest` on that legacy parent read. Qualified Agent checkout source
`bd2394615`/`a8132af` now requires the manifest's exact
`internal_timelines[].timeline_id` owner mapping, so it correctly returned:

```text
integrity_error: pinned internal revision has no exact owner timeline
```

The smallest correction is in the worker-scoped `seed3` fixture setup: enable the
existing Astrid authoring profile, then POST the same timeline identity/name through
Runtime's existing timeline creation/adoption boundary. Runtime upgrades the exact
legacy baseline to the commit-owned closure and retains the complete authenticated
manifest. The P3 service body, selector, gesture sequence, commands, and assertions
remain unchanged.

Changed file: `tests/e2e/local/three-products.spec.ts`.

Evidence: ESLint passed; qualified Agent owner-scope/revision-diff tests passed
23/23. The original browser/build/full/service run remains unverified and should be
rerun centrally.
