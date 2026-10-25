#!/usr/bin/env bash
# D140 Farm receiver: prerequisite census only.
#
# This command intentionally has one mode.  It never invokes the child maker,
# Python imports, pytest, the Store, a queue, or the D73 launcher.  The Farm
# owner supplies every path as a receipt binding; this script has no Main-only
# path fallback.
set -u -o pipefail

if [ "$#" -ne 1 ] || [ "$1" != "--check-only" ]; then
    printf '%s\n' 'usage: receive-farm.sh --check-only' >&2
    exit 2
fi

readonly AGENT_SHA=41ad656529fa8489829de9078b1b6e157c7433c8
readonly AGENT_TREE=d29e47fe7be6e55940b42fa1477a23e7925f62fa
readonly RUNTIME_SHA=f103bb46866999c961a8865636f2e66d544e0c9b
readonly RUNTIME_TREE=5d0cedf2e5134acf895e8d43191cc5fdc09f9883
readonly APP_SHA=5696769dfca056676cde1ab46d8bc94354b3a44a
readonly APP_TREE=0748df404125114a0f68b701fa76f43abd3fc79a
readonly COMPOSITION_SHA=635f4de06fda22a85fc2e4cfc764d0153a4c9f40
readonly COMPOSITION_TREE=5ab5191a296980a0a6bcd1178ab6902d6478a148
readonly AGENT_ORIGIN=https://github.com/peteromallet/astrid-agent
readonly RUNTIME_ORIGIN=https://github.com/banodoco/banodoco-workspace-runtime
readonly APP_ORIGIN=https://github.com/banodoco/reigh-app
readonly COMPOSITION_ORIGIN=https://github.com/peteromallet/timeline-composition
readonly CANONICAL_SHA=be9e8bc9c6d2411809da2d99126a9b3eef72678de2066bb6ad196d5d16ebcd30
readonly CANONICAL_AGENT=4c4ee35d5687c4cd40a0e5395efda53aa56f939d
readonly CANONICAL_RUNTIME=ab1e4f6141987706132916e2da16477f5a019464
readonly MAKER_SHA=fd83c9e2017f75fb0d76a2d633d4a63aed090df37c4d7417b03152e7a4fc22b5
readonly WRAPPER_SHA=60d2238a748cb21789db5f35174a5186609fc511496701e1327e946fa0412504
readonly CHECKER_SHA=8215f5d9d5134eb1e5d143748c4ef9facc8b7e2946c426341e7dd6ccea272d7c
readonly LAUNCHER_SHA=9f668e398b1ea4cce48a6c610102723e0a3dab27a764be4191015aa7fc4110cd
readonly SUITE_SHA=782fb81cea67ce71b785dd5dbf891bb1d32df74c136425d83d53e938bdf8b51c
readonly LOCK_BLOB=01559de71798c40ba6da1e12c7fba0643902d3e2
readonly LOCK_SHA=073d218447f28e48ef0d39cd01c811443b20b0328982eac1b126bcc5b9df390a
readonly CLIENT_BLOB=b8dd84cf35db2420ba23bb560abcbd5d6115a77b
readonly CLIENT_SHA=952fe98a54c9529af723a029957994efec52821da24a2e9c9c34a8dce99e274b
readonly CLIENT_TYPES_BLOB=92bf7890a84c69e009e4b471ed4ef45049b95fe8
readonly CLIENT_TYPES_SHA=6c0d21d3eb87cff2977f9e33a5b4d0da13676c4ebad0df4c935f39106a45b417
readonly AGENT_SCHEMA_BLOB=1b3f12da05da3bb89fa76881184eefdf8232e076
readonly AGENT_SCHEMA_SHA=572845f1102cefd2c8c9cae1f889393e3ba1b7b2b8d681f3f1f0bd96c63321ce
readonly RUNTIME_SCHEMA_BLOB=a97f1b31e27a6c27373799a84ec839b49188acdc
readonly RUNTIME_SCHEMA_SHA=ad3a316aa60d2fd475327a2156373f77384f327bc96cccea1ee939bac7049d7f
readonly COMMIT_SCHEMA_BLOB=d94415a7d57e7d113223a425c076af7b1a8a4248
readonly COMMIT_SCHEMA_SHA=3654ca3c68f5b3d2022ee91f532aa388b198033d6ae54cda8d8b25cecf739815
readonly LAUNCHER_BLOB=f1bde17ea107a8b669cb6924fbdbd2f3979da988
readonly SUITE_BLOB=fbde96168dca681a76cff1526c23b8d0b74001eb

