#!/usr/bin/env bash
set -euo pipefail

ROOT=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)
CANDIDATE=$ROOT/bin/test-run
SOURCE_PREIMAGE=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/test-run
EVIDENCE=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-OPS-D141-P4-named-admission-0146/evidence
TMP_ROOT=${TMPDIR:-/tmp}
FIXTURE=$(mktemp -d "$TMP_ROOT/d141-p4-admission.XXXXXX")
ORCH_FIXTURE=$FIXTURE/orch
TRACE=$FIXTURE/setsid.trace
RESULTS=$FIXTURE/results.tsv

mkdir -p "$ORCH_FIXTURE/tests/cache" "$ORCH_FIXTURE/queue/pending" \
  "$ORCH_FIXTURE/workers/fixture-agent" "$ORCH_FIXTURE/workers/fixture-composition" \
  "$FIXTURE/worktree" "$FIXTURE/fakebin"
printf '%s\n' fixture > "$FIXTURE/worktree/.fixture"
printf 'worktree=%s\n' "$FIXTURE/worktree" > "$ORCH_FIXTURE/workers/fixture-agent/meta"
printf 'worktree=%s\n' "$FIXTURE/worktree" > "$ORCH_FIXTURE/workers/fixture-composition/meta"

# The fixture contains only admission inputs. The command is never reached: the
# mocked setsid records the production handoff and returns without executing it.
printf '%s\n' \
  'agent p4-current-becfe-http-3legs :' \
  'composition p4-current-becfe-http-3legs :' \
  'agent ordinary-light :' \
  'agent full-other :' \
  'agent agent-core-full :' \
  'agent wrong-suite :' \
  'composition wrong-suite :' > "$ORCH_FIXTURE/tests/suites.conf"

printf '%s\n' '#!/usr/bin/env bash' \
  'if [ "${ADMISSION_DF_MODE:-valid}" = invalid ]; then printf "Avail\\nnot-a-number\\n"; else printf "Avail\\n%s\\n" "$ADMISSION_AVAILABLE"; fi' > "$FIXTURE/fakebin/df"
printf '%s\n' '#!/usr/bin/env bash' \
  'case " $* " in *" --git-path index "*) printf "%s\\n" "$FIXTURE/index";; *" write-tree "*) printf "fixture-tree\\n";; esac' > "$FIXTURE/fakebin/git"
printf '%s\n' '#!/usr/bin/env bash' \
  'printf "%s\\n" "$*" >> "$TRACE"' > "$FIXTURE/fakebin/setsid"
chmod 755 "$FIXTURE/fakebin/df" "$FIXTURE/fakebin/git" "$FIXTURE/fakebin/setsid"
printf 'fixture-index\n' > "$FIXTURE/index"

# Relocate only the runner's private root for this harness. The candidate bytes
# and every admission branch remain the source under test.
RUNNER=$FIXTURE/test-run
sed "s|^O=.*|O=$ORCH_FIXTURE|" "$CANDIDATE" > "$RUNNER"
chmod --reference="$CANDIDATE" "$RUNNER"

PATH="$FIXTURE/fakebin:$PATH"
export PATH FIXTURE TRACE

run_case() {
  local name=$1 repo=$2 suite=$3 available=$4 expected=$5 phrase=$6 conflict=${7:-0}
  local id=case-$name d=$ORCH_FIXTURE/tests/case-$name rc
  mkdir -p "$d"
  printf 'target=fixture-%s\nrepo=%s\nsuite=%s\nfiles=\nnocache=1\nrequested=fixture\n' \
    "$repo" "$repo" "$suite" > "$d/request"
  if [ "$conflict" = 1 ]; then
    local other=$ORCH_FIXTURE/tests/other-heavy-$name
    mkdir -p "$other"
    sleep 60 &
    local peer_pid=$!
    printf '%s\n' "$peer_pid" > "$other/running"
    : > "$other/heavy"
  fi
  set +e
  ADMISSION_AVAILABLE=$available ADMISSION_DF_MODE=valid ADMISSION_CONFLICT=$conflict \
    "$RUNNER" "$id" > "$d/stdout" 2> "$d/stderr"
  rc=$?
  set -e
  if [ "$conflict" = 1 ]; then
    kill "$peer_pid" 2>/dev/null || true
  fi
  if [ "$rc" != "$expected" ]; then
    printf 'FAIL %s: expected exit %s, got %s\n' "$name" "$expected" "$rc" >&2
    exit 1
  fi
  if [ -n "$phrase" ] && ! grep -Fq "$phrase" "$d/stdout" "$d/stderr"; then
    printf 'FAIL %s: missing diagnostic %s\n' "$name" "$phrase" >&2
    exit 1
  fi
  printf '%s\t%s\t%s\t%s\t%s\n' "$name" "$repo" "$suite" "$available" "$rc" >> "$RESULTS"
}

