# G5 normal CLI durable undo/redo — frontend draft

DRAFT ONLY / P1 NO-GO. No integration merge requested. Base: `tl/agt-G5-current-draft-join-sol-1450` (`f57d283d2`). This task completed the bounded frontend correction; it does not establish cumulative G5 PASS or actual Runtime journey credit.

## Public interface

Published in this worker report at 15:19 UTC, within five minutes of the 15:18 start:

```sh
python -m astrid timelines undo TL --project P --commit RECEIPT_ID --json
python -m astrid timelines redo TL --project P --commit ACCEPTED_UNDO_RECEIPT_ID --json
python -m astrid timelines undo TL --project P --commit RECEIPT_ID --steps '{"RECEIPT_ID":["step-1"]}' --json
```

Repeat `--commit` oldest first. `--idempotency-key KEY` and `--dry-run` use the existing carrier. Numeric steps and named drafts remain local without a commit selector; local `--json` also keeps the local operation. Explicit numeric counts/drafts with `--commit` are refused before opening a session. A step-ID JSON map uses the existing G2 selector, without another inverse engine.

Both accepted verbs call the existing public methods:

```python
session = TimelineSession.open(project, timeline, client=client)
session.undo(publications, steps=None, idempotency_key=None, dry_run=False, via="cli")
```

`publications` is the exact selected receipt-ID list. `steps`, when supplied, is `{publication_id: [step_id, ...]}`. Redo selects the accepted undo receipt, not the original edit. The session retains its exact authenticated base pair, full v2 label/steps/merge request, frozen retry body/key, and existing receipt acknowledgement checks. No schema, pin, contract, private inverse/provider code, journal, separate publish, native edit subparser, commands-file route, or legacy selector was restored or changed.

## Implementation and decisions

- Parser/dispatch options live in `cli.py` and `cli_native.py`. The only inverse writer call is `TimelineSession.undo`, which emits `timeline.inverse` through the contracted commit route.
- Exact selectors are checked using the existing public `RuntimeRevisions.list` reader. It verifies pinned pagination and complete ancestry; no inferred latest publication or synthetic base is introduced. The frontend matches selected receipt ID, project, accepted revision, previous pair, publisher, provider/compiler versions, canonical scope, and full label/step/merge metadata. Redo requires an accepted undo entry. Runtime/provider still own guarded execution, effect/closure authentication, and later-write scans.
- Frontend refusals retain a structured code and details containing path, head (null when unverified), hint, and a copyable JSON history command. Existing upstream refusal details and explicit request keys survive. No force/overwrite route exists.
- Checkout/status hints now name the existing document `commit --file ... --idempotency-key ...` command, using the actual working-copy path; obsolete publish/three-way hints were removed.
- Tests are additive in the two authorized files. Every original function/class in both files is AST-identical to the draft base. No assertion reversal, skip, xfail, or deletion was used.

The bounded tests reuse the public session and current provider with an in-memory acceptance transport. The fixture projects the provider's actual label/steps/merge metadata into its receipt/history and preserves the full request, full canonical closure, recorder bindings/effects/dependencies, nulls, raw opaque data, order, `undo_steps`, preview `would_status`, and original receipt result. It does not manufacture an inverse or substitute a Runtime journey.

Important finding: before the frontend selector check, changing a selected receipt ID in the existing detached in-memory port's history did not prevent provider acceptance. The final CLI rejects that mismatch before submitting a command. This is source/fake-port evidence only, not proof of a vulnerability in Runtime's authenticated ledger. Provider owner should assess the underlying boundary independently; no forbidden provider hunk was edited.

## Exact bounded verification

Environment used for pytest (dependencies read-only):

```sh
export PYTHONDONTWRITEBYTECODE=1
export ASTRID_RUNTIME_CHECKOUT=/home/user/work/wt/rt-pin-cfa0af0d
export PYTHONPATH=.:/home/user/work/wt/rt-pin-cfa0af0d
```

Final commands from the assigned worktree:

```sh
/home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider --timeout=40 tests/packs/timeline/test_cli_parity.py -k 'not publish'
```

