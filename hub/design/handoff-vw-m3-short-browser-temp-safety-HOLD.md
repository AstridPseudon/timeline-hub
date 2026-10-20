# vw-m3-short-browser-temp-safety-gate

## Decision: REJECT / HOLD

Do not apply `owner-fix.patch` or run the normal MP4 retry yet. The patch is
cleanly applicable (`git apply --check` passes; SHA-256
`2be35cc23825952cdb18abfa405600a30938f2e7eecb8b0dd0ae5a31074db36d`), but
its selected browser parent is outside the existing attempt accounting seam.

## Exact path and ownership review

The reviewed patch changes only
`astrid/packs/rendering/rendering/renderers/remotion/root_preparation.py` and
adds two pure tests. It selects the existing absolute `TMPDIR` only when the
path is canonical, existing, a directory, current-UID-owned, and has no
group/other mode bits; otherwise it falls back to the staging parent. The
normal path remains:

`RenderService` workspace beside `attempt/outputs` -> Root preparation ->
`TemporaryDirectory(.remotion-runtime-*)` -> child `TMPDIR/TMP/TEMP` -> Chrome.

The `TemporaryDirectory`/`ExitStack` cleanup still removes the invocation
child and does not remove the pre-existing `TMPDIR`; outputs and authority stay
under the attempt. The pure helper tests pass, and a direct symlink test shows
fallback works. However, validation is not race-free: after `resolve/stat`, a
same-UID actor can replace the checked directory before `mkdir`/`mkdtemp`.
The check also accepts owner-only modes such as `0500`, so a valid-but-
non-writable `TMPDIR` raises during setup instead of taking the documented
fallback.

## Accounting finding

Runtime 2c4’s contract defines `scratch_bytes` as peak temporary space and
checks `scratch + output` against free space at admission and claim. Its
`storage_preflight` measures `shutil.disk_usage(self.root)`, and its persisted
attempt staging path is only the Runtime settlement path
(`staging/settlements/<attempt_id>`). It neither owns nor accounts for the
Agent host’s external `TMPDIR`.

On the Agent side, the existing live guard computes scratch as
`_attempt_tree_bytes(attempt) - _storage_tree_bytes(attempt/outputs)`;
`EvidenceBudget` likewise keys and measures one attempt root. Both are called
while the child runs and at cleanup. They do not walk or charge an external
`TMPDIR`.

Direct no-render probe: a 4,096-byte file placed in an external admitted-temp
directory was accepted with estimate `{scratch_bytes: 0, output_bytes: 0}`;
the attempt live guard returned successfully and `EvidenceGuardPolicy`
reported `attempt_observed_bytes == 0`. Thus the patch creates a real scratch
budget/evidence-budget escape even when the selected directory is `0700`.

## Required condition / minimal change

Approval requires the existing Runtime/host execution seam to make the browser
parent an accounted attempt root: it must be a real, invocation-scoped private
directory whose bytes are included in the same admitted storage envelope,
sampled by the live scratch/evidence guards, and deleted or retained under the
existing attempt cleanup outcome. If the short path remains outside the
attempt tree, the minimal owner-side change is to extend those existing host
accounting and cleanup calls to charge that exact path; this must use the
existing task estimate/attempt identity and not add a DTO, store field, public
knob, or hidden quota bypass. A Runtime-only free-space check is insufficient.

Until that condition is proven on the actual normal MP4 environment, the safe
owner change is not to select external `TMPDIR` (retaining the current
attempt-local fallback), even though the long Chrome socket remains unresolved.

## Evidence

- `git apply --check /tmp/.../workers/vw-m3-normal-chrome-socket-boundary/owner-fix.patch` — PASS.
- Private source-copy run of the two owner pure tests with the patch applied — `2 passed`.
- Runtime 2c4 private source-copy storage tests — `3 passed, 11 deselected`.
- Agent host controls:
  `PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider tests/core/execution/test_remotion_host_session.py`
  — `24 passed, 2 failed`; both failures are sandbox `PermissionError: [Errno 1] Operation not permitted` socket-channel cases, reported separately and not evidence against this path review.
- No renderer, browser, capture, full suite, install, or product-source application was run. Assigned worktree remains clean.
