**APPROVE** the corrected delivery tool for the script and source tuple below. The originally supplied script is **REJECTED** by independent fixtures; two bounded tooling corrections were necessary. Product code was not reviewed or changed.

Script SHA256: cee29952d65b306414c9c5492b6be594a5b47d8a091f307bbb525bc42a4db81e.

Original SHA256: 68425da746cb407e392b7baa9f38a0ddd97e2abdf9e1f02bd737b9ef63f6dcc4.

| Repo | Pinned origin/main | Pinned tl/integration / exported bundle tip | Matching patch, bundle and integration tree | Result |
|---|---|---|---|---|
| agent | 96b283d5d6fd8031538f881e486bb2ebf45dce75 | cf7448ed6c1298b172d004914cfe2bb8c99048e7 | c8a5e0cb320095129e9a1be125295dfa7adc2793 | PASS |
| runtime | 29d0954b6d78a7d7937d81bc36567b6dee7ca976 | 2c4ac180c2220bdad966bc01e95ad230e99ce26a | 7ab412cc4bcbe517efcfa806e092336390312e18 | PASS |
| app | 44f0b9ca9d0247d909f86f56955a04ef6c18a2aa | 6ff21cac9deee3aae014e5c9e65d9871a3452f77 | 27d41c1b0e64ff9028f78576804f3b8cb3b9f1d5 | PASS |
| composition | 67b8aa3d0d6831d3e3504a340ff583c3da253707 | e80c46baf5aa4b50a10b77a5ceadcb7ec4ab27ab | 23a994070b8e25aba18703af1c6a0c840df1ab62 | PASS |

Source heads were identical before and after the service run. Every exported bundle advertised exactly its reported pinned integration commit. Artifact checksums matched. App was the actual shallow source, not a fixture replacement.

Two defects and the bounded repair:

- The original tool reported a pinned tip but still read the moving branch for line counts, bundle creation and expected tree. A private fixture moved the branch to a different commit with the same tree, even restoring it after bundle creation: the original tool returned PASS for the wrong exported commit. Counts and expected tree now use the pinned tip; verification requires the fetched bundle commit to equal that exact tip and rechecks both source refs before returning a repo result. Mismatches produce FAIL. The bundle still comes from the source's original integration ref; no source refs are written.
- The depth-1 main fetch dropped real ancestors needed by ranged bundles from merge histories. The older design document's depth-1 verification assumption is insufficient. The private verifier now fetches the pinned base with its source ancestry, accepting existing source shallow boundaries through --update-shallow. It does not create a new depth-1 boundary. The separate squash fetch retains the existing ahead + 1 bound. No prerequisite is removed or fabricated.

Fresh-main verification remains real: a new initialized repo fetches the immutable base into local main, checks it out, verifies and fetches the original ranged bundle, applies the emitted binary patch using ordinary git am, and compares both trees against the immutable integration tip. Full/unrelated bundles still verify in an empty repository. No replace refs or graft files exist in the four sources. Every listed prerequisite was independently confirmed to be a real ancestor of its pinned main. Agent, Runtime and App bundles each genuinely require both their original main baseline and current main; Composition requires current main. These requirements were retained and passed verification.

Results:

- PYTHONDONTWRITEBYTECODE=1 python3 /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-m4-delivery-ref-fix-final-review/test_delivery_final.py: **11 passed**, 10.133 seconds. Covers binary/rename/delete, merge prerequisites, shallow source, unrelated standalone bundle, transient same-tree wrong bundle commit, base movement, late tip movement, corrupt patch, wrong bundle tree, byte-identical source Git directory and wrong script hash refusal. Private main ancestry must exactly match source base ancestry. An empty repo must reject a ranged bundle.
- Against the preserved original script, the merge-prerequisite and transient same-tree identity regression tests both failed as expected. The original reproducer returned PASS while reporting and exporting different tip SHAs. Evidence: /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-m4-delivery-ref-fix-final-review/original-regressions.log and original-ref-race.json.
- Syntax compilation of the final script using Python compile(..., 'exec'): **PASS**, no cache file.
- Appended one new runtime delivery-final-ref-integration suite, without editing existing lines. Exact service command:

~~~sh
env TIMELINE_DELIVERY_SCRIPT_SHA=cee29952d65b306414c9c5492b6be594a5b47d8a091f307bbb525bc42a4db81e python3 /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/delivery-build --dry-run --repos "agent runtime app composition"
~~~

Requested exactly once with /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/request-test integration:runtime delivery-final-ref-integration. Central result runtime-delivery-final-ref-integration-1020114303-31023: **PASS**, exit 0, 121 seconds, actual execution rather than cache reuse. Agent 28s, Runtime 4s, App 87s, Composition 1s; one patch each; all patch/bundle/pinned trees equal. Final /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/wait-test runtime-delivery-final-ref-integration-1020114303-31023 0 exited 0. Earlier waits exited 124 while the same run was still active; no resubmission occurred. Script hash was checked before registration and after the result and was unchanged.

Central log: /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/tests/runtime-delivery-final-ref-integration-1020114303-31023/log.txt.

Full artifact README, checksum manifest, bundle headers, source identities and ancestry audit are retained in /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-m4-delivery-ref-fix-final-review/. The 14.5 MiB dry-run staging directory was removed after inspection; temporary verifier repos were removed by the tool.

No blocker remains for this delivery-tool repair. No full suite, ZIP creation, publication, product gate qualification, owner-film viewing, or remote-main freshness check was performed. Here current main means the explicit local origin/main identities above; there was no fetch from any external remote. All fetches were from local source repositories or generated bundles. Shared dependencies and caches were untouched; the assigned runtime worktree remains clean. The test service alone managed its standard runtime snapshot.

Recommended next step: the orchestrator may use this corrected script for the next authorized delivery build after the other M4 gates are satisfied. Approval does not transfer to a changed script or source tuple; requalify those through the service when authorized. The earlier failed central30446 run is not final verification.
