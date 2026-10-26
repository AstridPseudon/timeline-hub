# U2/U4a D141 cumulative independent review — FAIL

## Exact source qualification — PASS

Candidate `b4eb5db76fda523407b90a9dbe820f4e20cc1f1d`, tree
`2ebe2ddf5a61f013953ab1e21d51ebaab746e58a`, is clean and has the approved
cumulative scope: only `artifacts.json` and `runtime.lock.json` differ from
`aa5a91a618f4d28308772169bc08e8e79274cd6a`. Frozen upstream
`8b6ed2116fd1803d24b2be5bc08bd9490407fe4a` and current ancestor
`c585cb2aa73c5298d474e614cb2144f58f27e605` are both verified ancestors.

After confirming every other tree blob is identical to `aa5a91`, the prior
2357 full-source-conservation PASS remains applicable: 19 upstream-only paths
and 922 current/later paths have zero mismatches, both live test families are
preserved, and there are no semantic conflicts. D100a blobs remain exactly
`09cbeeddefdc6375ba7d026406c95fb35bafda40` and
`39ed571d5f3e49d2545fc31e1f868ee7c58dbc8a`.

The normal tools pass read-only checks. `artifacts.json` contains only the
normal `am-footage` digest update. `runtime.lock.json` is bound by normal
vendor tooling to clean Runtime `6a011d58e69173d70e2e9bb3ac434ac8f9e87d8d`
(tree `ac5b862744bece65b2e30565db1777bacd60da28`); all 15 mappings, hashes,
modes, consumer bytes, and producer bytes match `c585cb2` and the actual
producer.

## Test qualification — FAIL

The corrected dependency-backed Bun run passed:

- `bun run check:chat-bundle` — exit 0.
- `bun test ./astrid/chat` — exit 0, 200 passed, 0 failed.

The required Python targeted command completed once with exit 1: 476 passed,
61 failed, 73 errors, 1 skipped. The raw stdout/stderr and JUnit XML are
preserved at `/tmp/agt-U2-D141-cumulative-review-0008/python-targeted.log` and
`/tmp/agt-U2-D141-cumulative-review-0008/targeted.xml`. Representative errors
include the selected integration tests' missing `runtime_protocol`/live
dependency setup. These are recorded as observed; no tests were skipped,
weakened, xfailed, or changed.

The unchanged render-node PASS and parent-proved Ruff 574/Mypy 168 inherited
inventories are reused only after exact source comparison. No full suite,
Farm core, REG0, or ship claim is made.
