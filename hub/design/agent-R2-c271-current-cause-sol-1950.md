R2 current root guard cause — classification 2; current port HELD; G5 DRAFT / P1 NO-GO.

The exact captured failure depends on unmerged G5 native/state mechanics. No ordinary supported current-caller R2 defect was established. No source or test was changed, no guard was bypassed, and no retirement ancestry was imported. This completes the authorized causal classification; it does not qualify the current port or the G5 draft.

Read PLAN §3 R2/G5, C0 §§2–5, the 1933 repair report, the 1944 current-port report and worker report, and the 1924 report and complete packet manifest. Verified the complete original archive and all 72 file members against that manifest. The original c271 body was not run.

The one reproduction

From `/home/user/work/wt/agt-R2-c271-current-cause-sol-1950`:

```sh
PYTHONDONTWRITEBYTECODE=1 ASTRID_RUNTIME_CHECKOUT=/home/user/work/wt/rt-pin-2a9e347f CAUSE_EVIDENCE=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-R2-c271-current-cause-sol-1950/evidence/guard-capture.json PYTHONPATH="$TMPDIR/cause":.:/home/user/work/wt/rt-pin-2a9e347f /usr/bin/timeout 30 /home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider -p cause_capture tests/editing_conformance/test_captured_config_root_mirror.py::test_captured_config_root_redo_preserves_exact_history
```

Result: **1 failed in 0.60s**, once, offline. Durable stdout/stderr: `evidence/reproduction.log`. The observation-only pytest hook reads failure traceback locals after execution; it does not replace functions, alter records, install G5 code, or modify source. Its exact source is retained in `evidence/cause_capture.py`.

Stack: test line 202 → `commands.py:254` → `inverse.py:889` → `_root_inverse.py:198` → `_recording.py:286`. Error: `original authored guard changed`, kind `history_unavailable`, ref `parent`, path `['occurrences']`. The test's preliminary `inverse_stages()` assertions succeeded; the observed refusal is during actual `execute()` root-baseline restoration, not the mirror-partition assertion.

At the failed guard:

- Expected: present full occurrence rows ordered `chapter-shot-837324ae5797370162ac-occ`, `occ-film`, `chapter-shot-3f756cd1547d015ebd4b-occ`.
- Actual: exactly `{'state': 'absent'}`.
- The detached projected bundle's `placements` equals the complete expected row array, including every authored field. This is an address/projection mismatch, not a changed owner or changed occurrence bytes.
- Its parent has only `clips`, `config`, `opaque`, `registry`; there is no stored `occurrences` parent member.
- The failing accepted native write is zero-based index **3**, `parent/occurrences`, after config, registry and clips writes. It reorders those three rows to `occ-film`, first chapter, third chapter. Later writes remove the third occurrence, restore `occ-film`, remove the first occurrence, restore `shot:film`, and remove the two chapter shot roots.
- The root being restored is `shot:chapter-shot-837324ae5797370162ac`. Its physical shot/internal revision pins, source mapping, source/landing owners, accepted before/after documents and projected stage are retained without filtering in `guard-capture.json`.

Actual source identity and ranges

Scope is project `704b309863a44d64b80d1a11a078db4b`, timeline `t`. Accepted forward is `txn-dca405e7f44942b0a5818dd683a3a009`, command `timeline.restructure`, revision `authoring-parent-revision-77cdbab23556f4cf1be87de1914499675d54a3788a2caf7f4df2a7e06cf4fd5b`, digest `sha256:9e2c37ed6967eda37b007901e6b12f7bc38544ef262fbf67ec65dda83761ac76`. It has one `restructure-0` step, ordinal `[0]`, 10 native writes, 9 effects and zero derived writes.

Accepted whole undo is `txn-d59a7caf610544b5a747c99cc8a67d58`, command `timeline.inverse`, revision `authoring-parent-revision-306f5597077eed2194e4eb8a75fb381e9568b6e2e46b8dff49cc7f8c4d57db2f`, digest `sha256:0a55a7d9d7e1c0ebbea6141c6cbf4446aacc8c55158be628b0c977643402205f`. It has one `inverse` step, ordinal `[0]`, 10 native writes, 9 effects and zero derived writes. Its inherited binding is exactly the forward publication, `restructure-0`, ordinals `[0]`, native range `[0,10]`, effect range `[0,9]`.

