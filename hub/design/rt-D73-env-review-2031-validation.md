# D73 independent launcher environment review

## Verdict

`PASS_SOURCE_ONLY`: the candidate clears the inherited `PYTHONNOUSERSITE`
startup override in both launcher child shells. The production launcher path,
manifest guards, private source-origin bindings, and body custody behavior are
covered by focused controls. No frozen tuple body or production request was
run.

## Source trace

`astrid/core/rendering/remotion_runtime.py:214-236` includes
`PYTHONNOUSERSITE` in the rejected Python startup-variable set and refuses the
environment with `runtime validation refuses unsupported loader/interpreter
overrides`. A direct probe control reproduced that rejection and accepted the
supported environment with policy `clean-schema-env/v1`.

The launcher diff from its parent is exactly:

```text
-    export PYTHONNOUSERSITE=1
+    unset PYTHONNOUSERSITE
```

at lines 128 and 149. Existing manifest format, required keys, SHA/tree/clean
checkout checks, Agent parent guard, original P4 hash, lock/schema/profile
checks, custody evidence, and private exports remain unchanged.

## Focused controls

The two focused tests invoke the actual worktree launcher at
`tools/p4-d73-pinned-launch.sh`; they do not copy it into a synthetic Agent
checkout. Their manifest and helper repositories are temporary fixture inputs,
with the source launcher’s guards still active.

The positive control sets outer `PYTHONNOUSERSITE=1`, reaches the body exactly
once, returns exit `17` unchanged, observes `PYTHONNOUSERSITE=None` in both
preflight interpreter invocations and in the body shell, and asserts exact
Runtime checkout/source-root, Remotion profile, Node, node_modules, PYTHONPATH,
and Agent cwd bindings. An unrelated `D73_UNKNOWN` variable is preserved,
documenting the launcher’s narrow policy rather than introducing a broad
environment clear.

The poisoned-manifest control replaces the Agent SHA with forty zeroes and
observes nonzero launcher exit, zero body invocation, and no body evidence
files.

## Commands and results

```text
PYTHONPATH=$PWD:/home/user/work/runtime /home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider tests/sdk/test_p4_d73_pinned_launcher.py
2 passed

bash -n tools/p4-d73-pinned-launch.sh
PASS

/home/user/work/venv-agent/bin/ruff check tests/sdk/test_p4_d73_pinned_launcher.py
All checks passed!

PYTHONPATH=$PWD:/home/user/work/runtime /home/user/work/venv-agent/bin/python -c 'compile(...)'
private compile: PASS

git diff --check
PASS
```

Direct probe control: poisoned `PYTHONNOUSERSITE=1` was rejected; the
supported environment was accepted as `clean-schema-env/v1`.

## Boundaries

This is source/control evidence only. It did not run the frozen D73 body,
provider, browser, sockets, Remotion build, acquisition/install, full suite,
or a production request. It did not alter the dispatcher, installed
entrypoint, captured tuple, credentials, or public protocol. The temporary
fake Git/Python/Node helpers exercise the real launcher’s shell and guard
control flow; they are not evidence of frozen-tuple admission or live
Remotion execution.
