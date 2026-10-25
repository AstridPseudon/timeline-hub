#!/usr/bin/env bash
set -euo pipefail

bundle_dir=$(CDPATH= cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)
selector_file=${MAIN_BATCH_SELECTOR_FILE:-"$bundle_dir/selector-argv.txt"}
launcher=${P4_LAUNCHER:?set P4_LAUNCHER to the pinned launcher}
manifest=${P4_D73_MANIFEST:?set P4_D73_MANIFEST to the fresh four-repo manifest}
evidence=${P4_D73_EVIDENCE:?set P4_D73_EVIDENCE to an absolute MAIN evidence directory}
request_id=${P4_D73_REQUEST_ID:?set P4_D73_REQUEST_ID to the fresh MAIN request id}

[[ -f "$selector_file" ]]
mapfile -t selectors < "$selector_file"
[[ "${#selectors[@]}" -eq 268 ]]
for selector in "${selectors[@]}"; do [[ -n "$selector" ]]; done

exec "$launcher" "$manifest" run -- \
    -m pytest -q -n 3 -o addopts= -p no:cacheprovider --timeout=45 -m integration \
    --junitxml="$evidence/$request_id.xml" \
    "${selectors[@]}"
