# Scanner 1.0.6 required Agent fixes — ORCH report

Completed offline on Linux. **UNPUBLISHED REVIEW CANDIDATE**, held for manager + Agent review. No repository files changed, no commit/merge/push, and no owner data used. Assigned Agent worktree remains clean at `ef6eec5572c5c0def7ca8a22c14caa12f24f0b82`.

## Changes

Started only from the exact four members of `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/artifacts/owner-film-viewing-tools-v1.0.5.tgz`, SHA256 `1d5b3df5d85d32319d806e7d4f213d362b2f635b576b222514b9988243c87b60`. That archive remains unchanged.

- Audio findings now prefix fade and curve source paths with the record's actual input path, including parent payload/config clips and occurrence-child internal revision clips. Property names stay unchanged; track and asset paths retain `projected.`.
- Malformed transition shapes and codec exceptions now add a bounded source-path error and make the report `incomplete`, rather than silently producing a complete empty inventory. Exception messages and malformed authored values are never copied. Absent/null transitions still mean no declaration; valid incoming mappings and free-form string IDs/types still inventory unchanged.
- The source-index helper refuses repeated internal revision IDs instead of resolving them last-wins. Scan-time closure validation still uses the ONE existing Agent projector. No whole-authoring validator or ID grammar was added.
- README now explicitly states that asset IDs appear in source paths and authored transition IDs/types are emitted as free-form strings. Version changed once to 1.0.6.
- Preserved the 24 baseline cases, with only the defective ambiguous-index test corrected to use a distinct unused revision ID when proving source-list position and occurrence identity. Separate regressions assert both identical and conflicting duplicate IDs are refused. AST comparison confirms all other original test functions/helpers are unchanged; conftest is byte-identical. Added 12 ordinary cases, no new xfail/skip markers.

The diff is `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m4-scanner-agent-required-fix/1.0.5-to-1.0.6.patch`. Canonical source files are in `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m4-scanner-agent-required-fix/delivery`; flat review copies are `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-viewing-scanner-final-1.0.6-{scanner.py,tests.py,conftest.py,README.md,metadata.json}`.

## Review qualifications and count correction

**1.0.5 ships 24 ordinary tests, not 25.** Its test file has no xfail markers. The manager's 25-pass selection was those 24 **plus one separately selected flat independent audit**, with `--runxfail` to execute that audit's pre-existing strict-xfail test body. The Agent reviewer ran only the shipped 24 and did not run the external 25th; its inference that the manager's combined 25 count was unreproducible missed the additional selected file. This report does not claim 25 shipped tests.

The unchanged external audit is `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-vw-m4-scanner-v103-independent-review-audit-tests.py`, SHA256 `d2054eb92024a621fb6ec0929e3f8e845a15c170ccf3446c0a58887cd2434313`. It imports the canonical `tests/test_owner_film_cliplook_scan.py` next to `owner_film_cliplook_scan.py`; those names are retained. The combined run below explicitly selected it and actually executed its assertions under `--runxfail`: **37 passed**, zero xfailed/skipped.

One review detail is narrower than inferred: on this qualified Agent checkout the canonical projector already rejects duplicate internal revisions (`astrid/core/timeline/shot_composition_projection.py`, internal revision index construction). Thus end-to-end duplicate scanning was already incomplete. The actual red-before defect is the scanner's directly callable source-index helper selecting a duplicate row. Its guard is now explicit and narrow, and end-to-end incompleteness is retained. The private commit codec's broader authoring/digest validation was inspected and deliberately not added to this scanner.

## Exact validation commands and results

All targeted runs use the maintained Agent dependency environment and this assigned worktree's code. These are scanner-only tests, not an Agent full suite. Variable definitions expand to absolute paths:

```sh
W=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m4-scanner-agent-required-fix
A=/home/user/work/wt/vw-m4-scanner-agent-required-fix
P=/home/user/work/venv-agent/bin/python
AUDIT=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-vw-m4-scanner-v103-independent-review-audit-tests.py
```

1. Unchanged 1.0.5 shipped selection:

```sh
PYTHONDONTWRITEBYTECODE=1 "$P" -I -B -m pytest -q -p no:cacheprovider "$W/base-1.0.5/tests/test_owner_film_cliplook_scan.py" --agent-root "$A"
```

**24 passed in 5.41s**; `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m4-scanner-agent-required-fix/logs/base-1.0.5.log`.

2. Red-before: new 1.0.6 regressions + corrected index fixture against unchanged 1.0.5 scanner source, before applying scanner fixes:

```sh
PYTHONDONTWRITEBYTECODE=1 "$P" -I -B -m pytest -q -p no:cacheprovider "$W/delivery/tests/test_owner_film_cliplook_scan.py" --agent-root "$A"
```

