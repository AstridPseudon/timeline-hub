Implemented D10 owner-preservation fix.

- Updated `scripts/gen_effect_registry.py` to retain source-less Composition winners and route valid shadow owners through the existing selector.
- Added permanent `text-card` public-winner/local-override regression coverage; unknown missing components still fail closed.
- No catalog changes; freshness remains truthful.

Tests:

```text
20 passed
normal catalog freshness: PASS
git diff --check: PASS
```

Used pinned Composition `0.0.13` in a private overlay with Node `v20.19.4`; shared dependencies were untouched.

The nine source deletions and their existing revision changes remain held for orchestrator/App provenance refresh. Commit message and `DONE` marker written.