## PASS/FAIL

**FAIL — App producer envelope ownership.** Runtime/Agent are not defective.

The production App source at `e99cde635e` / `93f1061e10` (`tree 2620ff…`) emits:

```json
"intent": {"ownership": "parent"}
```

at `timelineLocalSaveHandoff.ts:278`.

The canonical Agent schema (`d106dfe8…`) and Runtime schema (`8ea0766f…` → `abd47e68…`, both `tree 6047ac…`) define `clip.add-media.intent` as an empty closed object. Agent registration at `astrid/sdk/timeline/commands.py:105` also uses intent policy `{}`; execution rejects non-empty intent at lines 240–245.

The existing correct carrier is:

```json
{
  "schema_version": 1,
  "op": "clip.add-media",
  "version": "1",
  "select": "parent",
  "args": {"row": "<authored row>", "media": "<Runtime five-field selection>"},
  "intent": {}
}
```

All outer v2 metadata remains unchanged: base pair, label, steps/patch/tags/ordinals, merge mode, dry-run, source, and exact Runtime-managed `args.media`. `intent` is not an authority claim.

## Actual failure

Original failed worker command with Runtime checkout:

```bash
ASTRID_RUNTIME_CHECKOUT=/home/user/work/runtime \
PYTHONPATH=/home/user/work/wt/agt-A4-image-provider-2223:/home/user/work/runtime \
/home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider \
tests/editing_conformance/test_prepared_image_runtime_witness.py::test_prepared_image_app_request_accepts_preview_readback_retry_and_undo
```

Result: **1 failed**.

Stack:

```text
service.py:2437 commit_timeline
timeline_commit_port.py:62 validate_request
timeline_commit_validation.py:97 _validator(...).validate
timeline_commit_validation.py:99 ValidationError
```

Schema path:

```text
commands/items/allOf[23]/then/properties/intent
instance: commands[0].intent
error: Additional properties are not allowed ('ownership' was unexpected)
```

The original worker’s broader scope remains **1 FAIL / 3 PASS**. The initial run without `ASTRID_RUNTIME_CHECKOUT` was environment-blocked and is not product evidence.

The new witness test was discarded by the author and is unavailable; the durable original log remains at:

`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-A4-image-provider-2223/log.txt`

## Provenance and limits

- Agent base: `c36ca8c9…`, tree `50689a44…`; schema SHA-256 `d106dfe8…`.
- Runtime reviewed: `8ea0766f…`; actual merged checkout used by the failed run: `abd47e68…`, tree `6047ac30…`.
- App source: `e99cde635e`, owned implementation `93f1061e10`; identical tree.
- The request body in the discarded test was reconstructed, although the offending production field is source-proven. No browser/generated-transport capture or successful Runtime/provider acceptance is qualified.
- No product, schema, pin, or test changes were made. No failed image body was rerun.

## Recommended next step

App owner should change the prepared-image caller to the existing empty-intent carrier, obtain independent review, then produce a **new** authentic packet and rerun the provider witness. Do not repair Runtime/Agent or strip ownership silently.