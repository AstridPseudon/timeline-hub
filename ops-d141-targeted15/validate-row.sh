#!/usr/bin/env bash
set -u

root=$(cd "$(dirname "$0")" && pwd)
row=$(sed -n 's/^runtime full-d141-targeted15 //p' "$root/row.txt")
test -n "$row"
test "$(grep -c '^runtime full-d141-targeted15 ' "$root/row.txt")" -eq 1
test "$(grep -c '^runtime full-d141-pristine ' "$root/row.txt")" -eq 0
test "$(grep -F -c -- '--junitxml="$D66_OUTPUT_DIR/runtime-targeted15.xml"' "$root/row.txt")" -eq 1
test "$(grep -F -c -- 'runtime-full.xml' "$root/row.txt")" -eq 0

repo=/home/user/work/wt/rt-pin-fa9cd546
run_root=$(mktemp -d "${TMPDIR:-/tmp}/d141-targeted15-controls.XXXXXX")
stub=$root/stub-python
stubbed=${row//\/home\/user\/work\/venv-runtime\/bin\/python/$stub}

out=$run_root/positive
test ! -e "$out"
(cd "$repo" && D66_OUTPUT_DIR="$out" bash -c "$stubbed")
test -d "$out"
test ! -L "$out"
test -f "$out/disk-start"
test -f "$out/disk-stop"
test -f "$out/runner-exit"
test -f "$out/KEEP"
test -f "$out/runtime-targeted15.xml"
test ! -e "$out/runtime-full.xml"
test "$(cat "$out/runner-exit")" = 0
grep -Fxq 'KEEP before service cleanup' "$out/KEEP"
grep -Fq 'tests="15"' "$out/runtime-targeted15.xml"
test "$(grep -c '^tests/' "$out/stub-argv")" -eq 15
while IFS= read -r node; do
  grep -Fxq "$node" "$out/stub-argv"
done < "$root/nodes.txt"
test "$(grep -Fxc -- '-m' "$out/stub-argv")" -eq 1
test "$(grep -Fxc -- 'pytest' "$out/stub-argv")" -eq 1
test "$(grep -Fxc -- '-q' "$out/stub-argv")" -eq 1
test "$(grep -Fxc -- '-n3' "$out/stub-argv")" -eq 1

poison_agent=$run_root/agent-poison
ln -s /home/user/work/wt/agt-pin-8b6ed211 "$poison_agent"
poisoned=${stubbed//\/home\/user\/work\/wt\/agt-pin-8b6ed211/$poison_agent}
if (cd "$repo" && D66_OUTPUT_DIR="$run_root/source-poison" bash -c "$poisoned"); then
  exit 1
fi
test ! -e "$run_root/source-poison/stub-argv"

poison_output=$run_root/output-poison
ln -s /tmp "$poison_output"
if (cd "$repo" && D66_OUTPUT_DIR="$poison_output" bash -c "$stubbed"); then
  exit 1
fi
test ! -e "$run_root/output-poison/stub-argv"

printf '%s\n' 'targeted15 row controls PASS'
