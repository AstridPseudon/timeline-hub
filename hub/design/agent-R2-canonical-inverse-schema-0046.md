# Agent R2 canonical inverse-schema handoff

Source worktree: `/home/user/work/wt/agt-R2-canonical-inverse-schema-0046`
Owned source: `astrid/core/timeline/schema/edit-command.schema.json`
Consumer/export path: `astrid/sdk/timeline/commands.py:_SCHEMA`, loaded by `validate_command()`.

The committed source adds this optional `InverseArgs.steps` shape while retaining
the historical whole-undo form by omission:

```json
"steps": {
  "type": "object",
  "description": "When present, select nonempty unique step IDs for every target publication; omitted selects the whole target commits.",
  "propertyNames": {"$ref": "#/$defs/ID"},
  "additionalProperties": {
    "type": "array",
    "items": {"$ref": "#/$defs/ID"},
    "minItems": 1,
    "uniqueItems": true
  },
  "minProperties": 1
}
```

`InverseArgs` still requires nonempty unique `publications` and remains closed
(`additionalProperties: false`). Publication-key coverage and unknown
publication/step IDs remain provider semantic validation in
`astrid/sdk/timeline/_step_undo.py`; no provider or generated Runtime/client
file was changed.

Canonical schema SHA256 (after this worker's edit):
`d106dfe8212500709b4072d7bc0486f83c27d5d8de33d215cb52b9ea7d46357d`

Harness committed source: `7689fd97b72d93061b50d3d85922b33a13703cd5`, branch `tl/agt-R2-canonical-inverse-schema-0046`. Independent Luna schema/source review `agt-R2-schema-review-0054` is active. Runtime may inspect this exact source now; final review verdict and any narrow corrections follow, with no whole-provider merge prerequisite.
