# AM-sprite current element catalog unit

## Result

Prepared the approved `bdd02bd3f753e24092b982772bd481afc84f49da` AM-sprite capability unit for landing by running the normal element-catalog generator against the Agent-owned catalog only.

The tracked change is exactly one generated revision line in `astrid/packs/rendering/elements/catalog.ts`:

```text
sha256:f88ce18c3486aca0cf5a844420b822c554ff3b3eb396ab4c1ea54430a43be5b3
-> sha256:da9e894e6ad65f4503f60a9adf80596ad88ec1436302dcf57783d880496e1966
```

The approved AM-sprite component and its 33-case capability/SSR test are byte-unchanged from `bdd02bd3`. No generator, root CLI, or other artifact was edited.

## Evidence

- Normal catalog freshness: PASS.
- Targeted Agent lane: **33 passed in 25.55s**. This includes the registered SSR hash test, host neighbours, and the SDK address diagnostic.
- Ruff on the direct sprite test: PASS.
- `git diff --check`: PASS.
- Independent approved handoff source audit: **35/35 registered SSR samples byte-equal** between parent and candidate, aggregate `963140ecb235706a8f4c0ab57f5ba8f17984bad9ed58fa4f3647a128d888ca2b`; the current source files remain unchanged.
- Current diff scope: only `astrid/packs/rendering/elements/catalog.ts`.

The standalone replay against the archived review staging directory was not counted as fresh evidence: that directory lacks the complete alias closure and esbuild refused unresolved non-sprite element imports. The authoritative targeted pytest lane passed its own fresh SSR staging and assertions.

No full suite, browser, local listener, render, network, install, shared dependency/cache write, or git mutation was performed.

