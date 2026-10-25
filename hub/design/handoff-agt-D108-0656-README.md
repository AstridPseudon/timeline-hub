# D108 Agent core input handoff

Status: SOURCE COMPLETE / BODY NOT RUN.

This is the exact source and membership handoff for the existing sole Runtime
controller rt-D108-agent-core-main-0645. It does not request a second body,
launcher, framework, checkout, install, registry write, or source pin. D110
(agt-R2-D110-removed-shot-0651) has priority over any same-tuple full body;
the D110 source fix and review remain upstream of this handoff. No mutable
four-repository final tuple was captured.

## Authoritative source

Agent source is the current normal integration head used by this worker:

  Agent commit b27ff3449ec4d9b5e14ac25b8f5a18c1999c21f6
  Agent tree   972188c76ed7a9e8f41d1baf6768673de2596efc
  checkout     /home/user/work/wt/agt-F-D108-core-input-0656
  remote       https://github.com/peteromallet/astrid-agent

The producer is the existing immutable Runtime receipt, not mutable
/home/user/work/runtime:

  Runtime commit 1daca2a33f6d7b10053e07c539a54843e3984e19
  Runtime tree   a522511414947e48e317a5e5c2103483b121a750
  checkout       /home/user/work/wt/rt-pin-1daca2a3
  runtime.lock   source_commit matches 1daca2a33f6d7b10053e07c539a54843e3984e19
  status         clean

The current production caller remains the registered commitTimeline path:
Timeline.commit/TimelineSession.commit_many capture the exact v2 request and
durable outbox flight; RuntimeCommitService.commit is the provider; remote
commit_timeline dispatches the request; and NativeSheet uses the same session
batch seam. No caller or policy was changed.

## Exact current membership

The authoritative recipe is tests/suites.conf row 181,
OWN-REHEARSAL-SUITE, with its existing roots copied unchanged into
handoff-agt-D108-0656-core-roots.txt. The body selector is intentionally
unfiltered: no -m integration, no --ignore, no hand filtering of red IDs,
and no removal of D13, D23, D14-deferred, or retained D107 legacy-only tests.
The body recipe retains -n 3, -o addopts=, -p no:cacheprovider, and
--timeout=45.

The one permitted source check was a pytest --collect-only invocation using
Agent plus immutable Runtime 1daca2a3 and the qualified schema environment.
Result: 9268 tests collected, 409 source test files, exit 0. The exact
collector output, XML, selector list, and per-file source inventory are kept
in:

  /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-F-D108-core-input-0656/evidence/

The inventory aggregate is
7ac5cdd0bfa2b811f9a0a4fb719d9a28ef6080d2bb879ed29fe54fc1a6882b69.
The current normal source includes D107's
tests/editing_conformance/test_m1_legacy_archive_read.py. The held D110
candidate test is not overlaid because it is not in normal row-181
membership.

## Family and history boundaries

The 47 proof-owed normal family bodies are replaced by this one root-level
body. core-roots.txt maps each of the 47 historical family inputs to its
allowed row-181 root(s), with the exact limit that this is membership coverage
only: it grants no family-level result or classification before the controller
returns its body receipt. Held candidates remain held and are not secretly
added. The production caller uses the handoff unchanged.

The prior rehearsal accounting remains historical, not a prediction for D108:
PRE-EXISTING=16 / KNOWN=37 / ENV=73 / NEW-OURS core=424 /
NEW-OURS non-core=0 / REGRESSION=0 = 550. The earlier rehearsal also retains
23 NO_JUNIT_CASE; neither is rewritten here. Do not guess a new core-open
count before the D108 body result. Current FAIL evidence, when later
classified, overrides an earlier PASS; an absent selector after the existing
rename check is NEW-OURS, not a guessed pre-existing result. D13 environment
and D23/D14 deferred selectors remain explicit and are not deselected.

## Post-run classification inputs

Use the existing authentic upstream-924 full XML and D63 maps only after the
controller returns a terminal body result:

  upstream XML:
  /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-F-D60-snapshot-return-1342/evidence/upstream-full-9244377.xml
  sha256 2941565205663912985f766210bfead7db42264976fabee7dc899d03d4f4657f

  D63 exact-276 rollup:
  design/handoff-agt-F-D63-final-rollup-1517-d63-final-rollup-1517.{json,tsv}
  D63 rename/name-body correction:
  design/handoff-agt-F-D63-rename-return-1508-d63-rename-correction-1508.{json,tsv}
  D63 different-cause A/B limits:
  design/handoff-agt-F-D63-different-causes-1528-d63-different-causes-1528.{json,tsv}
  D54 current rollup:
  design/agt-F-D54-current-rollup-1254.json
  Historical 550 rollup/dispositions:
  design/handoff-agt-F-successor-0209-original550-{rollup,dispositions}.tsv

The upstream XML is the exact path/hash source for D54a comparison. The D63
maps preserve authentic path/hash/count/cause limits: exact 276 is partitioned
by the existing rename check; missing selectors are not silently PASS; the
four different-cause rows remain open; and no new baseline body is created.

## Request/reply contract reminder

The controller must retain the C0 v2 request shape: api_version, project and
timeline IDs, exact base revision/publication pair, ordered commands with
schema_version/op/version/select/args, nonempty label, steps with
patches/reads, merge (fields or atomic), optional reads, HTTP Idempotency-Key,
dry_run, source, rationale, and group_id. Accepted and merged replies retain
canonical document, base/landing pair, receipt, records, bindings, effects,
dependencies, steps, history, and undo steps; conflict retains reason/head;
invalid retains code/path/hint/suggested command; preview has would_status and
a null receipt. Historical rebased retries, refusal, inverse, ABA, no-write,
and freshness guards remain unchanged.

No body result, regression count, release claim, or D108 credit is made here.

