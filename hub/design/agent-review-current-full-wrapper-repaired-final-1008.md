# Final review: current public full wrapper

## Verdict

**REQUEST CHANGES. Do not request the full lane.** The exact committed wrapper
is present at
`scripts/full_coherent_public_current_integration.sh` on branch
`tl/agt-review-current-full-wrapper-repaired-final-1008` (HEAD
`475fb69df31fc5af059669343f1fae4545e8e723`). Its blob is
`233e115294b9db7b72792f9c2528fb2c99de5dcd`; its SHA-256 is
`de8b93c85d27e658902635017430cecaebc424efb8a7d3bd8d2be52cdce2c669`.

### First counterexample: client wheel/source parity cannot pass

At wrapper lines 286--319, the client wheel entry uses `source_prefixes` of
`("packages/python/astrid_runtime_client",)`. The wheel payload keys retain
`astrid_runtime_client/<file>`, while the `git archive` payload is stored in
`source_bytes` under the unstripped archive names
`packages/python/astrid_runtime_client/<file>`. The comparison at line 318
therefore compares different key spaces and rejects the intended public95
client wheel even when every file's bytes are correct.

Read-only evidence:

```text
git archive ... -- packages/python/astrid_runtime_client
packages/python/astrid_runtime_client/__init__.py
...
unzip -Z1 .../astrid_runtime_client-0.2.14-py3-none-any.whl
astrid_runtime_client/__init__.py
...
```

The same function has no source-prefix normalization before `wheel_bytes !=
source_bytes`. This is a deterministic false refusal in the newly added
wheel/source guard, so the wrapper does not yet satisfy the requested parity
proof.

### Registration / durable lease is still absent

The exact name `full-coherent-public-current-integration` has no entry in the
current ORCH `tests/suites.conf`, and no manager `notes/*.lease` names this
wrapper or its profile/wheel inputs. The only related file,
`managers/agent/notes/coherent-gate-environments.lease`, says it was retired
and identifies the f4edcb4b profile only as a handoff. The 0948 report's
“stable ORCH wrapper lease” is therefore prose, not a live lease. Existing
`agent full-remotion12*` lines are different direct pytest callers and do not
invoke this wrapper.

The wrapper is durable as a Git blob/branch, but the required active caller
and input lease are not. The current `/home/user/work/agent` checkout also
does not currently have the expected c4b identity (it is at
`e211a328815142fd9fd0cec055fdf2c688715cbe` when checked); the wrapper's
default `SOURCE_ROOT=$PWD` would likewise identify the wrapper-repair HEAD,
not c4b. A future caller must explicitly supply and lease a clean c4b source
checkout, the exact private profile, wheel, and 164-pin carrier.

### What passed by inspection / bounded checks

- Constants retain the settled values: 164 pins and hash
  `478af081b0f27c1e90dac1ab4b0b645583f34787ecfe7b8079d1bb88ca034761`;
  166 RECORD/distribution closure; Agent c4b/tree
  `c4b964f6...`/`d7796be2...`; Runtime b92/tree
  `b92d3e7a...`/`6abc2f11...`; client public95/tree
  `95bd3c5f...`/`d3a290b4...`; C13 source/hash and Node pins remain present.
- RECORD rows, installed-file closure, wheel RECORDs, installed bytes, and
  source-byte checks are present. The client source-prefix bug above prevents
  claiming that the combined guard succeeds on the intended profile.
- Final import bootstrap preserves source `astrid` while preloading private
  Runtime/client/schema packages and checks their post-import origins. No
  checkout is used as private package authority after bootstrap.
- Final invocation remains exactly `exec "$PROFILE_PY" -m pytest -q -n 3
  "$@"`; no marker, cache-provider, `--basetemp`, or temporary-directory
  override was added. Direct exec preserves nonzero and collection-failure
  statuses; the repaired report's planted child/SIGTERM results were not
  rerun here because the first source-parity defect is conclusive.
- No skip/xfail/deselection, assertion weakening, whole-fixture bypass,
  profile build/install, pytest body, full request, native/HTTP/browser/
  renderer run, or shared-dependency write was performed.

### Commands run

- `bash -n scripts/full_coherent_public_current_integration.sh` — PASS.
- `git diff --check` — PASS.
- Missing-input preflight with `SOURCE_ROOT=/home/user/work/agent` and profile,
  wheel, and pins unset — exit **2**, no pytest invocation; it reported the
  missing profile/wheel and the live source-root mismatch.
- Read-only `git archive`/wheel member inspection — CONFIRMED the
  `packages/python/astrid_runtime_client/...` versus
  `astrid_runtime_client/...` key mismatch.

### Required next steps

Normalize the client archive names to the wheel package names (or compare
after applying the inverse prefix mapping), add a real ORCH suite registration
that invokes this exact wrapper, and create a live lease covering the wrapper
blob plus the exact c4b source, private profile, wheel, pin carrier, Runtime,
client, and C13 inputs. Then rerun only the compact guard negatives and a
profile preflight; this review does not approve any unbuilt profile or any
source mismatch.
