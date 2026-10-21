# Gate7 current-frontier delivery dry-run preflight

Date: 2026-10-21 UTC

## Result

**BLOCKED — STORAGE NEED 2.091911315918 GiB for current Gate7.**

The mandatory at-least-10-GiB free-space floor was not met. The final
read-only probe found `8,491,245,568` bytes free (`7.908088684082 GiB`),
against a floor of `10,737,418,240` bytes; the shortfall is `2,246,172,672`
bytes (`2.091911315918 GiB`). Per the Gate7 brief, no polling, copying,
central test-service request, or delivery dry run was made. No peer or
protected input was cleaned.

The prior `runtime-delivery-owner-extras-dryrun-1021040405-30942` PASS remains
historical for Agent `7ab6cbae`, Runtime `b92d3e7a`, App `1557`, and
Composition `7bb54bb`; it is not relabelled as current.

## Current source snapshot

The exact clean `tl/integration` sources observed before stopping were:

| repository | commit | tree | `origin/main` ancestry |
| --- | --- | --- | --- |
| Agent | `cc37291af12ac6504eb48dd71ea39b9dfdb56d71` | `0698a30b3eb42d47db84ed5ed2e21221158795c4` | PASS |
| Runtime | `b92d3e7a05eec65c142294ef4873edd059e9b31d` | `6abc2f117391de8e7e35c0283f575a002199894d` | PASS |
| App | `bc6f9dd39c7e5154ddf075cb87b7202cf5702e65` | `4cd13d09b7cffd60612d8521f1a2921ca4e762d2` | PASS |
| Composition | `7bb54bbd64107e5090643ecca1e4d33164173e85` | `20467712e66dbadff4d562c0d5baae22b8c077a7` | PASS |

All four worktrees were clean. `git rev-list --objects --missing=print`
reported no missing objects for each `origin/main..tl/integration` graph.
Agent current `cc37291a` descends the adopted `091aa23e`; App current
`bc6f9dd3` descends adopted `3be3c116`; Runtime current `b92d3e7a` descends
producer `95bd3c5f`.

## Immutable cohort and carrier checks

- Producer `95bd3c5f6d00e9bc8cc8cbe5ef510b68ed660f3c` exists and is an
  ancestor of Runtime `b92d3e7a`.
- Runtime `contract/artifacts.json` has all 76 entries; all 76 current blobs
  exist, match their manifest hashes, and are byte-equal to producer95's
  corresponding blobs. Manifest hash:
  `a902387c6a2315374f7e73511feea47da30191aba831b48820b3864b773a532d`.
- Ordinary `6ba7b51e9518e7fb08b27ad5b7225855276b657d0adebf704dd853f699768f2d`
  matches both Runtime `contract/schemas/edit-command.json` and Agent
  `astrid/core/timeline/schema/edit-command.schema.json`.
- The fixed C13 identity remains the documented Main95bd/Runtime95bd profile
  with pinned Node20. The retained Remotion0013 project, its `node_modules`,
  and the pinned Node executable exist; the historical
  `venv-agent-child-c13-a8a40afd` Python path is absent. No C13 execution was
  attempted or claimed.
- Reviewed builder:
  `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/delivery-build`
  SHA-256
  `3dfd5c28a9be9ab809e6c1fe1e9a83fbf8417ea888afc1b10eec5f751023e990`;
  `--dry-run` help and executable checks passed.
- Frozen scanner extra SHA-256:
  `204a7aac78177824219954574f67fcaf4c56ac81620d533ecb376030340c93ee`.
  Frozen owner-instructions extra SHA-256:
  `969fe3034ca1e7b7aab061ff16575fe7f7d973d9c9ec1f81c347464c4d9da220`.
  Both are existing regular non-symlink files.
- Delivery output directory and README template exist; no final
  `timeline-delivery-*.zip` exists. The named
  `delivery-owner-extras-dryrun` service entry and request/wait tools exist.

## Commands and results

- `git -C /home/user/work/{agent,runtime,app,composition} rev-parse ...`,
  `git status --porcelain`, `git merge-base --is-ancestor`: PASS for the
  snapshot above.
- `git rev-list --objects --missing=print origin/main..tl/integration`: PASS,
  no missing objects in all four repos.
- Read-only Python `git show` manifest verification: **76/76**, zero missing,
  zero hash mismatches, zero producer95-to-current listed-blob differences.
- SHA-256, `realpath`, regular-file/non-symlink, builder `--help`, output ZIP
  absence, and service-tool probes: PASS.
- `df -PB1 /home/user/work` plus `shutil.disk_usage`: **BLOCKED** at
  `8,491,245,568` bytes free; exact need `2,246,172,672` bytes /
  `2.091911315918 GiB` to reach the preserved floor.
- Central `delivery-owner-extras-dryrun`: **not requested** because the floor
  failed. No Runtime test suite, full suite, browser, renderer, install,
  final ZIP, owner scan, or film run was performed.

No Runtime product files were changed. The worktree remains clean.