checks=()
missing=0

json_quote() {
    local value=${1-}
    value=${value//\\/\\\\}
    value=${value//\"/\\\"}
    value=${value//$'\n'/\\n}
    printf '"%s"' "$value"
}

add_check() {
    local id=$1 status=$2 owner=$3 detail=$4 required=${5:-true}
    [ "$status" = PASS ] || missing=1
    checks+=("$(printf '{\"id\":%s,\"status\":%s,\"owner\":%s,\"required\":%s,\"detail\":%s}' "$(json_quote "$id")" "$(json_quote "$status")" "$(json_quote "$owner")" "$required" "$(json_quote "$detail")")")
}

require_env() {
    local name=$1 owner=$2
    if [[ -v $name ]] && [ -n "${!name}" ]; then
        add_check "binding.$name" PASS "$owner" "bound=${!name}"
    else
        add_check "binding.$name" MISSING "$owner" 'required receipt binding is absent'
    fi
}

physical_path() {
    local path=$1 expected=$2 actual
    [ -n "$path" ] || return 1
    actual=$(readlink -e -- "$path" 2>/dev/null || true)
    [ "$actual" = "$path" ] || return 1
    [ -e "$path" ] || return 1
    case "$expected" in
        dir) [ -d "$path" ] && [ ! -L "$path" ] ;;
        file) [ -f "$path" ] && [ ! -L "$path" ] ;;
        executable) [ -f "$path" ] && [ ! -L "$path" ] && [ -x "$path" ] ;;
        *) return 1 ;;
    esac
}

check_bound_path() {
    local id=$1 name=$2 kind=$3 owner=$4 path=
    if [[ -v $name ]]; then path=${!name}; fi
    if [ -z "$path" ]; then
        add_check "$id" MISSING "$owner" "$name is not bound"
    elif physical_path "$path" "$kind"; then
        add_check "$id" PASS "$owner" "$name=$path"
    else
        add_check "$id" MISMATCH "$owner" "$name is not an exact physical $kind: $path"
    fi
}

check_repo() {
    local name=$1 var=$2 commit=$3 tree=$4 origin=$5 repo=
    if [[ -v $var ]]; then repo=${!var}; fi
    local actual actual_tree actual_origin clean object tree_object
    if ! physical_path "$repo" dir; then
        add_check "source.$name.checkout" MISSING 'Farm source owner' "$var must bind an exact physical checkout"
        add_check "source.$name.object" MISSING 'Farm source owner' "cannot inspect $commit without $var"
        return
    fi
    actual=$(git -C "$repo" rev-parse --verify HEAD^{commit} 2>/dev/null || true)
    actual_tree=$(git -C "$repo" rev-parse --verify HEAD^{tree} 2>/dev/null || true)
    clean=$(git -C "$repo" status --porcelain --untracked-files=all 2>/dev/null || true)
    if [ "$actual" = "$commit" ] && [ "$actual_tree" = "$tree" ] && [ -z "$clean" ]; then
        add_check "source.$name.checkout" PASS 'Farm source owner' "$var HEAD/tree/clean match"
    else
        add_check "source.$name.checkout" MISMATCH 'Farm source owner' "$var observed head=$actual tree=$actual_tree clean=$([ -n "$clean" ] && echo false || echo true); expected=$commit/$tree/clean"
    fi
    object=$(git -C "$repo" cat-file -e "$commit^{commit}" 2>/dev/null && echo present || true)
    tree_object=$(git -C "$repo" cat-file -e "$commit^{tree}" 2>/dev/null && echo present || true)
    if [ "$object" = present ] && [ "$tree_object" = present ]; then
        add_check "source.$name.object" PASS 'Farm source owner' "$commit and tree $tree are present in the read-only object store"
    else
        add_check "source.$name.object" MISSING 'Farm source owner' "commit/tree object unavailable for $commit/$tree"
    fi
    actual_origin=$(git -C "$repo" remote get-url origin 2>/dev/null || true)
    if [ "$actual_origin" = "$origin" ]; then
        add_check "source.$name.origin" PASS 'Farm source owner' "origin=$origin"
    else
        add_check "source.$name.origin" MISMATCH 'Farm source owner' "observed origin=$actual_origin expected=$origin"
    fi
}

