# tf-zip-dryrun-1905: report

One bounded, test-only patch-export dry run. No push, no integration or ref write, no live `ORCH/delivery` or kit write, no ZIP, no delivery claim, no build/render/gate. Result: the four squash patches were exported and apply-check cleanly, but **they are not safe to package**. Each one encodes reverts of upstream work for Agent, Runtime and App (details in section 4).

## 1. Before identity (captured once, read-only)

| Checkout | HEAD | Tree | Clean |
|---|---|---|---|
| integration `/home/user/work/agent` | `a30e74e901a28b39c28facba3deb00d76f186e23` | `ece8e0887e48…` | yes |
| integration `/home/user/work/runtime` | `e319fdbcd512bd5fc9bc5b2c43abfa4d749c34d9` | `d5cb9335a03b…` | yes |
| integration `/home/user/work/app` | `d5a1d1ab6550187e377fd7387d300102b8b82ece` | `7be73e2cbbcf…` | yes |
| integration `/home/user/work/composition` | `635f4de06fda22a85fc2e4cfc764d0153a4c9f40` | `5ab5191a2969…` | yes |
| pin `wt/agt-pin-547e1045` (detached) | `547e10456250c1b5bcf63b44a50c90ff0563ce1e` | `68df11fad2b0…` | yes |
| pin `wt/rt-pin-e319fdbc` (detached) | `e319fdbcd512bd5fc9bc5b2c43abfa4d749c34d9` | `d5cb9335a03b…` | yes |
| pin `wt/app-pin-d5a1d1ab` (detached) | `d5a1d1ab6550187e377fd7387d300102b8b82ece` | `7be73e2cbbcf…` | yes |
| pin `wt/vw-pin-635f4de0` (detached) | `635f4de06fda22a85fc2e4cfc764d0153a4c9f40` | `5ab5191a2969…` | yes |

Upstream objects all exist in the farm repos (`cat-file -t` = commit): Runtime `dbcdb97c50`, Agent `886a3183bd`, App `213318f1ec`, Composition `origin/main` = `67b8aa3d0d`. All four `origin/main` refs equal the upstream SHAs.

**Mismatch:** `tl/integration` in `/home/user/work/agent` is `a30e74e9`, not the pinned `547e1045`. The other three `tl/integration` refs match their pins. Agent's pin and tip are not ancestors of each other (merge-base `070dfc5e`).

## 2. How the export ran, and why not bare

The installed `ORCH/bin/delivery-build` cannot run here as-is:
- `DELIVERY` is hard-coded to `ORCH/delivery`, and `--dry-run` still creates `build-<stamp>` there. That path does not exist now, so the script would create it.
- No private-root option; `WORK` is `/home/user/work`, and its agent tip comes from `tl/integration` (`a30e74e9`), not the pin.
- The README template it requires (`ORCH/delivery/README.template.md`) is absent.

