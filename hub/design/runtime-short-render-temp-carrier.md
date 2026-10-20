# Runtime answer: short browser temp carrier for normal MP4

Date: 2026-10-20 UTC  
Worker: `rt-m3-short-render-temp-existing-carrier`  
Runtime base: `601d533d91e3726c4f7ae74723e8eff4adbe2f90`

## Decision

Runtime has no additional private attempt/work/browser-temp knob for this
failure. The existing supported carrier is the already-admitted private
process environment, specifically `TMPDIR` (with `TMP` and `TEMP` kept in
step). Runtime already propagates it; the normal render path later replaces
that value with a nested invocation directory. Runtime does not own that
path construction.

The minimal owner location, if a patch is needed, is Agent's:

`astrid/packs/rendering/rendering/renderers/remotion/root_preparation.py:_prepared_remotion_root`

That function currently chooses `staging_parent` (the nested attempt/render
workspace) as the parent of `.remotion-runtime-*`. The existing admitted
private `TMPDIR` is the only suitable short-parent input already crossing the
Runtime boundary. It must be selected there only after the Agent-owned
canonical/private/ownership checks in the proposed handoff patch. No Runtime
DTO, public setting, authority, wrapper, symlink, browser flag, codec, or
render-profile change is indicated.

This is an owner recommendation, not an approval to apply the Agent patch:
moving browser scratch outside the attempt tree must retain Agent-side
accounting and cleanup proof. Runtime's storage estimate is a byte budget,
not a path registration or sandbox-root carrier.

## Exact Runtime boundary

The normal local relay path is:

1. `runtime_protocol/local_worker_composition.py:_prepare_relay` builds the
   relay environment. It copies only the Runtime-selected values in the
   allowlist, including `TMPDIR`, `TEMP`, `TMP`, and `XDG_RUNTIME_DIR`, then
   starts `runtime_protocol.local_execution_supervisor`.
2. `runtime_protocol/local_execution_supervisor.py:NativeHostSession` repeats
   the launch allowlist when it starts the Agent GenericHost. Its fixed launch
   `cwd` is `config["support_root"]`; the selected host argv has no attempt,
   render-workspace, or browser-temp argument.
3. Runtime claim/admission stores and returns `execution_request`, but its
   normalized shape contains target/inputs/workflow/execution/limits/etc.; no
   filesystem temp carrier is added. GenericHost copies the claimed request
   into `task_data` and executes it. The attempt root is allocated by Agent's
   `GenericPackHost._allocate_attempt_root`, not by Runtime.
4. Agent's normal MP4 path then runs `RenderService` beside
   `attempt/outputs`, creates `.render-service-*`, and passes that as
   `staging_parent` into Remotion root preparation. Root preparation creates
   `.remotion-runtime-*` there and sets the child `TMPDIR`/`TMP`/`TEMP` to
   that nested root before Chrome starts.

The Runtime path therefore already has the required private input but no
Runtime-owned place to repair its later override.

## Path-length evidence

Viewing's supplied central error reports a 228-byte Darwin socket path:

```text
/tmp/vw-m3-normal-TGpDXE/tmp/astrid-attempt-e8da1f00235b43cabcbc5a4b3d05c129-tk0y3w29/.timeline-5d66df56-f091-48af-a1c9-1c6fa2007c00.mp4.render-service-yrr6h1rb/.remotion-runtime-9x9u2k0m/com.google.Chrome.F0OceF/SingletonSocket
```

The path is the composition of the attempt root, the output-derived
`.render-service-*` directory, the Remotion `.remotion-runtime-*` directory,
and Chrome's `com.google.Chrome.<id>/SingletonSocket` suffix. The supplied
short private parent produces an equivalent 96-byte socket path. This is
consistent with the current Runtime custody source, which treats Darwin
Unix-socket paths as bounded to 103 bytes (it checks the candidate
`root / "s"` in `astrid_runtime/custody_broker.py:_create_compact_socket_root`).

The offline construction probe also found the distinct Agent host-only
carrier can be long before Chrome: `support_root/host-output/attempts` feeds
`attempt_base`, then `astrid-remotion-host-*` becomes the HostRemotionSession
TMPDIR. That path is for `rendering.timeline_visualize`, not the failing
normal MP4 path; it is not a valid fix for this request.

## Carriers considered and ruled out

- `execution_request`: no temp/workspace field and no reason to add one. It is
  scheduler/claim data, not a local filesystem authority.
- Runtime `support_root`/launch `cwd`: fixed host launch roots; changing them
  would alter owner authority and does not repair Agent's later nested temp
  selection.
- Agent `attempt_base` and `HostRemotionSession._root_parent`: an existing
  private attempt carrier for the managed visualization lease only. Viewing's
  normal MP4 trace explicitly does not use `HostRemotionSession`.
- Agent `PersistentRemotionFrameSession._owner_paths`: the existing fixed
  `/tmp/astrid-rfo/owner-<hash>.sock` frame-owner control socket is short, but
  it is not Chrome's profile `SingletonSocket`; managed-host tests explicitly
  reject selecting that legacy owner namespace.
- `HOME`, `XDG_RUNTIME_DIR`, or a new Runtime env key: already propagated or
  prohibited by the settled boundary, and would not address the nested
  `TMPDIR` override.

## Safety boundary for the owner patch

The short parent must remain an Agent-owned private directory selected from
the already-admitted `TMPDIR`, while output and authority remain under the
assigned attempt. The Agent patch must preserve the existing
`TemporaryDirectory`/`ExitStack` cleanup and prove that moved browser bytes
are included in the existing scratch/evidence budget and cleanup uncertainty
handling. Runtime has no existing path-accounting API or sandbox-root record
that can make an outside-attempt directory safe by itself.

No Runtime product patch was made. No full, browser, renderer, or actual
render repeat was run, per the task boundary.

## Evidence read

- Runtime `runtime_protocol/local_worker_composition.py`,
  `local_execution_supervisor.py`, `verified_host_launch.py`, `store.py`,
  `contract/schemas/task.json`, and `astrid_runtime/custody_broker.py`.
- Agent frozen source (read-only): `generic_host.py`,
  `remotion_host_session.py`, `core/rendering/service.py`,
  `root_preparation.py`, Remotion `run.py`, and
  `remotion/src/astrid-frame-worker.mjs`.
- Runtime handoff: `/home/user/banodoco/banodoco-workspace-runtime/RT-worker-handoff.md`.
- Viewing peer request and central error report:
  `peer-viewing-to-runtime-20261020T1858-short-browser-temp-safety.md` and
  `handoff-vw-m3-normal-chrome-socket-REPORT.md`.

## Commands

- `git status --short --branch` — clean Runtime worktree at the assigned base.
- Read-only `rg`/`sed` source trace commands — completed.
- Offline path-construction Python probe — completed; no files or processes
  created.
- No targeted Runtime test was necessary: no Runtime source changed. No full,
  browser, renderer, or actual-render suite was run.
