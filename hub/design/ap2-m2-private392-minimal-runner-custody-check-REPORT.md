# private392 minimal HTTP runner custody review

## Verdict

**HOLD execution; approve the source shape only.** The runner preserves the
intended HTTP-only/non-hosted-UI boundary and the exact private contract
guards, but it has one concrete cleanup defect: it installs an `EXIT` trap and
then `exec`s Vitest. `exec` replaces the shell, so the trap cannot remove the
runner's `RUN_ROOT`. The wrapper must retain a shell around Vitest (or perform
equivalent explicit cleanup) before execution is approved.

The current `tl/integration` App tree must not be used: its committed lock is
public Runtime `2c4ac180c2220bdad966bc01e95ad230e99ce26a` with artifact
`sha256:6f000bc615a9cb24fb00cc69a97af75eae71006ebfe87e3caa272fcdbbb1af56`.
The private runner correctly refuses that mismatch.

## Approved source handoff

The counterpart handoff confirms that no regeneration is needed:

- Generated counterpart: `tl/ap2-m2-private392-app-counterpart-preparation`
  at `acc27e8dcf13b2296e7738d2e06199777ab3cb1f`, tree
  `ee76df404b0d2cae283cb70951264c97b94416a0`.
- Runner-ready App source: `tl/ap2-m2-private392-unmocked-door-driver-source`
  at `85ae206b815381da31c229cc9107e322cb9c612f`, tree
  `593ab0296b8cd14e06b1e5251f48ef1fe9125ea1`.
- Candidate wrapper source: `tl/ap2-m2-private392-app-http-runner-minimal-source`
  at `7a8762e05a97dbd3fdf2c188aa14292d066933c5`.
- Exact driver SHA-256 remains
  `85a6f1b2caa7929fb4f6d29855529b6ff837a4ad293b85dd187d080e74d7b981` in
  both the original driver source and candidate wrapper source.

The wrapper is a three-file source delta (runner, Vitest registration, and
the unchanged driver) relative to its own parent. It is not a public pin or
generated-byte change. Apply/review it against the retained `85ae206b` App
source in a private exact checkout; do not run it from public `tl/integration`.

## Custody and contract checks

The wrapper constants and read-only inspection agree on:

- Agent checkout `/home/user/work/wt/agt-pin-1303ce6b`: HEAD
  `1303ce6be32e7bd96ed5c6b35afcb15819e81b50`, tree
  `2f2685d85c3f65b458795100a8045371eb19ee06`, parent
  `e010e6a3868e963471244491bb6672c3e4a5135e`, schema digest
  `39211e63a50b9fb495fdf3feb5beaf0e4d0b4eab9a7e13f4d5f769e0d317429d`.
- Runtime checkout `/home/user/work/wt/rt-pin-f8da4b6d`: HEAD
  `f8da4b6d46b0ec5ebeb7a42be47c5bf3438c5414`, tree
  `8be43e13acb436120f8a63b1a178d64c49422461`.
- Runtime health/schema
  `242d2bc193bf16b699eb87592736769aacd8fdb75a1bb859dff3255d83ea5042`, raw
  bundle
  `fa7717e25c95126b18bb6f37b4c2d813d4a815456a06d438d52ef41c2cf1eab3`,
  component manifest
  `1ad76db27c1d9716bb234f811bf63e1f5898cb3d5f9b835a821765e6cad895e5`,
  artifact manifest version
  `52df520b8384c70dc10d0b15bdce00e758c153019d26ddb9e141f5840885ba2d`, and
  manifest file digest
  `1c684f53582a44b12a7438b79ddeace8696768b4fb98f8f704d58a640fa6cd5f`.
- Runtime manifest contains exactly 75 artifacts. The wrapper rehashes every
  committed artifact, bundle, component manifest, metadata/schema marker, and
  byte-compares Agent/Runtime edit-command schemas.

Both exact Agent and Runtime checkouts were read-only clean. The counterpart
App source is retained as a Git ref, not currently as a separate worktree;
the final runner must provide an exact clean checkout/snapshot of `85ae206b`.

The counterpart lock audit passed for all 13 entries: every consumer blob,
lock hash, producer file, and Runtime 75-artifact manifest hash matched. The
three generated TypeScript blobs are byte-identical to their producer files.
The recorded producer-backed command also passed on the original counterpart
source:

```text
node scripts/vendor-lock.mjs check runtime.lock.json --producer /home/user/work/wt/rt-pin-f8da4b6d
ok runtime.lock.json (matches pinned producer commit)
```

No public lock was changed, no artifact was generated, and no new pin was
created.

## Product-precondition and transport review

The blank disposable `index.html` satisfies only the existing
`harnessUnavailableReason()` static HTTPS listener prerequisite. The test
still performs its product setup: exact identity checks, Runtime realm
creation, Runtime startup, product credential provisioning, project creation,
composition-revision publication, authoring-profile restart, authenticated
health/schema verification, and cleanup.

The driver retains authentic calls through `DirectHarness.doorRequest()` for
the primary App provider and direct authenticated Runtime HTTP for the second
credential/session. It uses the real `RuntimeDataProvider`, command session,
generic patch capture, IndexedDB-backed outbox, lost-ACK/reload/exact retry,
disjoint rebase, guarded undo, stale zero-write refusal, and zero legacy POST
assertions. Fake IndexedDB is only the App outbox persistence dependency. No
hosted App page is mounted, read, or claimed.

The wrapper also refuses ambient `ASTRID_PUBLIC_CHECKOUT` and caller-supplied
`ASTRID_APP_DIRECT_DIST`, requires the exact Python executable paths, checks
Agent/Runtime checkout cleanliness, and refuses the public `2c4` lock before
creating the disposable dist. Those controls remain appropriate.

## Checks performed

Read-only/static checks performed:

- `git show`/SHA-256 comparison of candidate runner and driver — PASS; driver
  exact85a6 hash unchanged.
- Exact Agent/Runtime HEAD, parent/tree, clean-status, and schema/artifact
  digest inspection — PASS.
- Runtime manifest count and 75-file hash audit — PASS.
- Retained private App lock/generated-byte/producer-manifest audit — PASS for
  all 13 locked files.
- Inspection of runner, harness, driver transport, credential/project/receipt
  and outbox paths — PASS for source custody and authentic-call preservation,
  except the cleanup defect above.
- Candidate public App lock check — EXPECTED FAIL and remains fatal; it pins
  public `2c4` rather than private `f8da`.
- No browser, hosted build, localhost/HTTP/socket process, full suite,
  `request-test`, or live Door execution was run.

## Required next steps

1. Fix the wrapper cleanup control so `RUN_ROOT` is removed after Vitest
   exits, including failure/interrupt paths.
2. Use an exact clean private App checkout at `85ae206b` with the private
   generated counterpart, not `tl/integration` or the public postbuild source.
3. Ensure the exact `/home/user/work/venv-agent/bin/python` and
   `/home/user/work/venv-runtime/bin/python` paths exist; the handoff reports
   both absent in this sandbox, so live execution was not available here.
4. Only then run the single exact Vitest selector centrally, preserving every
   guard and reporting any actual Door result separately from source approval.
