#!/bin/bash
set -euo pipefail

fixture=${1:-"$(dirname "$0")/registry-row.scope-fixtures"}
evidence=$(dirname "$fixture")
extract() {
  local id=$1
  local count
  count=$(awk -v r=agent -v s="$id" '$1==r && $2==s { $1=$2=""; sub(/^ +/, ""); print; exit }' "$fixture" | wc -l)
  [ "$count" = 1 ]
  awk -v r=agent -v s="$id" '$1==r && $2==s { $1=$2=""; sub(/^ +/, ""); print; exit }' "$fixture"
}

for scope in actual candidate; do
  positive=$(extract "p4-r2-d83-positive-$scope")
  poison=$(extract "p4-r2-d83-poison-$scope")
  bash -n -c "$positive"
  bash -n -c "$poison"

  set +e
  bash -c "$positive" > "$evidence/d83-positive-$scope.log" 2>&1
  positive_rc=$?
  bash -c "$poison" > "$evidence/d83-poison-$scope.log" 2>&1
  poison_rc=$?
  set -e

  [ "$positive_rc" = 17 ]
  [ "$(grep -Fxc called "$evidence/d83-positive-$scope.body.log")" = 1 ]
  [ "$poison_rc" != 0 ]
  [ ! -e "$evidence/d83-poison-$scope.count" ] || [ "$(wc -l < "$evidence/d83-poison-$scope.count")" = 0 ]
done
{
  printf 'fixture=%s\n' "$fixture"
  printf 'scope_labels=actual-integrated-head,source-candidate-donor2\n'
  printf 'positive_bash_n=0\npositive_exit=17\npositive_stub_calls=1\n'
  printf 'poison_bash_n=0\npoison_exit=nonzero\npoison_stub_calls=0\n'
  printf 'original_execution=none\n'
} > "$evidence/d83-preflight-summary.txt"
