# G5 SDK FOUR independent readonly review

## Verdict

- Fixture/source fidelity: **PASS**.
- Original FOUR behavior: **FAIL — 3 failed, 1 passed in 22.43s**.
- No product, Runtime, contract, generated, pin, dependency, Git, daemon, or
  test changes were made. No live body was rerun.

The passing body was
`test_open_bundle_keeps_http_rows_raw_and_round_trips_canonical_images`.
The three failing bodies were the retained-history inverse/redo,
retained-draft restore, and catalog-recover/restore cases. Each reached the
normal authenticated move/setup acceptance boundary, then the provider
rejected inverse/restore validation with:

```text
candidate.timing: legacy word anchor is missing
code=validation_error path=[] reason=invalid_document status=invalid
```

## Authority and custody

- Reviewed Agent target: `dc5c84b9a31082f877401865efeaa3be3fe6b12a`,
  based on `9da584010a4c14c1f80ed66131083c5f407aa529`.
- The target diff changes only
  `tests/sdk/test_timeline_checkout_history_runtime.py`.
- Current target-file SHA-256:
  `02cd704852b9da1b76c58253eaf385e74177202cce97fa585c4ab722e8a3b4df`.
- All four original test function AST bodies are identical to the parent
  commit. The fixture change is setup/metadata only; no assertion or body was
  weakened.
- Authentic archive SHA-256:
  `2915bd4ac0d46954d19c30f87a517b82074218699978e650fab03fcba81b72d3`.
- Qualified Runtime source: commit
  `d9e2a71e87c827290a3ff58a94f6fb8b4bc11e0b`, tree
  `9b07545cac9a8bbafb16246aaa6f72050ef7cffe`.
- Restored authentic pair: parent revision
  `a3e671256f1c42b8837d3e118c97b21b`, publication
  `txn-11c90075be6c4c8bb9e2627366f0fe4f`, digest
  `sha256:b6069d1ddccc0279e871b142773b63b73b107ebf9d0adc11ab73832b69097afb`;
  predecessor is `film-parent-v1` / `txn-55c0651b2cd64255ae06e73f9708220a`.
- Provider packet:
  `g5-sdk-authentic-four-1649-provider-failure.md`, SHA-256
  `bb4b6dbd0d98bc11f60a28a76db4525515cd1aea98c8a849cd15cb0e0b826eda`.
  It retains all three failing request bodies and partial canonical/history
  facts, but no prepared response was exposed.
- The author’s private outbox/realm/capture paths were harness-owned and are
  gone. No lossless prepared/base/output packet is claimed. The causal
  reconstruction below is explicitly source-backed and reconstructed from the
  retained archive, packet, and production functions; it is not a recovered
  raw capture.

## Precise cause

The authentic archived parent has the following `music-bed` aliases in both
`parent.clips` and `parent.config.clips`:

```text
app.on                    = "word:word-1"
app.until                 = null
app.until_film_end        = true
app.astrid.on             = "word:word-1"
app.astrid.until          = null
app.astrid.until_film_end = true
app.astrid.fixed_start    = false
app.astrid.for            = 5.5
```

The normal SDK writer is not losing these bytes accidentally. In
`astrid/sdk/timeline/capture.py:228-232`, `move()` explicitly clears
`app.on`, `app.until`, `app.until_film_end`, and their `app.astrid` mirrors,
then writes `app.astrid.fixed_start=True` and `app.astrid.for`. The generated
move record contains the exact prior values for every one of those fields.
This is the existing `anchor=fixed` move policy.

A source-only execution of the production command engine against the retained
authentic canonical document confirmed:

1. A truly unrelated `music-other` move leaves both `music-bed` alias objects
   byte-identical.
2. The selected `music-bed` move produces only the intentional fixed-start
   form, with both legacy `word:word-1` declarations absent.
3. Applying the move record’s recorded `before` values back to that post-move
   candidate recreates the original aliases in both parent representations.
4. `validate_final_candidate(restored_candidate, baseline=post_move_head)`
   returns exactly `candidate.timing: legacy word anchor is missing`.

The causal validation path is existing source:

