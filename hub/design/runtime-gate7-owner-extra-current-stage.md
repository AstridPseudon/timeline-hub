# Gate7 owner extras on retained current stage

Date: 2026-10-21

## Disposition

The missing owner extras are qualified on a private copy of the retained
delivery stage. No four-repo build or test-service request was repeated. The
existing four-repo tree-equality proof remains exactly the recorded tuple from
`runtime-gate7-current-integration-dryrun.md`; this report adds only the
missing carrier proof.

This is not a final ZIP and is not a full Gate7 claim.

## Inputs

- Reviewed installed helper:
  `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/delivery-build`
  - SHA-256: `3dfd5c28a9be9ab809e6c1fe1e9a83fbf8417ea888afc1b10eec5f751023e990`
- Retained owned stage (not sourceGit):
  `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/delivery/build-20261021T004311Z`
- Scanner source:
  `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-vw-m4-owner-scanner-delivery-payload-scanner-v1.0.8.zip`
  - SHA-256: `204a7aac78177824219954574f67fcaf4c56ac81620d533ecb376030340c93ee`
- Owner-instructions source:
  `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-vw-m4-owner-scanner-delivery-payload-owner-film-differences.md`
  - SHA-256: `969fe3034ca1e7b7aab061ff16575fe7f7d973d9c9ec1f81c347464c4d9da220`

Both sources were regular, non-symlink files. The retained stage initially had
10 files: README, four bundles, four patches, and SHA256SUMS.

## Existing four-repo proof, preserved exactly

The prior central run was `runtime-delivery-dryrun-1021004301-18070`, exit 0,
99 seconds. Its source tuple and tree results were:

| repo | integration commit | integration tree | patch tree | bundle tree | applied tree |
|---|---|---|---|---|---|
| Agent | `57d6635616f2982b814cfcc059b670ea1a7c9f2c` | `0174fd49bd175a726a44542d1d6e31bca13c0f02` | `0174fd49bd17` | `0174fd49bd17` | `0174fd49bd17` |
| Runtime | `9d1c43c647301da48a6e86ad82e466b501bd2418` | `50e74e3243c5da4cf77b6e6cc76605fae8aeb649` | `50e74e3243c5` | `50e74e3243c5` | `50e74e3243c5` |
| App | `780c502368cb6eb379cf3848af7009067c7cd744` | `8eed52bb7f8555c7765a8b485e00920bbf906639` | `8eed52bb7f85` | `8eed52bb7f85` | `8eed52bb7f85` |
| Composition | `e7ef7a0729a2d7dad3c0ae60da9e6bb8f844d332` | `408633d6b73dde63f683eaf9d13a132bb34a3bd7` | `408633d6b73d` | `408633d6b73d` | `408633d6b73d` |

## Private-stage insertion proof

The retained stage was copied to a private temporary directory. Only the
reviewed helper's existing functions were used for insertion and checksum
generation, in this order:

```python
delivery_build.add_extras(private_stage, [
    "extras/owner_film_cliplook_scan-v1.0.8.zip="
    "/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/"
    "handoff-vw-m4-owner-scanner-delivery-payload-scanner-v1.0.8.zip",
    "extras/owner-film-differences.md="
    "/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/"
    "handoff-vw-m4-owner-scanner-delivery-payload-owner-film-differences.md",
])
delivery_build.write_checksums(private_stage)
```

Results:

- 10 files before; 12 staged members after.
- The eight bundle/patch hashes and README hash were unchanged:

  ```text
  48253d03178fa7338b993e01f3ec08d9d82a066929becdd6c794b4aa25699822  README.md
  6c0cb863e7a43398c23da883fba4b80d43accc85c520fcc29b37e45537e56309  bundles/agent.bundle
  62b48f12bb26d77a8a456d023616e06d87080ce106f7dcfebde868bd508c5373  bundles/app.bundle
  031ab6e4463aadf904bfdf44853b8b9ca6da7a42385489970a3e692ba8ab5041  bundles/composition.bundle
  e555600570311a14d217a36c6a90b629f1c61be4f04b2c5d54131944bd429d93  bundles/runtime.bundle
  ee9e3aac912a3546dac56c24c3a138f55430b2dd1526e6a9cbb9bb4c25f6e2b4  patches/agent/0001-Squash-tl-integration-of-agent-onto-origin-main.patch
  37168b1cf76da5f58094824c733fd0e86ac48f4663bef584dc795dd32f09364d  patches/app/0001-Squash-tl-integration-of-app-onto-origin-main.patch
  1e26cd36400b8df07c9bca2c25d099e8bc1c8ee449690c5efb4f13b7dcad3788  patches/composition/0001-Squash-tl-integration-of-composition-onto-origin-mai.patch
  2e8ecb746eb4d2587ce56a570b72630b01bcfc64b83d5077bba3169e6a04649c  patches/runtime/0001-Squash-tl-integration-of-runtime-onto-origin-main.patch
  ```

- Both extras were byte-exact and retained their frozen hashes:

  ```text
  204a7aac78177824219954574f67fcaf4c56ac81620d533ecb376030340c93ee  extras/owner_film_cliplook_scan-v1.0.8.zip
  969fe3034ca1e7b7aab061ff16575fe7f7d973d9c9ec1f81c347464c4d9da220  extras/owner-film-differences.md
  ```

- Normal checksum generation covered all 11 non-self members; including the
  `SHA256SUMS` file itself, the stage has 12 total members. The generated
  SHA256SUMS hash on the private proof copy was
  `21360592f3eaf1d68656d65ad203c96569c20bfe616598002634b602fededbfe`.
- The private copy was removed after verification. The retained shared stage
  was not modified.

## Fixed future test-service suite

Added exactly one allow-listed suite line, without changing existing suite
lines:

- Suite: `runtime delivery-owner-extras-actual`
- It uses the installed helper SHA above and contains both literal `--extra`
  arguments in the command before any future `request-test` submission.
- It is an actual delivery command (no `--dry-run`); it has not been
  submitted in this task.

The fixed command is:

```bash
env GIT_CONFIG_GLOBAL=/dev/null PYTHONDONTWRITEBYTECODE=1 \
TIMELINE_DELIVERY_SCRIPT_SHA=3dfd5c28a9be9ab809e6c1fe1e9a83fbf8417ea888afc1b10eec5f751023e990 \
python3 /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/delivery-build \
  --repos "agent runtime app composition" \
  --extra "extras/owner_film_cliplook_scan-v1.0.8.zip=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-vw-m4-owner-scanner-delivery-payload-scanner-v1.0.8.zip" \
  --extra "extras/owner-film-differences.md=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-vw-m4-owner-scanner-delivery-payload-owner-film-differences.md"
```

## Limits

No new packaging API or framework was added. No sourceGit ref or retained
stage was mutated. No duplicate four-repo build, full suite, browser/render
run, final ZIP, owner-data/owner-film scan, macOS check, physical parity check,
or full Gate7 claim was made. The future actual suite remains unverified until
the orchestrator deliberately submits it.
