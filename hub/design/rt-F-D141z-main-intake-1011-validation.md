# F D141z Main receiving validation

All commands below were run against the private candidate and the real Main registry. No command below performs an installation.

## Exact accepted lifecycle check

This is the independent reviewer command. It creates a private source-faithful fixture from the four exact accepted exports, makes only check.sh executable, and runs the accepted check:

    set -e
    F=/tmp/d141z-main-intake-1011-check
    mkdir -p "$F/source" "$F/tmp"
    cp /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/app-D141z-qualified-61f915-run-final-delivery.py "$F/source/run-final-delivery.py"
    cp /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/app-D141z-qualified-61f915-delivery_lifecycle.py "$F/source/delivery_lifecycle.py"
    cp /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/app-D141z-qualified-61f915-check.sh "$F/source/check.sh"
    cp /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/app-D141z-qualified-61f915-install-map.json "$F/source/install-map.json"
    chmod 0755 "$F/source/check.sh"
    TMPDIR="$F/tmp" "$F/source/check.sh"

Result: PASS, exit 0. It exercised the exact local lifecycle controls, mounted-cancel and outer-parent-death controls, early leader/orphan and normal EOF controls, control-pipe controls, TERM/KILL/reap, low/equal disk and sampler-fault controls, and five main source/inventory/builder/tuple/gate refusal controls. It reports that genuine F1/dispatch admission and install remain unverified.

## Receiving and static controls

    EV=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-F-D141z-main-intake-1011/evidence
    PYTHONDONTWRITEBYTECODE=1 PYTHONPYCACHEPREFIX=/tmp/d141z-main-intake-1011-pycache python3 -m py_compile "$EV/candidate/run-final-delivery.py" "$EV/candidate/delivery_lifecycle.py" "$EV/candidate/install-final-services.py" "$EV/candidate/receiving_controls.py"
    bash -n "$EV/candidate/check.sh"
    python3 -c 'import json,sys; [json.load(open(p)) for p in sys.argv[1:]]' "$EV/candidate/install-map.json"
    ruff check --select F "$EV/candidate/run-final-delivery.py" "$EV/candidate/delivery_lifecycle.py" "$EV/candidate/install-final-services.py" "$EV/candidate/receiving_controls.py"
    PYTHONDONTWRITEBYTECODE=1 TMPDIR=/tmp python3 "$EV/candidate/receiving_controls.py"

Result: all commands PASS. The receiving control reports exact caller/helper closure, current Main preimage, private install/readback/backup/fsync path, outside-row conservation, drift refusal, and poisoned-caller refusal.

## No-install guard

    REG=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/tests/suites.conf
    BEFORE=$(sha256sum "$REG" | awk '{print $1}')
    PYTHONDONTWRITEBYTECODE=1 python3 "$EV/candidate/install-final-services.py" --registry "$REG" --candidate "$EV/candidate/runtime-final-service-rows.txt" --builder /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/delivery-build
    AFTER=$(sha256sum "$REG" | awk '{print $1}')
    test "$BEFORE" = "$AFTER"

Result: PASS; both hashes were 7b1ffdd7225ad9db6a21dd3f2ced1ae7aa3335249ae9994f529aec6d15fd98df.

## Disk-floor sampler

evidence/disk-trace.txt records a genuine sampler at five-second cadence: first, periodic, and final samples. Minimum available bytes were 5,673,127,936, above the 4,000,000,000 stop floor. sampler-lifecycle.json records sampler PID 10, explicit TERM, wait return code 0, and reaped=true.

No full suite, browser, live socket, builder, admission, registry write, or installation was run.
