# Composition 0.0.13 final gate

## Verdict

**APPROVE** `tl/vw-m3-release13-admission-only` for the local merge queue.

The approved source is `af98594dce80c0350a1fc21dfc44839b2279edf1` (`af98594dc`),
based on the approved proposal. The release-only delta from that source is exactly:

- `package.json`, `package-lock.json`: `0.0.12` -> `0.0.13`;
- `README.md`: one version line;
- `CHANGELOG.md`: one release line.

The source delta from `tl/integration` is exactly the existing
`encodedEnvelopeSource` / `EncodedEnvelopeSource` re-export in
`typescript/src/evaluation.ts` and its admission test. The validator/body is
unchanged. No consumer pin or dependency change is present.

## Artifact and archive checks

- Artifact: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/artifacts/banodoco-timeline-composition-0.0.13.tgz`
- SHA-256: `9412ae25c306d5118241f4d631e8eecc6eef9b2fb5a98302d40938e9f6d54738`
- Size: 58,477 bytes; 77 regular members.
- The actual sorted tar member list exactly matched the supplied 77-member manifest.
- Archive package metadata is `0.0.13`; root main import, `./evaluation` export,
  emitted `encodedEnvelopeSource`, and emitted `EncodedEnvelopeSource` declaration
  were inspected.
- Existing 0.0.11 and 0.0.12 hashes matched the recorded immutable values:
  `dfa824a475737598477d98a2be2c2ad6ab9c3e6c8b0f967fad22e154afd74601` and
  `0a7b61529099ce994f807c6d7b1078303a09e7c0219144cc4b07467977f0f1a3`.
- The admission worker reported repeated 0.0.13 packs byte-identical. I did not
  repack, per the final-gate instruction.

## Tests actually run

- `npm run build --prefix /tmp/vw-m3-release13-final-gate-review/source` on a
  private extraction of the release branch — **PASS**;
  registry check and build completed.
  The same extraction was removed after testing.
- `npm run build:test --prefix /tmp/vw-m3-release13-final-gate-review/source` —
  **PASS**.
- `node --import /tmp/vw-m3-release13-final-gate-review/source/typescript/tests/register-extensionless.mjs --test /tmp/vw-m3-release13-final-gate-review/source/typescript/test-dist/tests/audio-envelope-admission.test.js /tmp/vw-m3-release13-final-gate-review/source/typescript/test-dist/tests/evaluation.test.js`
  — **PASS**, 2 file subtests, 0 failures.
- `(cd /tmp/vw-m3-release13-final-gate-review/consumer && node smoke.mjs)` —
  **PASS**: public evaluation ESM import, valid
  admission, four forged negatives, root main import, SSR, declaration export,
  and installed-package byte immutability.
- `(cd /tmp/vw-m3-release13-final-gate-review/consumer && node_modules/typescript/bin/tsc --project tsconfig.json)` — **PASS**;
  scoped strict NodeNext consumer type check with `skipLibCheck: true`.
- Central rerun required for the prior registry-child `EPERM`:
  `R=$(/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/request-test vw-m3-release13-final-gate targeted --files "scripts/gen-registry.test.mjs") && /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/wait-test "$R"` — **PASS**, 1/1
  (`node --import tsx --test scripts/gen-registry.test.mjs`).
  The original worker `npm test` result remains honestly recorded as 10/11
  files because of its sandbox child-process `EPERM`; it was not relabeled as a
  full-suite pass.
- `(cd /tmp/vw-m3-release13-final-gate-review/consumer && node_modules/typescript/bin/tsc --project tsconfig-strict.json)` and the same command in `consumer12` — **exit 2 on both 0.0.12 and 0.0.13**, with the identical pre-existing error:
  `dist/lib/audio-envelope.d.ts(1,35): TS2307: Cannot find module './audio-curves.generated'`.

## Limits

No full suite, browser, renderer, socket, network, install, repack, publication,
or consumer pin adoption was run. The review worktree is clean; no source files
were changed by this final-gate worker.
