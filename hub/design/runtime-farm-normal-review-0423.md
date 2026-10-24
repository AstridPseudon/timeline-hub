## Result

PASS — fresh-only route packet correction complete.

Updated:

- `FARM-CODEX-BRIEF.md`
- `README.md`
- `MANIFEST.sha256`

The handoff now authorizes the D21c first managed Runtime build, permits only authenticated maker reuse, forbids legacy adoption/manual rebuilds, and requires fresh baseline byte preservation.

Exact manager-to-Farm handoff:

> Run README’s exact eight-field `request-runtime` with approved `remotion-env-nodes` + Node v20.19.4/npm 10.8.2 carrier. A first managed build for this fresh Store key is authorized under D21c; if the normal maker authenticates reuse, reuse that entry. Never adopt or relabel a legacy graph, fabricate registration, run the maker manually, or force a rebuild.

## Verification

- `test_normal_setup.py`: **6 passed**
- Template/row checks: **2 passed**
- Manifest SHA check: **all OK**
- Python compile: passed
- `bash -n .../request-runtime`: passed
- Ruff: passed
- `git diff --check`: passed
- Exact eight-argument carrier, selected template/Node, and overlay guards: passed

No full test, provisioning, installation, helper execution, or live farm mutation performed.

## Held helper

**HELD / FAIL separately:** prior result remains **8 passed, 2 failed** for identical-byte `owner.json` and `index.json` replacement. No helper changes or rerun.

## Attachment facts

- Agent: `8657e836...`, tree `b5cbc402...`
- Runtime: `45c3a7f4...`
- Runtime lock SHA: `aa480e04...`
- Template row: 709 decoded bytes including LF; SHA excluding LF `ffdb0b13...`
- Environment: 523 bytes; SHA `e53a69a4...`
- Existing `agent full` row remains byte-exact, SHA `65fd24fa...`
- Farm registry baseline: `64afaf61...`
- Selected Node: v20.19.4 / npm 10.8.2

No blockers for packet review. Production setup remains for Farm Codex and is unverified here.