# R2 c271 mirror review — PASS

Reviewed `70be7e9fcf3dc29c4195993755bebee0c3126b7a` against
`89c38c9355f5d4bcc68597ec74e4729435a7a07a` under PLAN §3 R2/G5 and the
settled mirror-repair design. No product changes were made by this reviewer.

## Findings

- **PASS — causal scope.** The only production change is
  `astrid/sdk/timeline/_step_undo.py`; the only added test is
  `tests/editing_conformance/test_captured_config_root_mirror.py`. The repair
  replays the captured whole-config native assignment, updates mirror
  eligibility at the same point as `Recording.assign`, consumes derived
  observations in order, and checks the accepted parent-root effect through
  its captured `clips`/full `config` projection. It does not add a broad
  inverse exemption, synthesize native facts, drop observations, flatten
  ranges, or accept an untracked ordinary config path.
- **PASS — capture fidelity and guards.** The lossless archive SHA-256 is
  `502266a70f0d1a3cb21d354e9cce01245acb39ea014649fe528039e997de1e8c`; its
  `actual/cases/058-provider-entry.json` SHA-256 is
  `9056bdaa7926863a3c44d24a0303a6b3c790067623842f13e7f85bb2357974cd`.
  The embedded fixture SHA-256 is
  `16d87e20b1dc37be2246c8f9db0e61d3af12069c42acd03a980a9cd68a94c970`.
  An independent replay checked the accepted config/revision source,
  native/effect ranges, step/ordinal identity, root projection, and zero
  derived-write invariant. The 19 tamper probes cover config before/after/site,
  native order/images, effect images, extra derived writes, ranges, source,
  step, ordinal, owner, digest and scope.
- **PASS — unchanged surrounding scope.** The seven neighboring core paths
  (`inverse.py`, `_root_inverse.py`, and the five named conformance files plus
  `test_transient_root_baseline.py`) are byte-identical to the base. No
  Runtime, schema, pin, generated artifact, public caller, original c271 body,
  or frozen fixture was changed.
- **PASS — security/scope.** Diff scope is exactly the two authorized blobs;
  credential scan found zero matches. Runtime imports resolved from
  `/home/user/work/wt/rt-pin-2a9e347f`, commit
  `2a9e347ff0e1df1dedff5ab7b59ddb27dfe3129d`, tree
  `f79a2355cfb39d9ada7721978bd20d5702105778`.

## Tests and checks

The mandated author selector was run once, exactly as specified:

```text
143 passed in 71.85s
```

The new captured test contains 20 passing cases (one exact replay plus 19
strict tamper cases), included in that 143-test result.

Additional checks:

- Independent source/fixture challenge: PASS.
- Scoped Ruff command over the exact 9 files: `All checks passed!`.
- Private mypy command with the requested options: `Success: no issues found
  in 9 source files`.
- `scripts/vendor_lock.py check runtime.lock.json`: `ok runtime.lock.json`.
- `scripts/artifact_manifest.py --check`: `artifacts.json is current`.
- `git diff --check`: PASS.
- Worktree status: clean.

## Limits and next steps

No review blocker or decision change. This review did not run full suites,
HTTP/browser/daemon/live-socket checks, the original c271/FOUR body, or public
redo qualification. Per the settled plan, retain **G5 DRAFT / P1 NO-GO** until
the manager-owned original c271 qualification completes. The source repair is
independently PASS and may proceed to the normal ordinary-leaf merge queue;
that is not a G5 retirement or gate-GO approval.
