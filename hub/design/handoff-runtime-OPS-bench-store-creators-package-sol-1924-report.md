# OPS-bench-store creator package1924

**SOURCE PASS for the exact new exported source packet. Combined FAIL / UNQUALIFIED / STOPPED. STOP1905 remains pending. Evidence only; no installation or product change. Independent review next.**

Deliverables are new flat files under `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-runtime-OPS-bench-store-creators-package-sol-1924-*`. No old packet was rewritten. Assigned Runtime and integration Runtime are unchanged at `2a9e347ff0e1df1dedff5ab7b59ddb27dfe3129d`; the worktree has no product diff to merge. Full C0v2 requests/replies, dry-run schemas and frozen34e are unchanged.

## Recovery and cause classification

Read PLAN, independent1921 report and flat handoff, complete1912 log, short worker report, full flat report, validation/receipt logs, artifact-summary and exact current exports. The1912 log contains the actual finalization statements at lines2090–2255 and final SHA256 output around2330. Replaying only those text edits recovers:

- Maker `d32ede5ff3de131c0fdc25395bdb3fe934b5bb8aa7f00d3d310f689eee38d5cc`, matching the1912 logged final hash and old manifest.
- Receipt fixture `97b5d9ab62485ade0f39ca85d12dcddc54240e676e62cdef09d7f54de0397cb7`, matching the1912 final hash output. The current old manifest instead lists `23338d5321723b42d2763863bd23f3becb2c846e9115acf741fbca209ddb4363`. No claim is made to recover that uncorroborated alternate digest.
- Validator `108c1958c4c23d935f48bf133181096f10b2e37c9e408cb37f21fe1384b37983`, matching the old manifest and logged hash. It still contains the unanchored extraction bug; this worker fixes that in the new copy.

Current exported1912 source hashes all match its durable artifact-summary, while four entries disagree with its manifest. That proves a mixed-version/stale export relative to the logged final edits; it does not establish which process restored or copied the earlier bytes. The prior PASS log describes a different byte set and is not validation of the failed exported packet. The final new packet has fresh validation below. Old1912 manifest is deliberately still FAIL (four entries), old1850 manifest still PASS (ten entries), and every old source file listed by1912 artifact-summary still matches it. The old manifest file itself differs from its artifact-summary digest as well; this inconsistency is preserved. No lost bytes were invented and no prior validation was promoted.

## Every source delta

Relative to current1912 export, maker recovery restores exactly the logged section-to-retained-marker checks, unique retained source snapshot check, `-B` for the retained interpreter, and the extractor-safe `source.split("\nIDENTITY_SCRIPT=" + "'", 1)` spelling. These changes are confined to the already reviewed wrapper/report verification; the complete builder and original custody verifier remain byte-identical to1850 and the terminal1839 verifier remains byte-identical. No report declaration, receipt authority, projection path, deletion authority, success condition or custody key was redesigned. Final maker equals the recovered1912 intended hash above.

Receipt fixture recovery restores the logged memory marker inputs, identity compile, legacy verified-reuse parser fixture, and exact maker failure flow (stub refuses before any child build/publication). Its dynamic filename PREFIX resolves all creator source reads to package1924; original1850 stays the intentional oldRED control. No production parser is reimplemented or weakened.

Validator recovers logged dry runs, compile coverage and old1850 comparisons, then changes extraction to a unique multiline regex anchored at each shell assignment (`^NAME='…'\nrun_stage`). It compiles every Python heredoc (Store, request verifier, Runtime registration/component/integrity/candidate checks and relocation), Runtime inline Python, original child verifier, provenance, distribution and identity Python, plus all three exported Python modules, in memory to avoid cache writes. It records/checks installed baseline hashes, runs explicit dryrun/replay/cmp for all four patches (including empty runtime requester patch), checks both Runtime trees, and verifies manifests again at completion. Combined fixture is compiled only.

Runtime maker, both requesters, combined adapter fixture and historical interface request remain byte-identical to current1912 export. Runtime maker/requester and combined fixture also remain byte-identical to1850. The child requester differs from1850 only by its previously reviewed `status=passed` marker after successful original verification. All four patches were regenerated from the actual installed files below after final source bytes were fixed. Only maker patch differs from1912; it now matches recovered maker bytes. Interface document remains an unchanged historical request, not an assertion about current core implementation.

Old/new SHA256 differences (all unchanged rows are in `old-new-comparison.json`):

