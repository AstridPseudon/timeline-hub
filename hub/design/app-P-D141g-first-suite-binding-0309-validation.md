# D141g source-only binding validation

Status: PASS for prospective production-builder preparation; no registration, checkout request, service request, browser, journey, provider import, or body execution.

## Exact binding

- target: `app-pin-520d7e4f`
- repo: `app`
- selector: `p2-automatic-child-placement`
- normal suite: `d141g-p2-automatic-child-placement-520d7e4f-submit`
- preflight suite: `d141g-p2-automatic-child-placement-520d7e4f-submit-preflight`
- registration: `false` (row names absent from the registry preimage)

## Read-only Git checks

Commands run for each source home:

`git -C <repo> rev-parse HEAD`

`git -C <repo> rev-parse HEAD^{tree}`

`git -C <repo> status --porcelain=v1 --untracked-files=all`

Results:

- app: head 520d7e4fc12a03392afaed3f486aba34a2b5c319 (expected 520d7e4fc12a03392afaed3f486aba34a2b5c319; match=true), tree 70ad390c56b0e45d9279b4179598b6cdbad9ed65 (expected 70ad390c56b0e45d9279b4179598b6cdbad9ed65; match=true), status porcelain=empty
- agent: head 28e56cacb42d3da85b02e5b3543895b44f3d0f70 (expected 28e56cacb42d3da85b02e5b3543895b44f3d0f70; match=true), tree 2ebe2ddf5a61f013953ab1e21d51ebaab746e58a (expected 2ebe2ddf5a61f013953ab1e21d51ebaab746e58a; match=true), status porcelain=empty
- runtime: head 6a011d58e69173d70e2e9bb3ac434ac8f9e87d8d (expected 6a011d58e69173d70e2e9bb3ac434ac8f9e87d8d; match=true), tree ac5b862744bece65b2e30565db1777bacd60da28 (expected ac5b862744bece65b2e30565db1777bacd60da28; match=true), status porcelain=empty
- composition: head 635f4de06fda22a85fc2e4cfc764d0153a4c9f40 (expected 635f4de06fda22a85fc2e4cfc764d0153a4c9f40; match=true), tree 5ab5191a296980a0a6bcd1178ab6902d6478a148 (expected 5ab5191a296980a0a6bcd1178ab6902d6478a148; match=true), status porcelain=empty

## Pure production builder

Command:

`/home/user/work/runtimes/agent-remotion-app-p1-787-2a9-1830/.toolchain/node-v20.19.4-linux-x64/bin/node /home/user/work/wt/app-P-D141g-first-suite-binding-0309/generate-d141g-binding.mjs`

The temporary harness imported only `serviceRecipe` from `/home/user/work/app/scripts/testing/d66-plain-stack.mjs`, invoked it for the normal and paired preflight recipes with the full pinned tuple, and supplied no diagnostic helper. The generated command files contain exactly the production-returned UTF-8 bytes with no trailing newline. Hashes and exact row hashes (one terminal LF convention) are recorded in `binding.json`.

Builder source: Git blob `59b65214bc74c1ca118b097bc3b13c0ffe480a93`, SHA256 `2032f3087faab5bc1037b54faa593cb32536de15b748809601731ad5f6a7602f` (49914 bytes).

## Independent prior-row comparison

The authentic registry rows 408/409 for the prior 867 tuple were regenerated with the same pure builder and compared byte-for-byte. Both matched exactly; differences are explicitly recorded as `null` in `binding.json`.

The new 520d normal and preflight names were absent from the current registry preimage SHA256 `5ce57b6ee789de40c6d25874a29af37c4fff3d477b913219617eff8b1d01f072` (733149 bytes). No registry bytes were written.

## Scope and handoff

No tests were run because this task is source-only and the brief forbids journey/browser/body checks. The later normal D66 `--submit` caller must use the exact tuple and suite names, atomically register the paired rows through the production path after kit admission, and compare genuine registered command bytes to these prospective hashes before dispatch. The future submit-plan path is not written here.
