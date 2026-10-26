#!/bin/bash
set -euo pipefail

SOURCE=${1:?candidate test-run path}
LABEL=${2:?control label}
TMPBASE=${TMPBASE:-/tmp}
ROOT=$(mktemp -d "$TMPBASE/test-run-controls.XXXXXX")
FAKE="$ROOT/fake"
ORCH="$ROOT/orch"
mkdir -p "$FAKE" "$ORCH/tests/cache" "$ORCH/workers" "$ORCH/queue/pending"
cat > "$ORCH/tests/suites.conf" <<'EOF'
agent agent-core-full true
agent p4-current-becfe-http-3legs true
agent targeted-light true
agent full-other-heavy true
EOF

cat > "$FAKE/df" <<'EOF'
#!/bin/sh
if [ "${DF_EXIT:-0}" != 0 ]; then exit "$DF_EXIT"; fi
printf '%s\n' "${DF_VALUE:-0}"
EOF
cat > "$FAKE/setsid" <<'EOF'
#!/bin/sh
printf '%s\n' "$*" >> "$CONTROL_LOG"
exit 0
EOF
chmod 755 "$FAKE/df" "$FAKE/setsid"

RUNNER="$ROOT/test-run"
sed "s#^O=.*#O=$ORCH#" "$SOURCE" > "$RUNNER"
chmod 755 "$RUNNER"
bash -n "$RUNNER"

make_request() {
    local id=$1 suite=$2 d="$ORCH/tests/$1"
    mkdir -p "$d"
    cat > "$d/request" <<EOF
target=integration:agent
repo=agent
suite=$suite
files=''
nocache=1
requested=2026-10-26T01:36:41Z
EOF
}

case_run() {
    local name=$1 suite=$2 available=$3 expected=$4
    local df_value=${5:-$available} df_exit=${6:-0}
    local id="case-$name" d="$ORCH/tests/case-$name" log="$ROOT/$name.setsid.log" rc count
    make_request "$id" "$suite"
    : > "$log"
    set +e
    PATH="$FAKE:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin" \
      DF_VALUE="$df_value" DF_EXIT="$df_exit" CONTROL_LOG="$log" \
      "$RUNNER" "$id" > "$ROOT/$name.stdout" 2>&1
    rc=$?
    set -e
    count=$(wc -l < "$log")
    printf '%s rc=%s expected=%s setsid_calls=%s\n' "$name" "$rc" "$expected" "$count" >> "$ROOT/results"
    test "$rc" = "$expected"
    case "$expected" in
        0)
            test "$count" = 1
            test "$(cat "$d/status")" = running
            if [ "$suite" = agent-core-full ] || [ "$suite" = p4-current-becfe-http-3legs ] || [ "$suite" = full-other-heavy ]; then
                test -f "$d/heavy"
            else
                test ! -f "$d/heavy"
            fi
            ;;
        3) test "$count" = 0; test -f "$d/why" ;;
        *) echo "unexpected expected rc $expected" >&2; return 1 ;;
    esac
}

# The named P4 exception is heavy, inclusive at 4,700,000,000, and rejects one byte below.
case_run p4-at-floor p4-current-becfe-http-3legs 4700000000 0
case_run p4-below-floor p4-current-becfe-http-3legs 4699999999 3

# Light suites remain inclusive at 5,000,000,000.
case_run light-at-floor targeted-light 5000000000 0

# Unrelated heavy suites retain the strict 5,200,000,000 floor.
case_run other-heavy-at-floor full-other-heavy 5200000000 3
case_run other-heavy-above-floor full-other-heavy 5200000001 0

# The original agent-core-full exception remains inclusive at 4,700,000,000.
case_run core-at-floor agent-core-full 4700000000 0
case_run core-below-floor agent-core-full 4699999999 3

# The global hard start guard rejects exactly 4,500,000,000, before suite admission.
case_run global-guard targeted-light 4500000000 3

# Invalid disk output still refuses admission.
case_run invalid-disk agent-core-full 4700000000 3 not-a-number
case_run unreadable-disk agent-core-full 4700000000 3 4700000000 1

# Reciprocal single-heavy-slot protection covers the named P4 and another heavy suite.
busy="$ORCH/tests/busy-heavy"
mkdir -p "$busy"
printf '%s\n' "$$" > "$busy/running"
touch "$busy/heavy"
case_run p4-while-other-heavy-busy p4-current-becfe-http-3legs 4700000000 3
busy="$ORCH/tests/busy-named"
mkdir -p "$busy"
printf '%s\n' "$$" > "$busy/running"
touch "$busy/heavy"
case_run other-heavy-while-p4-slot-busy full-other-heavy 5200000001 3

cp "$ROOT/results" "${TMPBASE%/}/test-run-controls-${LABEL}.results"
printf 'label=%s\nroot=%s\ncentral_body_invoked=false\n' "$LABEL" "$ROOT"
cat "$ROOT/results"
