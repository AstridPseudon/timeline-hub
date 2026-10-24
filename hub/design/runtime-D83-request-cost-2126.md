Measured verification multiplicity. **No product change retained:** the candidate failed to demonstrate an accepted-history cost reduction. Reviewed metadata parent `1fa23066f` remains intact; worktree is clean.

| Request | Prior accepted entries | Commands | `_verify_accepted` | `_historical_sequential` | Capture-document checks | Schema checks |
|---|---:|---:|---:|---:|---:|---:|
| 1 | 0 | 1 | 1 | 0 | 0 | 2 |
| 2 | 1 | 2 | 11 | 1 | 16 | 24 |
| 3 | 2 | 3 | 21 | 16 | 144 | 212 |

The genuine daemon control passed in **4.24s**. Request 3 reverified its two-command ancestor 15 times. Capture checks by command ordinal were **68, 68, 8**, across original and landing sides. History retrieval repeats accepted-edge verification; each retained sequential proof then traverses its recorded ordinals. This does not establish a causal leaf or lock cause. Entry count and command count covaried, so this control does not isolate their scaling independently.

Authentic14690 handler 54 recorded **48 accepted verifications, 31 historical sequential verifications and 1,220 capture-document checks**. Its profiles predate merged corrections. Current1960 and the 22971 pending window do not establish current causal attribution or budget compliance.

The immutable setup-dispatch probe passed independent security review. Its initial helper comparison improved CPU 6.70%, but accepted-history replay measured **0.433276s → 0.434615s**, with all **44 predicate/count frames equal**. I rejected and reverted it. Final changed product blobs: **none**.

Validation:

- Restored-parent focused suite: **378 passed, 1 failed**, exit 1. Failure is the existing legacy `recorder_abi=1` metadata assertion.
- Central daemon control: **1 passed**, exit 0.
- Central ABA controls: **3 passed**, exact-tree cache hit.
- Exploratory candidate suite: **384 passed, 2 failed**—the legacy failure plus an added probe that incorrectly assumed native `evolve(schema=None)` succeeds.
- Ruff: zero findings; Pyright: zero new diagnostics. Compile and `git diff --check` passed.

[Exact commands](evidence/commands.json), [measurements and source explanation](evidence/measurement-notes.md), and [origins/hashes](evidence/origins.json) are retained under the assigned evidence directory.

No additional gain or original-budget proof is established. The orchestrator must choose the next bounded immutable-preparation investigation or reconsider the relevant design constraint; this result does not justify memoization or fresh-check removal. No original/full/browser runs were performed.

Commit message and `DONE` written.