| File | Current old1912 export | Final package1924 |
| --- | --- | --- |
| make-child-venv.sh | `f339a3f3db3c85bd7fb3c17f199ceeb3d09476f9906cff45cb663007eb0a48e6` | `d32ede5ff3de131c0fdc25395bdb3fe934b5bb8aa7f00d3d310f689eee38d5cc` |
| make-child-venv.patch | `dbda817c251cb2803702a9f709e217e6b301dde4355307c02007d23d84a9ca8f` | `4f453badd875e64851eda6cc0deff754d8ca4649feeaf20b5e14482494e4f8f9` |
| test-receipts.py | `943994484ec81f912e1caef5658627064ec20d2e8a159144fd6b753b3d5336a8` | `97b5d9ab62485ade0f39ca85d12dcddc54240e676e62cdef09d7f54de0397cb7` |
| validate-packet.py | `7c25a8d7b27c7166a7cb2578bb4997c5d9b6d9ded08ceccc1bd0c74a3d4d3718` | `926d4ecf7c9730698e2ce6f3e88d88b8bb32f8cd5e43e5bf3936c13bea16900d` |

## Exact installed baselines

These files were read, hashed and copied only into TMPDIR for patching. No actual installed file changed. Final validator checks their hashes both before and after replay.

| Installed file under ORCH/bin | SHA256 |
| --- | --- |
| make-child-venv | `39450feacd8ff7d566e19fd6ce0aadc5c02366db1bccd9c88f9cd3a3ceef614f` |
| request-child-venv | `f9e5ea6f2ff577ebd25218a1eba751e17fafd474b1e1a3a3adbb8524a80c440e` |
| make-runtime | `f63adc876ee489cc1bb3a9e038b31b2a432bb17557f566c84d93305c35dbccec` |
| request-runtime | `f13a1d073699712ccfb05e8463ad97ff69dc210a2617f2c9e0140a242591f7b1` |

Static caller inspection retains queue payload and dispatcher positional call → maker → `Store.ensure`; final fixture source reads target this final packet through PREFIX. Created/reused receipts pass the unchanged actual Proof grep commands from `handoff-ap2-P1-current-diagnostic-OPS-1813.md`, SHA256 `08b0e19abfcff0c8211f2bd1ba7ccba2411b1997c703a8fed9dae2c251db0d7e`. Full child Agent/backend/client tuple and Remotion tree-only identity are retained. This is source compatibility, not an executed production journey or authorization to install.

## Exact tests and results

From `/home/user/work/wt/rt-OPS-bench-store-creators-package-sol-1924`, with `TMPDIR=/tmp/w-fe279df0c7`:

```sh
python3 -I /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-runtime-OPS-bench-store-creators-package-sol-1924-validate-packet.py
python3 -I /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-runtime-OPS-bench-store-creators-package-sol-1924-test-receipts.py
```

Both exit0. Exact nested commands and outputs are retained in new flat `validate-packet-log.txt` and `test-receipts-log.txt`. Validator runs `bash -n` on all four exported shells; embedded Python compile; `patch --dry-run --batch`, `patch --batch`, and `cmp` for each of four actual-installed-input copies; all13 final manifest entries; all10 original1850 manifest entries; exact build/verifier/Runtime guard comparisons; `git status --porcelain` and `git diff --check` for assigned and integration Runtime. Both statuses empty and diff checks exit0. Receipt fixture passes created/reused and legacy oldRED/newGREEN, exact report declaration, failed/duplicated status, wrong tuple, malformed bytes, absent verified cache, mutated report, absent/changed projection, and refusal-without-success controls. It executes only extracted functions with memory inputs and a refusing Store stub, never actual Store.ensure child builds.

Source hashes for all13 final manifest entries are byte-identical before and after these checks; flat `source-hashes-log.txt` retains both lists. Hash manifest SHA256: `2916b09d06b14fcf347dab826b107f5fb871914df85fe86dd188e1dfec32fc6f`. `old-export-integrity-log.txt` retains the expected historical four-entry FAIL. `old-new-diff-log.txt` retains the complete source/patch/fixture delta. `caller-inspection-log.txt` retains the read-only source route and dispatcher/Proof hashes. Old/new comparison and baselines include full hashes.

## Limits and next step

No combined adapter run, child build, readonly publication/deletion, retry, chmod, alternate publication, HOST/test-service, full/gate body, network, live kit/config/queue/bench/provision/install, product/tests/generated/pin/Git mutation or cleanup was performed. No receipt/report authority change was made. Current core integration and actual production preflight acceptance remain unverified and STOP1905 remains pending. Evidence-only source PASS cannot qualify the combined behavior.

Scratch is below10MiB; durable packet plus worker records are below3MiB (exact final measurements in worker `limits.json`). Only reports/logs/small evidence are durable; recovery scripts and recovered intermediate files stay in harness TMPDIR. No tracked file was deleted. Next action: immediate independent Luna review of this exact unique flat packet. Resolve permission disposition and core/caller integration under their owners before any combined execution or installation.
