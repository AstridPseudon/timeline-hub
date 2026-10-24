**PASS — five exact scenarios at the mandated base. PASS — production final save funnel, by source review.** Neither verdict relabels the five units as C0 end-to-end proof.

Reviewed Agent `2007cf7aaf5d304964e68a33e967502a16de1d24` / tree `68b0309c`, Runtime `1d9ddba546f8fb1300f55ff62607ed492719cbaa`, PLAN, author0540, reviews0544/0548, return0547 and peer0553.

The retained [JUnit]( /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-F-CLI-remainder-0540/evidence/cli-five-baseline.xml) names all five passing selectors: **5 passed in 6.30s; zero errors, failures or skips**. Reviewed command, not rerun:

```bash
PYTHONDONTWRITEBYTECODE=1 \
PYTHONPATH=.:/home/user/work/runtime:/home/user/work/runtime/packages/python \
ASTRID_RUNTIME_CHECKOUT=/home/user/work/runtime \
/home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider \
tests/packs/timeline/test_cli_assets.py::test_edit_replace_asset_and_swap_asset_forward_to_the_sdk \
tests/packs/timeline/test_cli_voice_bindings.py::test_repeated_gap_flags_and_script_gap_override_preserve_sdk_rules \
tests/packs/timeline/test_cli_voice_bindings.py::test_replace_insert_and_from_script_forward_existing_sdk_arguments \
tests/packs/timeline/test_cli_edit_flags.py::test_edit_nudge_frames_set_and_close_gap \
tests/packs/timeline/test_cli_edit_flags.py::test_voice_line_swap_reflows_and_reports \
--junitxml=<author0540-evidence>/cli-five-baseline.xml
```

No author0540 or current-review weakening occurred: retained pre/post source/body/AST identities match, and current whole-file SHA256 values match that evidence. Import-origin paths also match pre/post.

The preserved assertions cover exact asset arguments/order/replacement output; voice replace/insert/script arguments; script-before-gap ordering and `0.2`/`0.4` gaps; frame nudge, canvas conversion and reload; and line words plus candidate-export guidance. Three tests intentionally mock SDK collaborators; two intentionally use `--file`.

This is **not frozen-R4 byte identity**: existing pre-base G5 changes translated two navigation assertions and the `--takes` representation. Agent must retain those mappings when deciding original credit.

The final save trace is:

- `_cmd_edit` (`cli.py:3185–3258`) falls back to `_edit_checkout`/`Checkout.load`, applies edits, calls `Checkout.save`, then prints complete-candidate export and check/commit commands.
- `Checkout.save` (`checkout.py:156–240`) persists local files/history. Its pending-sheet exception uses `NativeSheet.apply → TimelineSession.commit_many`, also the commit funnel.
- The **actually printed caller**, `timeline_document.main` (`timeline_document.py:253–333`), opens the pinned session, calls `emit_document_publish_commands → emit_document_commands`, then `session.commit_many`.
- Mounted `timelines commit --file` uses `_cmd_commit → commit_document → _preview_detached_document → Timeline.commit → _capture_free_edits → emit_document_commands → session.submit`.
- Connected sheet `apply` similarly reaches `NativeSheet.apply → commit_many`.
- All converge on `TimelineSession._flush → client.timelines.commit → WorkspaceClient.commit_timeline → generated.commit_timeline`, issuing **POST `/v1/projects/{project}/timelines/{timeline}/commit` with `Idempotency-Key`**.
- Runtime `server._timeline_commit` (`server.py:294`, mounted at `:522`) calls `service.commit_timeline` (`service.py:2433`) and the existing commit coordinator/store.
- `Checkout.publish` also uses emitter/session submission; restructure and narration follow-ups use that boundary. Runtime’s old `publish_parent_composition` directly refuses (`service.py:2783`).

Relevant Agent blobs include CLI `257ba096`, printed script `0984594f`, emitter `1d0498ff`, session `1d3692b6`, and publish `54ae6410`, all at the stated Agent commit.

**Correction:** reviews0544/0547/0548 stopped before the final publication boundary. Their immediate-unit C0 limitation remains valid; the inference that these families lack a production C0 continuation is unsupported and is explicitly withdrawn. Local staging alone establishes no second Runtime writer. No product correction owner is justified.

Production retains scope/base pins, labels/steps, conservative atomic patch handling, immutable retries, receipt/actor/request-hash checks and structured refusals. Optional request metadata need not appear in every unit; full C0 acceptance remains a production-path requirement.

No tests, probes or live calls were run. `diff -u` on retained identities and `git diff --check` passed; worktree is clean. Prior Ruff/mypy evidence has two existing errors each, not green checks.

No blockers. Agent retains count ownership; **201/66 remains unchanged** pending exact original-credit mapping. Operation-specific end-to-end publication and every reply variant remain unverified here. Prior reports are untouched; commit message and `DONE` were created.