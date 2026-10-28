#!/usr/bin/env bash
set -euo pipefail

if [[ -z "${ASTRID_SANDBOX_VENV:-}" ]]; then
  echo "Set ASTRID_SANDBOX_VENV to the disposable paired-wheel venv." >&2
  exit 2
fi
if [[ -z "${ASTRID_RUNTIME_CHECKOUT:-}" ]]; then
  echo "Set ASTRID_RUNTIME_CHECKOUT to the pinned Runtime source archive directory." >&2
  exit 2
fi

PYTHON="$ASTRID_SANDBOX_VENV/bin/python"
RUNTIME="$ASTRID_SANDBOX_VENV/bin/astrid-runtime"
for executable in "$PYTHON" "$RUNTIME"; do
  if [[ ! -x "$executable" ]]; then
    echo "Missing executable: $executable" >&2
    exit 2
  fi
done

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
SMOKE_ROOT="$(mktemp -d "${TMPDIR:-/tmp}/astrid-u1-smoke.XXXXXX")"
DATA_ROOT="$SMOKE_ROOT/runtime-data"
REALM_ROOT="$SMOKE_ROOT/realm"
MEDIA_DIR="$SMOKE_ROOT/media"
FRAME_DIR="$SMOKE_ROOT/frame"
SOURCE_MANIFEST="$SMOKE_ROOT/astrid-source-profile.json"
mkdir -p "$MEDIA_DIR" "$FRAME_DIR"
PROJECT="u1-smoke-$(date -u +%Y%m%d%H%M%S)-$$"
TIMELINE="demo"

# Do not let the checkout shadow the installed wheel: all CLI processes run
# from this private directory with only the selected venv on sys.path.
cd "$SMOKE_ROOT"
export ASTRID_RUNTIME_DATA_ROOT="$DATA_ROOT"
export ASTRID_RUNTIME_SOURCE_MANIFEST="$SOURCE_MANIFEST"
export XDG_STATE_HOME="$SMOKE_ROOT/state"

"$PYTHON" - "$SOURCE_MANIFEST" "$ASTRID_RUNTIME_CHECKOUT" "$REPO_ROOT" "$ASTRID_SANDBOX_VENV" <<'PY'
import json
import sys
from pathlib import Path

manifest = {
    "profile": "astrid",
    "runtime_checkout": str(Path(sys.argv[2]).resolve()),
    "source_checkout": str(Path(sys.argv[3]).resolve()),
    "runtime_environment": str(Path(sys.argv[4]).resolve()),
}
Path(sys.argv[1]).write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
PY

RUNTIME_STARTED=0

cleanup() {
  result=$?
  if [[ "$RUNTIME_STARTED" == 1 ]]; then
    "$RUNTIME" down --data-root "$DATA_ROOT" --json || true
  fi
  return "$result"
}
trap cleanup EXIT

run_json() {
  status=0
  result="$("$@")" || status=$?
  if [[ "$status" != 0 ]]; then
    printf '%s\n' "$result" >&2
    return "$status"
  fi
  printf '%s' "$result" | "$PYTHON" -c '
import json, sys
value = json.load(sys.stdin)
if value.get("ok") is False:
    print(json.dumps(value, sort_keys=True), file=sys.stderr)
    raise SystemExit(1)
data = value.get("data")
if isinstance(data, dict) and isinstance(data.get("rows"), list):
    data = {"rows": [{k: row.get(k) for k in ("clip_id", "type", "start", "end", "asset")} for row in data["rows"]]}
elif isinstance(data, dict) and "filename" in data:
    data = {"filename": data["filename"], "media_type": data.get("media_type")}
elif isinstance(data, dict) and "slug" in data:
    data = {"slug": data["slug"], "id": data.get("id") or data.get("project_id")}
else:
    data = sorted(data) if isinstance(data, dict) else data
print(json.dumps({"ok": True, "data": data}, sort_keys=True))
'
}

echo "SMOKE_ROOT=$SMOKE_ROOT"
"$PYTHON" - <<'PY' "$MEDIA_DIR"
from pathlib import Path
import sys

from PIL import Image, ImageDraw

output = Path(sys.argv[1])
for name, color in (("red", "#d83a3a"), ("green", "#278a55"), ("blue", "#315fc0")):
    image = Image.new("RGB", (640, 360), color)
    ImageDraw.Draw(image).text((24, 24), f"U1 stand-in: {name}", fill="white")
    image.save(output / f"{name}.png")
PY

run_json "$RUNTIME" workspace create --data-root "$DATA_ROOT" --source-manifest "$SOURCE_MANIFEST" \
  --hosted-origin off --realm-root "$REALM_ROOT" --json
