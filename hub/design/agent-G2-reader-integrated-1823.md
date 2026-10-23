# PASS — integrated G2 exact current-pair reader proof

## Result

Integrated Agent head `78738040d72ce74c42ddf7731221aecb06f9246d` is the normal merge of reviewed `75fde1b96259ab3bc29923229e3b01e668a61bc6` onto the independent A4/R1 parent. The assigned source/test pair is byte-identical to reviewed `75fde1b96`:

- `astrid/sdk/timeline/store.py`: SHA-256 `2ab1380ba947c121fa0973ff316ada8726222898c22224f53a52da3563586f7c`
- `tests/editing_conformance/test_current_pair_reader.py`: SHA-256 `37a57c0de8bb9e2a5911fa0f833dae4dccd4adb479f886848548695cdc3382d0`

The production seam exercised by the authentic reset case is `Checkout._reset_base()` in `astrid/sdk/timeline/publish.py`, which calls `store.fetch_bundle()`. The reader first opens the public bundle, obtains Runtime’s scoped history head pair, checks the revision matches, then reopens with the exact revision/publication pair. No alternate authority or writer path was exercised.

## Tests and checks

Using `/home/user/work/venv-agent/bin/python`, pinned Runtime source `2a9e347ff0e1df1dedff5ab7b59ddb27dfe3129d`, and authentic archive SHA-256 `2915bd4ac0d46954d19c30f87a517b82074218699978e650fab03fcba81b72d3`:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.:/home/user/work/runtime:<runtime-2a9e-source> ASTRID_RUNTIME_CHECKOUT=<runtime-2a9e-source> ASTRID_AUTHENTIC_LEGACY_ARCHIVE=<reviewed2915archive> TMPDIR=<private-run> /home/user/work/venv-agent/bin/python -m pytest -q --tb=short -o addopts= -p no:cacheprovider -m integration tests/editing_conformance/test_current_pair_reader.py --basetemp=<private-run>/pytest
16 passed in 3.54s
```

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.:/home/user/work/runtime /home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider tests/sdk/test_remote_timeline_owner_scope.py
6 passed in 0.45s
```

The first attempt used the harness `tmpdir` path, which is a file; it stopped before pytest setup. The rerun used the assigned worker’s private sibling directory and entered all 16 cases.

Pinned Runtime same-process source stability: 476 files before/after importing service, commit-store, auth, and backup modules; zero changed, missing, or added files. Vendor lock: `ok runtime.lock.json`. Artifact manifest: `artifacts.json is current`. `git diff --check`: pass.

## Preservation and limits

- Merge delta from the A4/R1 parent is exactly the two assigned paths above.
- R1/A4/registry protected files and `runtime.lock.json` have identical Git blobs before/after the merge.
- `runtime.lock.json` still pins Runtime `34eac0041b0891e9011966b39bcbd26053fde5bc`; the recorded Agent schema digest remains `d106dfe8212500709b4072d7bc0486f83c27d5d8`; the external `819acf6b3815d6eeabe772a9569581fedbe4f9c9` artifact was not in this Agent change scope.
- The authentic archive has zero credential-shaped findings. Worker evidence, SHA manifest, and scan are under `workers/agt-G2-reader-integrated-1823/evidence/`; manifest SHA-256 is `a86ed65aa99799139325f15a993fe94962a622a738df9d089eec8c770f3b4d24`.
- No product/test/schema/client/pin/Runtime/environment/Git/daemon changes were made.
- G5’s retained original dynamic failure remains unqualified; its body was not run, changed, skipped, or xfailed. No full, browser, live-socket, or prohibited suite was run.

Recommended next step: orchestrator-controlled merge disposition, followed by a separate faithful G5 oracle/support qualification. This proof qualifies only the exact current-pair reader seam and the six existing owner-scope guards.
