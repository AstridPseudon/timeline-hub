# Handoff: P1 diagnostic current port

Status: PASS for the source-only test port; no integrated behavior credit.

## Exact base, head, tree, and donor

- Worktree: `/home/user/work/wt/ap2-P1-diagnostic-current-port-0603`
- Branch: `tl/ap2-P1-diagnostic-current-port-0603`
- Base and current pre-harness HEAD: `cffa91c93e80717cec1a4e740fae67140394eb88`
- Base/current pre-harness tree: `8eb4d915848663c5cd1ea9ee2eabb8c14404f411`
- Donor commit: `cc05d7de25d4842964d3a4e5d5ff792f53294e0e`
- Donor path: `tests/e2e/local/three-products.p1-chain.spec.ts`
- Donor Git blob and current worktree blob: `4f0e7a97e67051ccd5c587f7e9ea6c3ae70f9cf2`
- Donor/current file SHA-256: `956aaf219aae927d23a4f13e0ce8b0e358fe235508454fe70b0c6ad6ed84eb8c`
- `git merge-base --is-ancestor cc05d7de25d4842964d3a4e5d5ff792f53294e0e HEAD` — exit 1; donor is outside current-base ancestry.

The resulting uncommitted tree is the base tree plus the one exact donor blob
at the requested path; the harness will create the commit. No donor branch was
checked out and no donor product/report ancestry was introduced.

## Change and allowed observations

Only the existing P1 spec was ported. The diagnostic addition records bounded
counts/booleans/fixed enum values and route templates for failure context. It
does not record arbitrary keys, text, auth/cookie/header/body/URL/path/query
values. Original two-case bodies, 90-second owner wait, navigation, connected
state, lost-ACK/restart flow, exact retry, accepted/merged/refused predicates,
canonical/head/digest/receipt/history/dependency/raw/opaque/order/rollback and
undo assertions remain byte-for-byte donor content.

## Commands and results

```text
TMPDIR=/tmp/ap2-P1-diagnostic-current-port-0603 npm exec -- playwright test --config playwright.three-products.config.ts tests/e2e/local/three-products.p1-chain.spec.ts --list
PASS — Total: 2 tests in 1 file

npm exec tsc -- --noEmit
PASS

npx --no-install tsc -p tsconfig.app.json --noEmit
PASS

npx --no-install tsc -p tsconfig.node.json --noEmit
PASS

npx --no-install eslint tests/e2e/local/three-products.p1-chain.spec.ts --max-warnings 0
PASS

git diff --check
PASS
```

Exact donor comparison, changed-path listing, and no-ancestry checks also
passed. The E2E spec is outside the App/Node tsconfig include sets; the type
checks therefore do not claim semantic coverage of the spec. The donor's
erased type-annotation spelling was preserved without broadening scope.

## Limits and next step

The original two-case service on port 19451 was already running on the exact
donor for retained diagnostics. I did not change the suite, duplicate the body,
or run HTTP/socket/body/build/full/browser/service execution. No integrated
behavior or H3 credit is claimed. Independent Luna review and the manager's
normal integration/remote-queue handling remain the next steps; only this
worker's own commit should be selected.
