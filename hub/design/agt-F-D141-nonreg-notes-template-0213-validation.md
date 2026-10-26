# F/D141 validation

Status: `PASS` for documentary evidence construction. No product, test, import, collection, typecheck, lint, Farm cut, or join execution was performed; those are `NOT APPLICABLE` or intentionally pending.

## Standard-library validation

Command:

```text
python3 - <<'PY'
# stdlib JSON/hash/membership assertions over per-id-template.json,
# source-manifest.json, retained D134 root JSON/TSV, and retained pristine per-ID JSON
PY
```

Result:

```text
PASS rows=370 roots=52 unique=370 source_inputs=14 pristine_hash=exact outcomes=3082+173=3255 admission>=floor outputs=4
```

Checks included:

- 370 unique original IDs, each present once; 52 root clusters; root membership sums to 370 with no duplicate membership.
- Named-slice accounting is non-additive: media48 remains nested in managed105/root-019.
- Exact retained pristine per-ID SHA-256 is `7535b9a70b0da2f36e2c9e2f0115cf70ef429d3b8152496a7f44a723033ae6a5`.
- Pristine inventory conservation is `3,255 = 3,082 concrete IDs + 173 explicit null-ID aggregate records`.
- D134-row pristine matches are 17 PASS, 3 FAIL, 1 ERROR; 349 rows have no exact pristine match and remain UNKNOWN.
- Upstream-presence counts are `y=21`, `n=3`, `UNKNOWN=346`; `n` is used only for exact test-file paths explicitly absent in frozen-source preflight.
- Every row has `cut_status=PENDING` and `final_classification=PENDING`.
- The task-recorded source-only admission is 4,854,058,016 bytes, which is above the 4,600,000,000-byte floor; no body was executed.

## Artifact hashes

Exact final `sha256sum evidence/*` output:

```text
fe0866d38ca7bf3002020a84ff74132d94613969519e3c47d612cddef31211cc  handoff.md
e37accbfd13153c8c92dfcb1e5cd11ed6b384325366cde7f1aaed1a0f2fc173d  notes-template.md
d3729a6a2665bfd8d0081bdb2b89004eaec1bb5c6a8de3054711fe7d9f840f10  per-id-template.json
32feeb9f5d503f246d9a6a8b8aa5143c17c0d0b79178fa83a49463f4fd9839a05  source-manifest.json
```

## Scope evidence

- `git status --short` in the assigned Composition worktree: clean; no product source or test files were changed.
- The production caller remains Runtime `commitTimeline`; Agent provider behavior remains unchanged.
- The five output files are the only requested deliverables. Current cut facts are missing, so the later join is explicitly not run.
