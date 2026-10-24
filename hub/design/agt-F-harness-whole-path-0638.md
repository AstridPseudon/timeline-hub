# Report

Verdict: both 0632 harnesses remain unqualified. No product/test edits or executions were made.

## Whole-path facts

The already-qualified path is:

1. Manager requests an existing named `suites.conf` row via `bin/request-test`.
2. `bin/test-run` resolves/recreates the worker snapshot, records the exact tree, and runs from a detached snapshot.
3. Managed bench lease revalidates the exact suite row and holds custody through descendants.
4. Normal child provisioning supplies the source carrier, immutable child, receipt, markers, RECORDs, direct URLs, and import-origin map.
5. The installed child runs the unchanged pytest fixture.
6. Durable `status`, `exit`, `summary`, logs, JUnit, origins, and before/after custody determine the result.

This is evidenced by [D40 qualified evidence](</tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/agt-F-D40-observed-qualified-0551.md): one production invocation, JUnit pass, 32 custody files, genuine child-site origins, and no source mutation.

## Failed branches

- Discovery branch: `060fab94151db3a4319af00f27db387f1bc84cb2`; runner SHA `03be7e7b…a0ada`.
  - The harness requires Agent `bb50a43c…`, but its own checkout is the harness commit `060fab…`; this is the self-HEAD failure.
  - Public child mode can bypass parent receipt resolution.
  - Postflight records source/body state but does not make all custody/origin failures fail closed.
  - Setup failures do not always retain complete environment, origin, result, exit, and timing evidence.
  - It checks only selected installed files/imports, not complete package custody.

- Generic branch: `3ade574fbcc28ed30ea07a4a5653479b2a55fbdb`; runner SHA `3ea291035…a39c5`.
  - It has the same harness-self-HEAD problem: expected source is `bb50a43c…`, while the runner is executed from its own harness branch.
  - `--child-root`, `--provision-receipt`, and related paths are caller-selected; receipt validation is substring-based.
  - The reviewed SHA is only an accidental body-launch guard, not source or media authority.
  - Post-run origin/profile failures are recorded but ignored; only source failure changes the return status.
  - No named `suites.conf` row invokes this runner.

The exact prior return findings are retained in [discovery review](</tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/agt-F-discovery-harness-review-0632.md>) and [generic review](</tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/agt-F-generic-harness-review-0632.md>).

## Missing candidate

No genuine bb50/f320 candidate child exists.

- Discovery expects the normal receipt for `venv-agent-child-discovery-bb50-f320`.
- Generic has only `<qualified-child>`; no qualified path was supplied.
- Normal provisioning previously refused at `pinned-requirements` with `rc=124`.
- Existing D40 child `child-3b5c…` is the older `ba8f/f320` source and cannot qualify `bb50`.

## Minimal same-owner repair guidance

Agent/F ownership should:

1. Obtain the genuine bb50/f320 child through the existing normal child-venv maker using the exact Agent and Runtime source carriers.
2. Add one exact reviewed runner command to `ORCH/tests/suites.conf`; authorize execution by the existing manager `request-test` enqueue and managed bench lease.
3. Remove caller-selected authority: resolve the normal managed receipt/child, and compare source/runtime markers, direct URLs, complete RECORDs, profile locks, Composition archive, and installed production origins against fixed expected identities.
4. Preserve the reviewed script digest only as an accidental-call/body guard.
5. Emit durable `NOTRUN` evidence for setup failures and make every post-run custody/origin/profile failure nonzero. Do not fabricate JUnit when the body never started.

Source/runtime/media custody and body-launch authorization are separate. No new trust backend, permission ledger, gate artifact, peer-hash policy, API, or executor is needed.

## V2 scope

No claim is made about the full v2 request/reply wire surface. The required `api_version`, scope/base IDs, commands, label/steps/patches/reads, merge, idempotency, dry-run, source annotations, accepted/merged receipts, canonical data, dependencies/bindings/history/undo, conflict, and invalid fields remain outside this harness comparison.

## Verification

Read-only inspection only:

- `git status --short --branch` — clean.
- Branch/source/hash inspection with `git show`, `git diff --stat`, `rg`, and `sed` — completed.
- No pytest, preflight, Node, provisioning, install, browser, probe, or original body run, as explicitly required.

Completion marker and conventional commit message were written.