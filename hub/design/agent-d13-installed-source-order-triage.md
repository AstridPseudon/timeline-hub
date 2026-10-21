# D13 installed source-order triage

**Security SOURCE verdict: REQUESTCHANGES. This is not D13 qualification.**

Reviewed exact `tl/agt-m2-d13-runtime-installed-origin-close` commit
`0dbcd7a4a2f5a7a09bd168d0d43f61cc77a679e3`, tree
`3f78a595571667df87bae553fb5e3b5f35720f38`. This worker's clean HEAD equals
that candidate. Read PLAN.md and AGENTS.md. No settled decision changed;
no product or test edits, adversarial payload generation/execution, bytecode
alteration, or full/native/browser/render run occurred.

## Blocking source findings

1. **The launcher origin probe executes parent packages before content validation.**
   `astrid/sdk/host_bootstrap.py:711-717` imports the installed measurement
   helper, checks three Runtime origins, then calls `importlib.util.find_spec`
   on dotted Agent module names. Python's implementation imports their parents
   (`/usr/lib/python3.13/importlib/util.py:91`). In particular, resolving
   `astrid.core.execution.generic_host` imports `astrid.core.execution`.
   Its startup check at `astrid/core/execution/__init__.py:6` immediately returns
   for this `-I -c` probe: `astrid/core/source_identity.py:105-108` only guards
   the isolated `-m astrid.core.execution.generic_host` entrypoint. Execution
   then reaches `execution/__init__.py:8` and
   `execution/persistent_supervisor.py:17`, which imports Runtime platform code.
   There is no closure-digest comparison in the probe. Its containment and
   symlink checks on returned Agent origins run only after the subprocess
   completes (`host_bootstrap.py:723-733`). A real, non-symlink source file
   at the expected Runtime path can therefore be imported without verifying
   its admitted content. Rejection by a later actual-host guard cannot undo
   execution in this earlier probe.

   The launcher module itself also imports Runtime at `host_bootstrap.py:28`,
   before any of its function-level validation. `ensure_pack_host` probes at
   line 1365, imports `generic_host` at line 1385, and only measures the closure
   at line 1393. The foreground route at lines 1750-1765 reuses that process
   and calls `_cli()`; it does not enter the new isolated-module fence.
   Consequently the direct host fence is not a general preimport guarantee
   for launcher/service paths. No normal-launcher success or failure is claimed
   here.

   **Smallest repair direction:** make the existing origin probe non-executing
   for every product module, using explicit package search directories and
   `PathFinder` rather than dotted `util.find_spec` calls. Perform the existing
   admitted closure comparison from the trusted launch boundary before
   importing the installed Runtime/launcher modules being validated, including
   the foreground path. Use the existing selected interpreter, exact installed
   root, and source-closure digest; do not mint an authority from the probe's
   unverified output or restore checkout-derived imports.

2. **The executable closure omits cached code Python can load.**
   `astrid/core/source_identity.py:22-24` excludes every file under
   `__pycache__`. Although both Runtime trees now participate in the closure
   (lines 51-63), their executable caches do not. An expected `.py` origin
   and a `SourceFileLoader` do not imply execution of those measured source
   bytes. Python 3.13's `SourceLoader.get_code` reads the cache at
   `_bootstrap_external.py:1120`, applies timestamp/hash-header checks, and
   returns cached code at line 1156 before the source-compilation branch.
   The `sys.dont_write_bytecode` condition appears later at line 1163: `-B`
   suppresses writes, not reads. Isolation also does not force source loading.
   Ordinary cache acceptance and unchecked-hash caches remain relevant;
   source metadata or a hash in the cache header is not a digest of its code
   body. Thus executable bytes can differ while all currently measured source
   digests and required `.py` origins remain equal. This is a source-proved
   coverage defect, not a claim that this worker executed modified bytecode.

   `tests/sdk/test_installed_runtime_source_identity.py:29` removes caches from
   its fixture. Its source-substitution cases therefore cannot establish cache
   coverage. Other file forms outside `__pycache__` are hashed by the directory
   walk; this finding concerns the explicit exclusion and loader precedence,
   not a blanket claim that all native or sourceless modules are omitted.

   **Smallest repair direction:** at the existing trusted preimport boundary,
   ensure Python executes only the validated source bytes, or bind every
   cache/file the selected loader can actually execute into the existing
   closure and enforce that binding before imports. Apply the same rule to
   bootstrap/launcher code, not only Runtime leaves. Merely adding `-B`,
   forcing hash-header checks, or deleting caches once before launch is not
   a complete content/custody fence. Preserve post-probe revalidation and the
   existing exact-tree and no-symlink requirements; do not mutate shared installs.

