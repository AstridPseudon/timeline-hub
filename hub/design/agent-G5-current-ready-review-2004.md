# G5 current-ready independent readiness review — 2004

## Verdict

**PASS — bounded source/readiness review.** The current draft is mechanically
ready as the reviewed G5 source port, with no scope or identity finding. It is
still **DRAFT / P1 NO-GO**. This review does not approve activation, deletion
beyond the draft, or whole-G5 qualification.

The owner-run combined FIVE is **not PASS**: it terminated with 4 passed and 1
setup error before the c271 body. Its evidence is audited below and remains
unverified for that node.

## Scope and source custody

- `HEAD` is `f120159fae86b5fb1e5379437737b4e0a16627eb`, with sole parent
  `07e6d83df69146c7dddea207f32330dc8b58dbc5` and no worktree changes.
- The base-to-HEAD manifest is exactly 50 paths: **43 modified, 6 added, 1
  deleted**. `document_diff.py` is the sole deletion.
- The joined reviewed source is `f27d524798b14d11bcbe654ce7eee49d47e0b739`.
  Every allowed HEAD path matches its source blob/deletion exactly (50/50,
  zero mismatches). The full HEAD/source tree delta is exactly one path:
  retaining `tests/editing_conformance/test_a4_parent_media_raw_witness.py`.
  That witness is byte-identical to the base (`5aafdc44…`) and is absent from
  the source tree as required.
- The review-chain path union is independently exact: current-final 47,
  docs 1, c271 2, restore 1, union 50; both set differences are empty.
  The later history/restore and mirror source blobs are the exact joined
  `f27d` blobs. No donor ancestry or report artifact entered the tree.
- The base has 3,431 tracked paths; the exact diff contains no outside-scope
  changes. The own branch contains one commit only.

Protected custody checks passed. R1 core files, inverse core, media transcript,
all three A4 track/transcript/raw witnesses, generated client, `.env.example`,
runtime lock, artifact manifest, registry lock, and frozen schema/artifact are
base-identical. The schema digest is `d106dfe8…`, the Composition artifact is
`819acf6b…`, the client/runtime schema digest remains
`sha256:35c2d9c5…`, and vendor lock validation matches producer
`rt-pin-34eac004` (`34eac004…`). The actual artifact hash matches its recorded
`819acf6b…` value.

Reviewed body/baseline authority is exact for `_step_undo.py`, the c271 mirror
test, the 68fbe restore test, and both Ruff/mypy baseline files. The 68fbe
adaptation remains the narrow receipt-identity correction: it binds
`base_parent.publication_id` to the restore receipt while retaining exact
closure/document/source-mapping assertions. The D14 equal-text undo tests are
unchanged; the D23 child-word positive remains visible and unskipped; no added
skip/xfail/deselection or refusal conversion was found. Deferred V4 behavior
remains preserved and unqualified.

## Checks run

The mandated five-file selector was run once, exactly, with no trailing dot or
marker filter:

```sh
PYTHONDONTWRITEBYTECODE=1 ASTRID_RUNTIME_CHECKOUT=/home/user/work/wt/rt-pin-2a9e347f PYTHONPATH=.:/home/user/work/wt/rt-pin-2a9e347f /home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider tests/editing_conformance/test_captured_config_root_mirror.py tests/sdk/test_g5_retained_sheet_basis.py tests/editing_conformance/test_inverse_aba_partition.py tests/editing_conformance/test_transient_root_baseline.py tests/editing_conformance/test_a4_parent_media_raw_witness.py
```

Result:

```text
71 passed in 22.82s
```

Scoped Ruff command (the 46 paths came from the base-to-HEAD diff) returned
exit 1 with 112 findings. The same command from the reviewed `f27d` source
produced the same 112 diagnostic identities exactly (normalized only for
checkout path), with zero added findings. Private mypy over the 15 changed
Agent modules returned exit 1 with 104 errors; the reviewed source produced the
same 104 identities exactly, again zero delta. Existing whole ratchets are
therefore reused by source equality: Ruff 2148 and mypy 1911; no broad ratchet
was duplicated.

