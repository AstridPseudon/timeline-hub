# D86 MAIN affected-node batch preparation (superseded predecessor)

This is the superseded 110-selector predecessor. The current source/harness
candidate is the exact 251-node bundle in
`tools/main_affected_batch_d86/`; do not submit this predecessor.

This predecessor is a source/harness candidate only. It preserves the existing D73 pinned
launcher and central test-service route; it does not install a row, request the
service, collect tests, run a body, build a profile, or change live config.

## Prepared input

`selector-manifest.tsv` is the exact reviewed union: 108 selectors from the six
assigned D86 families in `design/agt-D86-main-families.md`, plus the two exact
ABI20 selected-PARAM selectors from author2316/review2322. The seven manifest
families contain `10/10/46/8/20/14` assigned selectors and `2` ABI20 selectors,
for `110` unique nodes across nine files. Every parametrized id is retained
literally; no aliases, retired selectors, or synthetic nodes are included.

`tests/suites.conf.candidate` contains one candidate named-suite row,
`agent d86-main-affected-node-batch`. Its body is the existing D73 launcher
with every selector quoted so parametrization ids containing spaces remain
single pytest arguments. The central `tests/suites.conf` registry is unchanged.

The ABI20 selectors are exactly:

```text
tests/sdk/test_selected_param_neutral_stage.py::test_mounted_param_custody_refuses_corruption_atomically
tests/sdk/test_timeline_selected_schema_runtime.py::test_paired_provider_requires_exact_installed_contract_digest
```

The received 2342 handback was the separate F-D85
`test_native_batch_ingress.py` source return. Its protected review failed
because it bypassed the real CLI, so its 24 selectors are not part of the
authoritative six-family D86 union and are intentionally excluded.

At eventual submission, the row's manifest must be a standard `p4-d73-v1`
tuple. Capture Agent, Runtime, App, and Composition SHAs once; request the four
normal checkout receipts; and render all paths, trees, parent guards, profile
values, lock values, service versions, and source hashes from those receipts.
Do not recapture a moving integration head. Keep `7627` out of every input and
use only the qualified successor tuple.

## Ready render and submit recipe

Run this only after owner authorization and after the four genuine checkout
receipts have been verified. `tuple.env` is the normal D73 receipt-derived
manifest; it is deliberately separate from the selector TSV.

```bash
set -euo pipefail
ORCH=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch
AGENT=<captured Agent receipt checkout>
EVIDENCE=$ORCH/workers/rt-D86-batch-union-2356/evidence/d86-main-submit
TUPLE=$EVIDENCE/tuple.env
BEFORE=<central-suites-sha256-before>
mkdir -p "$EVIDENCE"

python3 - "$TUPLE" "$AGENT/tests/suites.conf.candidate" \
  "$EVIDENCE/suites.conf.d86" <<'PY'
import sys
from pathlib import Path

tuple_env, candidate, rendered = map(Path, sys.argv[1:])
values = {}
for line in tuple_env.read_text().splitlines():
    if line and not line.startswith('#') and '=' in line:
        key, value = line.split('=', 1)
        values[f'__D86_MAIN_{key.upper()}__'] = value
values.update({
    '__D86_MAIN_MANIFEST__': str(tuple_env.resolve()),
    '__D86_MAIN_EVIDENCE__': str(rendered.parent.resolve()),
    '__D86_MAIN_REQUEST_ID__': 'd86-main-affected-node-batch',
    '__D86_AGENT_PATH__': values['__D86_MAIN_AGENT_PATH__'],
})
text = candidate.read_text()
for key, value in values.items():
    text = text.replace(key, value)
if '__D86_' in text:
    raise SystemExit('unresolved D86 render token')
rendered.write_text(text)
PY
bash -n "$EVIDENCE/suites.conf.d86"

python3 "$AGENT/tools/install_p4_launcher.py" \
  "$EVIDENCE/suites.conf.d86" "$ORCH/tests/suites.conf" "$EVIDENCE" "$BEFORE" \
  d86-main-affected-node-batch
R=$("$ORCH/bin/request-test" integration:agent d86-main-affected-node-batch --no-cache)
ID=$(basename "$(printf '%s\n' "$R" | sed -n '1p')")
"$ORCH/bin/wait-test" "$ID"
```

Before that one request, verify the rendered tuple's four checkout receipts,
clean SHA/tree/parent state, 15-file Runtime lock, contract `0.2.14`, schema
digest, module origins, and the recomputed nine-file source aggregate. The
single batch uses the existing mounted real provider/setup callers and retains
the existing strict C0 request/reply checks. No new wire shape, generated
client, pin, provider shortcut, or live install belongs here.

## No-body controls

The existing D73 controls remain valid for this extension: exact launcher
preflight passed once, the dry stub was called once and returned `17`, and the
poisoned Agent SHA stopped before any stub call. The launcher and tuple route
were not changed; only the quoted selector union and private evidence changed.
No collection, test body, service request, installation, browser, full/core
suite, or original P4 run was performed.