**57 passed, 4 deselected**, 32.83 s. Includes 22 new normal-frontdoor cases and 35 preserved neighboring cases. New cases cover whole/step undo, accepted redo, previews/no acceptance, exact v2 request/reply/history, frozen lost-ack retry, ordered batch acceptance/reversal refusal, identity/receipt/label/ancestry refusal without submission, incompatible local options, deleted/overwrite option refusal, and local numeric JSON undo/redo.

```sh
/home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider --timeout=40 tests/packs/timeline/test_cli_edit_flags.py::test_undo_steps_back_through_the_working_copy tests/packs/timeline/test_cli_edit_flags.py::test_undo_is_one_edit_per_step_and_redo_goes_forward tests/packs/timeline/test_cli_status_publish.py::test_status_absent_draft_reports_head_without_creating tests/packs/timeline/test_cli_status_publish.py::test_status_existing_draft_reports_base_head_changes_and_check tests/packs/timeline/test_cli_status_publish.py::test_checkout_fresh_keeps_dirty_draft_and_allows_named_fresh tests/packs/timeline/test_cli_status_publish.py::test_checkout_fresh_refuses_parent_config_edit_when_clip_diff_is_empty
```

**6 passed**, 10.27 s. The neighboring edit-flags file was read/run only, never edited.

```sh
/home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider --timeout=40 tests/packs/timeline/test_cli_status_publish.py::test_checkout_and_status_hints_use_the_existing_document_commit
```

**1 passed**, 0.92 s. Total final bounded coverage: **64 passing distinct nodes**. New nodes were collected before their bounded runs. Initial collection without the Runtime PYTHONPATH failed with `ModuleNotFoundError: runtime_protocol`; the documented read-only Runtime checkout fixed the environment. Early development failures were corrected; no passing original behavior was rewritten.

Static comparisons used a private `git archive HEAD` source copy in `/tmp/w-1c0a8e8f30/base`, never a checkout over other work. The same paths and flags were run in the worktree and archived draft base:

```sh
/home/user/work/venv-agent-typecheck-v2/bin/python -m mypy --follow-imports=silent --cache-dir /tmp/w-1c0a8e8f30/mypy-current astrid/packs/timeline/cli.py astrid/packs/timeline/cli_common.py astrid/packs/timeline/cli_native.py tests/packs/timeline/test_cli_parity.py tests/packs/timeline/test_cli_status_publish.py --no-error-summary --hide-error-context --no-pretty
/home/user/work/venv-agent/bin/python -m ruff check astrid/packs/timeline/cli.py astrid/packs/timeline/cli_common.py astrid/packs/timeline/cli_native.py tests/packs/timeline/test_cli_parity.py tests/packs/timeline/test_cli_status_publish.py --output-format json
```

Private mypy: **88 base / 88 current, zero added (path, message, code) identities**. Ruff: **16 base / 16 current, zero added (path, rule, message) identities**. Raw tools exit 1 on inherited findings; no baseline/config/dependency was relaxed. Separate private caches were used. Logs are in `/tmp/w-1c0a8e8f30/{mypy,ruff}-{base,current}.{txt,json}` as applicable.

```sh
PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-agent/bin/python scripts/vendor_lock.py check runtime.lock.json --producer /home/user/work/wt/rt-pin-34eac004
PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-agent/bin/python scripts/artifact_manifest.py --check
git diff --check
```

**PASS**: producer manifest matches, artifact manifest current, whitespace clean. All shared installs remained read-only. No Git writes, daemon/provisioning, live sockets, full suite, known-failed public redo/restructure/moved-head body, or P1/P4 body was run.

## Remaining work / handoff

No blocker to this bounded frontend draft. Legacy separate-publish positive tests remain unchanged and unresolved; they were not run or converted into refusal expectations. Independent Luna ports of native move/trim/sheet/verbs tests must replace the retired selector with the normal interface and supply authentic immutable history/full v2 transport. In particular, an empty fake `history.items` array is insufficient: selected entries need the complete pinned chain, exact receipt, recorded label/steps/merge metadata, and `records.undo_of` for redo.

The four deselected parity nodes are the three `[publish]` project-resolution cases and `test_publish_requires_a_message`; they remain intact for a faithful normal-commit port. Other untouched separate-publish cases in `test_cli_status_publish.py` likewise remain outside this correction. Real Runtime journeys and cumulative retirement qualification remain unverified. Keep this draft out of integration until P1 GO and the independent port/provider owners' reviews and qualification.