run_case p4-below agent p4-current-becfe-http-3legs 4699999999 3 'floor=4700000000'
run_case p4-at agent p4-current-becfe-http-3legs 4700000000 0 ''
run_case p4-above agent p4-current-becfe-http-3legs 4700000001 0 ''
run_case recorded-stop agent p4-current-becfe-http-3legs 4000000000 3 'below or at 4500000000'
run_case global-at agent p4-current-becfe-http-3legs 4500000000 3 'below or at 4500000000'
run_case p4-other-heavy agent p4-current-becfe-http-3legs 5000000001 3 'a full suite is already running' 1
run_case same-suite-wrong-repo composition p4-current-becfe-http-3legs 4800000000 3 'floor=5000000000'
run_case ordinary-light-below agent ordinary-light 4999999999 3 'floor=5000000000'
run_case ordinary-light-at agent ordinary-light 5000000000 0 ''
run_case ordinary-heavy-at agent full-other 5200000000 3 'floor=5200000000'
run_case ordinary-heavy-above agent full-other 5200000001 0 ''
run_case core-at agent agent-core-full 4700000000 0 ''
run_case wrong-suite-default agent wrong-suite 4800000000 3 'floor=5000000000'

# Exercise the unchanged malformed-disk guard through the same candidate path.
id=case-invalid-df; d=$ORCH_FIXTURE/tests/$id; mkdir -p "$d"
printf '%s\n' \
  'target=fixture-agent' 'repo=agent' 'suite=p4-current-becfe-http-3legs' \
  'files=' 'nocache=1' 'requested=fixture' > "$d/request"
set +e
ADMISSION_AVAILABLE=4700000000 ADMISSION_DF_MODE=invalid \
  "$RUNNER" "$id" > "$d/stdout" 2> "$d/stderr"
rc=$?
set -e
[ "$rc" = 3 ] && grep -Fq 'disk availability invalid' "$d/stdout" "$d/stderr"
printf 'invalid-df\tagent\tp4-current-becfe-http-3legs\tinvalid\t%s\n' "$rc" >> "$RESULTS"

SOURCE_SHA=$(sha256sum "$SOURCE_PREIMAGE" | awk '{print $1}')
CANDIDATE_SHA=$(sha256sum "$CANDIDATE" | awk '{print $1}')
SOURCE_MODE=$(stat -c '%a' "$SOURCE_PREIMAGE")
CANDIDATE_MODE=$(stat -c '%a' "$CANDIDATE")
SOURCE_BYTES=$(stat -c '%s' "$SOURCE_PREIMAGE")
CANDIDATE_BYTES=$(stat -c '%s' "$CANDIDATE")
# git hash-object is used only to record the CAS identity; no object is written.
CAS_SHA=$(command -p git hash-object "$CANDIDATE")
DIFF_FILE=$FIXTURE/source.diff
set +e
diff -U0 "$SOURCE_PREIMAGE" "$CANDIDATE" > "$DIFF_FILE"
DIFF_RC=$?
set -e
[ "$DIFF_RC" = 1 ]

mkdir -p "$EVIDENCE"
bash -n "$CANDIDATE"
bash -n "$ROOT/controls/validate-admission.sh"
python3 - "$EVIDENCE/source-manifest.json" "$SOURCE_SHA" "$CANDIDATE_SHA" \
  "$SOURCE_MODE" "$CANDIDATE_MODE" "$SOURCE_BYTES" "$CANDIDATE_BYTES" "$CAS_SHA" <<'PY'
import json
import pathlib
import sys

