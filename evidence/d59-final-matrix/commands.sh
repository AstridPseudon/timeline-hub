#!/usr/bin/env bash
set -euo pipefail

# D59 normal caller.  The tuple is captured and checkout receipts are verified
# by the existing D73 submit seam before this invocation.  This command never
# recaptures current heads; it consumes exactly one READY tuple.
ROOT=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
TUPLE=${1:?path to the one READY final-source-tuple.json}
RECEIPT=${2:?path for the machine-readable final matrix receipt}
TUPLE_SHA=$(sha256sum "$TUPLE" | awk '{print $1}')

exec python3 "$ROOT/run-final-matrix.py" \
  --mode submit \
  --tuple "$TUPLE" \
  --tuple-sha "$TUPLE_SHA" \
  --receipt "$RECEIPT"
