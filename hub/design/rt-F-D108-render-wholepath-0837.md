## D108 whole-path investigation

- No source changes; worktree remains clean.
- Evidence: [D108-render-wholepath-source-hashes.txt](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-F-D108-render-wholepath-0837/evidence/D108-render-wholepath-source-hashes.txt)
- Commit message written; `DONE` created.

Findings:

- Retained D108 Agent applied commit/tree are unavailable as Git objects. Current Agent HEAD/tree is not a valid substitute; exact commit identity is therefore UNKNOWN.
- Normal path confirmed: `Backend.stage → service_declaration → Runtime ServiceSupervisor → generic_host → run_pack_host_foreground → ensure_pack_host`.
- Canonical reusable seams are the existing D13 installed-profile validator and Agent `_installed_execution_origins`; production `ensure_pack_host` remains the final guard.
- Runtime performs exact whole-token argv substitution in order. It does not deduplicate or resolve duplicate flags; normal service declaration emits one canonical host argv.
- Smallest missing actual gate input: authentic D108 installed deployment receipt/profile plus seven-key binding carrier tied to the exact retained Agent/Runtime identities. Render inputs remain separately unavailable.
- The private readiness checker duplicates canonical preflight and should be reduced to custody/input-presence checks. Ordinary invocation is recommended but UNAPPLIED.

Checks:

- `git diff --check` — PASS.
- AST compilation of touched source anchors — PASS.
- Tests, installation, service startup, and rendering — NOT RUN as required.