```sh
changed_py=$(git diff --diff-filter=AM --name-only 07e6d83df69146c7dddea207f32330dc8b58dbc5 f120159fae86b5fb1e5379437737b4e0a16627eb5 | rg '\.py$')
/home/user/work/venv-agent/bin/python -m ruff check $changed_py --output-format=json --no-cache
mypy_paths=$(git diff --diff-filter=AM --name-only 07e6d83df69146c7dddea207f32330dc8b58dbc5 f120159fae86b5fb1e5379437737b4e0a16627eb5 | rg '^astrid/.*\.py$')
PYTHONPATH=. MYPY_CACHE_DIR="$TMPDIR/g5-diagnostic/mypy-current" /home/user/work/venv-agent-typecheck-v2/bin/python -m mypy $mypy_paths --hide-error-context --no-color-output --no-pretty --show-error-codes
```

Also passed:

```text
PYTHONPATH=. /home/user/work/venv-agent/bin/python scripts/vendor_lock.py check runtime.lock.json --producer /home/user/work/wt/rt-pin-34eac004
PYTHONPATH=. /home/user/work/venv-agent/bin/python scripts/artifact_manifest.py --check
git diff --check 07e6d83df69146c7dddea207f32330dc8b58dbc5 f120159fae86b5fb1e5379437737b4e0a16627eb5
```

Both before and after import probes resolved the actual backend
`runtime_protocol` from `/home/user/work/wt/rt-pin-2a9e347f`, commit
`2a9e347ff…`, tree `f79a2355…`. The added-diff high-confidence credential scan
found zero matches. Exact retired identifiers (`commands_file`,
`publish_bundle`, `store.three_way`, `document_diff`, separate-publish,
`--publication`, `apply --native`, and `timelines publish`) are absent from
active production Python. Remaining “three-way” prose is descriptive text,
not the retired writer. Production callers continue through the session/emitter
commit boundary. The preserved request mapping includes `api_version`, exact
scope/project/timeline and base revision/publication pair, commands, label,
per-step patches and reads, merge, declared reads, idempotency key, and
`dry_run`; accepted/merged replies carry canonical document, full receipt,
records, bindings, effects, dependencies, history, and undo steps, while
preview carries `would_status` and a null receipt and refusals carry structured
errors. `show --native --as sheet` is the retained read projection, and no
`apply --native` writer exists.

## Owner-run FIVE audit and limits

The terminal `agt-G5-final-five-2002` packet was audited without rerunning its
bodies. It selected exactly 5/5 explicit nodes with 0 deselected and no
`-m` filter. The actual run was **4 passed, 1 setup error in 92.81s**. The
c271 test body was unreached: setup asserted that `runtime_protocol.__file__`
was the pinned `rt-pin-2a9e…` checkout while `use_runtime()` selected a
temporary authentic archive. This is a harness/fixture identity mismatch, not
evidence for a source or Runtime change, and no retry was made.

The packet has 61 members, 4,794,006 bytes, and SHA-256
`a44b8b3af9077e085828e307351ce39eb81979c083713f31e03576fa59485ea8`. The
preflight reports archive SHA
`2915bd4ac0d46954d19c30f87a517b82074218699978e650fab03fcba81b72d3`, exact
body locks for all five nodes, correct Agent/Runtime/client identities, and
credential scan 0. The observer recorded 56 seam entries/exits, zero seam
exceptions, zero observer failures, and zero origin mismatches. The owner
reports no source/test/Runtime/pin changes, no writes to expectations, no
retry, and no prohibited suite. These are custody/results facts only; they do
not turn the setup error into a FIVE PASS.

Not run here: full suite, browser/live sockets, P1/P4, public redo, FOUR,
c271 redo, or any prohibited lane. The next required evidence is an owner-run
resolution of the c271 setup-origin mismatch and a separately authorized
qualification on the exact reviewed source. Until that and actual P1 GO,
lane management must keep G5 unmerged and inactive.
