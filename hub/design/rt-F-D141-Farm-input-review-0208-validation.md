# D141 Farm input-producer review validation

## Exact checks

```text
cmp -s evidence/<nine producer files> /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-F-D141-Farm-input-producers-0201/evidence/<same file>
```

PASS for all nine recovered files. Their hashes and the reviewed commit are recorded in the absolute `source-manifest.json`.

```sh
/home/user/work/venv-runtime/bin/python -m json.tool evidence/input-map.json
/home/user/work/venv-runtime/bin/python -m json.tool evidence/source-manifest.json
/home/user/work/venv-runtime/bin/python -m json.tool /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-F-D141-Farm-input-review-0208/evidence/review.json
bash -n ops-d140-farm/receive-farm.sh
git diff --check
```

PASS. The review itself made no worktree source changes.

```sh
sha256sum /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/{make-child-venv,request-child-venv,check-child-imports,verify_dependency_seed.py,verify_farm_distribution_inputs.py}
```

PASS against the recorded full SHA-256 values, byte counts and modes. Frozen Agent/runtime lock, D73 launcher and Runtime C0 schema hashes also pass.

```sh
sha256sum /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/queue/done/checkout-composition-635f4de06fda22a85fc2e4cfc764d0153a4c9f40
```

PASS: 87 bytes and `ea43438c8e7327f152faf44d2d8e56133dd4b6aaf2205c4196d61b6c7b1e9ab1`.

```sh
git diff 1b709a79..2912e517 -- ops-d140-farm/receive-farm.sh ops-d140-farm/receipts.py ops-d140-farm/test_recipe.py ops-d140-farm/commands.md
```

PASS: no recipe bytes changed. The producer's existing targeted result `97 passed in 168.38s` is reused under the task rule; no duplicate suite was run.

## C0 and census checks

The frozen `timeline-commit.json` hash is `3654ca3c68f5b3d2022ee91f532aa388b198033d6ae54cda8d8b25cecf739815`. Its request, accepted, accepted-step, failure, preview, mutation-envelope and history required/properties were compared to `commands.md`; the documented field names and enum values match.

The actual Farm packet is `NOT_READY`, exit `1`, with 22 non-pass checks and output hash `8532e8de9f0cf38ae281aa0097e1ab2c0d705d9a6877babc40a0522db45dc7f2`. Its receipt result is the decisive correction: Agent/Runtime/App passed; Composition remained mismatched.

## Not run

No Farm run or live route was repeated. No full suite, child request, import/product code, control, service, core, install, Store, acquisition, network, cleanup, or Git write was performed.
