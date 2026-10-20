# Parent automatic completion: independent review

**Verdict: APPROVE bounded.** No blocking implementation defect found in this private parent-completion follow-up. This approves neither public schema/client adoption nor automatic production/App cutover.

Reviewed immutable Agent commit **0937d6fd867c13ec55691966a830a708fdd3b0d3**, tree **6c44598437dc4b05197fc72d0c37155358435d1b**, whose direct parent is **537c2ecd28f92b391c79e383e0e045fd71b3258f**. The review worktree itself starts at another integration commit; every execution below used an archive of the reviewed commit, never that newer working tree. Runtime was privately archived from **2c4ac180c2220bdad966bc01e95ad230e99ce26a** and normally generated from the complete reviewed Agent schema. PLAN.md, the absolute parent-completion design, and the implementation worker report were read first. No product source, integration worktree, shared dependencies, or git state was changed.

## Findings

- The complete schema is byte-identical to the parent: SHA256 **8a55a9fd84d6fc188e48f63976dacc1c27ea25c7747ea88e7eba7589974dd85a**, **54 definitions / 28 operations**. Public `runtime.lock.json` and `artifacts.json` are also byte-identical. No new operation, wire argument, policy DTO, journal, coordinator, or whole-parent replacement was introduced.
- The two original positive functions (four parametrized cases) are AST-identical after excluding decorators. Their only test-file changes remove two strict xfail markers and their restoration comments. I also executed the original parent-version file, with those markers retained, using `--runxfail`: **4 passed, 81 deselected**. The worker's retained pre-removal log reports the same checkpoint; my reconstruction independently verifies the unchanged expectations against the committed implementation.
- `native_auto_placement.py:154` resolves parent policy once into ordinary `clip.add-media` v1, with exactly `{row, media}`. The builder requires explicit parent ownership, an explicit track input and a caller-provided raw clip ID. The selected existing parent lane is validated by the ordinary birth, including visual/active/output status and occurrence-lane exclusion. No owner or latest lane is inferred.
- Present anchor uses its end and saved preferred lane; absent anchor uses the saved fallback lane/time; only absent saved time consults lane extent. Empty, boolean and deleted selected saved lanes refuse. Saved fallback reads no unrelated extent. Lane-end reads each parent's clip track, plus timing of clips on the selected lane, so other-lane timing changes rebase while movement into the selected lane refuses.
- The provisional query recorder is not accepted as authority. `native_parent_media_commands.py:41` independently observes each permitted supplemental read with `ctx.read` in the same recorder as birth. Required fps, source-window, target-track, occurrence-lane, registry, collection-order/membership and collision guards remain those of the existing handler. Supplemental fields are restricted to existing raw parent clips and `at/at_ms/track/hold/from/to/speed`. My probes verify each anchor timing field appears in both the submitted command and the actual record; unsupported scope/path, absent/born identity and unknown policy keys refuse.
- `commands.py` verifies original claims before calling the handler and compares its complete capture afterward. `commit.py` executes against the immutable base and rebases the original plan; it never invokes the automatic builder on the latest head. My stale-anchor/extent probes confirm an explicitly rebuilt new capture differs while original replay refuses, with original command/record/head unchanged. Caller-supplied snapshots cannot freshen the original guards.
- Completion image is always five seconds, including supplied duration; video defaults to five seconds, or uses explicit completed duration, with source window `0..duration`, speed 1 and verified-media bounds. It does not silently use the full media length. Existing refusal for default placement of a video shorter than five seconds remains; explicit supported duration succeeds. Parent source windows remain unsupported and guarded. These are the stated bounded policies, not new broad legacy timing compatibility claims.
- `_end_frame`, `_kind`, `_birth`, `auto_place_shared` and `unplace_shared` are AST-identical to the parent. The occurrence completion body is unchanged after the parent dispatch/new parent-only keyword guard. Occurrence goldens and timing/fallback/read tests pass; shared four-second extent, collision and pool tests pass. Read-only comparison with App `origin/main` **17e46de99b7cef52fe494de1703a9865a8d4be24** confirms anchor/preferred versus missing-anchor/saved-fallback precedence and image-five/video-explicit-or-five insertion policy. No App source or public client was changed or qualified.
- The exact completed five-field selection reaches ordinary Runtime media verification and registry binding. Real managed settlement tests pass even after newer-primary promotion. IDs are created/reserved once: real reload/reopen retry avoids semantic execution; undo restores the disjoint head; reusing the retired ID refuses; redo restores exact state. My additional occupied-ID probe also refuses.