**10 failed, 26 passed in 5.73s** (expected): four parent/config + incoming/outgoing audio-path cases, three malformed transition cases, one codec exception, and two identical/conflicting duplicate source-index cases. `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m4-scanner-agent-required-fix/logs/red-before.log`. Reproduce that historical state by running `add-regressions.py` against a fresh copy of the four source members before `apply-fixes.py`; the scripts record the sequence, not a current red test expectation.

3. Final 1.0.6 shipped selection, same exact command as (2) after scanner fixes:

**36 passed in 5.51s**; `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m4-scanner-agent-required-fix/logs/ordinary-1.0.6.log`. Includes unchanged relocated CLI execution with only PATH/PYTHONNOUSERSITE in its environment, same-path/symlink/hardlink output protection with input hash+mtime preservation, optional asset=None clear preservation, opaque-data redaction, rational FPS/half-open intervals, known/unknown cases, and the new regressions.

4. Final shipped suite **plus separately selected unchanged independent audit**:

```sh
PYTHONDONTWRITEBYTECODE=1 SCANNER_CANDIDATE="$W/delivery/owner_film_cliplook_scan.py" SCANNER_AGENT_ROOT="$A" "$P" -I -B -m pytest -q -p no:cacheprovider --runxfail "$W/delivery/tests" "$AUDIT" --agent-root "$A"
```

**37 passed in 5.63s**; `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m4-scanner-agent-required-fix/logs/ordinary-and-independent-audit.log`.

5. Lint (repository's Python target and selected rules, explicit files outside repo lint include scope):

```sh
/home/user/work/venv-agent/bin/ruff check --no-cache --isolated --target-version py311 --select E4,E7,E9,F,I,BLE "$W/delivery" "$W/add-regressions.py" "$W/apply-fixes.py" "$W/build-candidate.py" "$W/write-report.py"
```

**All checks passed**; `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m4-scanner-agent-required-fix/logs/lint.log`.

6. Deterministic build and archive/member checks:

```sh
python3 -I -B "$W/build-candidate.py"
```

**PASS**: two in-memory ZIP/TGZ builds byte-identical, each exactly four canonical files, ZIP and TGZ member bytes equal tested delivery files. Fixed timestamps/modes/order/owner metadata; gzip filename empty. `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m4-scanner-agent-required-fix/logs/build.log`. Baseline-function AST preservation, unchanged conftest, and unchanged source TGZ also pass; `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m4-scanner-agent-required-fix/logs/preservation.log`. Generated bytecode was removed from the assigned Agent worktree; `git status --short` is empty.

## Exact artifacts and hashes

Archives remain in this worker's ORCH directory, outside the repository and unpublished. Nothing was placed into the shared published-artifact directory. Metadata: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m4-scanner-agent-required-fix/metadata.json`.

| Archive | Bytes | SHA256 |
|---|---:|---|
| `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m4-scanner-agent-required-fix/archives/owner-film-viewing-tools-v1.0.6.zip` | 16038 | `f07cb7b3df199244b7284c4a7a4e280a016e75312561d03f1e8a005057b82192` |
| `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m4-scanner-agent-required-fix/archives/owner-film-viewing-tools-v1.0.6.tgz` | 14659 | `1df2ee0a64709b1a275fcd8aa0a8937979f7fbe6b99e341aa309ae0cb48cefa3` |

Exactly four members in each archive:

| Member | Bytes | SHA256 |
|---|---:|---|
| `README.md` | 5347 | `fb77b4f2afccd556885bf5be3574430bd105b353f11063637fa913475da9bc90` |
| `owner_film_cliplook_scan.py` | 32861 | `e241041756cd5eb4657fa37bd5631eff08276eb3fb457973e162a35b65d49f9e` |
| `tests/conftest.py` | 385 | `ea7d84927b97d78e2eb17fa87180ce2b7591f2c53645d1799b99f2c34197e430` |
| `tests/test_owner_film_cliplook_scan.py` | 24188 | `d643cac596c42e8591a0c213aee78fa3675be797625fb8426afb89bca88daae8` |

## Decisions, limits, and next steps

Used bounded closure errors for unreadable transitions, as explicitly permitted by the review, rather than adding a new semantic category or copying malformed data. Kept the canonical projector as the only projection/closure authority; the extra duplicate guard addresses only this utility's emitted-source index. Preserved free-form IDs, opaque authored fields, optional clears, and all prior passing behavior outside the explicit duplicate policy correction.

No blockers. No full suite requested/run; no browser, sockets, database, media, network, install, owner-film access/copy, macOS verification, or owner closure-matching environment claim. This is synthetic scanner evidence, not film cleanliness or render parity evidence.

Next: manager reviews the minimal patch and exact candidate hashes, then Agent re-reviews 1.0.6. Keep unpublished until both reviews approve; only then can the owner run the existing qualified-environment command on a local immutable closure duplicate.