out, source_sha, candidate_sha, source_mode, candidate_mode, source_bytes, candidate_bytes, cas_sha = sys.argv[1:]
pathlib.Path(out).write_text(json.dumps({
    "source_preimage": {
        "path": "/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/test-run",
        "sha256": source_sha,
        "mode": source_mode,
        "bytes": int(source_bytes),
    },
    "candidate": {
        "path": "ops-d141-p4-admission/bin/test-run",
        "sha256": candidate_sha,
        "mode": candidate_mode,
        "bytes": int(candidate_bytes),
    },
    "cas_expected": {"git_blob_sha1": cas_sha},
    "route": {
        "repo": "agent",
        "suite": "p4-current-becfe-http-3legs",
        "floor_bytes": 4700000000,
        "global_stop_bytes": 4000000000,
        "hard_start_guard_bytes": 4500000000,
        "heavy_serialization": True,
    },
}, indent=2) + "\n")
PY

python3 - "$EVIDENCE/controls.json" "$RESULTS" "$SOURCE_SHA" "$CANDIDATE_SHA" "$DIFF_RC" <<'PY'
import json
import pathlib
import sys

out, results_path, source_sha, candidate_sha, diff_rc = sys.argv[1:]
rows = []
for line in pathlib.Path(results_path).read_text().splitlines():
    name, repo, suite, available, exit_code = line.split("\t")
    rows.append({"name": name, "repo": repo, "suite": suite, "available": available, "exit": int(exit_code)})
pathlib.Path(out).write_text(json.dumps({
    "candidate_executed": True,
    "source_preimage_sha256": source_sha,
    "candidate_sha256": candidate_sha,
    "source_diff_exit": int(diff_rc),
    "fixture": "private admission-only fixture; no product body, queue, service, or live registry",
    "cases": rows,
}, indent=2) + "\n")
PY

{
  printf '%s\n' '# D141 P4 named admission validation' ''
  printf '%s\n' "- Candidate shell: ops-d141-p4-admission/bin/test-run (bash -n passed)."
  printf '%s\n' "- Controls shell: ops-d141-p4-admission/controls/validate-admission.sh (bash -n passed)."
  printf '%s\n' "- Source preimage SHA-256: $SOURCE_SHA; candidate SHA-256: $CANDIDATE_SHA."
  printf '%s\n' "- Candidate CAS blob SHA-1: $CAS_SHA; source/candidate modes: $SOURCE_MODE/$CANDIDATE_MODE; bytes: $SOURCE_BYTES/$CANDIDATE_BYTES."
  printf '%s\n' '- The candidate itself handled every case below; `setsid` was the only mocked handoff and never ran a suite body.' ''
  printf '%s\n' '| Case | Repo | Suite | Available | Exit |' '|---|---|---|---:|---:|'
  while IFS=$'\t' read -r name repo suite available exit_code; do
    printf '| %s | %s | %s | %s | %s |\n' "$name" "$repo" "$suite" "$available" "$exit_code"
  done < "$RESULTS"
  printf '%s\n' '' '- Verified the 4.5GB hard-start refusal, Agent P4 4.7GB inclusive floor, one-heavy refusal, same-suite wrong-repo default, unchanged light/heavy/core floors, wrong-suite default, and malformed-disk refusal.'
} > "$EVIDENCE/validation.md"

{
  printf '%s\n' '# D141 P4 admission handoff' ''
  printf '%s\n' 'This is a private Composition worktree candidate only. It changes no live kit, service, queue, registry, Agent source, request row, or test body.'
  printf '%s\n' '' "The receiving CAS must apply the candidate only against source preimage SHA-256 $SOURCE_SHA with mode $SOURCE_MODE and $SOURCE_BYTES bytes. If that preimage differs, return the smallest exact input instead of rewriting blindly."
  printf '%s\n' '' 'The sole special route is repo=agent plus suite=p4-current-becfe-http-3legs. It is heavy-serialized and admits at or above 4,700,000,000 bytes, subject to the unchanged global 4,500,000,000 refusal. Other light, heavy, agent-core-full, wrong-repo, and wrong-suite routes retain their existing floors.'
  printf '%s\n' '' "Expected candidate CAS blob SHA-1: $CAS_SHA. Normal independent review and CAS publication remain required before Agent receives it."
} > "$EVIDENCE/handoff.md"

python3 -m json.tool "$EVIDENCE/source-manifest.json" >/dev/null
python3 -m json.tool "$EVIDENCE/controls.json" >/dev/null

printf '%s\n' "D141 P4 private admission controls passed; candidate=$CANDIDATE source_sha256=$SOURCE_SHA candidate_sha256=$CANDIDATE_SHA cas_blob_sha1=$CAS_SHA" > "$EVIDENCE/harnessreport"
printf '%s\n' "validated private candidate at $FIXTURE; evidence=$EVIDENCE"
