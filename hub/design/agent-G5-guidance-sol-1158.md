# G5 guidance correction — BLOCKED / DRAFT ONLY

No integration merge: P1 remains NO-GO. This draft corrects guidance but cannot certify its complete JSON workflow end to end against the paired Runtime. No provider workaround or test refusal substitution was made.

## Exact source

- Agent base: `tl/agt-G5-guidance-return-1145/e1dbde787937792b1270e1d2444f068f9fc0ca41`; current worker branch `tl/agt-G5-guidance-sol-1158`.
- Paired Runtime: `/home/user/work/runtime` at `3b926efab2eed122d374540baee297d4cdcec62a` (clean on inspection).
- Read PLAN §3 G3/G5 and golden path, C0 §§1–5, independent `agent-G5-guidance-review-1153.md` and original `agent-G5-draft-review-1137.md`.
- Uncommitted patch: `/tmp/w-b0cecb32e9/final.patch`, SHA-256 `0f2efdcc6cd39bb00d5f490fbcea5ad956eeb2ed6f7eb046bec7f1be55f0c540`. Harness will commit; no Git mutation was performed.
- `astrid/packs/rendering/docs/scripts/timeline_document.py`: SHA-256 `5ec4a3f2b2ef1585e6707c029dc271acb6a4bd7f11f010def18f086d51f28e33`
- `astrid/packs/timeline/cli.py`: SHA-256 `3d739fa2e75c8d20294b6e3227e663d3e915198701e324010a077bfcadc81f59`
- `tests/v10/test_domain_cli_projects_timelines.py`: SHA-256 `16d534c58c72b6b04fa63a82284da56b150052e9dfb906fcf2c33130411ce504`

## What changed and why

1. JSON navigation retains the complete parent/shot/internal-timeline checkout. It suggests the existing JSON commit caller, never cut-sheet `timelines apply`.
2. The only parser migration is in `astrid/packs/rendering/docs/scripts/timeline_document.py:205`: its existing `publish` command is now named `commit`, with `publish` retained as a compatibility alias for existing callers/tests. This is necessary to expose already implemented commit behavior under the G5 workflow name. It does not add an executor or gateway flags. The existing body still emits commands and calls `TimelineSession.commit_many` at line 327 with exact revision/publication base, atomic merge and the supplied idempotency key. The production CLI emits this module invocation.
3. A local working-copy file is an annotated JSON format, not a timeline ref and not immediately a plain authoring candidate. Its follow-up explicitly exports `Checkout.load(source).document()` to `source + ".commit.json"` in the same directory, preserving relative media context and the source file. Existing `Checkout.document()` consumes the annotations and returns the complete editable composition. Check and commit consume that exported JSON. This is guidance using an existing API, with no writer modification.
4. Quoting uses `shlex.join` for project, ref, source/candidate paths and commands, including the draft `show` continuation. Tests use project/ref/path values with spaces and apostrophes. A concrete valid example key `timeline-edit-1` is emitted; guidance requires a fresh key for new intent and the same candidate/key for retry.
5. Updated both remaining show/visualize executable workflow epilogs to `checkout → edit → check → commit`. Ordinary publication terminology remains. The original navigation assertion changes only its authorized workflow literal; all scope/resource assertions remain.

## Blocking evidence

All three new tests execute the actual suggested checkout/edit/export/check/commit commands, using public-launcher/read seams and the real session plus in-process Runtime service (no socket). The test setup's pinned read seam mirrors production `_remote_timeline.py:173–218`, including the exact publication pin. The real command engine accepts the generated `doc.patch`; Runtime then refuses its records:

```json
{
  "code": "validation_error",
  "message": "provider atomic dependency union omits a touched scope",
  "details": {
    "status": "refused",
    "reason": "invalid_records",
    "base": null,
    "current": null,
    "conflicts": []
  }
}
```

The failure originates at paired Runtime `runtime_protocol/timeline_commit_auth.py:1044–1046`, requiring atomic step dependencies to cover every touched physical scope. Every mode (`checkout`, `file`, `draft`) reaches this same failure. It occurs after JSON loading, validation, command emission and `session.commit_many`; it is not a sheet/parser error. Script execution after argument parsing is unchanged from the base, so renaming the existing parser does not repair the underlying writer.

