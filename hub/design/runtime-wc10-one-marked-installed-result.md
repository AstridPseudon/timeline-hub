# Runtime WC10 one marked installed-launch result

Date: 2026-10-21. This is analysis only; no Runtime source change was made.

## Result

The exact newest named run was awaited once and failed during setup:

```text
request: rt-m2-wc10-installed-complete-one-proof-0303
suite: wc10-installed-launcher-integration
request time: 2026-10-21T03:13:41Z
result: exit=1; 1 failed in 1.60s
command: env PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-runtime/bin/python -m pytest -q -p no:cacheprovider -m integration tests/test_wc10_installed_launcher.py::test_wc10_installed_normal_launcher_provider_bootstrap
result directory: /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/tests/rt-m2-wc10-installed-complete-one-proof-0303-wc10-installed-launcher-integration-1021031341-3134
```

The source checks passed through the Agent and normal Runtime checkout
identity/cleanliness assertions and the reviewed launcher-source assertion.
The first failing operation was `_approved_distributions()` in
`_make_installed_environment()`: the central `/home/user/work/venv-runtime`
inventory lacked the declared closure (`aiofiles`, `annotated-types`,
`anthropic`, `anyio`, `asyncstdlib`, `certifi`, `cffi`, `charset-normalizer`,
`click`, `cryptography`, `distro`, `docstring-parser`, `fal-client`, `filelock`,
`google-auth`, `google-genai`, `h11`, `httpcore`, `httpcore2`, `httpx`,
`httpx-sse`, `httpx2`, `idna`, `jiter`, `msgpack`, `numpy`, `openai`,
`opencv-python-headless`, `pillow`, `platformdirs`, `pyasn1`, `pyasn1-modules`,
`pycparser`, `pydantic`, `pydantic-core`, `pyjwt`, `python-dotenv`, `requests`,
`scenedetect`, `sniffio`, `tenacity`, `tqdm`, `truststore`, `typing-extensions`,
`typing-inspection`, `urllib3`, `websockets`, and `xxhash`).

This is not a normal CLI/bootstrap/provider failure: no installed venv was
created, no product wheel was built or installed, and no Runtime child was
started. Consequently there is no installed-origin path, byte hash, package
provenance, or canonical-read result to report. The original positive
assertions for healthy startup, authenticated door, `bootstrap` head, and no
`publish_parent_composition` were not executed. No installed-authority claim
was fabricated.

## Exact tuple and scope

- Corrected fixture: `efd8e21347c90cd03bf666bf1c8752fa7b14e595`, tree
  `7ecac255c50d2935ddf9a37d3fc9ba0bda434b60`.
- Launcher product source under review: Runtime
  `8f70a8184aca5bb61b2fcb133c5cedc3c6e0800a`.
- Normal Runtime/client source: `95bd3c5f6d00e9bc8cc8cbe5ef510b68ed660f3c`;
  client contract `0.2.14`, schema digest
  `sha256:7d4afa05962b8cd61643213fc79cdde41e16046c4e2a777bd299b48af0f31816`.
- Agent: `6efc81500a0e0688c2bb41e736503f0fc3e04abb`, tree
  `2ed2b8a12b5b3391ca221ba6ff05390f71a73556`.
- Expected installed product distributions: `astrid==0.1.0`,
  `astrid-runtime==0.1.0`, `astrid-runtime-client==0.2.14`.

The fixture contains the intended safeguards for exact matched versions,
private module origins, no shared symlink components, isolated `-I` execution,
and child execution with `PYTHONPATH` removed. None were observed in this run
because the closure inventory failed first. No D13 render, browser, model,
consumer migration, pin, or integration-adoption claim follows.

## Custody and cleanup

The setup failure occurred before private environment, wheelhouse, support
realm, socket, or installed package creation. No shared dependency or source
checkout was modified. The central result directory retains only the test
service metadata/log; there are no worker-created build outputs in this
worktree. Remaining custody is the pre-existing shared dependency inventory;
this run did not establish custody of any installed product bytes.

## Evidence

The earlier unmarked request (`03:11:36Z`, exit 5, one deselected) remains a
historical wrong-marker result. It is not overwritten or treated as this
marked run. No additional run, retry, normalization, source edit, full suite,
browser, render, or model test was performed.
