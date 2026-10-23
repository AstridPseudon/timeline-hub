# R2r history current-only port report

## Result

Ported cumulative sequential verifier/private-port/history-store changes from cfa0af0d4..1948d06a onto actual integration 2593942dfbbbe1d70bb6e776f811285deb2ab18b (tree 3bd06dc517f347976541ae4dde3caf3d29d03419).

Current atomic-birth and native-order changes remain intact. Sequential auth changes were inserted as hunks; timeline_commit_auth.py was not copied wholesale. Exact author-candidate bytes match for:

- runtime_protocol/timeline_commit.py
- runtime_protocol/timeline_commit_port.py
- runtime_protocol/timeline_commit_store.py
- tests/test_timeline_commit_sequential_verifier.py
- tests/fixtures/timeline_sequential_capture.json

The auth diff against candidate 1948d06a is limited to the current integration's retained atomic/native-order hunks.

## Tests and static checks

Exact required nine-file command:

    PYTHONDONTWRITEBYTECODE=1 ASTRID_CHECKOUT=/home/user/work/agent PYTHONPATH=.:packages/python:/home/user/work/agent /home/user/work/venv-runtime/bin/python -m pytest -q -o addopts= -p no:cacheprovider tests/test_timeline_commit_authentication.py tests/test_timeline_commit_read_basis.py tests/test_timeline_commit_inputs.py tests/test_timeline_commit_port.py tests/test_timeline_inverse_stage_authentication.py tests/test_timeline_source_duplicate_authority.py tests/test_timeline_source_document_boundary.py tests/test_timeline_raw_capture.py tests/test_timeline_commit_sequential_verifier.py

Result: exit 0, 395 passed in 96.08s.

Focused sequential command:

    PYTHONDONTWRITEBYTECODE=1 ASTRID_CHECKOUT=/home/user/work/agent PYTHONPATH=.:packages/python:/home/user/work/agent /home/user/work/venv-runtime/bin/python -m pytest -q -o addopts= -p no:cacheprovider tests/test_timeline_commit_sequential_verifier.py

Result: exit 0, 57 passed in 10.81s.

Static commands:

- /root/.local/bin/ruff check runtime_protocol/timeline_commit.py runtime_protocol/timeline_commit_auth.py runtime_protocol/timeline_commit_port.py runtime_protocol/timeline_commit_store.py tests/test_timeline_commit_sequential_verifier.py --output-format json: exit 1 with 22 existing diagnostics.
- /root/.local/bin/pyright runtime_protocol/timeline_commit.py runtime_protocol/timeline_commit_auth.py runtime_protocol/timeline_commit_port.py runtime_protocol/timeline_commit_store.py --outputjson: exit 1 with 80 existing diagnostics.
- git diff --check: exit 0.

Compared with an exact HEAD archive baseline, normalized diagnostic identities show Ruff 0 added / 1 removed (23 baseline, 22 current) and Pyright 0 added / 0 removed (80/80). No new product behavior or public wire changes were introduced.

## Preservation and source proof

- contract/artifacts.json: 78 entries; 78/78 declared hashes match current bytes and 78/78 match HEAD bytes.
- contract/schemas/edit-command.json: unchanged, SHA-256 d106dfe8212500709b4072d7bc0486f83c27d5d8de33d215cb52b9ea7d46357d.
- Original Agent test /home/user/work/wt/agt-pin-67ba416b/tests/editing_conformance/test_doc_patch_sequential_rebase.py: byte SHA-256 75ccd026898b241d2241f5c058342aeb728e3a70f039a8701343b55f6fc648f6; AST SHA-256 be9a7dce79a3fbe8be453a0dcb8f4c0a8d33eb35cbe8fd6e34d0194bfe5206ea.
- Current owned candidate hashes: port 0d44b5a5e1e0374239df461cb5094ff4fe5bb70761233efd4e3a65c2b29b0859; store b1cfdceefc533220ea9a5478f61a971109d1cc2d70fa2c7a76341ffa977f2246; sequential test 35451bda9486c042fa907454b41e7b90439fa1964ec9a68ad3936acc25a22800; fixture 51e353be23b2ebf80e454f2b5cd165a904ab0478c41a6065ed310535d55976cd.
- Worktree changed paths are only the four allowed runtime modules plus the new sequential test and required fixture.
- 1948d06a is not an ancestor of the current base; no merge/integration was performed. The harness should create one conventional R2r commit over the current integration head.

## Decisions and limits

The sequential test fixture was restored because it is a cumulative source blob present on 85b2/1948d06a and required by the exact new test; the integration base had omitted it. This was a mechanical test-input restoration, not a semantic change.

No original Agent nine was rerun, per the brief; independent review 1604 owns it. No full/browser/daemon/journey suite was run. No guard/public wire/schema/client/lock/pin changes were made. No semantic conflict was encountered.