- `astrid/sdk/timeline/commit.py:1030-1063` loads authenticated inverse
  boundaries and exact restore closures; it does not synthesize a document or
  accept caller-supplied inverse writes.
- `astrid/sdk/timeline/inverse.py:609-700` restores each inverse write from its
  authenticated `before` value.
- `astrid/sdk/timeline/_commit_timing_validation.py:245-264` grants a D12
  exemption only when the candidate declaration equals the current baseline’s
  declaration and its basis is unchanged. After the move, the baseline has no
  declaration, so the restored declaration is treated as newly authored.
- `astrid/sdk/timeline/native_word_anchor.py:136-170` then searches the
  retained transcript sources; the authentic dependency manifest has no
  transcript document, so the legacy lookup correctly reports “legacy word
  anchor is missing.”

## Classification and handoff

- **Normal SDK writer byte preservation:** PASS for an actually unrelated move
  (`music-other`); FAIL is not caused by unrelated-field serialization. The
  selected `music-bed` move intentionally clears its own timing declaration.
- **Inverse emission:** source PASS. The inverse path emits the authenticated
  prior bytes, including both legacy aliases; it does not omit or rewrite the
  declaration.
- **V2 dependency/baseline handling:** FAIL for authenticated inverse/restore
  of this accepted legacy state. The current-head baseline overcounts the
  restored historical declaration as new instead of recognizing its exact
  authenticated source boundary.
- **Real new invalidity:** not established and not the best classification.
  The declaration is present in the accepted authentic source and is restored
  from accepted history; it is not a newly authored word reference. The move
  itself is a real semantic timing change and its fixed-start clear is present
  in the recorded writes.

Primary owner handoff: the V2/R2 validation boundary in
`_commit_timing_validation.py` and its `commit.py` baseline/source-boundary
caller. Preserve the existing refusal for genuinely new or changed legacy
word declarations. Do not remove the inverse writes, weaken `legacy_binding`,
or change Runtime authentication. If the intended policy instead says a move
of an anchored clip must retain the anchor, that is a separate concrete policy
question because the existing move command explicitly declares fixed-start
semantics; no such contract decision is made here.

## Commands and evidence

Retained original FOUR command (from the provider packet):

```text
ASTRID_RUNTIME_CHECKOUT=/home/user/work/runtime PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.:/home/user/work/runtime /home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider -m integration tests/sdk/test_timeline_checkout_history_runtime.py
```

Result: `3 failed, 1 passed in 22.43s`. No rerun was made.

Review commands run:

```text
git diff --check HEAD^ HEAD
git diff --name-status HEAD^ HEAD
AST comparison of the four test bodies against HEAD^
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.:/home/user/work/runtime ASTRID_RUNTIME_CHECKOUT=/home/user/work/runtime /home/user/work/venv-agent/bin/python -m pytest --collect-only -q -o addopts= -p no:cacheprovider tests/sdk/test_timeline_checkout_history_runtime.py
MYPY_CACHE_DIR=<private worker cache> ... python -m mypy --cache-dir=<private worker cache> tests/sdk/test_timeline_checkout_history_runtime.py
```

Results: diff check PASS; one changed test file; AST body lock PASS (4/4);
collection `4 tests collected`; mypy `Success: no issues found`.

Raw scoped Ruff on the changed file reports four inherited diagnostics (one
unused `renderer_off`, two related redefinition/import findings, and one
import-order finding). The parent file has the same diagnostic identities;
the new authentic fixture adds none. The reusable joined G5 proof remains
`184 passed`, mypy `1911/1911`, Ruff `2148/2148`; it was not rerun.

The offline causal reconstruction used the retained archive/fullraw JSON,
`bundle_from_document`, `capture_move`, `commands.execute`, and
`validate_final_candidate` only. It performed no Runtime HTTP, SQL, CAS,
history, daemon, or authentication write. No full, P1/P4, native14, original9,
public-redo, or prohibited `c271` body was run.

## Next step

Keep G5/P1 **NO-GO**. Send this precise red to the V2/R2 owner for an
authenticated inverse/restore baseline decision and implementation review;
retain the three failing expectations unchanged. The fixture/source review
itself is complete and does not justify merge or behavioral credit.