A separate real-engine witness reconstructed the exact pinned base from the retained test Runtime and executed the same request successfully: **1 doc.patch, 1 step, atomic merge, 6 authoritative effects**. Its declared dependencies include parent and internal field/scope reads. Runtime's stronger record-authentication check still refuses it. Full witness (request, engine steps, refusal) is retained at `/tmp/w-b0cecb32e9/engine-witness.json`; the request is embedded below to make this evidence durable.

```json
{
  "api_version": 1,
  "project_id": "90404685a1194541a4738ab2bdb1fecf",
  "timeline_id": "t",
  "base_revision_id": "saved-parent",
  "base_publication_id": "txn-a265a73b7f2c4e27bd9b74d2cb12077e",
  "commands": [
    {
      "schema_version": 1,
      "op": "doc.patch",
      "version": "1",
      "select": null,
      "args": {
        "changes": [
          {
            "op": "set",
            "ref": "parent",
            "path": [
              "config",
              "app",
              "astrid",
              "slots"
            ],
            "before": {
              "state": "absent"
            },
            "value": {}
          },
          {
            "op": "set",
            "ref": "internal-revision:internal-film",
            "path": [
              "clips",
              "id:inside",
              "params",
              "x"
            ],
            "before": {
              "state": "absent"
            },
            "value": 15
          }
        ]
      },
      "intent": {},
      "resolved": [],
      "reads": [
        {
          "ref": "parent",
          "path": [
            "config",
            "app",
            "astrid",
            "slots"
          ],
          "state": {
            "state": "absent"
          }
        },
        {
          "ref": "occurrence:occ-film/clip:inside",
          "path": [
            "params",
            "x"
          ],
          "state": {
            "state": "absent"
          }
        }
      ],
      "selections": [],
      "bindings": {},
      "created": [],
      "expect": {
        "parent::config.app.astrid.slots": {
          "state": "absent"
        },
        "occurrence:occ-film/clip:inside::params.x": {
          "state": "absent"
        }
      },
      "authorship": {
        "parent::config.app.astrid.slots": "direct",
        "occurrence:occ-film/clip:inside::params.x": "direct"
      }
    }
  ],
  "source": {
    "via": "script"
  },
  "dry_run": false,
  "label": "Publish document",
  "steps": [
    {
      "id": "step-1",
      "label": "Publish document",
      "intent": "",
      "tags": [],
      "command_ordinals": [
        0
      ],
      "patch": [
        {
          "op": "set",
          "ref": "parent",
          "path": [
            "config",
            "app",
            "astrid",
            "slots"
          ],
          "before": {
            "state": "absent"
          },
          "value": {}
        },
        {
          "op": "set",
          "ref": "internal-revision:internal-film",
          "path": [
            "clips",
            "id:inside",
            "params",
            "x"
          ],
          "before": {
            "state": "absent"
          },
          "value": 15
        }
      ]
    }
  ],
  "merge": "atomic"
}
```

Do not weaken the failing tests, substitute semantic-only edits for complete JSON editing, invent `reads: []`, or relax Runtime authentication in this guidance task. Provider/Runtime ownership must resolve this dependency-union mismatch. Consequently the requested all-guidance-executable end-to-end result is **not achieved**.

## Exact checks

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.:/home/user/work/runtime ASTRID_RUNTIME_CHECKOUT=/home/user/work/runtime PYTEST_ADDOPTS= /home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider --basetemp=/tmp/w-b0cecb32e9/protected-final tests/sdk/test_scene_save_core.py tests/v10/test_domain_cli_projects_timelines.py -k 'scene_save_core or navigation_preserves_resolved_scope_and_editing_resources or timelines_help_is_executable or render_help_includes_copyable_flat_profile or visualize_help_describes_filmstrip_navigation or show_defaults_to_readable_authored_rows or visualization_human_navigation_footer_is_compact'
```

**27 passed, 89 deselected in 6.24s**. Includes all original **16** scene-save cases, exact `navigation_preserves_resolved_scope_and_editing_resources`, related existing help tests and readable/footer navigation tests. Log: `/tmp/w-b0cecb32e9/protected-final.log`.

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.:/home/user/work/runtime ASTRID_RUNTIME_CHECKOUT=/home/user/work/runtime PYTEST_ADDOPTS= /home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider --basetemp=/tmp/w-b0cecb32e9/guidance-final tests/v10/test_domain_cli_projects_timelines.py -k editing_guidance_consumes_its_json
```

