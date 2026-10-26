# F D141i D89c operational validation

The source packet is ready for a bounded independent final source check. No measurement body or service request was run.

Exact commands executed (all exited 0 unless explicitly noted):

```text
python3 /tmp/w-9caf3180ad/build_packet.py
bash -n /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-F-D141i-admission-return-sol-0253/evidence/measurement-command.sh
PYTHONDONTWRITEBYTECODE=1 python3 /tmp/w-9caf3180ad/manifest_and_sources.py
PYTHONDONTWRITEBYTECODE=1 python3 /tmp/w-9caf3180ad/admission_controls.py
PYTHONDONTWRITEBYTECODE=1 python3 /tmp/w-9caf3180ad/dry_controls.py
/home/user/work/venv-agent/bin/ruff check --no-cache /tmp/w-9caf3180ad/admitted_dispatch.py
/home/user/work/venv-agent/bin/mypy --cache-dir=/tmp/w-9caf3180ad/mypy-cache --follow-imports=skip --ignore-missing-imports /tmp/w-9caf3180ad/admitted_dispatch.py
PYTHONDONTWRITEBYTECODE=1 python3 /tmp/w-9caf3180ad/final_validate.py
```

Results:

- Bash syntax PASS; JSON/hash/argv/path/22-root/source guards PASS. Full body argv and terminal block are byte-identical to 0238. Source guard, die, terminal handling and monitor functions are byte-identical. All frozen source, client, schema, launcher, profile, original control/review, and actual 24049 hashes read back unchanged.
- Twenty tiny operational controls PASS. Every exact invocation and result is in admission-controls.json. Positive authority is only the genuine original 0249 receipt and brief, 4821594112 >=4700000000 bytes. Its post-preparation 4687142912 sample and inclusive 4000000000 sample reach only an isolated sentinel (exit17), with production setsid/body excluded. Missing receipt/arguments/brief, malformed receipt, non-admitted receipt, and copied forged-positive authority refuse with exit78 and no sentinel.
- Current disk3999999999 refuses both at the source sample and immediately before body. Unreadable disk refuses. Extracted unchanged monitor stops at3999999999 with124, read failure97, write failure98; five-second sleep argument remains5. Terminal after_body read97/write98 produce FAIL, never PASS. No control result is a service/test success marker.
- Fresh final serialized positive: preflight0/stub17/one call. Agent-SHA-only poison: exit1/zero calls. Exact retained stub38afc8a5b177801f86f33b0166c8ecd4489ee997629e91b336b9c248ca360ad0; serialized/materialized positive hashes equal6398e02116849c6f73bb71cd56679a8fef37103d93d854c61d4e02193b2cef58. Normal launcher preflight performs its existing import guard; no standalone product/provider import was authored or executed.
- Ruff PASS; mypy PASS (one new operational Python source extracted from wrapper). Source syntax compiled without running its imports. No pytest, collection, full suite, body, request-test, row installation, dependency installation, source overlay, queue operation, or product edit occurred.

The initial static validator incorrectly expected the literal JUnit shell variable in both argv copies; its first run exited1. The production body uses positional $2, correctly bound by the existing JUNIT_XML argument. The validator was corrected to verify that existing binding; final validation exited0. The operational wrapper did not change following controls.

Private raw controls and exact driver sources are retained beneath privatecontrols/ with KEEP. Historical raw files and markers were only read and hashed. Final serialized hashes are in readiness.json. The independent whole-path review published at /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-F-D141i-admission-wholepath-0253/evidence/review.json confirms the original duplicate gate, but predates the completed new packet; a new final independent source check remains required.
