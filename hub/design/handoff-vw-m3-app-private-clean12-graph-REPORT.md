# Private clean12 App dependency graph preflight

**BLOCKED. No READY graph, private import root, source copy, or new qualification fingerprint exists.**

Full physical traversal of `/home/user/work/app/node_modules` found **152 self-targeting package symlinks**. Five are covered by the six exact authorized exclusions; the sixth authorized exclusion is Composition/package, pointing to another worker overlay. **147 self-targeting links remain** after the allowed exclusions. Examples: `@vitest/spy/spy`, `@babel/runtime/runtime`, `@rollup/rollup-linux-x64-gnu/rollup-linux-x64-gnu`. Retaining those absolute links violates the required no external borrowed paths/cycles condition; removing them exceeds the explicit ONLY-six rule. No broader private-copy cleanup was inferred.

The earlier audit's “full package graph” is the old controller's **11 named packages**, not the full physical dependency tree. Its filtered `215e32c6fc86ba57ad36f766a273e43b8c9d328341308fafcda752b03e9eb858` is reproduced exactly. It cannot certify packages outside that set. The full source inventory records 35,618 entries, 193 links, and 447,800,429 regular-file bytes. Pre/post inventories match exactly. Source inventory SHA256 `6eaabbcd0344b935057b981ce6a9a565f12fa7235d4ed83aa4ac9cf439dfb9c4` includes path/kind/mode/file bytes and source inode metadata; it is a diagnostic of the shared source, **not a private graph qualification**.

Frozen inputs verified read-only:
- App `5117b9da2e17828ec0b3cfbcdf3ff4987dc77ab3`, tree `e7e282fc958942cea263566a66b2e72d21913e0e`; 5,798 tracked blobs / 295,053,441 bytes.
- Root manifest SHA256 `0c77703dab8eeb46e05fa7555bbaf5e9ea4fbef077b4759610049fe110894090`; lock SHA256 `310d447508a2f0c023176a3283724455cd5823b6ffe116177f8e30d541de82a0`. No overlay lock written or pins edited.
- Frozen Composition 0.0.12 tarball: 58,444 bytes, 77 regular members, SHA256 `0a7b61529099ce994f807c6d7b1078303a09e7c0219144cc4b07467977f0f1a3`; exact resolved path/version and declared SHA512 integrity match the frozen lock. Members hashed directly in memory, not extracted.
- All six public12 handoff peer manifest hashes and versions match; their filtered package tree hashes are recorded. This does not validate every installed package against registry tarballs or every lock integrity field.

Exact verification command:

```sh
python3 /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-vw-m3-app-private-clean12-graph-audit.py
```

Result: **exit 2, expected fail-closed BLOCKED**, after passing source pre/post equality, exact-six identity, all six old filtered package hashes, old selected-11 fingerprint, frozen tarball SHA256/77-member/lock SHA512 checks, and six peer manifest/version checks. `git status --short --branch` returned only `## tl/vw-m3-app-private-clean12-graph` (clean). No behaviour suite ran: no dependency tree was created, so private physical import assertions, Vitest, and Playwright listing cannot run against a qualified root. No browser, socket, grant, central request, installation, network, product edit, shared graph/cache write, or Git mutation performed.

Resource preflight: source allocation measured 534,405,120 bytes; frozen App blob bytes 295,053,441. A future single combined copy is estimated at 900,000,000 allocated bytes, under the own 1 GiB budget. Free after audit: 12,497,686,528 bytes; standing floor 10,737,418,240 bytes. No large allocation was started. Recheck free space before any future copy.

Artifacts (all flat):
- `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-vw-m3-app-private-clean12-graph-audit.py`: reproducible read-only preflight.
- `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-vw-m3-app-private-clean12-graph-REPORT.json`: checks, source identity, peer hashes, exact exclusions, resources.
- `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-vw-m3-app-private-clean12-graph-source-manifest.json`: complete source physical traversal, no symlink following.
- `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-vw-m3-app-private-clean12-graph-unexpected-self-links.json`: all 147 retained self-targeting links.
- `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-vw-m3-app-private-clean12-graph-package-versions.json`: all physical package.json records, not a claim of lock conformance.
- `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-vw-m3-app-private-clean12-graph-frozen12-members.json`: 77 frozen tar member hashes.
- `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-vw-m3-app-private-clean12-graph-README.md`: capability-port coordination; no provisional root may be used.

Next step for lead: supply a complete clean dependency source, or explicitly authorize a separately reviewed set of additional private-copy exclusions. Shared repair remains outside this worker's authorization. No current Runtime, pixel, audio, Player/export parity, or actual product qualification claim is made.
