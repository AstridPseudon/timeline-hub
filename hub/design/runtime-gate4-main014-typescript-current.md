# Runtime Main014 Gate 4 TypeScript evidence

Date: 2026-10-21 UTC

The current generated TypeScript Gate 4 gap is closed by one central named
run. The run used the current Runtime integration commit
`b92d3e7a05eec65c142294ef4873edd059e9b31d`, tree
`6abc2f117391de8e7e35c0283f575a002199894d`, which is unchanged in the
published Main014 TypeScript package relative to published Runtime source
`95bd3c5f6d00e9bc8cc8cbe5ef510b68ed660f3c`, tree
`d3a290b407fa61e6ab2d476f50c068073f70df00`.

## Source and test binding

`git diff --quiet 95bd3c5f6d00e9bc8cc8cbe5ef510b68ed660f3c b92d3e7 --
packages/typescript` passed: the package and all generated source/test blobs
are byte-identical between the published source and current integration.
The conformance TypeScript inputs and generator are also byte-identical.

Current `packages/typescript` Git blob identities:

| Path | Blob |
| --- | --- |
| `package-lock.json` | `42748348c0055afba7653ce303dfde065a9aa70c` |
| `package.json` | `20de522232bb5fad007ed67231c2b985dd7a2a49` |
| `src/contract-metadata.ts` | `1042b6a3f627a7bc1daddb2ffd6a4a9f44a6764f` |
| `src/generated.ts` | `16d8e5609f41b3d73373e7698b132ff118d2ec9d` |
| `src/index.ts` | `270fdf03fc27473a1b12560bd9592241b9861c9d` |
| `src/operation-handle.ts` | `000d9d334c392bb00a0ec0dd2efa6bf5cbbc5a3d` |
| `src/timeline-commit-types.ts` | `213a70634532ba45ad1f3e02239a14e673d06657` |
| `test/client.test.mjs` | `5292ab7abff843b093c270a51f58621c2e5af0eb` |
| `test/operation-handle.test.mjs` | `70ad70841a3a8477e86be2eb516eddbdbb39b683` |
| `test/public-api.mts` | `a53a3050a5b759dc2838838d102d46008bbf40f9` |
| `tsconfig.json` | `8c6d3074e9524435ff34591a946aeea18d6b5468` |

The package version is `0.2.14`. The prior 61-test result was correctly
retained as historical 0.2.13 evidence because it was not bound to these
published generated blobs; this run supplies that missing current proof.

## Central result

Suite: `runtime ts-client-check`  
Result ID:
`rt-m2-gate4-main014-ts-evidence-0407-ts-client-check-1021040813-12394`  
Result tree: `6abc2f117391de8e7e35c0283f575a002199894d`  
Command:

```text
cd packages/typescript && PATH=/home/user/work/app/node_modules/typescript/bin:$PATH npm test
```

Result: **61 passed, 0 failed, exit 0**, duration 3 seconds. The suite's
Node test summary was `# tests 61`, `# pass 61`, `# fail 0`.

No full, Python, browser, renderer, install, or code/pin/version run was
performed. Shared dependencies were read-only; no cache or build output was
left in the worker worktree.
