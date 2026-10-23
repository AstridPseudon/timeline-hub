# P1 diagnostic source identity disposition

**SOURCE PASS for `956aaf219aae927d23a4f13e0ce8b0e358fe235508454fe70b0c6ad6ed84eb8c`.** The committed source is exactly the final author source substantively reviewed and checked by 0551. No unreviewed source delta was found. This resolves source metadata only; it awards no live P1/H3 behavioral credit.

## Exact source

- App HEAD: `cc05d7de25d4842964d3a4e5d5ff792f53294e0e`
- App tree: `576deeb1a1d361be539176624083ae31679c8be3`
- Spec: `tests/e2e/local/three-products.p1-chain.spec.ts`, 32,557 bytes
- Git blob: `4f0e7a97e67051ccd5c587f7e9ea6c3ae70f9cf2`
- Git blob bytes, current worktree bytes, final 0545 logged diff reconstruction, and 0551 recorded reviewed/tested source all bind to the SHA-256 above.
- Original `ec8e8a25c` assertion region from `// Source proof only:` through EOF: SHA-256 `479f14ded6abf56261ab6670447cc54cb0c9d4d0a93c2c4629748902c5e763a1`, byte-identical to this candidate.

## Explanation of the mismatch

This was an actual final source edit, not line endings, a Git filter, or serialization. Independently applying the author's logged unified diff to the exact `f7f45ad0babfa6cb6e17070182c7021adef20587` parent reproduces intermediate Git blob `527f5f5f45257d6bf43cb1fba94efe9b0443ef65` and SHA-256 `f316c8bd63b87837673a517e8fbab6bf4f4cdb4997b0d2b8f948f6f477dec929`. Applying the final logged diff reproduces the committed blob and `956aaf...` exactly, including Git blob identity and file length. Both versions use LF; filter/text/eol attributes are unspecified for this spec.

The entire intermediate-to-final delta is one hunk in `summarizeOutboxes`: add `const observed = records.slice(0, DIAGNOSTIC_LIMIT);`, then derive `intentLengths`, `pendingIntentLengths`, and `outcomeKinds` from `observed` instead of `records`. This caps those three emitted arrays at the existing 40-entry limit. The author's log announces the hardening at lines 5148–5153, records the final type/lint/list/witness checks at lines 5485–5523, and records the final `956aaf...` hash at line 5528. Earlier report metadata had recorded the pre-hardening hash; the dispatch/review brief retained it. The author subsequently corrected its report/handoff to `956aaf...` in the same log. Actual author is **ap2-P1-diagnostics-return-0545**, not 0455.

The independent **ap2-P1-diagnostics-return-review-0551** log records HEAD/tree and `956aaf...`, runs checks on that source, and explicitly passes structural allowlist safety, original assertions, and the adversarial witness. Its FAIL was the stale required `f316c8...` identity. The final array cap is therefore already within the substantively reviewed bytes. No safety check is removed or bypassed.

## Checks performed here

