# A3 child-placement caller return — PASS

The existing `ownerRef` identity carrier now reaches `placeGeneration` from both `useAddImageToShot`/`runAddImageMutation` and `usePositionExistingGenerationInShot`. The property is omitted when absent, preserving parent-only callers. Explicit malformed owners fail closed in the service; canonical foreign/ambiguous/destination guards remain in the existing fork path.

Changed only the six assigned service/caller/test files. Targeted five-file Vitest passed 61 tests; App TypeScript, scoped ESLint, diff check, normal Runtime/Agent lock checks, and private exact819acf Composition graph/archive checks passed. No shared install was mutated. Live Runtime admission, browser, build, full suite, and HTTP/body proof remain unverified.
