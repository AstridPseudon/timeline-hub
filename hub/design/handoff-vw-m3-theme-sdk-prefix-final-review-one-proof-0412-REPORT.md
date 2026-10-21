# SDK Theme prefix review: c955e7558116832462df5c426a3a4761cedb3f42

## Decision

Source review **APPROVED for the one authorized named case** against custody-approved base `37006ab9c9586739ffc0956d9a8fe1581f73be69`. The candidate is a minimal single-test delta in `tests/integrations/test_generic_host_remotion_render.py` (`95` additions, `20` deletions).

The central case was submitted exactly once and reached the candidate snapshot, but failed before the scoped proof:

`HostRegistrationError: worker credential is not bound to executor`

The failure occurred at `host.register()` (test line 556), before SDK invocation, admission, task materialization, resolver execution, or Root props. This is the terminal result; no retry, alternate Runtime, unsupported `production_worker_credentials` argument, render, MP4, browser, export, or parity claim is made.

## Source review

- The Theme case uses the real `astrid.sdk.invoke("rendering.render", kind="executor", ...)` producer with `wait=False` default.
- Timeline, empty assets registry, and explicit Theme are all imported through the owner client and passed as Runtime-managed `{object_id, digest, filename}` descriptors.
- There is no manual `admit_task`, manifest/order construction, hidden media ID, `timeline_ref`, or mixed timeline mode. The test observes the actual delegated `owner.tasks.create` request and compares the admitted Runtime task manifest/spec to it.
- The title film is media-free at the timeline/registry level; the unrelated black/silence MP4 fixture and its assertions remain unchanged.
- The proof endpoint is existing named materialization, the real Theme resolver, and Root props. The test explicitly disclaims final render, video, browser, and parity completion.
- The printed observer payload is limited to the SDK admission request, public admission response data, and `InvocationResult.to_dict()`. Source review found no transport client, headers, tokens, credentials, or private auth capsule in that payload. The terminal run failed before this print, so no observer payload was emitted.
- Assertion preservation: Theme case `12` base assertions are a subset of `19` current assertions. The dependency-copy test (`4` assertions) and unrelated MP4 test (`9` assertions) are AST-identical to the approved base.

## Immutable custody and environment

Reused approved custody evidence; no dependency copy/readiness proof was repeated. The immutable Remotion source graph is `/home/user/work/runtimes/agent-remotion-viewing13-d0a5072b/node_modules`, `21,455` entries, tree SHA-256 `4913a37e5403c8372a283dcca8fd30c846b636abd88f59cfc572809d2fd0bd3c`. C13 artifact SHA-256 is `9412ae25c306d5118241f4d631e8eecc6eef9b2fb5a98302d40938e9f6d54738`. Prior before/after custody records show the private fixture had matching bytes but independent inodes (`nlink=1`) and was retired; the immutable source hash stayed `4913a37e…bd3c`, with only the expected internal source hardlink group remaining.

The named command preserved the required roots: Runtime checkout `/home/user/work/wt/rt-pin-8f105c26` (Runtime `8f105c26e3b62f9c2683f717a9773a12bc775a8e`) with `/home/user/work/venv-runtime/bin/python`; Remotion graph `4913a37e…bd3c` / C13; Node `v20.19.4` at `/home/user/work/toolchain/node-v20.19.4-linux-x64/bin/node` (SHA-256 `43d6cf63f2a460b463eba6b19df5e9a259771c56f11b5130e04178a15bb99490`).

## Central result

Test ID: `vw-m3-theme-sdk-prefix-final-review-one-proof-0412-integration-viewing-theme-normal-props-0234-1021041356-8119`

Service candidate snapshot: `tree=ed639e33d68c41d4b91eb561b39c754bffaed228`, exact test selected:

`tests/integrations/test_generic_host_remotion_render.py::test_generic_host_normal_imported_theme_reaches_props_and_rejects_local_source`

Result: **FAIL, exit 1, 87s**. Failure phase: executor registration. Runtime 8f returned HTTP 401 `unauthorized: worker credential is not bound to executor` while registering `astrid-theme-proof-host`. No test assertion after registration ran.

## Exact checks

- `/home/user/work/venv-agent/bin/ruff check --no-cache tests/integrations/test_generic_host_remotion_render.py tests/packs/rendering/test_explicit_theme_normal_route.py` — PASS.
- `git diff --check 37006ab9c..HEAD` — PASS.
- Python `compile()` syntax check for `tests/integrations/test_generic_host_remotion_render.py` — PASS.
- `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD" /home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider tests/packs/rendering/test_explicit_theme_normal_route.py` — **2 passed**.
- Exact one-case collection with the supported Runtime/Remotion/Node environment — **1 collected**.
- Central named command `integration-viewing-theme-normal-props-0234` — **1 failed before admission**, as recorded above.

## Blocker and next step

The required one-case witness is unverified because the Runtime 8f fixture did not bind the worker credential to `astrid-theme-proof-host`. The next step is an orchestrator/Runtime-fixture decision to provide the supported binding in the existing named service setup. Do not rerun this case under a different Runtime, add unsupported `production_worker_credentials`, or claim the SDK/Root proof from this failure.