check_git_file() {
    local id=$1 var=$2 repo_var=$3 commit=$4 rel=$5 expected_blob=$6 expected_sha=$7
    local repo=${!repo_var-} blob got
    if ! physical_path "$repo" dir; then
        add_check "$id" MISSING 'Farm source owner' "$repo_var is unavailable"
        return
    fi
    blob=$(git -C "$repo" rev-parse "$commit:$rel" 2>/dev/null || true)
    got=$(git -C "$repo" show "$commit:$rel" 2>/dev/null | sha256sum | awk '{print $1}' || true)
    if [ "$blob" = "$expected_blob" ] && [ "$got" = "$expected_sha" ]; then
        add_check "$id" PASS 'Farm source owner' "$rel blob=$blob sha256=$got"
    else
        add_check "$id" MISMATCH 'Farm source owner' "$rel observed blob=$blob sha256=$got expected blob=$expected_blob sha256=$expected_sha"
    fi
}

check_hash_mode() {
    local id=$1 name=$2 expected=$3 expected_bytes=$4 expected_mode=$5 owner=$6 path=
    if [[ -v $name ]]; then path=${!name}; fi
    local got bytes mode
    if ! physical_path "$path" file; then
        add_check "$id" MISSING "$owner" "$name must bind an exact physical file"
        return
    fi
    got=$(sha256sum "$path" | awk '{print $1}')
    bytes=$(stat -c '%s' "$path")
    mode=$(stat -c '%a' "$path")
    if [ "$got" = "$expected" ] && [ "$bytes" = "$expected_bytes" ] && [ "$mode" = "$expected_mode" ]; then
        add_check "$id" PASS "$owner" "$name sha256=$got bytes=$bytes mode=$mode"
    else
        add_check "$id" MISMATCH "$owner" "$name observed sha256=$got bytes=$bytes mode=$mode expected sha256=$expected bytes=$expected_bytes mode=$expected_mode"
    fi
}

check_d139a_schema() {
    local dist=${SCHEMA_INSTALLED_DISTRIBUTION-} record=${SCHEMA_RECORD_CLOSURE-} direct=${SCHEMA_DIRECT_URL-} manifest=${SCHEMA_SOURCE_MANIFEST-}
    local record_sha row_count hashed unhashed expected_unhashed direct_sha
    if ! physical_path "$dist" dir || ! physical_path "$record" file || ! physical_path "$direct" file || ! physical_path "$manifest" file; then
        return
    fi
    if [ "$(basename "$dist")" != banodoco_timeline_schema-0.0.2.dist-info ]; then
        add_check schema.dist-info-name MISMATCH 'D139a schema owner' 'dist-info directory name is not the pinned package/version'
    else
        add_check schema.dist-info-name PASS 'D139a schema owner' 'pinned dist-info directory name'
    fi
    record_sha=$(sha256sum "$record" | awk '{print $1}')
    row_count=$(awk 'END {print NR}' "$record")
    hashed=$(awk -F, 'NF == 3 && $2 != "" {count += 1} END {print count + 0}' "$record")
    unhashed=$(awk -F, 'NF == 3 && $2 == "" && $3 == "" {print $1}' "$record" | sort | paste -sd '|')
    expected_unhashed='banodoco_timeline_schema-0.0.2.dist-info/RECORD|banodoco_timeline_schema/__pycache__/__init__.cpython-313.pyc|banodoco_timeline_schema/__pycache__/generated.cpython-313.pyc|banodoco_timeline_schema/__pycache__/materialize.cpython-313.pyc|banodoco_timeline_schema/__pycache__/theme.cpython-313.pyc|banodoco_timeline_schema/__pycache__/validate.cpython-313.pyc'
    if [ "$record_sha" = 844b2a2e1ee19d7a1656d57cb49c2bc8febf67295e653f93ff8f96217a0c7220 ] && [ "$row_count" = 18 ] && [ "$hashed" = 12 ] && [ "$unhashed" = "$expected_unhashed" ]; then
        add_check schema.record-content PASS 'D139a schema owner' 'RECORD sha/18 rows/12 hashed/six named unhashed rows match'
    else
        add_check schema.record-content MISMATCH 'D139a schema owner' "RECORD sha=$record_sha rows=$row_count hashed=$hashed unhashed=$unhashed"
    fi
    direct_sha=$(sha256sum "$direct" | awk '{print $1}')
    if [ "$direct_sha" = b7a0a4f90218d54bc1fb118609d40a381f5762650f8e5863ec39098ec269165e ] \
        && grep -Fq 'https://github.com/banodoco/ArtAgents.git' "$direct" \
        && grep -Fq '242f9c4306bf3b501222cb041a9eb246ef47bc85' "$direct" \
        && grep -Fq 'packages/timeline-schema/python' "$direct"; then
        add_check schema.direct-url-content PASS 'D139a schema owner' 'direct_url sha and pinned VCS URL/commit/subdirectory match'
    else
        add_check schema.direct-url-content MISMATCH 'D139a schema owner' "direct_url sha=$direct_sha or pinned fields differ"
    fi
    if grep -Fq '"url": "https://github.com/banodoco/ArtAgents.git"' "$manifest" \
        && grep -Fq '"commit": "242f9c4306bf3b501222cb041a9eb246ef47bc85"' "$manifest" \
        && grep -Fq '"subdirectory": "packages/timeline-schema/python"' "$manifest" \
        && grep -Fq '"source_tree": "75a5a697f630affee40632e500b3f5b704a9b834"' "$manifest"; then
        add_check schema.trusted-manifest-content PASS 'D139a schema owner' 'trusted manifest fields match the fixed identity'
    else
        add_check schema.trusted-manifest-content MISMATCH 'D139a schema owner' 'trusted manifest fields are missing or changed'
    fi
}