The captured redo request's full scope/base pair points to that undo. It has idempotency key `inverse-redo`, one public `timeline.inverse` command, label `Undo timeline edit`, step `inverse` with its submitted empty patch, merge `fields`, and `dry_run: false`. No request `reads` key was invented. Both selected complete entries equal the original packet's accepted history entries, context equals the original context, and both canonical documents occur byte-equivalently as parsed JSON in the complete source packet. Receipt, records, effect/dependency/ownership/native structures were retained, not regenerated.

Exact causal dependency

1. Current `07e6d83df` `_command_state.State.get()` resolves ordinary parent dictionary members. It does not project `parent/occurrences` from `bundle['placements']`.
2. G5 `89c38c935` adds exactly that projection at `State.get()` plus a `State.set()` branch that only permits permutations preserving every authored occurrence row. The State diff is 13 lines. These mechanics are absent on current and absent from the two-path `70be` port.
3. G5 registers a new `timeline.restructure` operation in `commands.operations()` and adds `native_restructure.py`. Its recorder explicitly reads/writes `parent/occurrences` after native occurrence/root work to capture the reorder. That is the actual source of this captured write. Current has neither the registration nor this module.
4. `_root_inverse.restore_root_baselines()` replays accepted native writes into a detached plain `State` using `guard()` and `State.set()`. The unchanged replay therefore works with G5's global occurrence projection but cannot interpret this new native address on current.
5. Current `inverse.py` already has a narrower `_physical_state()` / `_recording_storage()` view for authenticated inverse application with an address resolver. That does not establish an ordinary current producer of this accepted G5 native history. Extending or bypassing the root replay on this evidence would import support for an unmerged native/state capability, not demonstrate a bounded ordinary-current regression.
6. Current `doc.patch` refuses whole occurrence membership/order paths in `validate_submitted_change()` and `Closure.native_sites()`. Allowed occurrence leaves record at occurrence-local native addresses. Current `timeline.duplicate` removes `occurrences` from its parent-copy payload and records occurrence creation individually; it does not emit this whole-parent reorder. No meaningful supported current producer of this captured aggregate/root-removal sequence was found in the inspected command sources.

The G5 `_doc_patch.py` diff extracts the existing guarded payload implementation into `apply_change()` for new G5 caller use; the existing patch handler then calls it. That extraction is not on this failing stack and does not explain the absent state. It is not a proposed repair. The relevant State/registration/native source delta appears in G5 draft refresh commit `c59a751774cf74267daab779f6e3dc2604fc3993`; it is not present in current `07e6d83df`.

Eight-path comparison

`evidence/identities-before.json` contains full Git blobs and SHA-256 identities for current, G5 base, reviewed `70be`, and this worktree, plus the four state/command differences and captured test. All eight reviewed core preimages match between `07e6d83df` and `89c38c935`. `_root_inverse.py` is `30f6d7803e1a76ecdcda1daf3c6d8496c7ea4d57` and `inverse.py` is `1b551173ebdf7a31a012573a92a02190918218ca` throughout. `_step_undo.py` preimage is `db1dd6cc09a6f9b7cf59f8af9e49cdb9d682eb74`; current port and reviewed repair are both `0bdefdb813c9ffcbe94c7a627512784e60da3532`. The other five core guard/partition test blobs also match exactly. The captured test is `9d3e3330b24dba2e3c2b9d5e14c0e46677c30fa5` in both the port and reviewed repair.

This worktree HEAD is `8caee1bc9fb31b9c49b9ee75c4a99786fb0fe129`, tree `a27dc4f81db6db42fff4bba38650c64195727d60`. Before/after working source identity changes: **0**. Git status: clean. Diff outside the existing port's two paths versus `07e6d83df`: empty. No guard, accepted-history, digest, physical pin, owner, ABA, ordering, range, collection or causal-derived-observation rule was changed.

