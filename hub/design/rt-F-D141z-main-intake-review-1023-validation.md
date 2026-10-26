# F D141z Main receiving independent validation

All checks used fresh private directories under `/tmp/w-ef9580f02b` unless
otherwise noted. The real registry was read-only.

1. Accepted unchanged 33-purpose check:

   `TMPDIR=<fresh-private-dir> <fixture>/source/check.sh`

   PASS, exit 0. The fixture used the four published accepted exports and ran
   the unchanged lifecycle, Main/D68 stub, lease/cancellation, parent-death,
   control-pipe, disk-floor, sampler, and refusal controls.

2. Exact receiving command:

   `PYTHONDONTWRITEBYTECODE=1 TMPDIR=<fresh-private-dir> python3 <author-evidence>/candidate/receiving_controls.py`

   PASS, exit 0: exact caller/helper closure, current Main preimage, private
   install/readback/backup/fsync path, outside-row conservation, drift refusal,
   and poisoned-caller refusal.

3. No-install installer against genuine Main registry:

   `PYTHONDONTWRITEBYTECODE=1 TMPDIR=<fresh-private-dir> python3 <author-evidence>/candidate/install-final-services.py --registry /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/tests/suites.conf --candidate <author-evidence>/candidate/runtime-final-service-rows.txt --builder /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/delivery-build`

   PASS, exit 0. Before and after registry SHA-256 were both
   `7b1ffdd7225ad9db6a21dd3f2ced1ae7aa3335249ae9994f529aec6d15fd98df`; mode
   remained `0600`.

4. Static checks:

   - AST parse: PASS.
   - private-cache `python3 -m py_compile`: PASS.
   - `bash -n candidate/check.sh`: PASS.
   - scoped JSON parse: PASS.
   - `ruff check --select F` on caller, helper, installer, and controls: PASS.

5. Additional private controls: PASS. Source/hash/path/mode/symlink, registry
   preimage and unknown outside-row drift, tuple marker, occupied backup, and
   injected replace-failure rollback all refused or preserved the private
   preimage.

6. Own disk lifecycle trace: three real samples at first/periodic/final over
   5.838 seconds; minimum available bytes `5,656,694,784`, above the
   `4,000,000,000` stop floor; explicit TERM, wait return code 0, and reaped
   sampler are recorded in `disk-trace.txt` and `sampler-lifecycle.json`.

No full suite, real delivery body, live admission, canonical installation,
builder/main, rehearsal, or final build was run.
