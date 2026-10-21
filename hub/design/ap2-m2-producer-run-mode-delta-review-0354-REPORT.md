# AP2 M2 producer run-mode delta0354 review

## Verdict

APPROVE the narrow explicit run/list delta after frozen source0346.

Exact candidate:

- source commit: `00bbc22d63b4abe7275cfe9ad5f3762157d7394f`
- source tree: `f41a45c01293b0248a27c490bb9e8aa02be33ecd`
- parent/frozen source: `70dec48e88ea036bf160539b58b68bb64c38f3b3`
- new wrapper SHA-256: `11080069b40aab7e9fd9798974cc43d9b244de5f17d930ebc74dc0f935136fc2`
- protected public13 runner SHA-256, unchanged: `40c25724b502ce5582caf04c6ebf44ab89a509b5f3d629876d599f57c3e5fa7a`

The source diff versus 0346 is exactly one file: `scripts/testing/run-producer-public13-list.sh`. The shared test-service allow-list has the intended distinct entries:

```text
app ap2-m2-producer-existing-graph-command-e2e-integration sh scripts/testing/run-producer-public13-list.sh "$PWD" list
app ap2-m2-producer-existing-graph-command-actual-e2e-integration sh scripts/testing/run-producer-public13-list.sh "$PWD" run
```

## Review findings

- The run child uses the exact same Playwright config and spec as list, with only `--list` removed.
- List mode remains a collection preflight only: it requires exit 0, rejects zero-test markers, and requires `Total: 1 test in 1 file`; list1 is not treated as an actual-body pass.
- Run mode requires exactly one `1 passed` or `1 failed` result, rejects zero/missing output and multiple outcomes, rejects pass/nonzero and fail/zero mismatches, and returns the child status for a real nonzero failure.
- Existing body, helper, config, Agent `8130a401…`, Runtime `2c4ac180…`, public13 source `9412ae25…`, 75-artifact manifest, 77-member Composition tarball, graph guards, traps, and short paths are unchanged.
- Live callers changed: only the two shared test-service allow-list entries above. No App product caller changed; the wrapper self-reference is the only repository caller.

## Evidence

Commands run by the source worker and reviewed here:

- `sh -n scripts/testing/run-producer-public13-list.sh` — PASS.
- `git diff --check` — PASS.
- `node_modules/.bin/playwright test --config playwright.producer-ownership-current-pin.config.ts tests/e2e/local/producer-ownership-current-pin.spec.ts --list` — PASS; exactly 1 test in 1 file.
- Planted mode/argv/zero/RC probes — PASS: list includes `--list`; run omits it; pass returns 0; failed child returns 1; zero output, status mismatches, multiple outcomes, and invalid modes fail closed.
- Missing parent mode and invalid parent mode probes — PASS; both return 2.
- Independent read-only `git diff --check 70dec48e88ea036bf160539b58b68bb64c38f3b3 00bbc22d63b4abe7275cfe9ad5f3762157d7394f` — PASS; one changed source path.

No hosted build repeat, browser, actual journey, or full suite was run, as required. The actual producer body remains unverified; the next authorized command is the distinct `ap2-m2-producer-existing-graph-command-actual-e2e-integration` suite above.
