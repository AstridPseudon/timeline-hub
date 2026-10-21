# Agent coherent installed profile recipe

Date: 2026-10-21

## Disposition

**DESIGN ONLY.** The b979 child diagnosis is proven. The existing child is not
the profile to reuse for an installed runner: it contains `astrid` and the
vendored `astrid_runtime_client`, but no `runtime_protocol` or
`astrid_runtime`. The normal help path succeeds because it does not import the
Runtime observer; `astrid.sdk.documents` and the direct doctor diagnostics
import fail with `ModuleNotFoundError: No module named 'runtime_protocol'`.
The public doctor wrapper then masks that failure with its existing
`UnboundLocalError` path.

No build, install, child mutation, profile request, test-service request, or
full-suite request was made by this task.

## One concrete private fixture

Use this disposable, private layout for the one later manager-owned profile:

```text
PRIVATE_ROOT=/tmp/timeline-m4-coherent-installed-<final-agent-short-sha>
  wheelhouse/                         # three locally built product wheels
  source/agent/                        # private archive copy at AGENT_SHA
  source/runtime-b92/                  # private archive copy at RUNTIME_SHA
  source/client-95/                    # private archive copy of 95 packages/python
  venv/                                # non-editable installed runner
  profile/astrid.json                  # existing SourceProfile carrier
  provenance.txt                       # audit record, not Runtime authority
```

At this design's readback, the current Agent integration tip is
`3f1c13a47c5c701bf8d2bb963b23c47412eb9f20`, tree
`f1612693060cbfe4f5e5296d71bc1536346ab1cf`. This is the concrete candidate
for `AGENT_SHA` until the manager freezes a later final chosen public SHA. The
recipe must substitute that exact frozen SHA everywhere; it must never use the
old `b97979411` child marker as the Agent identity.

Runtime is split deliberately:

* build the Runtime product wheel from compatible Runtime
  `b92d3e7a05eec65c142294ef4873edd059e9b31d` (`tl/integration`, tree
  `6abc2f117391de8e7e35c0283f575a002199894d`);
* build the normal generated client wheel and retain the normal artifact
  inputs from immutable Runtime
  `95bd3c5f6d00e9bc8cc8cbe5ef510b68ed660f3` (tree
  `d3a290b407fa61e6ab2d476f50c068073f70df00`).

The normal contract/artifact checks remain the existing ones: client contract
`0.2.14`, protocol `workspace.v1`, schema digest
`sha256:7d4afa05962b8cd61643213fc79cdde41e16046c4e2a777bd299b48af0f31816`,
component manifest digest
`sha256:1ad76db27c1d9716bb234f811bf63e1f5898cb3d5f9b835a821765e6cad895e5`,
`133` operations, `contract/artifacts.json` hash
`a902387c6a2315374f7e73511feea47da30191aba831b48820b3864b773a532d`, and
Runtime artifact version
`sha256:54205b3ecb55038e416b31af936c9af26afa30dc1b05da16157ee4d861fe05ac`.

## Exact construction recipe

This is the existing Runtime 4406 installed-root recipe, extended only by
putting the missing Runtime packages into the same private environment. It
does not add a field, authority, route, package version, or source-code path.

1. Freeze `AGENT_SHA` to the final chosen public Agent commit. Verify the
   Agent source checkout is clean, then archive that exact commit into
   `PRIVATE_ROOT/source/agent`; do not expose the checkout through
   `PYTHONPATH`. Archive Runtime b92 into `source/runtime-b92`, and copy only
   `packages/python` from immutable Runtime 95 into `source/client-95`.
2. Build three wheels into `PRIVATE_ROOT/wheelhouse` using private source
   copies and the existing no-network/no-dependency build shape:

   ```bash
   python3.13 -m pip wheel \
     --no-index --no-build-isolation --no-deps \
     --wheel-dir "$PRIVATE_ROOT/wheelhouse" \
     "$PRIVATE_ROOT/source/runtime-b92" \
     "$PRIVATE_ROOT/source/client-95" \
     "$PRIVATE_ROOT/source/agent"
   ```

   The product wheel set must contain exactly `astrid-runtime==0.1.0`,
   `astrid-runtime-client==0.2.14`, and `astrid==0.1.0`. Record each wheel's
   SHA-256 and its source commit in `provenance.txt`. The command is a recipe
   for the later manager run; it was not executed here.
3. Start a new Python 3.13 venv at `PRIVATE_ROOT/venv`. Materialize all 164
   entries from the frozen
   `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/tests/provision/venv-agent-child-s2.txt`
   pin set from its read-only wheel/byte inventory. Its recorded SHA-256 is
   `478af081b0f27c1e90dac1ab4b0b645583f34787ecfe7b8079d1bb88ca034761`.
   Preserve every exact version and VCS revision in that file; the Agent line
   is the one intentional replacement with the locally built final Agent
   wheel. Do not omit dev/test pins merely because the first import probe does
   not use them.

   The 4406 fixture's `_safe_copy` discipline is the model if the approved
   inventory is materialized by bytes: source files must be regular files
   inside the read-only source environment, target paths must be private,
   collisions must be byte-identical, and no symlink may be copied. The
   shared child may supply bytes only; it is never an install target.