check_readonly_receipt() {
    local id=$1 name=$2 owner=$3 path=
    if [[ -v $name ]]; then path=${!name}; fi
    if ! physical_path "$path" file; then
        add_check "$id" MISSING "$owner" "$name must bind a current authenticated receipt"
        return
    fi
    add_check "$id" PASS "$owner" "$name=$path (contents are retained for Farm owner review)"
}

require_env AGENT_CHECKOUT 'Farm source owner'
require_env RUNTIME_CHECKOUT 'Farm source owner'
require_env APP_CHECKOUT 'Farm source owner'
require_env COMPOSITION_CHECKOUT 'Farm source owner'
check_repo agent AGENT_CHECKOUT "$AGENT_SHA" "$AGENT_TREE" "$AGENT_ORIGIN"
check_repo runtime RUNTIME_CHECKOUT "$RUNTIME_SHA" "$RUNTIME_TREE" "$RUNTIME_ORIGIN"
check_repo app APP_CHECKOUT "$APP_SHA" "$APP_TREE" "$APP_ORIGIN"
check_repo composition COMPOSITION_CHECKOUT "$COMPOSITION_SHA" "$COMPOSITION_TREE" "$COMPOSITION_ORIGIN"

check_git_file source.agent.runtime-lock AGENT_CHECKOUT AGENT_CHECKOUT "$AGENT_SHA" runtime.lock.json "$LOCK_BLOB" "$LOCK_SHA"
check_git_file source.agent.client AGENT_CHECKOUT AGENT_CHECKOUT "$AGENT_SHA" astrid_runtime_client/generated.py "$CLIENT_BLOB" "$CLIENT_SHA"
check_git_file source.agent.client-types AGENT_CHECKOUT AGENT_CHECKOUT "$AGENT_SHA" astrid_runtime_client/timeline_commit_types.py "$CLIENT_TYPES_BLOB" "$CLIENT_TYPES_SHA"
check_git_file source.agent.schema AGENT_CHECKOUT AGENT_CHECKOUT "$AGENT_SHA" astrid/core/timeline/banodoco_schema.py "$AGENT_SCHEMA_BLOB" "$AGENT_SCHEMA_SHA"
check_git_file source.runtime.schema AGENT_CHECKOUT RUNTIME_CHECKOUT "$RUNTIME_SHA" runtime_protocol/canonical_schema.py "$RUNTIME_SCHEMA_BLOB" "$RUNTIME_SCHEMA_SHA"
check_git_file source.runtime.commit-schema AGENT_CHECKOUT RUNTIME_CHECKOUT "$RUNTIME_SHA" contract/schemas/timeline-commit.json "$COMMIT_SCHEMA_BLOB" "$COMMIT_SCHEMA_SHA"
check_git_file source.agent.d73-launcher AGENT_CHECKOUT AGENT_CHECKOUT "$AGENT_SHA" tools/p4-d73-pinned-launch.sh "$LAUNCHER_BLOB" "$LAUNCHER_SHA"
check_git_file source.agent.d73-suite AGENT_CHECKOUT AGENT_CHECKOUT "$AGENT_SHA" tests/suites.conf.candidate.request.md "$SUITE_BLOB" "$SUITE_SHA"

