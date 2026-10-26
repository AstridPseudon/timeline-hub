# F D141i terminal floor correction validation

Author correction complete; one bounded independent final check remains before the existing controller continuation. Only D141I-FINAL-001 is corrected. PLAN §3 F and C0 are unchanged.

Exact author commands (exit0):

```text
PYTHONDONTWRITEBYTECODE=1 python3 /tmp/w-6d5dd4f42e/build_packet.py
bash -n /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-F-D141i-terminal-floor-return-sol-0309/evidence/measurement-command.sh
PYTHONDONTWRITEBYTECODE=1 python3 /tmp/w-6d5dd4f42e/terminal_controls.py
PYTHONDONTWRITEBYTECODE=1 python3 /tmp/w-6d5dd4f42e/dry_controls.py
PYTHONDONTWRITEBYTECODE=1 python3 /tmp/w-6d5dd4f42e/final_validate.py
/home/user/work/venv-agent/bin/ruff check --no-cache /tmp/w-6d5dd4f42e/build_packet.py /tmp/w-6d5dd4f42e/terminal_controls.py /tmp/w-6d5dd4f42e/dry_controls.py /tmp/w-6d5dd4f42e/final_validate.py
/home/user/work/venv-agent/bin/mypy --cache-dir=/tmp/w-6d5dd4f42e/mypy-cache --follow-imports=skip --ignore-missing-imports /tmp/w-6d5dd4f42e/build_packet.py /tmp/w-6d5dd4f42e/terminal_controls.py /tmp/w-6d5dd4f42e/dry_controls.py /tmp/w-6d5dd4f42e/final_validate.py
```

The terminal driver ran 12 exact commands, each `/bin/bash <absolute-control.sh>`; terminal-controls.json records all commands, raw paths and SHA256 readbacks. Above-floor4000000001 and equality4000000000 exit0. Below-floor3999999999 exit78. Unreadable sample exits97; an actual write attempt to a directory trace exits98. Existing monitor124/body17 remain nonzero. Five negative cases additionally execute the unchanged finish/source-guard path and retain state=FAIL with the same exits. No terminal control runs a measurement body; negative finalization uses an explicitly labeled non-test placeholder under privatecontrols only. Production runroot is absent.

The prior20 controls are reused as evidence for unchanged semantics:18 admission/current/beforebody/monitor/numeric-die cases are hash-bound and unchanged by function/prefix equality. The2 prior terminal read/write cases were rerun against the corrected exact terminal block. No prior terminal PASS is claimed as evidence for the added comparison. independent0301 reports all other bounded checks PASS; wholepath0253 is reused, with no new investigation.

Fresh serialized positive normal dry control: preflight0/stub17/one call. Agent-SHA-only poison: exit1/zero calls. The retained exact stub SHA256 is38afc8a5b177801f86f33b0166c8ecd4489ee997629e91b336b9c248ca360ad0. Positive serialized and materialized SHA256 both 5a4d5640ff927e0c3b4d7d1ad19ecc40e77fcf6298a173d822e8b3dfe5c0d643. Materialized runmanifest junit_paths exactly equals the new manifest/command XML path. Normal launcher preflight retains its existing import guard; no new product probe was authored.

Static final validation PASS: bash syntax, exact native row, final serialization, both argv copies,22 exact roots, flags -q -n3 -o addopts= -p no:cacheprovider --timeout=45, one launcher body and unchanged locks. All11 wrapper functions and preterminal body prefix are byte-identical after output-root rebinding. All28 physical protected files,386 historical files and6 named source inputs read back exact. Four source commits/trees/parents/origins/clean exact paths pass. venv-agent interpreter remains /usr/bin/python3.13, Python3.13.16. Profile lock remains f4fc0a32a8822e956dfa21ff35d19c0c83d147c754cdb3546f91c84e330be18d; launcher remains9f668e398b1ea4cce48a6c610102723e0a3dab27a764be4191015aa7fc4110cd.

Every operational packet changed line relative to0253:

- measurement-command.sh line6: EVIDENCE_ROOT points at this new absolute packet. RUN_ROOT, MANIFEST, LAUNCHER_EVIDENCE and XML derive from it, with their declarations unchanged.
- measurement-command.sh line366: `if record_disk after_body >/dev/null; then :; else after_body_rc=$?; fi` becomes `if after_body_available=$(record_disk after_body); then :; else after_body_rc=$?; fi`.
- measurement-command.sh new lines368–369: `test "$after_body_available" -ge "$CONTINUOUS_STOP_BYTES" ||` followed by `die "continuous disk stop floor reached after body: $after_body_available < $CONTINUOUS_STOP_BYTES"`.
- service-row.txt line1: only command path changes to this packet; receipt/brief arguments stay original0249.
- positive.manifest and poison.manifest line37: only junit_paths changes to this packet's absolute XML path. Positive/poison still differ only in agent_sha.

No other operational line changes. command-diff.json and manifest-diff.json contain full literal diffs. All other new files are required metadata/reports/private control evidence; no prior byte is overwritten.

Own operational Python final Ruff and mypy pass on4 driver sources. Initial checks exited1: Ruff E741 on inherited O name and one mypy heterogeneous-dict print error; only driver naming/final hash-print reads were adjusted. Exact executed pre-lint sources are retained as *.executed.txt beside final linted drivers, with explicit hash-bound equivalence in privatecontrols/driver-provenance.json. Wrapper/manifests remained identical throughout. Initial/final lint results are retained in privatecontrols/python-checks.json and harness raw logs.

No pytest, collection, body, request-test, service submission, registration, queue operation, dependency/source/test/generated/schema/pin/profile/launcher/guard/kit/globaladmission/registry edit occurred. No core outcome, REG/nonREG classification, service PASS or ship credit is inferred. P419479 remains held/unstarted. All raw KEEP; no deletion.