4. Install the three local product wheels into that private venv with the
   existing non-editable, dependency-closed shape:

   ```bash
   "$PRIVATE_ROOT/venv/bin/pip" install \
     --no-index --no-deps --force-reinstall \
     "$PRIVATE_ROOT/wheelhouse/astrid_runtime-0.1.0-*.whl" \
     "$PRIVATE_ROOT/wheelhouse/astrid-0.1.0-*.whl" \
     "$PRIVATE_ROOT/wheelhouse/astrid_runtime_client-0.2.14-*.whl"
   ```

   This is safe only after the complete 164-pin carrier has been materialized
   in the same private venv. The Runtime wheel supplies both
   `runtime_protocol` and `astrid_runtime`; the Agent wheel supplies the exact
   final Agent package. No checkout import, editable install, ambient
   `PYTHONPATH`, or shared-venv write is permitted.
5. Reuse the existing installed-root profile carrier. Write only the existing
   `SourceProfile` shape used by `test_wc10_installed_launcher.py`:

   ```json
   {
     "profile": "astrid",
     "runtime_checkout": "<PRIVATE_ROOT>/venv/lib/python3.13/site-packages",
     "source_checkout": "<PRIVATE_ROOT>/venv/lib/python3.13/site-packages",
     "runtime_environment": "<PRIVATE_ROOT>/venv"
   }
   ```

   The two installed-root paths are intentionally the same private site-packages
   root. Runtime resolves the existing `astrid.json` carrier and launches the
   selected venv interpreter. Do not add `runtime_command`, an authority
   selector, a new environment variable, a profile field, a protocol route, or
   an ambient checkout fallback.

## Required preflight checks

All checks below run from a neutral directory with `python -I -B` and an
environment containing only the normal executable `PATH`, locale/temp values,
and the test's existing Runtime inputs. In particular, the child probe has no
`PYTHONPATH`.

* Source provenance: `git rev-parse HEAD`, `HEAD^{tree}`, and clean status on
  the Agent final SHA, Runtime b92 source, and Runtime 95 client source. The
  installed Agent marker must equal `AGENT_SHA`; a marker mismatch is a hard
  refusal, not a warning. Runtime b92 and client/artifact 95 identities are
  recorded separately and may not be silently collapsed into one source claim.
* Distribution closure: compare all 164 pinned names, versions, and VCS
  revisions to the private environment; then require the three product
  distributions at the exact versions above. Every `RECORD` path must resolve
  below the private venv, have no symlink component, and remain byte-stable
  before and after the profile is written.
* Product origins: `importlib.metadata` and `importlib.util.find_spec` must
  resolve `astrid`, `astrid_runtime_client`, `runtime_protocol`,
  `astrid_runtime`, and `banodoco_timeline_schema` inside the private venv (the
  schema package is one of the 164 pins). Probe representative native/data
  packages such as NumPy, Pillow, OpenCV, and PyYAML the same way. No imported
  module may resolve to the Agent, Runtime, App, Composition, or another
  ambient checkout.
* Contract/artifacts: verify the client contract/schema/component/artifact
  digests listed above against the installed files and the immutable 95
  producer inputs. Verify the Runtime wheel contains its package data and
  `runtime_protocol` schemas.
* Profile custody: all three profile paths are absolute; the environment,
  site-packages root, and every path component are private and symlink-free;
  `runtime_checkout` and `source_checkout` equal the installed site root; the
  profile contains only the existing fields. The child interpreter must be the
  selected `runtime_environment/bin/python`.
* Hermetic doctor: first require direct imports of `runtime_protocol` and
  `astrid_runtime`; then run the normal read-only `python -I -B -m astrid
  doctor --json` through the installed environment. Expected resolution is a
  normal Runtime observation (or an explicit normal Runtime-unavailable
  result if no daemon is present), never the b979 missing-module traceback and
  never the wrapper `UnboundLocalError`. The later launcher proof is separate.

## Marker and failure boundary

The valid inherited 5664 run had a coherent runner identity: Agent commit
`5c5173dcb57669a9d43e5add2674543333f1c6d2`, tree
`8626f868a3869b23baaca9814adb930e8952e4c7`, child marker `5c5173d…`, and
schema path under `venv-agent-child-c13-5c5173dc`. Its six red nodes were
classified from terminal traces and are not setup evidence.

The 21969 snapshot is different: its source snapshot is tree
`0698a30b3eb42d47db84ed5ed2e21221158795c4`, while the selected child marker is
`b97979411` in `venv-agent-child-published14-b9797941`. Its suite also sets
`PYTHONPATH="$PWD:/home/user/work/runtime"`, so source-checkout imports are
possible. The retained run had not produced a terminal result when this
design was prepared. Therefore its observed `F` characters are not a terminal
classification, and no new failure may be attributed to the missing Runtime
profile without the final node, traceback, and exact import origin. The b979
missing-module diagnosis is independently proven by the bounded hermetic
probes above and remains the sole environment fix established here.

## Separate mypy/NumPy issue

The independent Python 3.11 typing problem is not part of this Runtime fix.
The observed toolchain used Python 3.13.16 with NumPy 2.5.2 stubs while the
repository mypy configuration targets Python 3.11; the installed NumPy stubs
use newer type-statement syntax, and PyYAML stubs are absent. Main CI's
Python 3.11 lock selects the compatible NumPy line. Do not resolve this by
`# type: ignore`, changing the mypy target, weakening the version target, or
silently selecting another NumPy version. The coherent Runtime profile must
preserve the 164 pins exactly; mypy qualification remains a separately
resolved Python 3.11/tooling issue.

## Manager handoff

Do not create this profile or request a suite from this design. The manager may
request exactly one fresh private profile only after the terminal 21969 result
confirms that the relevant failures are environment/profile failures and
after freezing `AGENT_SHA`. The profile path, wheel hashes, 164-pin digest,
source commits, origins, and doctor result must be recorded together. No new
CLI/API/package version/source code/test is needed.