check_hash_mode operational.maker MAKER_PATH "$MAKER_SHA" 111171 755 'D139a joined source owner'
check_hash_mode operational.wrapper WRAPPER_PATH "$WRAPPER_SHA" 18066 755 'D139a request-carrier owner'
check_hash_mode operational.checker CHECKER_PATH "$CHECKER_SHA" 14033 755 'D139a census owner'
check_bound_path operational.received-maker RECEIVED_MAKER file 'Farm receiving owner'
if [ -n "${RECEIVED_MAKER-}" ] && physical_path "$RECEIVED_MAKER" file && [ "$(stat -c '%a' "$RECEIVED_MAKER")" = 755 ]; then
    add_check operational.received-maker-mode PASS 'Farm receiving owner' 'received maker is a regular physical 0755 file'
elif [ -n "${RECEIVED_MAKER-}" ]; then
    add_check operational.received-maker-mode MISMATCH 'Farm receiving owner' 'received maker must be regular physical mode 0755'
else
    add_check operational.received-maker-mode MISSING 'Farm receiving owner' 'received maker receipt is not available'
fi

check_bound_path schema.installed-dist SCHEMA_INSTALLED_DISTRIBUTION dir 'D139a schema owner'
check_bound_path schema.trusted-manifest SCHEMA_SOURCE_MANIFEST file 'D139a schema owner'
check_bound_path schema.record-closure SCHEMA_RECORD_CLOSURE file 'D139a schema owner'
check_bound_path schema.direct-url SCHEMA_DIRECT_URL file 'D139a schema owner'
check_bound_path schema.canonical-census CANONICAL_CENSUS file 'D139 census owner'
check_d139a_schema
if physical_path "${CANONICAL_CENSUS-}" file; then
    got=$(sha256sum "$CANONICAL_CENSUS" | awk '{print $1}')
    if [ "$got" = "$CANONICAL_SHA" ]; then
        add_check schema.canonical-census-hash PASS 'D139 census owner' "supporting-only 1146-row census sha256=$got tuple=$CANONICAL_AGENT/$CANONICAL_RUNTIME"
    else
        add_check schema.canonical-census-hash MISMATCH 'D139 census owner' "sha256=$got expected=$CANONICAL_SHA"
    fi
else
    add_check schema.canonical-census-hash MISSING 'D139 census owner' 'supporting canonical census is not available on this venue'
fi

for binding in P4_PYTHON CHILD_BOOTSTRAP DEPENDENCY_SEED CENTRAL_SERVICE CENTRAL_SUITE D73_LAUNCHER NODE_BIN PROFILE P4_D73_MANIFEST P4_D73_EVIDENCE RETAINED_ROOT DISK_ADMISSION OUTPUT_ROOT JUNIT_ROOT RAW_ROOT STARTSTOP_ROOT KEEP_ROOT NORMAL_REQUEST_ROUTE IMPORT_CHECK_ROUTE D73_DRY_ROUTE CORE_ROUTE POSITIVE_CONTROL POSITIVE_COUNTER POISON_CONTROL POISON_COUNTER POISON_MANIFEST; do
    require_env "$binding" 'Farm receiving owner'
