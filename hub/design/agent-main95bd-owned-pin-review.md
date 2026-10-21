# Agent Main95bd normal consumer-pin review

Date: 2026-10-21 UTC

## Verdict

**APPROVE FOR STAGING.** This is approval of the exact finalized normal
consumer pin for staging and reciprocal App pairing only. It is not approval
for integration, publication, activation, adoption, or the project gates.

Runtime95bd was already reciprocally approved. This review did not rerun the
Runtime565 lane or any producer/full suite.

## Exact identities and ancestry

- Consumer HEAD: `e35ad5e72ed9acc61d659a6b4b9c32d69208ab8d`
- Consumer tree: `a2454c2cb472fa5404289c9f48bb7779d330879e`
- Meta base: `tl/agt-m2-main95bd-normal-owned-pin`
  (`e35ad5e72ed9acc61d659a6b4b9c32d69208ab8d`); review tree is unchanged
  from the meta base.
- Runtime producer: `95bd3c5f6d00e9bc8cc8cbe5ef510b68ed660f3c`
- Runtime producer tree: `d3a290b407fa61e6ab2d476f50c068073f70df00`
- Runtime checkout: `/home/user/work/wt/rt-pin-95bd3c5f`; it was clean.

The consumer is an actual descendant of Main `497714c73531f164082555ec81b61ca5bc8b6554`,
current integration `520fd21796f9a0480c1b5cc147fae10f4288444c`, and ordinary
source stage `ba21beffd177e7d80a5b839bde5a9e25b97235c2`.

## Pin, source, and leakage audit

- `runtime.lock.json` SHA-256:
  `920f4a3edf3d0e5ce9df5a0b2749f7b02bc2ea7db6fef2ec70db8d02b65be8e7`
- Producer `contract/artifacts.json` SHA-256:
  `a902387c6a2315374f7e73511feea47da30191aba831b48820b3864b773a532d`
- Producer version:
  `sha256:54205b3ecb55038e416b31af936c9af26afa30dc1b05da16157ee4d861fe05ac`
- 76/76 producer artifacts are present and hash-correct.
- All 15 locked consumer files are byte-identical to their authorized
  Runtime95bd producer sources and match both lock and manifest hashes.
- Normal `vendor_lock.py update` and `check` both passed in a private overlay;
  the real worktree and shared dependencies were not modified.
- Ordinary edit schema is byte-identical to Runtime:
  `6ba7b51e9518e7fb08b27ad5b7225855276b657d0adebf704dd853f699768f2d`,
  with 55 definitions and 29 `EditCommand` branches.
- Distinct contract identities are preserved: OpenAPI schema digest
  `sha256:7d4afa05962b8cd61643213fc79cdde41e16046c4e2a777bd299b48af0f31816`,
  health schema `dcaec4238eec1633683b3bc223c039f78e7f9066effb18d80667a4a903f4510e`,
  services schema `10614b9c5a8f044b4c6727701147197b91410ddaf4230b8fa990b78255574018`,
  raw edit schema `6ba7b51e9518e7fb08b27ad5b7225855276b657d0adebf704dd853f699768f2d`,
  and timeline bundle `6d707cb84a232f6ecd7e17c09c8722a379bb76b6a9d2869efea691d6bd8366e`.

The 61 paths introduced by the ordinary source stage remain byte-identical
after composition. The current source schema is not private392
(`39211e63a50b9fb495fdf3feb5beaf0e4d0b4eab9a7e13f4d5f769e0d317429d`) or
private84fc (`84fc0863a1f925f32c00b171eaf51b8f06afb7d34064296394bc8592386cbbc`).
The lock selects Runtime95bd, not old a0 (`a0dca169...`), private392, or
private84fc/0.2.15. The three generated client files that differ from the old
a0 consumer (`__init__.py`, `contract_metadata.py`, and `generated.py`) are
current-producer bytes; the unchanged `timeline_commit_types.py` is also
verified against the current producer by the 15/15 byte audit, so it is not a
copied stale artifact.

## Tests and checks

Passed in this review:

```text
python3 scripts/gen_cli_surface.py --check
python3 scripts/artifact_manifest.py --check
python3 scripts/vendor_lock.py check runtime.lock.json --producer /home/user/work/wt/rt-pin-95bd3c5f
→ all passed
```

The private-overlay normal updater/check also passed with the exact producer
and reproduced lock SHA `920f4a3e...b65be8e7`.

The composed pure control lane passed:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD:/home/user/work/wt/rt-pin-95bd3c5f" \
/home/user/work/venv-agent/bin/python -P -m pytest -q -p no:cacheprovider -m 'not integration' \
  tests/sdk/test_scene_caller_preservation.py \
  tests/sdk/test_scene_dispatch_contract.py \
  tests/packs/rendering/test_scene_only_executor.py \
  tests/sdk/test_scene_save_core.py \
  tests/sdk/test_timeline_sheet_native.py \
  tests/sdk/test_timeline_owned_move_publish.py
→ 112 passed, 2 skipped
```

An independent targeted vendor/client/schema superset also passed:
`180 passed, 1 skipped` across `tests/test_vendor_lock.py`, the stage1
generated/client/schema tests, and the focused SDK schema/client tests. The
normal pinner handoff separately records its focused vendor/client/schema
lane as 71 passed; no producer/full rerun was made here.

The bounded paired command was run against explicit Runtime95bd:

```text
ASTRID_RUNTIME_CHECKOUT=/home/user/work/wt/rt-pin-95bd3c5f \
PYTHONPATH="$PWD:/home/user/work/wt/rt-pin-95bd3c5f" \
/home/user/work/venv-agent/bin/python -P -m pytest -q -p no:cacheprovider -m integration \
  tests/editing_conformance/test_native_sheet_current_runtime.py \
  tests/editing_conformance/test_commit_runtime_native_checkout.py::test_authenticated_v1_commit_reload_undo_survives_stopped_renderer_and_preview_reports_unavailable
→ 11 failed in 4.53s
```

These are harness/setup failures, not product-green evidence. The ten sheet
cases fail during health/bootstrap because the in-process fixture's
`daemon_runtime` double supplies only `instance_id` (`tests/editing_conformance/test_native_batch_ingress.py:68-70`),
while Runtime95bd's health route calls `daemon.service_status()`
(`runtime_protocol/server.py:411-418`). The Gate3 case reaches the real daemon
startup and is blocked by the sandbox's `PermissionError: [Errno 1]
Operation not permitted` when binding its local socket. No health override,
fake healthy result, skipped assertion, or weakened test was added.

The central named `current-http-cli-durability` wrapper is missing at
`scratchpad/orch/tests/runtime-current-http-cli.sh` (the pinner recorded exit
127), so that named suite remains unqualified. The current-fixture worker owns
the actual fixture repair and the follow-up local-socket qualification.

## Remaining paired gates and boundaries

1. Repair the obsolete in-process daemon double through the current fixture
   worker's real Runtime service-status helper, then rerun the eleven bounded
   paired cases against immutable Runtime95bd.
2. Supply/restore the named current HTTP wrapper or run its approved direct
   current-fixture equivalent through the central test service.
3. Qualify real Gate3/local-socket commit, reload, undo, and renderer-off
   behavior after the socket-capable service run.

No full suite, Runtime565 lane, historical renderer/browser proof, App
integration, publication, activation, adoption, or integration-branch change
was performed or claimed. Product, producer, integration, shared dependency,
and public tuple state were left unchanged.
