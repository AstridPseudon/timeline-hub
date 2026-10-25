# D73 launcher environment correction validation

## Result

`PASS_SOURCE_ONLY`: the launcher now clears the inherited `PYTHONNOUSERSITE`
startup override in both the preflight and body child shells. The launcher’s
Remotion project and private source-origin bindings remain exported exactly as
before. No product guard, host bootstrap, subprocess policy, dispatcher,
captured source tuple, or public protocol was changed.

## Exact source

- Base Agent: `a30e74e901a28b39c28facba3deb00d76f186e23`, tree
  `ece8e0887e48e45cb1fce85b1256c49a0f6126c0`.
- Frozen source Agent: `a4e016b6a9f91fbe372672bdcf382c630bf59186`, tree
  `60d45288145414ee4702fcce61af7c7810c2a3df`.
- Base/frozen launcher SHA-256:
  `cec561761cb90adbe94dbcc1b1f6b62afb107f1a90e079c6ce2b823405a072d1`.
- Candidate launcher SHA-256:
  `9f668e398b1ea4cce48a6c610102723e0a3dab27a764be4191015aa7fc4110cd`.

## Focused controls

The own launcher control uses the real launcher script with a synthetic,
fully guarded manifest fixture (no checkout, install, service, or network
write). It injects `PYTHONNOUSERSITE=1` in the outer environment and verifies:

1. the body command is reached exactly once;
2. its exit code `17` is returned unchanged;
3. `PYTHONNOUSERSITE` is absent in the body;
4. private Runtime, source-root, Remotion profile, and Agent working-directory
   bindings are exact; and
5. a poisoned Agent SHA fails before the body, with zero body invocations and
   no body evidence files.

The frozen D73 body itself was not run. No provider, browser, socket, Remotion
build, live install, source adoption, full suite, or captured tuple retarget
was performed.

## Commands and results

```text
bash -n tools/p4-d73-pinned-launch.sh                         PASS
PYTHONPATH=...:/home/user/work/runtime /home/user/work/venv-agent/bin/python -m pytest -q tests/sdk/test_p4_d73_pinned_launcher.py
                                                               2 passed
/home/user/work/venv-agent/bin/ruff check tests/sdk/test_p4_d73_pinned_launcher.py
                                                               PASS
git diff --check                                             PASS
```

## Decision and remaining review

`unset PYTHONNOUSERSITE` is the smallest launcher-only correction that also
handles an inherited poisoned outer environment. Deleting only the outer
caller assignment would leave the frozen launcher’s two reintroductions in
place; changing the Remotion probe or host isolation would exceed ownership.

One independent Agent-owner review remains before adoption: verify this exact
launcher diff against the frozen four-repository tuple and run the authorized
real-launcher positive-17/poisoned-manifest controls after adoption. This is
source evidence, not a claim of production launch admission.
