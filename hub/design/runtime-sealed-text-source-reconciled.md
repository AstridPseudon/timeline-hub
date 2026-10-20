# Runtime sealed native text source reconciliation

## Result

The reported eleven sealed native text failures were an import/source-selection
problem, not a schema defect in the approved Runtime candidate. The exact
immutable pair passes unchanged: the marked native cohort returned **11 passed,
0 failed**.

No Runtime source, schema, authority path, frozen bundle, pin, or test
expectation was changed.

## Exact source provenance

Runtime was selected from the KEEP checkout:

- checkout: `/home/user/work/wt/rt-m2-pin-a0dca169-b`
- commit: `a0dca16975dfe8f5e762703b99d9791a16cf7fd7`
- tree: `4b7dd0fe44be973c344bab3de568eaf0bdd28476`
- imported `runtime_protocol.__file__`:
  `/home/user/work/wt/rt-m2-pin-a0dca169-b/runtime_protocol/__init__.py`
- bundle: `/home/user/work/wt/rt-m2-pin-a0dca169-b/runtime_protocol/schemas/timeline-commit-bundle.json`
- bundle SHA-256:
  `6d707cb84a232f6ecd7e17c09c8722a379bb76b6a9d2869efea691d6bd8366e3`
- Runtime contract schema digest:
  `sha256:ce3781c282564b650890456f6c257f3faabe2de3898a84363fecd47e48b30d59`

Agent was selected from the frozen source snapshot:

- source path:
  `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-m2-next-ordinary-official-prep/agent-final-source`
- source commit: `310e54840fa5fb8eb7e51bb64ed2c34b7a1063b3`
- content tree: `c5a8a3ec7e9e01c61c5ae31834da53bed4be406a`
- Agent schema SHA-256:
  `6ba7b51e9518e7fb08b27ad5b7225855276b657d0adebf704dd853f699768f2d`
- imported Agent package:
  `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-m2-next-ordinary-official-prep/agent-final-source/astrid/__init__.py`
- imported provider:
  `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-m2-next-ordinary-official-prep/agent-final-source/astrid/sdk/timeline/commit.py`

The source snapshot's hashes for the Agent schema, `native_text_binding.py`,
`commit.py`, and `commands.py` match `git show 310e548:<path>` byte-for-byte.

The exact Python `sys.path` observed before pytest was:

```text
["<cwd>",
 "/home/user/work/wt/rt-m2-pin-a0dca169-b",
 "/home/user/work/wt/rt-m2-sealed-text-source-reconcile/tests",
 "/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-m2-next-ordinary-official-prep/agent-final-source",
 "/usr/lib/python313.zip",
 "/usr/lib/python3.13",
 "/usr/lib/python3.13/lib-dynload",
 "/home/user/work/venv-runtime/lib/python3.13/site-packages"]
```

The candidate bundle contains the closed `TargetKey` branch for occurrence text
bindings, including the exact key:

```text
occurrence:occurrence-1/text-binding:voiceover_script::
```

## Actual marked test

Command, run from the exact Runtime KEEP checkout with no bytecode or pytest
cache writes:

```sh
env \
  ASTRID_CHECKOUT=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-m2-next-ordinary-official-prep/agent-final-source \
  PYTHONPATH=/home/user/work/wt/rt-m2-pin-a0dca169-b:/home/user/work/wt/rt-m2-sealed-text-source-reconcile/tests:/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-m2-next-ordinary-official-prep/agent-final-source \
  PYTHONDONTWRITEBYTECODE=1 \
  /home/user/work/venv-runtime/bin/python -m pytest -q \
  --import-mode=importlib -o addopts= -p no:cacheprovider \
  /home/user/work/wt/rt-m2-sealed-text-source-reconcile/tests/test_timeline_text_native_positive.py
```

Result: `........... [100%]`, **11 passed in 3.83s**.

This is the direct Runtime service fixture lane. Its `authorize=lambda: None`
callback is trusted host semantic setup allowed by the task; it is not HTTP
authentication evidence. No full suite or central service run was requested.

## Reconciliation

The prior failure metadata pointed at an unpacked private `candidate-0.2.14`
directory and reported a schema rejection before provider execution. That source
was not the immutable `a0dca169` KEEP checkout used here. With the exact a0/310
imports, the native provider executes and all eleven existing positives pass.
The correct action was therefore to fix source/import selection, not to widen a
schema, bypass authority, drop guards, or alter the frozen pair.