- `timeout 45 python /tmp/w-81adedbc88/identity.py` — PASS, exit 0. Reconstructs both author diff versions in memory, validates SHA-1 blobs and SHA-256 files, checks committed/worktree/reviewer identity, original assertion bytes, original 90-second idle-owner predicate, and unchanged tracked source outside this task. Saves the exact delta and identities in this worker's scratch directory.
- `timeout 45 python /tmp/w-81adedbc88/update-suite.py` — PASS, exit 0. Replaces only the existing P1 spec hash with a concurrent-edit guard. Inverse replacement restores the entire original suite file byte-for-byte; every other row and every other byte of this row is unchanged.
- `timeout 45 python - <<'PY' ... PY` (original-helper byte comparison, full inline script in this worker's tool log) — PASS, exit 0. Original pre-openChain request/reply/seed/history/observation helpers and the setPlayhead/split/trim/forward region are also byte-identical to `ec8e8a25c`.
- `git diff --check` — PASS, exit 0.
- `git diff --exit-code HEAD -- .` — PASS, exit 0; no tracked App change.
- `git status --porcelain=v1 --untracked-files=all` — empty.
- `git check-attr filter text eol -- tests/e2e/local/three-products.p1-chain.spec.ts` — all unspecified.

`tmpdir` in the worker directory is the harness pointer file containing `/tmp/w-81adedbc88`; scratch was written only to that resolved worker directory. No cleanup or deletion was performed.

## Reused 0551 checks on the exact same App tree/spec

- `npm exec tsc -- --project tsconfig.app.json --noEmit` — PASS.
- `npm exec tsc -- --project tsconfig.node.json --noEmit` — PASS.
- `npx eslint tests/e2e/local/three-products.p1-chain.spec.ts --max-warnings 0` — PASS.
- `npx playwright test --config playwright.three-products.config.ts tests/e2e/local/three-products.p1-chain.spec.ts --list` — PASS, exact 2 tests in 1 file.
- `git diff --check` — PASS.
- `node --input-type=module <<'NODE' ... NODE` (full script in 0551 log lines 5418–5462) — PASS: transpiles the actual helper region, injects quoted/unquoted secret-shaped JSON/error/key/body/path/header/cookie/alert/UI values, and asserts no exact secret survives; also checks fixed error, route, connection-state and outbox classifications.

The typecheck commands cover their configured App/Node inputs, not semantic typechecking of the e2e spec. An unchanged type-only annotation at spec line 119 says `RuntimeDiagnosticResponse` while the local alias is `DiagnosticRuntimeResponse`; both intermediate and reviewed final bytes contain it. It is erased by transpilation and does not change this source-identity or runtime allowlist disposition. No test rewrite or type repair was authorized or made.

## Single existing suite row update and outside proof

Only `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/tests/suites.conf`, line 37, `app ap2-P1-chain-h6`, changed:

- Spec hash before: `926cdadd0370f0648e03b4bba743b56c1e7c80f0ff3fa1887ba985e9bc772fd1`
- Spec hash after: `956aaf219aae927d23a4f13e0ce8b0e358fe235508454fe70b0c6ad6ed84eb8c`
- Row SHA-256 before: `91535affae05797a2c45e8844d41e8961677fb8d03e8be3e57f786f0e75705bf`
- Row SHA-256 after: `1f7b28683080afd245e30735487037621e874639a00a087d36fac344b99ceb09`
- Whole suite file SHA-256 before: `589985b8fe8a338f06773eca0ee2c5dcafb83611efccb3a00fd7abe72225a2c8`
- Whole suite file SHA-256 after: `8e2dac65bce1aa345c156ff2cce370ccdb4bd60bfac88ea73fd91cd8ebc453d5`
- All other rows SHA-256 before = after: `81c9bd02376fccd395708954769b74511e6c2b94683e32968cbd727598a21310`
- Suite file stays 89,540 bytes / 164 lines. Only one 64-character hash field replaced (60 byte positions differ).

The inverse-replacement equality proves all commands, other source hashes, pins, graph checks, and both 6144 settings unchanged. No graph/dependency files were written. App tracked files remain identical to `cc05...`; the candidate relative to its `f7f45ad0b` parent still changes only the one spec (135 additions / 61 deletions). This worker made zero product, spec, original assertion, schema, generated, client, lock, pin, launcher, or new-suite changes. The original initial idle wait/catch rethrow and complete two-case assertions remain unchanged; no refusal/rollback/retry/history/inverse expectation was relaxed.

## Limits and next step

Nothing blocked. No HTTP/socket/browser/test-body/build/full/service run was performed or requested. Reused checks establish source safety and identity only. The manager may now run the **original existing** P1 service on this valid source disposition, retaining every existing guard. No App commit is needed: this change is shared suite metadata plus ignored report/handoff documents; HEAD/tree remain exactly those above.
