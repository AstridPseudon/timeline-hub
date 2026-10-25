#!/usr/bin/env bash
set -euo pipefail

bundle_dir=$(CDPATH= cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)
selector_file=${D88_MAIN_SELECTOR_FILE:-"$bundle_dir/selector-argv.txt"}
launcher=${P4_LAUNCHER:?set P4_LAUNCHER only after manager releases exact D73 inputs}
manifest=${P4_D73_MANIFEST:?set P4_D73_MANIFEST only from four fresh checkout receipts}
evidence=${P4_D73_EVIDENCE:?set P4_D73_EVIDENCE to an absolute MAIN evidence directory}
request_id=${P4_D73_REQUEST_ID:?set P4_D73_REQUEST_ID to a fresh MAIN request id}

[[ -f "$selector_file" ]]
mapfile -t selectors < "$selector_file"
[[ "${#selectors[@]}" -eq 277 ]]
for selector in "${selectors[@]}"; do [[ -n "$selector" ]]; done

exec "$launcher" "$manifest" run -- \
    -m pytest -q -n 3 -o addopts= -p no:cacheprovider --timeout=45 -m integration \
    --junitxml="$evidence/$request_id.xml" \
    "${selectors[@]}"
