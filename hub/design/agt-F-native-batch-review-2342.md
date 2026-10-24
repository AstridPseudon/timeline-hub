# FAIL

Protected source review of `78930b3927` failed.

Finding:

- [`test_native_batch_ingress.py:141`](/home/user/work/wt/agt-F-native-batch-review-2342/tests/editing_conformance/test_native_batch_ingress.py:141) replaces the real CLI invocation with direct `TimelineSession.commit_many(..., via="cli")`.
- Current CLI behavior is [`commit` → `commit_document`](/home/user/work/wt/agt-F-native-batch-review-2342/astrid/packs/timeline/cli_native.py:138), not this helper. Thus the file-based CLI cases no longer exercise CLI source behavior, violating the settled G5 rule that CLI cases remain CLI.

AST conservation passed: all 24 assigned selectors preserved; only the helper and retired-parser expectation changed. Source hashes:

- Base: `1c6cbd9b10d452b1a4893600a4dbaa68517adc8868c140a4441a819cd9e18669`
- Candidate: `bdd5b0c07def96717a4244ad887b4f0254fec824866acbfe8821f68d28fcdada`

Checks passed:

- In-memory compile: baseline and candidate
- Ruff baseline/candidate: clean
- Mypy baseline/candidate: no issues
- `git diff --check`: clean

No pytest, service, build, render, or functional PASS was claimed. No merge requested. DONE marker created.