run_json "$RUNTIME" up --data-root "$DATA_ROOT" --source-manifest "$SOURCE_MANIFEST" --hosted-origin off --json
RUNTIME_STARTED=1

run_json "$PYTHON" -m astrid projects create "$PROJECT" --name "U1 sandbox smoke" --json
for media in "$MEDIA_DIR"/*.png; do
  run_json "$PYTHON" -m astrid media import "$media" --project "$PROJECT" --json
done
run_json "$PYTHON" -m astrid timelines create --project "$PROJECT" --name "Smoke timeline" \
  --slug "$TIMELINE" --json

EDIT_STATUS=0
EDIT_RESULT="$("$PYTHON" -m astrid timelines edit "$TIMELINE" --project "$PROJECT" \
  --add-layer media --layer-asset "$MEDIA_DIR/red.png" --on 0 --for 3 \
  --track V1 --id standin-red --idempotency-key "$PROJECT-add-red" --json)" || EDIT_STATUS=$?
if [[ "$EDIT_STATUS" != 0 ]]; then
  printf '%s\n' "$EDIT_RESULT" >&2
  exit "$EDIT_STATUS"
fi
printf '%s' "$EDIT_RESULT" | "$PYTHON" -c 'import json, sys; value=json.load(sys.stdin); print(json.dumps({"ok": value.get("ok"), "clip": "standin-red", "receipt_id": (value.get("receipt") or {}).get("receipt_id")}, sort_keys=True)); sys.exit(1 if value.get("ok") is False else 0)'
RECEIPT="$(printf '%s' "$EDIT_RESULT" | "$PYTHON" -c '
import json, sys
result = json.load(sys.stdin)
assert result.get("ok") is True, result
receipt = (result.get("receipt") or {}).get("receipt_id")
assert receipt, result
print(receipt)
')"

run_json "$PYTHON" -m astrid timelines show "$TIMELINE" --project "$PROJECT" --json
VISUALIZE_STATUS=0
VISUALIZE_RESULT="$("$PYTHON" -m astrid timelines visualize "$TIMELINE" --project "$PROJECT" \
  --at 1 --preset frame --mode inputs --format png --json)" || VISUALIZE_STATUS=$?
if [[ "$VISUALIZE_STATUS" != 0 ]]; then
  printf '%s\n' "$VISUALIZE_RESULT" >&2
  exit "$VISUALIZE_STATUS"
fi
printf '%s' "$VISUALIZE_RESULT" > "$SMOKE_ROOT/visualize.json"
OPEN_REFERENCE="$(printf '%s' "$VISUALIZE_RESULT" | "$PYTHON" -c '
import json, sys
result = json.load(sys.stdin)
if result.get("ok") is False:
    print(json.dumps(result, sort_keys=True), file=sys.stderr)
    raise SystemExit(1)
outputs = (result.get("data") or {}).get("outputs") or {}
artifact = (outputs.get("artifacts") or {}).get("png") or {}
object_id = artifact.get("object_id")
if artifact.get("status") != "available" or not object_id:
    print(json.dumps({"outputs": outputs}, sort_keys=True), file=sys.stderr)
    raise SystemExit("visualize returned no managed PNG artifact")
print(json.dumps({"kind": "artifact", "object_id": object_id}))
')"
OPEN_STATUS=0
OPEN_RESULT="$("$PYTHON" -m astrid media open --project "$PROJECT" --materialize \
  --cache-root "$FRAME_DIR" --max-bytes 10485760 "$OPEN_REFERENCE" --json)" || OPEN_STATUS=$?
if [[ "$OPEN_STATUS" != 0 ]]; then
  printf '%s\n' "$OPEN_RESULT" >&2
  exit "$OPEN_STATUS"
fi
VISUALIZE_PAGE="$(printf '%s' "$OPEN_RESULT" | "$PYTHON" -c '
import json, sys
from pathlib import Path
result = json.load(sys.stdin)
if result.get("ok") is False:
    print(json.dumps(result, sort_keys=True), file=sys.stderr)
    raise SystemExit(1)
path = (result.get("data") or {}).get("local_path")
if not path or not Path(path).is_file() or Path(path).suffix.lower() != ".png":
    print(json.dumps(result, sort_keys=True), file=sys.stderr)
    raise SystemExit("media open did not materialize a PNG")
print(path)
')"
echo "VISUALIZE_PNG=$VISUALIZE_PAGE"

run_json "$PYTHON" -m astrid timelines undo "$TIMELINE" --project "$PROJECT" \
  --commit "$RECEIPT" --idempotency-key "$PROJECT-undo-red" --json
run_json "$PYTHON" -m astrid timelines show "$TIMELINE" --project "$PROJECT" --json
echo "SMOKE_OK project=$PROJECT timeline=$TIMELINE receipt=$RECEIPT frame=$VISUALIZE_PAGE"
