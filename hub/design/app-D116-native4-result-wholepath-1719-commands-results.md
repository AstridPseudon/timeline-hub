# D116 review commands and results

All commands below were read-only or used private temporary caches. No behavior test or collection was run.

## Custody and no-change checks

```text
git rev-parse HEAD
PASS 795608e1b9d8077487b26eea50b65c1e79c3f522

git status --porcelain=v1
PASS empty

git diff --check
PASS

git -C /home/user/work/wt/rt-pin-5e9ad1c6 rev-parse HEAD
PASS 5e9ad1c6f74241d8771d3284fdd2ce7a214fd344

git -C /home/user/work/wt/rt-pin-5e9ad1c6 rev-parse 'HEAD^{tree}'
PASS de2954a0ceadb4455903d9abdfec3b773318a50f

git -C /home/user/work/wt/rt-pin-5e9ad1c6 status --porcelain=v1
PASS empty

git diff --stat 9350a674a85b9328e7ac1e8192e66dcc65cfbf77 HEAD
PASS exactly the two authorized companion files

git diff --stat b24d99bd3c286336c09d4d0661e9691d3b160559 HEAD
PASS two files, 13 insertions(+), 3 deletions(-)
```

## Static source checks

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPYCACHEPREFIX=/tmp/d116-native4-result-wholepath-1719-py311 /usr/bin/python3.11 -m py_compile tests/editing_conformance/native_checkout_current_fixture.py tests/editing_conformance/test_native_checkout_current_equivalent.py astrid/sdk/timeline/commit.py astrid/sdk/timeline/native_word_anchor.py astrid/sdk/timeline/emitter.py
PASS exit 0

/home/user/work/venv-agent/bin/ruff check --cache-dir /tmp/d116-native4-result-wholepath-1719-ruff tests/editing_conformance/native_checkout_current_fixture.py tests/editing_conformance/test_native_checkout_current_equivalent.py astrid/sdk/timeline/commit.py astrid/sdk/timeline/native_word_anchor.py astrid/sdk/timeline/emitter.py
PASS All checks passed!

AST parse of test_native_checkout_current_equivalent.py
PASS three top-level test functions, one two-case parametrization, four expected node IDs

PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=$PWD:/home/user/work/wt/rt-pin-5e9ad1c6 /home/user/work/venv-agent/bin/python import-only module-origin probe
PASS Agent modules resolve to this worktree; Runtime modules resolve to the pinned Runtime checkout; provider factory is astrid.sdk.timeline.commit.create_runtime_commit_service
```

The equivalent import-only probe with `/usr/bin/python3.11` failed because that interpreter lacks `jsonschema`; it was not a test run and was repeated successfully with the shared Agent venv above.

## Retained functional evidence reviewed, not rerun

```text
Admission: 5005950976 bytes available, floor 5000000000
Exact four-node launch: 3 failed, 1 error in 28.85s; 0 passed
Retries: 0
Raw XML SHA-256: 373b641a79231cc6ee0ee89088545857914e9493b7bc257aaf138ae9ccbc281d
Raw log SHA-256: 586bd0a66488db7e0701148b249ba2f3a13317cd208521d86b63ea03710d3f09
```
