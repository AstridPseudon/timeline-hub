# Get help

Start in the Python environment that contains the noneditable paired wheels.

```bash
python3 -m astrid doctor --json
astrid-runtime status --profile astrid --data-root "$ASTRID_SUPPORT_ROOT" --json
```

## Command or module not found

Activate the environment containing the paired wheels. If the installed
console script is missing from `PATH`, use the module form for the same
read-only diagnostic:

```bash
python3 -m astrid doctor --json
```

## Workspace selection is missing or ambiguous

Use the [canonical workspace create/attach recipe](release-recipe.md#workspace-selection-create-or-attach-in-place).
For a fresh install, use `python3 -m astrid.setup --create --apply` only with
an explicit absent or empty realm root. For an existing installation, use
`python3 -m astrid.setup --attach --apply` with its actual realm ID, realm
root, durable support root and discovery path. Preserve the selected realm
and support root; do not relocate data or create an automatic replacement.

If the selected realm is not known, stop and recover it from the existing
backup/configuration evidence before applying setup. Do not use a checkout
manifest or disable identity checks to make an ambiguous installation start.

## Setup check needs an explicit operation

`python3 -m astrid.setup` without `--create` or `--attach` is an interactive
guided path and is not the noninteractive installed recipe. Use the exact
existing-installation readiness check, which is read-only:

```bash
python3 -m astrid.setup --attach --check --offline \
  --workspace-id <existing-realm-id> \
  --data-root <absolute-support-root> \
  --realm-root <absolute-realm-root> --json
```

Review the proposal, then use the matching `--attach --apply` command from the
canonical recipe only when the selected realm and root are confirmed.

## Runtime cannot connect

Read the existing diagnostic from `python3 -m astrid doctor --json` and
`astrid-runtime status --profile astrid --data-root "$ASTRID_SUPPORT_ROOT" --json`.
If setup has not yet been applied, use the explicit create/attach route above;
do not use `workspace inspect` plus `up`, delete workspace state, or delete
credentials to force a fresh start.

## Renderer checker is unavailable after installation

`tools/check_black_frames.py` is a useful source-tree/contributor validator,
but `tools/` is not packaged in the installed wheel and is not a mandatory
installed-journey input. Use renderer doctor, the managed render receipt and
Runtime-owned output decode/readback for the installed path. Only use the
checker after a producer supplies it as a checksummed paired auxiliary
artifact. The retired `tools/render_and_check.py` wrapper is not a fallback.

## A tool needs a key or dependency

Read that pack’s skill and configure the executing environment. A healthy Runtime connection does not mean every optional tool is ready. See [Credentials](credentials.md).

## A run failed

```bash
python3 -m astrid runs show <run-id> --project <project> --json --evidence
python3 -m astrid runs events <run-id> --project <project> --json
```

Replace the bracketed values with your run and project. Correct the reported cause before retrying. For rendering issues, continue with the [renderer guide](../guides/debugging.md).

[Back to setup](README.md)
