# Composition 0.0.13 release handoff

## Scope

The approved source proposal is unchanged from `af98594d`: it only re-exports
the existing `encodedEnvelopeSource` helper and `EncodedEnvelopeSource` type
from the public `evaluation` entry point. This worker added only release
metadata: package/lock version `0.0.13`, the matching README version line, and
one changelog line. No consumer pins, dependencies, source behavior, or 0.0.12
archive were changed.

## Artifact

- `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/artifacts/banodoco-timeline-composition-0.0.13.tgz`
- SHA-256: `9412ae25c306d5118241f4d631e8eecc6eef9b2fb5a98302d40938e9f6d54738`
- SHA-512 (base64): `6qgEAcfYqEGuiesoRlBFj1QnEgDKdZsisQdrMivONtc3lAct8thdzVbNV6L7lY5f2D9vvTIZHTD8vKhfWgLOuQ==`
- Size: 58,477 bytes; 77 regular archive members
- Repeated `npm pack` runs were byte-identical.
- Sidecar: `banodoco-timeline-composition-0.0.13.tgz.sha256`
- Exact sorted member list: `banodoco-timeline-composition-0.0.13.manifest.txt`

The 0.0.11 and 0.0.12 archive hashes remained unchanged before and after:

```text
dfa824a475737598477d98a2be2c2ad6ab9c3e6c8b0f967fad22e154afd74601  banodoco-timeline-composition-0.0.11.tgz
0a7b61529099ce994f807c6d7b1078303a09e7c0219144cc4b07467977f0f1a3  banodoco-timeline-composition-0.0.12.tgz
```

## Verification

- `npm run build` — PASS.
- Direct `npm run gen-registry:check` — PASS (also run by build/prepack).
- Targeted admission/evaluation lane — **16 passed, 0 failed, 0 skipped**.
- `npm test` — 10 of 11 files passed; the only failure is the known sandbox
  `EPERM` child-process failure in `scripts/gen-registry.test.mjs`. No test was
  weakened or skipped.
- Fresh extracted archive — PASS: safe 77-member manifest, ESM + SSR, public
  admission positive plus four forgeries, and scoped strict NodeNext consumer
  types (`skipLibCheck: true`). No install or network was used; peer packages
  were linked read-only from the shared graph.
- Strict NodeNext with `skipLibCheck: false` still reports the pre-existing
  declaration issue in `dist/lib/audio-envelope.d.ts` (`./audio-curves.generated`);
  this was reproduced on both 0.0.12 and 0.0.13 and was intentionally not
  fixed in this release.

No full suite, browser, renderer, socket, network publication, or App/Agent
consumer pin adoption was run or claimed. Handoff order remains App first,
then Agent, through their owning managers.