The optional extra read constraints are deliberately not proof that a command originated in an approved producer. Removing them or rebuilding a literal row is another request. Automatic adoption still needs durable requester approval binding the original owner, immutable basis, saved policy, reserved ID, exact pin and exact request bytes. This review does not authorize anonymous old-task recovery or silent conflict recapture.

## Independent execution evidence

All commands used reviewer-owned source archives/overlays and read-only shared Python dependencies; pytest caches and bytecode writes were disabled. No sockets/browser, full/full* suite, or test-service full request was used.

| Execution | Result |
| --- | --- |
| Six targeted parent/occurrence/shared/schema files, exact commands in notes report | **620 passed**, 181.82 s, exit 0 |
| Normally generated private Runtime pair: new completion file plus pristine S3 composition journey | **15 passed**, 29.86 s, exit 0 |
| Own adversarial read/policy/guard/owner/source-window/ID/default probes | **24 passed**, 1.59 s, exit 0 |
| Original parent-version four positives with retained markers and `--runxfail` | **4 passed / 81 deselected**, 0.94 s, exit 0 |
| Normal Runtime generation, generation check, artifact manifest generation/check | All four exit 0 |
| Touched-file Ruff; candidate-versus-parent `git diff --check` | Both exit 0 |

The 15-case service run includes the final six image/video stale move, hold and target-lane-label controls. They require no provider acceptance, zero mutating SQL statements, identical SQL dump/head, and an unchanged **nonempty** CAS/staging/snapshot file-byte map. No synthetic accepted history, SQL write, patched embedded schema, baseline publisher or renderer supplies the success path. Native managed-output fixtures contain synthetic media bytes; this proves custody/selection and edit persistence, not decodability or render output. Owner-lane exclusion and lane kind/deletion/extent/membership changes are covered by conformance fixtures and my probes; the real stale lane authoring uses the existing `track.set(label)` command. Do not claim all those hypothetical lane edits have a public operation/service journey.

The normally generated Runtime bundle embeds the complete identical Agent schema. Its SHA256 is **a694f3caf7efcc7c39fa4083742c845761eba9d254f9d2f85e4bb9f5f83a0013**. All **11** changed Runtime input/generated/manifest files and hashes exactly match the implementation worker's recorded private pair. External reviewer pytest collection reports one harmless unknown-integration-marker warning in each external probe run; no test was skipped, disabled or weakened.

## Remaining release gaps and next action

1. Manager-controlled integration/revalidation against the actual intended tuple; this verdict names the candidate commit above, not the newer review-worktree head.
2. Existing S3/public review/adoption holds: released Runtime/Agent generated contract/client pairing and public route/transport qualification remain open.
3. Real App requester submission/outbox/lost-ack/restart/conflict handling and the registered automatic producer-attempt admission/approval chain remain unqualified. Bind the original request and require explicit approval for recapture; no implicit owner or anonymous coordinator.
4. Browser/HTTP, renderer-off public journey, pixels/audio, owner films and macOS were not run here. Synthetic media/private overlays are not a public App or render cut.
5. Full repository/make-check suites were intentionally not requested under this brief. Selected-track whole-row conservatism and existing short-video default refusal remain disclosed limitations, not newly solved requirements.

Recommended action: accept this bounded follow-up for the manager's controlled integration step; keep every release/adoption hold until its separate qualification. No blocker and no decision deviation arose.

Exact commands, logs, probe source and source hashes: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-review-parent-auto-current/notes/report.md`.