So I loaded the **installed file unchanged**, read-only (`SourceFileLoader`, bytecode writing off), via `dryrun/run-dryrun.py`. It redirects `DELIVERY`, `TEMPLATE`, `GATE_RESULTS` and `WORK` to private paths in memory, and sets its own SHA check to the installed hash `f25dfab13bbfb090bf26cf97a85e59bd4818859f5b974dac94aae7e6f2272708`. Agent is exported from a private bare `--shared` view whose refs are pinned to `886a3183` (origin/main) and `547e1045` (tl/integration). The farm refs are untouched. The D68 wrapper (`scripts/delivery_gate_build.py`, another worker's worktree) was not used.

## 3. Results

Dry-run verifier (the script's own `git am` on origin/main plus bundle check): **PASS for all four**. Applied tree = bundle tree = pinned integration tree for each repo.

Apply check against a fresh clone of current upstream main (`apply --cached --check`, index loaded from upstream main, equivalent to a working-tree check for an unchanged main):

| Repo | Patch sha256 | Bytes | Patch files (deleted) | Apply check |
|---|---|---|---|---|
| agent | `1ffd36dce1a03a6d733be7b9934e64d299fec9c19651f1676ab6599c747fcc61` | 12,789,085 | 977 (43) | applies, rc 0 |
| runtime | `de8e76eb6fea38691ecfe1ae7dcd70eb49b47b3e5e19f64e5af45e2cea51b861` | 15,177,343 | 342 (7) | applies, rc 0 |
| app | `e36f42a765006dccb47da3a09bada6ee3b743937044743f01a0068f66f3b7c90` | 10,667,149 | 701 (42) | applies, rc 0 |
| composition | `cb14e7c81da56ba434ab675daef76d9015861fca29c7a3e2a2469be7e1514e4f` | 507,922 | 118 (2) | applies, rc 0 |

No apply conflicts. Applying to current main is trivially clean, because main equals each patch's base.

## 4. Erasure risk (the finding that matters)

Upstream main has commits that integration lacks, and the base is not an ancestor of the integration tip:

| Repo | Upstream-only commits | Upstream-only files | Patch files also upstream-only |
|---|---|---|---|
| agent | 22 | 98 (+2724/-668 since merge-base) | **98 of 98** |
| runtime | 16 | 29 (+1048/-21) | **29 of 29** |
| app | 68 | 154 (+6890/-1089) | **154 of 154** |
| composition | 0 (linear) | 0 | 0 |

The squash patch is base→integration. Where integration lacks upstream work, the patch reverts or overwrites it. `git apply --check` passes because the preimage is current main. This is the silent new-main-to-old-tree deletion the brief asked me to rule out. I did not split reverts from overwrites, and I did not resolve it.

**Recommendation:** do not package these patches. Merge forward from current upstream main into `tl/integration` for Agent, Runtime and App first, so upstream main is an ancestor of the tip. Then the squash is a real delta. This needs an orchestrator decision; Composition is not affected.

## 5. Disk and identity

- Before: about 11 GiB free (`df -BG`, rounded). After: 9.66 GiB (`statvfs`). Floor 6.0 GiB held. Peak not sampled during the run.
- Staging: `dryrun/delivery/build-20261025T190713Z`, **1117.1 MiB**, mostly two full bundles (agent 307 MiB, app 768 MiB). That is over the 50 MB worker-folder limit. I did not delete it: there is no approved delete route here and the rules forbid `rm -rf`. It should be removed by the manager or an approved step.
- After identity: all eight checkouts equal their before values; every `tl/integration` and `origin/main` ref is unchanged.

## 6. Refusals and deviations (exact)

- `echo $ORCH`: refused (variable in command).
- `printenv TMPDIR`: needed approval (not run).
- `ls /tmp/w-195a7c12e9`: blocked (outside allowed dirs).
- `mkdir -p /tmp/w-195a7c12e9/dryrun/...`: needed approval (not run). I used the worker folder instead.
- `mkdir -p <worker>/tmpdir/...`: failed (`tmpdir` is a file pointing at `/tmp/w-195a7c12e9`).
- Write of `agent-view/.git/objects/info/alternates`: refused ("sensitive file"). I used `git clone --bare --shared` instead, which writes the alternates itself.
- Missing live `ORCH/delivery` and README template: noted above; a labelled stand-in template was used for the README only.

## 7. Evidence (worker folder, `evidence/`)

- `report.md` (this file)
- `commands.md`, sha256 `156d1d829b223cfa87fbb3c616e3d53c81b1669c2492db3c1261aff9e267b29e`
- `manifest.json`
- `patch-apply.json`, sha256 `2c39fc153ec583e2cbf1c11383a68bf1d87fe6e15c3016ee76a966f8aad5db58`
- `validation.md`
- `identity-before.json`, sha256 `05a5dec3fceaf419fb824b91c2581e6a37c10971f2b0b186026ebc6d798e3a35`
- `identity-after.json`, sha256 `0f52c324a1f8446af3ffab966672e5df224e1e990db6fc35e2358c4af44580e1`

Runner scripts: `dryrun/run-dryrun.py`, `dryrun/applycheck.py`, `dryrun/identity.py`, `dryrun/README.template.md` (all in the worker folder).

## 8. Not verified

- No later-main test: the check only compares against current main, which equals the base.
- No semantic review of patch contents.
- No test, lint, build or gate was run (none needed: no code changed).
- The revert/overwrite split inside the 281 overlapping files is unmeasured.

## 9. Next steps

1. Orchestrator decision: merge forward from current upstream main into the Agent, Runtime and App integration branches, then re-run this dry run.
2. Remove the 1.1 GiB staging from the worker folder via an approved step.
3. Resolve Agent's `tl/integration` (`a30e74e9`) versus the pinned `547e1045` before any future pin.
