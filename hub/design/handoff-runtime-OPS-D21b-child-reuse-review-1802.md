# Runtime OPS-D21b independent review — 1802

**Verdict: FAIL for qualification (partial controls only).**

The normal maker installs the Runtime backend (`make-child-venv:154-159`), imports it and its protocol (`:163-172`), and runs Runtime CLIs including `python -I -m astrid_runtime` (`:173-175`). The dispatcher calls this maker for `CHILDVENV` (`dispatcher-daemon:11`). The Runtime SHA marker is therefore a real source-custody guard, not just a label. The candidate requester correctly requires the current Runtime SHA (`request-child-venv:13-25`), but consequently rebuilds on backend-only changes despite describing the key as Agent SHA plus client tuple.

The actual completed shared fixture was not qualified: it had `.astrid-source-commit=079580ca46af77e0292d49dc34386b25c8391f99`, `.astrid-runtime-source-commit=2a9e347ff0e1df1dedff5ab7b59ddb27dfe3129d`, no client marker, and import origins pointing at a deleted partial source. Runtime CLI help and `-I -m` worked. Its installed client bytes matched the canonical Runtime client tuple, but those client rows belong to `astrid-0.1.0.dist-info/RECORD`; the candidate checks only `astrid-runtime-0.1.0.dist-info/RECORD`, which has no client rows. This is a normal-maker false negative, not a reason to waive guards.

Private, non-installing controls: matching baseline reused with zero pending files and truthful physical path; changed Agent/source race, corrupt Runtime marker, and partial identity queued; duplicate qualified benches refused as ambiguous. Two decisive failures: appending bytes to installed `astrid_runtime_client/generated.py` while leaving markers unchanged still reused; making the qualified bench root writable still reused. The requester does not verify canonical installed bytes or read-only state.

Decision needed: either (A) key by Agent SHA + Runtime backend SHA + generated client tuple and retain current maker, or (B) redesign the maker into a truly client-only reusable component with authenticated backend custody and corrected RECORD ownership. Do not force client-only reuse by waiving `.astrid-runtime-source-commit`.

Evidence/report: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-OPS-child-reuse-review-1802/report.md`.
