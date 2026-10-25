# D128/F validation

All work was read-only source/evidence review. No maker, fixture, provider, service, test body, installation, network acquisition, Farm route, recovery, or permission action was run.

## Checks

Commands and results:

```text
git diff --check                                      PASS
Python 3.13 AST parse of source1747 runner/support and retained parent maker  PASS
Python 3.13 JSON parse of evidence/*.json and retained JSON               PASS
Python 3.13 compile with PYTHONPYCACHEPREFIX in own TMPDIR                PASS
sha256 source1747/parent/candidate/helper bindings                         PASS
read-only fixture Git status/head/tree checks                              PASS
read-only retained Store index/owner/venue inspection                       PASS
retained stdout/stderr search                                               EXACTMISSING
typecheck                                                                    NOT RUN / unavailable and not required for evidence review
unit/full/provider tests                                                     NOT RUN by instruction
```

## Static path proof

The pinned source1747 runner has `prepare_venue()` create only `orch/bin` and `orch/tests` before calling `Store.initialize`. The retained helper's `Store.ensure()` invokes `_verify_projection()` before `build`; `_verify_projection()` reads `tests/suites.conf` unconditionally. The retained venue has no `tiny-orch/tests/suites.conf`, while both Store indexes remain empty and the parent work root has no stage or entry. This is sufficient to identify the first pre-build failure without replaying the body.

## Retained-record limits

The service record retains `parent_stages: []`, `exit_code: 2`, and the parent argv. It does not retain parent stdout or stderr, and no separate stdout/stderr file exists in `/tmp/w-f24ccbdde1`. Those records are `EXACTMISSING`; no output was fabricated.
