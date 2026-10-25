# D134 root-045 setup/source proof

## Result

No test-only fix was made. The exact source-control node reaches the live parser
with the authored helper unchanged and fails at admission with `SystemExit(2)`.
The parser emits `unrecognized arguments: film commands.json`; `parsed.handler`
is never called and the Runtime transport records zero calls.

The helper at `tests/editing_conformance/test_native_batch_ingress.py:141-151`
constructs:

```text
edit commands-file film FILE --project PROJECT --json
  --base-revision-id REV --base-publication-id PUB
```

Current `build_parser` registers the command inventory in `cli.py:3957-3972`.
There is no `commands-file` registration. `cli_native.configure_edit_options`
(`cli_native.py:446-454`) only adds dry-run, idempotency, and JSON options to
the ordinary `edit` command. The current supported document caller is
`commit` (`cli.py:3596-3608`) and requires a detached timeline JSON file,
message, and idempotency key; `apply` accepts an edited cut sheet
(`cli.py:3808-3815`). Neither is the authored `edit commands-file` ingress.

Git history independently records the route retirement in G5 commit
`dba6e4e7a80f5d7b88b2f8718644ac72dcbe9de6`; its diff removes the native
commands-file parser and `commit_many` branch. The earlier attempted
test-only adaptations route through `TimelineSession.commit_many` or synthesize
a detached document with `execute(...)`; those change the CLI ingress and do
not preserve the original parser, malformed-file admission, envelope, and
refusal semantics required by this task.

## Exact reproduction

```text
ASTRID_RUNTIME_CHECKOUT=/home/user/work/runtime \
PYTHONPATH="$PWD:/home/user/work/runtime" \
/home/user/work/venv-agent/bin/python -m pytest -q -o addopts='' -m integration \
tests/editing_conformance/test_native_batch_ingress.py::test_batch_original_claims_one_publication_reload_inverse[cli-False] -x
```

Result: `1 failed`; traceback first boundary is `test_native_batch_ingress.py:166`
inside `cli(...)`, then `astrid/packs/timeline/cli_parser.py:55` and
`argparse.ArgumentParser.exit`; `SystemExit: 2`. Runtime calls were `[]`.

The remaining 21 exact members were not rerun because there was no meaningful
source delta and the shared admission failure is common to the same retired
route. No product fault or setup correction is credited.