Evidence and integrity checks

Worker evidence directory: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-R2-c271-current-cause-sol-1950/evidence`.

- Complete original packet archive retained losslessly there: `g5-c271-complete-packets.tar.gz`, 9,182,178 bytes, SHA-256 `502266a70f0d1a3cb21d354e9cce01245acb39ea014649fe528039e997de1e8c`. All 72 file members match the original manifest. Scratch extraction of only `058-provider-entry.json` stayed in `$TMPDIR`; its 4,951,445 bytes have SHA-256 `9056bdaa7926863a3c44d24a0303a6b3c790067623842f13e7f85bb2357974cd`.
- `guard-capture.json` retains full actual failed-frame state, source/accepted boundaries, native record, binding/ranges, physical pins and original minimum fixture. `dependency-audit.json` retains archive member hashes, request/source summary, exact guard images, identity/origin checks and credential results. `evidence-manifest.json` gives file SHA-256 digests.
- Actual loaded Agent inverse modules originate in this worktree. Before/after actual `runtime_protocol.auth` and `runtime_protocol.timeline_commit_auth` originate at `/home/user/work/wt/rt-pin-2a9e347f`, hashes respectively `f45941cfee9dbda8262163b7e5fcabbe457a62f4beab8a1521292f7cdfb2246a` and `3b812936efaa35a165c056fbacee6d8e699d485ca912f12e11cc4cd4bbe8f2ef`; origin/hash changes **0**. Runtime HEAD/tree remain `2a9e347ff0e1df1dedff5ab7b59ddb27dfe3129d` / `f79a2355cfb39d9ada7721978bd20d5702105778`.
- Original packet credential findings `[]`; bounded credential-pattern scan of worker JSON/log/diff evidence: **0** findings. This is a pattern scan, not a claim to detect every possible secret.

Exact additional check commands:

```sh
PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-agent/bin/python scripts/vendor_lock.py check runtime.lock.json
PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-agent/bin/python scripts/artifact_manifest.py --check
git diff --check
PYTHONDONTWRITEBYTECODE=1 ASTRID_RUNTIME_CHECKOUT=/home/user/work/wt/rt-pin-2a9e347f PYTHONPATH=.:/home/user/work/wt/rt-pin-2a9e347f /usr/bin/timeout 30 /home/user/work/venv-agent/bin/python "$TMPDIR/cause/audit.py"
```

Results: `ok runtime.lock.json`; `artifacts.json is current`; whitespace check clean; audit **PASS** (72 files verified, source changes 0, origin changes 0, credential findings 0, outside-scope diff empty, clean worktree). The audit script is retained in evidence. No source changed, so no scoped Ruff/private-mypy repair baseline is claimed or needed. The 1944 report's scoped checks and 51 PASS / 1 FAIL are prior-worker evidence, not rerun results.

Decision, limits and next step

Classification **2**, as required: stop without product/test changes or an original-body retry. A bare two-path port is not independently executable for this captured history on current; keep it **HELD**. There is no basis here for a Runtime fix, a mirror change, an inverse guard waiver, pin injection, equal-byte retargeting or a new allocated root. No plan decision was changed. A complete supported-current-caller request/receipt/preview compatibility claim is unverified; this task does not manufacture that caller.

No additional 20/52/143 selector was run after classification, because the branch requires stopping without a code repair. No full suite, HTTP/browser/socket suite, public undo/redo journey, original c271/FOUR/P1/P4/9/14/40/281/58 body, integration write, dependency install, environment mutation, Git write or merge request was performed.

G5's draft can still be reviewed and qualified with its actual state/native prerequisites. Keep P1 NO-GO and do not pull retirement ancestry before P1 GO. Recommended orchestrator action: record this dependency against the held current port, retain G5 review on its own draft base, and do not dispatch a current guard relaxation based solely on this capture. No further worker action is blocked; the bounded diagnostic task is complete.
