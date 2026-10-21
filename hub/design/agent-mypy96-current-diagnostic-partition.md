# Gate7 current mypy +96 partition

Date: 2026-10-21 UTC  
Status: **RED, exact-diagnostic partition blocked by missing capture**

## What is proven

The retained named run is the current Agent tree `de36e302e3ee6e950e22aed5c02c02163f7cf5c8`
(`3cafb9450b3633fc7b974a7e0d761fe489badf39`), using the coherent declared
Python 3.11 / Runtime95 environment. Its command was the unchanged Make
target:

```text
make -C <snapshot> PY=<private-python-3.11>/bin/python mypy
```

The central suite `gate7-private311-mypy-capture-current` finished in 68
seconds with exit `2`. Its durable files contain only:

```text
Mypy findings: current=2075 baseline=1979
ERROR: Mypy regressed by 96; fix the new findings.
```

The central result's `log.txt` is empty, its summary has an empty `counts:`
field, and the retained `stdout.txt`/`stderr.txt` contain no per-finding lines.
The older `8afe5a87d` private run remains historical `UNKNOWN`; it did not
produce an exact diagnostic list either. Its retained `.mypy_cache` is from
the old source and is not a current diagnostic capture.

Therefore the only proved fact is the aggregate count and exit status. The
number 96 is not proof that 96 findings are authored-source findings, nor that
any particular file, owner, or diagnostic code owns one of them.

## Partition of the evidence

### Environment and dependency-stub input

The private run included the test-only `types-PyYAML==6.0.12.20260906`
stub (SHA-256 prefix retained in the environment report as
`bca893ff…5137b`). It is not declared in the repository's project metadata,
runtime lock, proof lock, or 164-entry inventory. This is an environment
input that can change diagnostics in unchanged YAML callers. No count or
per-file diagnostic proves how many of the +96, if any, it contributes.

The other retained environment facts are consistent with the requested
profile: Python 3.11.17, mypy 1.17.0, NumPy 2.4.6, and Runtime95 source
`95bd3c5f…`. They do not establish that the environment is the cause of the
RED result. No dependency, stub, target, ignore, or baseline change is
authorized by this report.

### Authored-source delta since the historical source

The only non-test source files changed between `8afe5a87d` and the current
tree are Timeline files:

| Path | Current lines in the changed hunk | What the hunk changes | Ownership | Exact new diagnostics |
| --- | ---: | --- | --- | --- |
| `astrid/packs/timeline/cli.py` | 3585–3597 | Parse the sheet once, choose native dispatch for native-shaped client sheets, and pass `client` to the legacy adapter. | Timeline / Agent | **Not captured** |
| `astrid/sdk/timeline/checkout.py` | 162–170 | Reconcile a retained sheet during `save()` and commit it through `NativeSheet`. | Timeline / Agent | **Not captured** |
| `astrid/sdk/timeline/checkout.py` | 496–620 | Add retained-sheet/session staging helpers and draft/pending-state checks. | Timeline / Agent | **Not captured** |
| `astrid/sdk/timeline_sheet.py` | 130–133, 841–845 | Retain an export and stage retained edits before the legacy writer. | Timeline / Agent | **Not captured** |
| `astrid/sdk/timeline_sheet.py` | 862–894 | Add duration-only retained-sheet translation. | Timeline / Agent | **Not captured** |

The remaining changes since `8afe5a87d` are tests. No changed Main-owned
product file is present in that source delta. This bounds the authored-source
inspection surface, but does **not** prove that all 96 belong to it: unchanged
Main files can acquire new findings when the dependency/stub environment
changes.

### Main-inherited versus Timeline

The exact diff needed to make this partition is absent. Accordingly:

* Timeline is a **candidate owner** only for the five changed-hunk groups in
  the table above.
* Main-inherited/environment-sensitive findings are **unclassified**, not
  zero. The unchanged source set cannot be cleared from an aggregate count.
* No repair should be assigned from the +96 count alone.

## Bounded follow-up repair briefs

These are intentionally evidence-gated briefs, not claims that the listed
hunks caused findings. Each remains disjoint by source hunk. The diagnostic
ID is explicitly marked unavailable because the required artifact was not
retained.

### Brief A — CLI sheet dispatch boundary

* Scope: `astrid/packs/timeline/cli.py:3585–3597`.
* Diagnostic IDs/lines: **unavailable; no per-finding capture**.
* Smallest direct check: compare the eventual exact finding set against this
  hunk, then inspect only the declared return type of `parse_sheet()` and the
  existing `NativeSheet`/`apply_sheet()` signatures. Preserve the two dispatch
  predicates; do not silence a type error with `Any`, `cast`, or `ignore`.
* Owner: Agent Timeline manager, only if an exact new diagnostic lands here.

### Brief B — `Checkout.save()` retained-sheet handoff

* Scope: `astrid/sdk/timeline/checkout.py:162–170`.
* Diagnostic IDs/lines: **unavailable; no per-finding capture**.
* Smallest direct check: inspect the exact `_pending_sheet()` return contract
  and `NativeSheet.apply()` parameter contract at the reported line. If a
  finding is real, add the narrow boundary annotation or correct the call
  shape; do not broaden the object to `Any` or weaken the checker.
* Owner: Agent Timeline manager, only if an exact new diagnostic lands here.

### Brief C — retained sheet/session state helpers

* Scope: `astrid/sdk/timeline/checkout.py:496–620`.
* Diagnostic IDs/lines: **unavailable; no per-finding capture**.
* Smallest direct check: inspect the exact diagnostic's state key and the
  existing `Outbox`, `TimelineSession`, `NativeSheet`, and `Plan` contracts.
  Repair only the reported boundary (including a precise return annotation or
  typed state carrier); retain the existing basis/pending guards.
* Owner: Agent Timeline manager, only if an exact new diagnostic lands here.

### Brief D — sheet export/staging/duration translation

* Scope: `astrid/sdk/timeline_sheet.py:130–133`, `841–845`, and `862–894`.
* Diagnostic IDs/lines: **unavailable; no per-finding capture**.
* Smallest direct check: inspect the exact reported expression and the
  existing parsed-sheet/`ELIDED`/`State.entity()` contracts. Keep the
  duration-only translation and fail-closed `None` paths; use a narrow type
  correction only where the captured diagnostic points. No blanket stub,
  `Any`, `cast`, `ignore`, or baseline adjustment.
* Owner: Agent Timeline manager, only if an exact new diagnostic lands here.

No fifth brief is warranted: the unmodified Main/environment partition has no
exact paths or diagnostic IDs and must not be turned into speculative work.

## Required next evidence

One bounded typecheck capture must preserve the raw mypy output before the
baseline comparator consumes it, or run the comparator equivalent with a
private output file that records every parsed `{path, line, column, message,
code}` item. Then compute set difference against the baseline **findings**,
not only `finding_count`, and group by path/code/first cause. The next report
must explicitly quantify:

1. dependency/stub/environment-only findings (including the PyYAML stub);
2. unchanged Main findings;
3. changed Timeline findings; and
4. any missing-baseline findings that are actually removals or message changes.

Until that capture exists, Gate7 remains RED and these four briefs remain
pending classification. This task made no source, test, dependency, stub,
baseline, or checker-configuration changes and ran no rerun, mypy, full suite,
or product test.
