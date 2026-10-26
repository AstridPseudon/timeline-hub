# U3 D141l review handoff

Verdict: **FAIL** for one blocking upstream-conservation finding.

The App merge candidate is source/test clean for the requested targeted scope:
Tour early gate, Runtime door/menu/voice, draft/outbox and dependent queue
recovery, sent-request filtering, whole-chat Markdown export, and calmer
preview transport all survive the two parents. The full 16-path upstream
accounting has no unrelated changes, and protected placement/loads and
Runtime/command source paths are unchanged.

The blocker is the manifest's qualified Agent pin. Upstream `61062e5556`
requires Agent `e1c751def`, which adds the installer download User-Agent in
`astrid/installer/tools.py`. Candidate Agent `28e56cac` does not contain that
behavior, and no later Agent freeze-2 receiving producer was available in this
review. The exact next step is Agent-side qualification of that producer,
followed by the existing manifest updater; do not repair this by hand in App.

Independent checks: targeted Vitest 5 files/116 tests exit 0; scoped ESLint
exit 0; app and node TypeScript exit 0; installer tests 4/4 exit 0;
vendor-lock exit 0; manifest updater exit 0; `git diff --check` exit 0.
No full/browser/journey proof is claimed.
