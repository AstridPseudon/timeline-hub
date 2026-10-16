# Transcript-editor trial merge and editor work: Astrid findings

Date: 2026-10-16. Source: a three-repo trial merge (Astrid, Runtime, App) on 15 Oct 2026, a CLI journey on the trial stack (Codex image, sprites, cut placement, render), and the editor efficiency work.
Re-verified against Astrid HEAD `8f0620ed`. Line numbers are at that commit.

## CLI defects

| # | Finding | Evidence | Fix direction |
|---|---|---|---|
| 1 | `--for` is silently ignored with `--add-cut`. In the trial, a 2.5 s sprite cut took the old picture's whole remainder (to 48.70 s) and re-pointed the spanning layers, so one clip stretched | `astrid/packs/timeline/cli.py:3346-3348` (`if parsed.add_cut:` ... `return`) precedes `--for` handling at `:3407-3408`. Only `--on` is required (`:3203-3205`) | Reject flags a verb ignores. The parser (`cli_parser.py:39-53`) only rejects unknown flags, not flags the handler drops. Or make `add_cut` accept a length |
| 2 | The unbounded default is undocumented: a split gives the new picture `old_end - t` ("a split never adds length", `astrid/sdk/timeline/edits.py` `_split_cut`). Not a bug alone, but dangerous for a short insert | `edits.py:116-205`; no user-facing doc found | Document it; warn when the remainder is long |
| 3 | `timelines show` defaults to the local working copy. After the published head moved (a restore, or another session's publish) it still printed the old copy under "WORKING COPY · 0 clips changed vs published <rev>", naming a revision that was no longer head | Banner `cli_show.py:157-159`. `base_revision` is the draft's own base (`cli_common.py:120-130`); nothing compares it to the head. Only `--published` shows the truth | Compare to the head and say "head moved to <rev>" |
| 4 | `timelines history` says "this Runtime cannot list earlier revisions" even when the Runtime lists them (50 items in the trial) | Message `cli_history.py:12-14`. `RuntimeRevisions.list` in `astrid/sdk/timeline/revisions.py` returns `None` when `head.parent is None`; the parent comes from the `open_composition` summary, which does not expose it. The vendored client has the list route (`banodoco_workspace_client/generated.py:847-851`) with no caller in `astrid/` | Use the composition-revisions list route |
| 5 | `--json` is accepted by `timelines checkout` and `publish` but not `edit` or `check` (argparse "unrecognized arguments", exit 2). Seen 15 Oct, not re-checked | | One shared flag set |
| 6 | Publishing an unchanged draft succeeds silently ("0 clips changed", new head). Seen 15 Oct, not re-checked | | Refuse or say so |
| 7 | `timelines check --at <t>` once exited 1 with a canonical-JSON recovery message and then printed a valid lint. Seen 15 Oct, not re-checked | | Exit code or error line is wrong |

## Unbounded and size-capped output

| # | Finding | Evidence |
|---|---|---|
| 8 | `runs list --json` defaults to everything and fails once a long-lived realm exceeds the 4 MiB canonical-JSON cap ("canonical JSON exceeds 4194304 bytes (7493675 bytes)"); it works only with `--limit`. The human view defaults to 50 | Default `astrid/core/cli/list_narrow.py:45-46` (`limit = 0 if as_json else 50`), help `domain_runs.py:187-189`; cap `astrid/core/receipts/canonical.py:24`, enforced `:131-156`. Fix: default `--json` to a page, with a cursor. The Runtime itself caps list pages at 200 |

## Generation and media

| # | Finding | Evidence |
|---|---|---|
| 9 | `execution: "codex"` still requires `model`, a field that does not select the image model. The documented 14 Oct snippet omits it and fails; callers pass a dummy such as `flux-dev` | `astrid/packs/generation/pack.yaml:684-692` (`model` `required: true`); `actions/generate_image/run.py:251-254`. `generate_image_codex/STAGE.md:4-9` says model/mode labels "do not select the actual image model". `docs/generation/30-image-contract.md:117-119` disagrees. Unchanged from origin/main |
| 10 | `media open run:<id>/generated_images#0 --materialize` returned `not_found: media object is not in the selected project` in an adopted realm, while `media list` worked and the file was on disk | Run-handle resolution `astrid/sdk/media_handles.py:56,122-133` calls `client.runs.show` and `list_managed_outputs` with no project argument, then the digest step is project-scoped (`:97-108`). Plain refs go through project-scoped `_find_project_object` (`astrid/sdk/media_open.py:89-104`). Whether handles survive adoption is unconfirmed |

## Renders and processes

| # | Finding | Evidence |
|---|---|---|
| 11 | Renders fail under machine load: "candidate reconciliation did not stabilize before its deadline" while two other heavy jobs ran; the same timeline rendered fine an hour earlier. The weight-3 heavy-job lease does not prevent it | Raised `astrid/core/execution/custody_broker.py:2793-2795`; deadline `_CANDIDATE_RECONCILIATION_SECONDS = 1.0` at `:2781` (min with any parent deadline, `:2784-2791`) |
| 12 | Orphaned local stacks: a Runtime started from a session died with it, and a generic host kept running against a dead endpoint. Runtime port changes per restart | Process-lifecycle work; no supervision |

## Contract and gates

| # | Finding | Evidence |
|---|---|---|
| 13 | The vendored Python workspace client is pinned by digest. A Runtime digest change (`4aa5215`) landed without the revendor, so the CLI failed its health check; true on the contributor's own branch too, so it was never run end to end. Fixed by revendor `283ceb40` and the pin update in `8f0620ed` | `tests/stage1/test_vendored_workspace_client_parity_luna.py:33-37` (`PINNED_SCHEMA_DIGEST`, `PINNED_GENERATED_SHA256`, `PINNED_METADATA_SHA256`), checked by `test_vendored_client_is_the_frozen_runtime_artifact` (`:45-53`). The pin only catches drift when the pin is bumped; nothing compares against the Runtime repo. Same copies live in the App (`generated.ts`) |
| 14 | Main is not green. Verified now: `scripts/gen_element_catalog.py --check` fails ("catalog.ts is stale"); `tests/test_canonical_aliases.py` has 3 failures (`test_orchestrator_api_uses_canonical_implementation`, `test_product_timeline_parser_exposes_only_the_ten_verbs`, `test_product_timeline_parser_has_no_obsolete_aliases`); the contributor's branch added 2 more forbidden verbs to it unnoticed. Seen 15 Oct, not re-run: 31 focused-test failures, 4 TSX failures. Known failures hide new regressions | `astrid/packs/rendering/elements/catalog.ts`; forbidden-verb list `tests/test_canonical_aliases.py:121-140`. Fix: regenerate the catalog; fix or retire the alias test; get a green baseline before merging branches |
| 15 | The App imports `@astrid/.../ui/transcript` from a pinned Astrid vendor; nothing checks that the imports resolve until vitest fails | See the App findings doc |

## Authoring model versus Runtime shot model

| # | Finding |
|---|---|
| 16 | The film is one opaque wrapper shot in the Runtime (one occurrence, 160 s, 0 parent clips; all 286 clips on 8 tracks inside the shot's internal timeline). The App draws one block; cuts, chapters and tracks are not first-class there |
| 17 | The film data has a broken chapter structure: `04 BACK TO WORK` appears twice around a 0.04 s `05 THE YEAR`. Present before any test edits |
| 18 | Test copies of a realm silently diverge from the source. Nothing says "this is a copy, N revisions behind" |

## Process lessons

- Test agents must write only to a sandbox project. Four test publishes to the film timeline were made once and had to be restored; verify the restored head by content digest, not by the working-copy banner (finding 3).
- Branches 12 to 43 commits behind main turn every delivery into a three-repo integration; breaks surface only at merge.