Both repairs must retain the existing process/source custody rules and original
strict tests. No new profile, public DTO, token, environment carrier, alternate
import root, or acceptance path is required. This report proposes corrections;
it does not implement or qualify them.

## What the candidate does establish

For the direct isolated host-module launch, the source order is improved:
`execution/__init__.py:6` runs before its Runtime-dependent imports;
`source_identity.py:119-124` requires the exact selected installed root,
checks required Runtime origins/search locations and symlinks, then compares
the existing closure digest. Both adjacent Runtime source trees participate.
Subject to the cache/bootstrap issue above and the existing filesystem custody
assumptions, ordinary Runtime source replacement present at that check is
detected before the later Runtime imports. No claim of atomic filesystem
immutability after measurement follows.

Compared with parent `38281f7274bfd799d3b87275f38a0a5d14dd2c5f`, the original
`tests/core/execution/test_worker_startup_identity.py`, `process_group.py`,
`custody_broker.py`, and `core/rendering/verified_source.py` are byte-identical.
The bootstrap test diff only extends required origin-key lists. This worker
left all tests unchanged.

## Evidence and limits

The stopped worker is
`ORCH/workers/agt-review-d13-runtime-origins-final`. Its STOPPED record says
orphan finalized at `2026-10-21T04:31:25Z` after no progress since 04:03 and
repeated errors; exit is 143. I read its retained script as text only and
verified four relevant retained source files against the exact candidate.
There is no current-worker `adversarial-result.txt`. The log contains an older
review's reproduced counterexample on **38281f727**, quoted report text, and
the later proposed script for this candidate, followed by errors. Those are
different evidence categories: the proposed cache/order probe was **not
successfully executed in the retained record**, and was not rerun here. Its
planned assertions/output strings are not observed results.

The repair worker's retained `security-neighbors-final.log` records **120 passed,
2 warnings in 30.38s**; `final-negatives.log` records **11 passed in 7.93s**;
`source-startup-overlay.log` records **7 passed in 1.13s**. These are historical
results, not independently repeated qualification. Its first `targeted.log`
has **85 passed, 1 failed**, the sanitized child missing installed Runtime;
the repair report records a baseline reproduction and private-overlay remedy.
None of these results tests the cache gap or fixes the source-order finding.

New checks in this worker (all exit 0):

```sh
ORCH=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch
WORKER="$ORCH/workers/agt-review-d13-installed-source-order-triage"
python3 -I -B "$WORKER/source_assertions.py"
```

**13 source/AST assertions passed.** They read exact candidate and local Python
loader source without importing candidate modules or executing the retained
probe. Log: `WORKER/source-assertions.log`. The loader source SHA-256 is
`283ca9ae00bd7758aa006df9be93f4b6b8d3228e3509f662cf54b1518797fbde`.

From the assigned worktree, unmodified trusted tests only:

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD:/home/user/work/runtime" \
  /home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider \
  --basetemp="$WORKER/pytest-tmp" \
  tests/sdk/test_host_bootstrap_source_identity.py::test_installed_profile_strips_source_pythonpath_and_probes_selected_interpreter \
  tests/sdk/test_host_bootstrap_source_identity.py::test_installed_profile_refuses_checkout_origins_from_isolated_probe \
  tests/sdk/test_host_bootstrap_source_identity.py::test_installed_profile_does_not_use_ambient_runtime_checkout \
  tests/core/execution/test_worker_startup_identity.py::test_startup_attestation_normalizes_and_records_exact_target \
  tests/core/execution/test_worker_startup_identity.py::test_source_closure_digest_changes_when_sdk_or_launcher_changes \
  tests/core/execution/test_worker_startup_identity.py::test_startup_fails_before_readiness_on_source_mismatch \
  tests/core/execution/test_worker_startup_identity.py::test_startup_fails_before_readiness_when_required_target_is_missing \
  tests/core/execution/test_worker_startup_identity.py::test_startup_rejects_malformed_target_before_claims
```

**8 passed in 0.76s** (`WORKER/trusted-targeted.log`). These are mocked probe and
pure identity neighbors; they do not execute altered product code, open sockets,
or prove installed qualification. Runtime on this test-only PYTHONPATH supplies
dependencies, not installed execution authority. Shared dependencies stayed
read-only. No full suite was requested. Temporary pytest output was removed.

Next: return both concrete source findings to the Agent owner, repair within the
existing launch authority, and obtain a fresh bounded source review on that exact
commit. Keep coherent installed normal-launcher and D13 qualification separate
and unverified until their own authorized proof succeeds.
