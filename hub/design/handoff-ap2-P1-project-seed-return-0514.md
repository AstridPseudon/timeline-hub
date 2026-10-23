# P1 project seed return handoff

## Verdict

PASS for the bounded test-support fixture repair; end-to-end behavior remains unverified here by instruction.

## Exact change

At `tests/e2e/local/three-products.p1-chain.spec.ts:90`, `seedOneClip` changed:

```ts
- project.body.data.slug
+ (project.body.data ?? project.body).slug
```

The POST publication status check immediately above it and every subsequent P1 assertion remain unchanged. The production caller is untouched; the helper now returns the authoritative Runtime-created project slug to `openChain`.

The full C0v2 surface is preserved: scope/base pair, commands, label, steps/patches/reads, merge/reads/dry-run/key, complete accepted/merged canonical head/digest/receipt/steps/dependencies, history, conflict, and invalid checks.

## API evidence

The frozen Runtime 34 `runtime_protocol/server.py` project route sends `GET /v1/projects/{selector}` as `self._send(200, self.runtime._project_resource(...))`. Its `_project_resource` contains the top-level `slug`. The same route wraps only project creation as `{"data": resource, ...}`. The current DirectHarness support code already uses `(project.body.data ?? project.body).slug` in `seedExtensions`, `seedThreeProducts`, and related seed paths.

Thus the original failure (`project.body.data` undefined at `seedOneClip` line 90) was a response-envelope mismatch, not a missing project or a behavioral refusal. No hardcoded slug, latest-project lookup, or fixture substitution was introduced.

## Evidence run

- Base resolved exactly: `38fbbc993e19e39615a99b7a5d524a0da11f91c3`.
- `npm run test:e2e:three-products -- --list tests/e2e/local/three-products.p1-chain.spec.ts` — PASS, exactly 2 tests listed.
- `npm exec tsc -- --noEmit` — PASS.
- `npx eslint tests/e2e/local/three-products.p1-chain.spec.ts --max-warnings 0` — PASS.
- `git diff --check` — PASS.
- No HTTP/browser/body/build/full/service run, as required; manager owns the original two-case retry.

## Source and suite guard delta

- P1 spec hash: `dfcdee357a822bb8516fdcadae88a074a78c7bdaca3d053991d28721ebfae7d2` → `926cdadd0370f0648e03b4bba743b56c1e7c80f0ff3fa1887ba985e9bc772fd1`.
- `ORCH/tests/suites.conf`: only the existing `ap2-P1-chain-h6` P1 spec hash changed to the new value. Other rows, source hashes, ancestry, dependency pin, and 6144 heap setting are unchanged.

## Files

- Worker report: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-P1-project-seed-return-0514/report.md`
- Commit message: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-P1-project-seed-return-0514/commit-msg`
