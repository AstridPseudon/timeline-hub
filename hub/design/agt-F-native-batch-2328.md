## PASS_SOURCE

Changed only [test_native_batch_ingress.py](/home/user/work/wt/agt-F-native-batch-2328/tests/editing_conformance/test_native_batch_ingress.py).

- Migrated the file adapter to `TimelineSession.commit_many(..., via="cli")` using genuine Runtime `commitTimeline`.
- Updated parser expectations for the settled G5 retirement of `edit commands-file`.
- Preserved all 24 assigned selectors, parameters, decorators, assertions, and raises. All test bodies are AST-identical except the approved parser-interface expectation.
- Baseline SHA256: `1c6cbd9b10d452b1a4893600a4dbaa68517adc8868c140a4441a819cd9e18669`
- Candidate SHA256: `bdd5b0c07def96717a4244ad887b4f0254fec824866acbfe8821f68d28fcdada`
- Baseline blob: `e570713ac808b9755f602c41465d18e2ef48bd96`

Checks passed:

- Baseline and candidate Ruff
- Baseline and candidate mypy
- `python3 -m py_compile`
- `git diff --check`

No pytest, service, build, render, or functional test run, per instruction. Protected review and the single batched rerun remain manager-owned.

Commit message written and `DONE` marker created.