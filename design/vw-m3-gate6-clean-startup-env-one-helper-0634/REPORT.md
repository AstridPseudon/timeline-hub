# Gate 6 corrected helper-only readiness

## Result

The one authorized central diagnostic was **NOT READY**. The full preflight
passed, then the corrected helper startup ran exactly once and failed before
`startRealPackHost-returned`:

```text
Error: Pack-host helper reported failure
  error_type=RemotionValidationError
  error_location=/home/user/work/wt/agt-pin-d0a5072b/astrid/core/rendering/remotion_runtime.py:480
  pack-host startup cleanup failed
```

This is a new retained failure after the requested one-line correction. The
frozen source at line 473 calls `probe_context`; line 476 rejects non-interactive
`GIT_*` overrides and line 480 raises the reported error. The corrected launch
command removed only `export PYTHONNOUSERSITE=1`; it did not weaken this strict
validator or add a retry. The central launch inherited the test service's
`GIT_CONFIG_COUNT`/`GIT_CONFIG_KEY_*` environment, which is the next visible
unsupported startup override. No further run is authorized.

## Central evidence

Result ID:
`vw-m3-gate6-clean-startup-env-one-helper-0634-e2e-viewing-gate6-clean-startup-env-one-helper-0634-1021063656-2838`

Exact command: `bash design/vw-m3-gate6-clean-startup-env-one-helper-0634/run.sh`

Central result: exit 1, 29 seconds. Log SHA-256:
`8a292ab267c707137b0c914febecfca83bc8ea2f76bb467896f22a0acbe39559`.
Summary SHA-256:
`c6fe79cb79299b4db60b68079991ede7a00df8bf6265db41691aadda45d027e5`.

The central preflight passed before startup, including the exact d00/a8bf App,
d0a Agent, SERVER8f Runtime, helper b70/bc75, Composition 5a4/public13,
archive9412/all77, source5902/prefixed7669, App graph8bdc/32393, Runtime
graph4913/21455, Node20.19.4/43d6, Chrome155, exact GET 200 of 20,742 bytes,
five-case collection, Python origins, peer bytes, and empty controls. It
recorded `token-issued:false`, `browserLaunched:false`, and
`runtimeStarted:false` before the helper boundary. No browser, export, issue,
grant, marker, physical allocation, or five-case run occurred.

Allocation forecast before the request: central snapshot 1,521,727 bytes,
stage links/metadata 1,048,576 bytes, empty-realm/helper reserve 67,108,864
bytes, total 69,679,167 bytes. Central free space was 11,006,492,672 bytes;
the 10,737,418,240-byte floor remained satisfied.

## Exact correction and retained guards

The complete launch correction is:

```diff
 export PYTHONDONTWRITEBYTECODE=1
-export PYTHONNOUSERSITE=1
 export PYTHONUNBUFFERED=1
```

The private copy also changes only worker-local paths and uses the existing
0617 source-binding fixture, existing 0623 flat ordering, and existing 0354
driver. Source, credential, graph, admission, toolchain, pinned Python,
`python -I` schema probe, cleanup, and lifecycle guards are retained. Old
0354/0617/0623 evidence and scripts were not modified.

Owned fixture SHA-256s:

```text
COMMAND cd905c4453552e1a9b086efbb88b7ff5a9290ce6878b964f9aa124c43237185a
run.sh 73d29fddfd4929a8bee7cfa57f3e4ad98ea182349576c0868a677a10e0b2c6b1
preflight.sh f067c4fcf013863c1b2161177f97120dc51bcbe7a02c0df91df2a05a9a3e022a
prepare.mjs 7ad93869a27ff241319559881ade5207c65005f1b1bf9cdb7eb5641a713fd074
issue.mjs 905f58098e1ef5658edf8ae43a63b03ee8b02d0807af35d334200d987dd003a8
dist-availability.mjs fb7632d2c69da10c65db04052f0b04ede1b6e72064817fdc600098135ea50dfd
current-pack-host-readiness.mjs f59783a7c5cf851b4e500e08567efdfbd0cc50178da29b15b7ad865246c5c796
```

## Checks

Passed:

```text
bash -n run.sh preflight.sh COMMAND
node --check prepare.mjs issue.mjs dist-availability.mjs
negative probe_context witness with PYTHONNOUSERSITE=1: refused
corrected probe_context witness: accepted clean-schema-env/v1
central complete preflight: PASS
```

The same complete preflight run directly in this sandbox reached the pinned
Python-origin probe but was blocked by sandbox child-process `EPERM`; the exact
check is before helper startup in the central command and passed there. No
repository product suite or full suite was run. A unique named composition
diagnostic was added to the central test-service allow-list:
`e2e-viewing-gate6-clean-startup-env-one-helper-0634`.

The central failure is terminal for this task. The next step requires a new
manager decision about the inherited Git environment; this worker does not
change it or retry.
