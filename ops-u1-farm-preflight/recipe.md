# D135 Farm source-only preflight and one six-file receiver

This packet is for the Farm venue only. It does not qualify the local Main
checkout and it does not claim a green source-only result. The Farm worker must
use the exact request-checkout receipts for the Runtime and Agent roots below;
the path names are intentionally not inferred from a sibling machine.

```sh
set -eu

PYTHON=/home/user/work/venv-agent/bin/python
RUNTIME_CHECKOUT=/path/from/the/receipted-runtime-checkout
ASTRID_CHECKOUT=/path/from/the/receipted-agent-checkout
PREFLIGHT_DIR=/path/to/ops-u1-farm-preflight
DURABLE_EVIDENCE=/path/to/Farm/permanent/rt-U1-D135-farm-preflight-2116

test -x "$PYTHON"
test -d "$RUNTIME_CHECKOUT"
test -d "$ASTRID_CHECKOUT"
mkdir -p "$DURABLE_EVIDENCE"
export ASTRID_CHECKOUT
export PYTHONDONTWRITEBYTECODE=1
export PYTHONPATH="$RUNTIME_CHECKOUT:$RUNTIME_CHECKOUT/packages/python:$RUNTIME_CHECKOUT/tests:$ASTRID_CHECKOUT"

# This is the only prerequisite gate. It imports the seven actual modules in
# independent child interpreters, and reports every failure before returning
# nonzero. It does not collect tests, load fixtures, call a provider, open a
# socket, initialize Store, acquire packages, or call pytest.main.
"$PYTHON" "$PREFLIGHT_DIR/preflight.py" \
  --runtime-checkout "$RUNTIME_CHECKOUT" \
  --agent-checkout "$ASTRID_CHECKOUT" \
  --output-dir "$DURABLE_EVIDENCE" \
  --expected-interpreter "$PYTHON"

# Only after the preflight PASS may Farm execute the one authorized body. The
# source roots, PYTHONPATH, ASTRID_CHECKOUT, interpreter and six file paths are
# unchanged from the census above. The XML/log/exit/collection records are
# receiver-owned durable outputs.
set +e
cd "$RUNTIME_CHECKOUT"
"$PYTHON" -m pytest -q -o addopts= -p no:cacheprovider --timeout=45 \
  --junitxml="$DURABLE_EVIDENCE/targeted.xml" \
  tests/test_process_control.py \
  tests/test_platform_signaling.py \
  tests/test_door_routes.py \
  tests/test_managed_output_public_api.py \
  tests/test_timeline_commit_contract.py \
  tests/test_timeline_legacy_authority.py \
  >"$DURABLE_EVIDENCE/pytest.log" 2>&1
actual_exit=$?
set -e
printf '%s\n' "$actual_exit" >"$DURABLE_EVIDENCE/actual-exit.txt"

# Record the actual XML counts. Do not substitute the historical 1571
# filtered-run outcomes or guess a six-file count. A missing or malformed XML
# is a failure to report, not a reason to rerun or weaken the body.
"$PYTHON" - "$DURABLE_EVIDENCE/targeted.xml" "$DURABLE_EVIDENCE/collection.json" <<'PY'
import json
import sys
import xml.etree.ElementTree as ET

xml_path, output_path = sys.argv[1:]
root = ET.parse(xml_path).getroot()
counts = {name: int(root.attrib.get(name, "0")) for name in ("tests", "failures", "errors", "skipped")}
counts["suite_name"] = root.attrib.get("name")
with open(output_path, "w", encoding="utf-8") as stream:
    json.dump(counts, stream, indent=2, sort_keys=True)
    stream.write("\n")
PY
exit "$actual_exit"
```

The preflight writes `preflight.json`, `all-missing.json`, `import.log`, and
`readiness.json` to the durable output directory even when the census refuses.
The receiver must preserve those files together with `targeted.xml`,
`pytest.log`, `actual-exit.txt`, and `collection.json`. A refusal must retain
the exact missing distribution/module names and all seven module results.

The result is venue-specific: the census is a portable prerequisite check, not
the six-file proof, and the six-file proof is not a full Runtime suite claim.
