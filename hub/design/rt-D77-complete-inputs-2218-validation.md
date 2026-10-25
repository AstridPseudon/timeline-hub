# D77 complete-input bundle validation

## Result

`NOT_READY` for Farm stage/render. Source custody is complete enough for review,
but current D139 publication is conditional and the installed/finite-footprint
inputs are incomplete.

## Checks performed

| Check | Result | Evidence |
| --- | --- | --- |
| JSON parse for `inputs.json`, `footprint.json`, `source-manifest.json` | PASS | local `python3 -m json.tool` and schema-key assertions |
| Required-input census contains every installer, source, tool, root, profile, binding, consumer and receipt item | PASS | `inputs.json` rows and ordered gate list |
| Current D139 tuple is distinct from preserved historical D77 tuple | PASS | separate current and historical rows |
| Public source/tree/hash custody | PASS/CONDITIONAL | exact public hashes retained; D139 census remains conditional on 38 documented exclusions |
| Guard source and independent receipt | PASS LIMITED | Sol1243 helper plus independent Luna1257 18-control PASS; wrapper only |
| Installer/consumer call chain | PASS | source inspection of `installer/cli.py`, `core.py`, `backend.py`, `tools.py`, `launcher.py`, and D13 consumer test |
| Safe-field check | PASS | no credentials, private paths, private identifiers, or private payload bytes in authored JSON/Markdown |
| Footprint arithmetic | PASS AS ARITHMETIC | `1,168,669,468 + 19,938,578 + 169,901,555 = 1,358,509,601`; OMP-inclusive planning sum `1,524,776,481` is explicitly non-binding |
| Finite peak bound | NOT_READY | exact Agent size, dependency/cache/build/render/backup upper quantities absent; status remains `UNKNOWN_UNBOUNDED` |
| Farm stage/render | NOT RUN | forbidden by task scope and blocked by missing current receipts |

## Exact validation commands

These are source/evidence checks only; no suite, browser, socket, installer or
provider was run:

```text
python3 -m json.tool evidence/source-manifest.json >/dev/null
python3 -m json.tool evidence/inputs.json >/dev/null
python3 -m json.tool evidence/footprint.json >/dev/null
python3 - <<'PY'
import json
from pathlib import Path

root = Path("evidence")
source = json.loads((root / "source-manifest.json").read_text())
inputs = json.loads((root / "inputs.json").read_text())
footprint = json.loads((root / "footprint.json").read_text())
assert source["schema"].endswith("/v1")
assert inputs["status"] == "NOT_READY"
assert footprint["status"] == "UNKNOWN_UNBOUNDED"
assert inputs["current_tuple"]["agent_commit"] != "91398e9de4500ce16c8e55741209ba3609cb1694"
assert inputs["current_tuple"]["runtime_commit"] != "1daca2a33f6d7b10053e07c539a54843e3984e19"
for path in root.iterdir():
    text = path.read_text()
    for forbidden in ("sec" + "ret", "cred" + "ential=", "BEGIN " + "PRIVATE KEY", "access" + "_token"):
        assert forbidden.lower() not in text.lower(), (path, forbidden)
print("D77 JSON/schema/safe-field checks: PASS")
PY

bash -n design/handoff-rt-D77-portable-1624-recipe.sh
```

The last syntax check targets the existing authoritative guarded recipe; no new
executable recipe was authored.

## Unverified / blocked

- No D139-tied `request-checkout`, `request-runtime`, or `request-child-venv`
  receipt is present in this bundle.
- The existing Farm child is built for the historical D77 applied tuple and has
  no installed render qualification.
- `ASTRID_RUN`, authenticated `INSTALL_MANIFEST`, verified uv, browser,
  current installed profile, seven-key carrier, and stage receipts are absent.
- FFmpeg/FFprobe hashes and all private roots remain Farm-owned and unverified.
- A finite peak bound cannot be derived honestly from the retained measurements.
- No product tests or full suite were run per task scope.