done
check_bound_path interpreter.normal P4_PYTHON executable 'Farm receiving owner'
check_bound_path bootstrap.normal CHILD_BOOTSTRAP executable 'Farm receiving owner'
check_bound_path dependency.seed DEPENDENCY_SEED dir 'Farm receiving owner'
check_bound_path service.central CENTRAL_SERVICE executable 'central test service owner'
check_bound_path suite.central CENTRAL_SUITE file 'central test service owner'
check_bound_path launcher.d73 D73_LAUNCHER executable 'D73 launcher owner'
check_hash_mode launcher.d73-hash D73_LAUNCHER "$LAUNCHER_SHA" 8487 755 'D73 launcher owner'
check_bound_path profile.remotion PROFILE dir 'Farm profile owner'
check_bound_path manifest.d73 P4_D73_MANIFEST file 'D73 manifest owner'
check_bound_path evidence.d73 P4_D73_EVIDENCE dir 'D73 evidence owner'
check_bound_path admission.disk DISK_ADMISSION file 'Farm admission owner'
check_bound_path retained.root RETAINED_ROOT dir 'Farm retained-state owner'
check_bound_path output.root OUTPUT_ROOT dir 'Farm receiving owner'
check_bound_path output.junit JUNIT_ROOT dir 'Farm receiving owner'
check_bound_path output.raw RAW_ROOT dir 'Farm receiving owner'
check_bound_path output.startstop STARTSTOP_ROOT dir 'Farm receiving owner'
check_bound_path output.keep KEEP_ROOT dir 'Farm receiving owner'
check_bound_path route.request NORMAL_REQUEST_ROUTE executable 'normal receiving route owner'
check_bound_path route.imports IMPORT_CHECK_ROUTE executable 'normal receiving route owner'
check_bound_path route.dry D73_DRY_ROUTE executable 'normal receiving route owner'
check_bound_path route.core CORE_ROUTE executable 'normal receiving route owner'
check_bound_path control.positive POSITIVE_CONTROL file 'D134 control owner'
check_bound_path control.poison POISON_CONTROL file 'D134 control owner'
check_bound_path control.positive-counter POSITIVE_COUNTER file 'D134 control owner'
check_bound_path control.poison-counter POISON_COUNTER file 'D134 control owner'
check_bound_path control.poison-manifest POISON_MANIFEST file 'D134 control owner'

if [ -n "${NODE_BIN-}" ] && physical_path "$NODE_BIN" executable; then
    node_version=$($NODE_BIN --version 2>/dev/null || true)
    if [ "$node_version" = v20.19.4 ]; then
        add_check toolchain.node PASS 'D73 launcher owner' "Node=$node_version"
    else
        add_check toolchain.node MISMATCH 'D73 launcher owner' "Node=$node_version expected=v20.19.4"
    fi
else
    add_check toolchain.node MISSING 'D73 launcher owner' 'Node 20.19.4 executable is not available'
fi

for receipt in FARM_CURRENT_AGENT_RECEIPT FARM_CURRENT_RUNTIME_RECEIPT FARM_CURRENT_APP_RECEIPT FARM_CURRENT_COMPOSITION_RECEIPT FARM_D139A_KIT_RECEIPT FARM_D73_RECEIPT; do
    check_readonly_receipt "receipt.$receipt" "$receipt" 'Farm receipt owner'
done

printf '{\n'
printf '  "schema": "timeline.d140.farm-prerequisite-census/v1",\n'
printf '  "mode": "check-only",\n'
printf '  "status": %s,\n' "$(json_quote "$([ "$missing" -eq 0 ] && echo READY || echo NOT_READY)")"
printf '  "side_effects": {"child": false, "pytest": false, "installer": false, "import": false, "store": false, "queue": false, "acquisition": false},\n'
printf '  "source_tuple": {"agent": %s, "runtime": %s, "app": %s, "composition": %s},\n' "$(json_quote "$AGENT_SHA/$AGENT_TREE")" "$(json_quote "$RUNTIME_SHA/$RUNTIME_TREE")" "$(json_quote "$APP_SHA/$APP_TREE")" "$(json_quote "$COMPOSITION_SHA/$COMPOSITION_TREE")"
printf '  "checks": [\n'
for i in "${!checks[@]}"; do
    [ "$i" -gt 0 ] && printf ',\n'
    printf '    %s' "${checks[$i]}"
done
printf '\n  ],\n'
printf '  "next": %s\n' "$(json_quote 'If NOT_READY, stop and name each owner; after every required gate is PASS, run the literal sequence in commands.md exactly once.')"
printf '}\n'

[ "$missing" -eq 0 ]