**3 failed, 97 deselected in 6.28s**: all three cases hit the records-authentication refusal above. The assertions for accepted replies, canonical child data, exact retry and unchanged history remain in the tests and are not reached. Log: `/tmp/w-b0cecb32e9/guidance-final.log`. No new test is skipped, xfailed, weakened or changed to expect refusal.

```sh
RUFF_CACHE_DIR=/tmp/w-b0cecb32e9/ruff-cache /home/user/work/venv-agent/bin/python -m ruff check astrid/packs/timeline/cli.py astrid/packs/rendering/docs/scripts/timeline_document.py tests/v10/test_domain_cli_projects_timelines.py --output-format json
RUFF_CACHE_DIR=/tmp/w-b0cecb32e9/ruff-cache PYTHONDONTWRITEBYTECODE=1 make ruff PY=/home/user/work/venv-agent/bin/python
```

Scoped Ruff exits 1 on **18 inherited findings**: CLI15 + original navigation-test module3; helper script0. Archived HEAD and current path/code/message multisets have **zero additions and zero removals**. Normal gate passes **2149/2149**. Witnesses: `/tmp/w-b0cecb32e9/ruff-{base,current}.json` and `ruff-identities.json`.

```sh
PYTHONDONTWRITEBYTECODE=1 MYPY_CACHE_DIR=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-G5-guidance-sol-1158/tmpdir/mypy make PY=/home/user/work/venv-agent-typecheck-v2/bin/python mypy
PYTHONDONTWRITEBYTECODE=1 MYPY_CACHE_DIR=/tmp/w-b0cecb32e9/mypy-current /home/user/work/venv-agent-typecheck-v2/bin/python -m mypy astrid scripts/reshape --hide-error-context --no-color-output --no-pretty --show-error-codes
# Same raw command from cwd /tmp/w-b0cecb32e9/base, cache /tmp/w-b0cecb32e9/mypy-base:
PYTHONDONTWRITEBYTECODE=1 MYPY_CACHE_DIR=/tmp/w-b0cecb32e9/mypy-base /home/user/work/venv-agent-typecheck-v2/bin/python -m mypy astrid scripts/reshape --hide-error-context --no-color-output --no-pretty --show-error-codes
```

Normal gate passes **1911/1911**. Private raw runs each exit 1 with **1911 errors in 252 files / 957 checked files**; exact path/message/code identity comparison is **1911 → 1911, zero added/removed** (`mypy-identities.json`, logs `mypy-base.log`, `mypy-current.log`). The historical 1912 → 1911 removal belongs to the inherited G5 deletion draft and the original1137 report; it is not newly claimed here.

The worker's named `tmpdir` is a file containing `/tmp/w-b0cecb32e9`, rather than a directory. Initial pytest/Ruff attempts using it as a directory failed with `NotADirectoryError` before running tests; after reading that pointer, all actual scratch/caches use the private directory. The initial normal mypy gate above still passed; the independent identity runs use valid private caches. No permission/automatic-review denial occurred.

```sh
git diff --check
PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-agent/bin/python scripts/artifact_manifest.py --check
PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-agent/bin/python scripts/vendor_lock.py check runtime.lock.json --producer /home/user/work/wt/rt-pin-34eac004
```

All pass. Manifest is current and runtime lock matches the frozen producer; these three changed paths require no generated/pin/contract update. No full, browser, live-socket, P1/P2/P3/P4, native14, original58 or D17 suite was run/requested. No dependency install/shared cache write, host daemon, push or Git mutation.

## Contract preservation and next step

No changes to checkout/store/publish/cli_working, providers, sync/commit_session, Runtime, generated clients/pins or contract. Full v2 base pair, commands, label, steps (patch/reads/ordinals), merge/reads/key/dry_run/source/rationale/group_id and accepted/merged envelopes, canonical documents, records/dependencies/effects/steps/history/undo_steps, preview/would_status and structured conflict/invalid fields are untouched. This is source preservation, **not a claim of newly passing those complete contract scenarios**. Actual new complete-document acceptance is blocked as described.

Keep this draft off integration (P1 NO-GO). Dispatch the existing provider/Runtime records owner with the three failing tests and exact request; rerun this narrow continuation selector after that fix. Review the compatibility alias and the explicit normalization guidance as part of G5 before integration. The obsolete external document-checkout guide still describes an older held broad writer; it is outside the allowed edit scope and should be reconciled by its documentation owner.
