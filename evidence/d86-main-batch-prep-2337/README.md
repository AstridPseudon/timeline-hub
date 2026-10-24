# D86 MAIN affected-node batch preparation

This is a source/harness candidate only. It preserves the existing D73 pinned
launcher and the central test-service route; it does not install a row, request
the service, collect tests, run a body, build a profile, or change live config.

## Prepared input

`selector-manifest.tsv` is the exact union from
`design/agt-D86-main-families.md`: 10 M1 outbox nodes, 10 shared-inverse
nodes, 46 native-word nodes across two files, and 8 CLI-document nodes. The
union is 74 nodes in five files. Future reviewed Agent families append another
named family to this manifest; they do not alter these four groups or use an
alias/retired selector.

`tests/suites.conf.candidate` contains one candidate named-suite row,
`agent d86-main-affected-node-batch`. Its body is the existing D73 launcher
with the exact selectors quoted so parametrization IDs containing spaces remain
single pytest arguments. The central `tests/suites.conf` registry is unchanged.

The row's manifest must be the standard `p4-d73-v1` tuple. At the eventual
submission boundary, capture Agent, Runtime, App, and Composition SHAs once,
request the four normal checkout receipts, and render all paths, trees, parent
guards, profile values, lock values, and service versions from those receipts.
Do not recapture a moving integration head. Recompute the original-test hash at
the actual pinned checkout. Keep `7627` out of every input and use only the
qualified successor tuple.

Render the candidate row only after that manifest exists. The existing D73
render convention is sufficient; these are the only D86 substitutions needed:

```bash
python3 - "$MANIFEST" "$AGENT/tests/suites.conf.candidate" \
  "$EVIDENCE/suites.conf.d86" "$EVIDENCE/d86-main-affected-node-batch" <<'PY'
import sys
from pathlib import Path

manifest, candidate, rendered, request_id = map(Path, sys.argv[1:])
values = {}
for line in manifest.read_text().splitlines():
    if line and not line.startswith("#") and "=" in line:
        key, value = line.split("=", 1)
        values[f"__D86_MAIN_{key.upper()}__"] = value
values.update({
    "__D86_MAIN_MANIFEST__": str(manifest.resolve()),
    "__D86_MAIN_EVIDENCE__": str(rendered.parent.resolve()),
    "__D86_MAIN_REQUEST_ID__": request_id.name,
    "__D86_AGENT_PATH__": values["__D86_MAIN_AGENT_PATH__"],
})
text = candidate.read_text()
for key, value in values.items():
    text = text.replace(key, value)
if "__D86_" in text:
    raise SystemExit("unresolved D86 render token")
rendered.write_text(text)
PY
bash -n "$EVIDENCE/suites.conf.d86"
```

## Future submission, after owner authorization

```bash
ORCH=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch
AGENT=<captured Agent receipt checkout>
EVIDENCE=$ORCH/workers/rt-D86-main-batch-prep-2337/evidence/d86-main-batch-submit

# The normal owned-row CAS installer may install only this candidate row after
# its rendered tuple and source/module-origin guards are ready. It is not run
# by this preparation change.
python3 "$AGENT/tools/install_p4_launcher.py" \
  "$EVIDENCE/suites.conf.d86" "$ORCH/tests/suites.conf" \
  "$EVIDENCE" <central-suites-sha256-before> d86-main-affected-node-batch

# Main critical qualification: one named existing service route, one request.
R=$("$ORCH/bin/request-test" integration:agent d86-main-affected-node-batch --no-cache)
ID=$(basename "$(printf '%s\n' "$R" | sed -n '1p')")
"$ORCH/bin/wait-test" "$ID"
```

Before that request, verify the rendered tuple's four checkout receipts, clean
SHA/tree/parent state, 15-file Runtime lock, contract `0.2.14`, schema digest,
and module origins. The production fixture must be the mounted real provider
fixture for the selected Runtime ABI and exercise the existing 20 strict C0
checks (full request fields, authenticated accepted/merged event, conflict /
invalid / refused details, and preview with a null receipt). No new wire shape,
generated client, pin, or provider shortcut belongs in this batch.

## No-body controls performed for this preparation

Use the existing qualified D73 tuple only for the launcher control, with a
stub command in `dry` mode. The expected positive is exactly one stub call and
exit 17; a poisoned Agent SHA must fail in launcher preflight with zero stub
calls. This proves the parsed command and poison guard without collecting or
executing any D86 test body. Keep all control output under the worker evidence
directory.
