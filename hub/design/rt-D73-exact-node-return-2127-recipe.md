# D73 exact-node receiving recipe

Verdict: `CANDIDATE_NOT_INSTALLED` / `NOT_READY`.

The private candidate is `ops-d73-exact-nodes/README.md` plus its
`dry-check.sh`. The central caller remains the existing `request-test` to
`test-run` path. The suite rows are direct launcher commands so the existing
runner appends `--files` selectors after `run --`.

The corrected argv begins `-m pytest -q -o addopts= -m integration -p
no:cacheprovider --timeout=45`. This is required because the launcher invokes
`python -P "$@"`; placing `-o` first is a Python argument error.

Each row binds `P4_D73_EVIDENCE` to the runner's `D66_OUTPUT_DIR` and derives
`P4_D73_REQUEST_ID` from its parent directory. XML is written below that same
per-request directory using the derived ID. No guessed environment variable,
fixed ID, or shared XML path is used.

The selected4 row has exactly four selectors: three local selected-schema
nodes and the selected HTTP node. The fork row has exactly one occurrence-fork
node. The source guard requires the reviewed launcher SHA, selected-file SHA,
fork-file SHA, clean canonical source receipt, immutable Runtime receipt, and
rendered four-repository manifest.

`dry-check.sh --bind-check PATH/central-a/d66 PATH/central-b/d66` is the local
ID-collision check. With an eligible source receipt,
`D73_AGENT_HOME=... D73_AGENT_RECEIPT=... D73_AGENT_COMMIT=... D73_AGENT_TREE=...
D73_RUNTIME_HOME=... D73_MANIFEST=... dry-check.sh --controls` runs the reviewed
focused launcher-control test. That test is the supported positive-17
one-call and poisoned-source zero-call control; it does not invoke a D73 body.

No installation, central request, provider/socket, live body, full suite, or
product change was made by this candidate.
