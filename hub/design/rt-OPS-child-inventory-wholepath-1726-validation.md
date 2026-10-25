# Whole-path inventory investigation

Verdict: `SOURCE_CONFIRMED_PRODUCER_SEAM; ACTUAL_LAYOUT_EXACTMISSING`.

The retained Farm refusal is the ordinary embedded `STORE_VERIFY` predicate at
`make-child-venv:1192`: `maker provision report differs from authenticated
installed inventory`. It is not the classifier and not a source-census refusal.

## Exact producer seam

`STORE_BUILD` creates the authenticated source carriers and installs both
distributions from `.source-inputs/{agent,runtime}.tar` (`626-641`). It then
creates `.astrid-distribution-metadata` from `importlib.metadata` and PEP 610
provenance (`665-700`), but creates the report's `pip_freeze` section by
capturing raw `pip freeze --all` output (`702-704`).

After relocation, `STORE_VERIFY` independently reconstructs the complete
inventory report (`1177-1192`): it normalizes distribution names with
`re.sub(r'[-_.]+', '-', name).lower()`, derives source lines from authenticated
`direct_url.json` plus archive hashes, preserves third-party metadata names,
and sorts the resulting rows. Any difference between raw producer output and
that canonical reconstruction reaches line 1192. The smallest exact seam is
therefore the producer report serializer at `702-704`; no verifier ignore or
source-ownership relaxation is supported by the evidence.

## Whole-path static result

- Source carriers: exact Git archives are retained under `.source-inputs/`; the
  retained source snapshots are separate committed-file trees.
- Installation/provenance: distribution name, version, direct provenance,
  archive digest, and provenance kind are emitted before relocation.
- Relocation: import-origin paths, `direct_url.json`, its RECORD row, launcher
  RECORD rows, report, and distribution metadata are rewritten from staging to
  final paths before the read-only-source stage (`820-887`).
- Remaining verifier predicates (`1154-end`) all remain active: source-tree
  file ownership; exact source/client markers; closed distribution metadata;
  exact report identity fields; canonical import origins and distribution
  inventory; report size/non-executable checks; and returned root inventory.
- The production caller extracts the embedded verifier, calls `verify`, then
  uses normal `Store.ensure('child', ..., verify, seal=seal)` and only invokes
  registration after verification. The diagnostic branch retains all register,
  adopt, reuse, publish, ready, and body barriers.

## Observed limits

The Farm log records all build stages through `readonly-source`, then the line
1192 refusal. The retained `child-717e53d7` tree is not present in this
worker's read-only environment, so the actual mismatching report field/path
cannot be recovered or reconstructed. Earlier review 1651/source 1643 was
source-only and explicitly marked the actual layout `EXACTMISSING`; its private
archive fixture passed, but that is not actual Farm acceptance. No build,
install, package acquisition, registration, collector, provider, body, or
retry was run here.

Static checks passed: `bash -n`, AST compilation of all seven embedded Python
blocks, production-caller assertions, protected-source hash comparison, and
`git diff --check`. Product tests/typecheck/lint were not run per the brief.
