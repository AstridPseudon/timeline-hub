# D128 whole-path validation

Outcome: source diagnosis complete; actual offending path is `EXACTMISSING`.

## Retained observation

The preserved D131 refusal is the ordinary embedded verifier refusal
`unowned retained source directory`, after `readonly-source` completed. The
retained flat output does not include the path, and the staged child root was
cleaned. There is no evidence of a classifier, permission, or safety denial.

The exact refused request is `venv-agent-child-d131-a4e016`, SHA-256
`208ee436d087552dc055e30d85348055f2923a66b9382d1f7f0e1048ae39b6db`. The
Store entry named by the request is
`child-3e16336b6a5a2d8293a95a99c3665cbafbefb234b4b421fab53e17edde29af30`.

## Source-derived diagnosis

The canonical maker does the following:

1. `archive-agent` and `archive-runtime` extract authenticated Git archives
   into `.child-venv-source-*/agent` and `runtime` (lines 616–624).
2. With no dependency seed, it installs directly from those source
   directories (lines 626–641); the D131 log has no `build-input-directory`,
   `build-agent-input`, or `build-runtime-input` stages, so this is the branch
   the refused request followed.
3. It later constructs `root_inventory` from committed files and archive
   carriers (lines 997–1049), derives `expected_dirs` from their parent
   closure, and rejects any other retained directory (1147–1156).

Static source inspection of the pinned setuptools 80.9.0 backend shows that metadata
discovery invokes `egg_info`, whose default `egg_base` is the top of the source
tree and whose `run()` creates that directory. The smallest source-proved
generator is therefore the direct no-seed setuptools source install producing a
project `.egg-info` directory under the retained source snapshot. Candidate
paths are `agent/astrid.egg-info` and `runtime/astrid_runtime.egg-info`.

This is a source-derived generator finding, not a claim that either candidate
path was observed in D131. The actual path and retained tree are
`EXACTMISSING`; no missing record was reconstructed.

The authenticated Agent and Runtime Git archive listings were also compared:
all explicit archive directories are parents of committed files. This rules
out archive extraction alone as the proved extra-directory generator. The
earlier Farm census source independently applies the same authenticated
file-parent rule and would name the relative path if its retained root were
available; its D131 corpus is also `EXACTMISSING` and it was not executed.

## Checks performed

- SHA-256 and mode checks of maker `1243cb6c…f8afd0b`, Store helper
  `123bb93c…b7adfe2`, and dependency verifier `116b4e6b…d7bfe2`: PASS.
- Embedded verifier AST parse, marker, `root_inventory`, `expected_dirs`,
  parent-closure, directory-guard, and file-guard checks: PASS.
- Agent archive `a4e016b6…` and Runtime archive `5e9ad1c6…` static listings:
  no directory outside committed-file parent closure: PASS.
- Farm census source AST/function and parent-closure rule checks: PASS.
- Product worktree status: clean before and after: PASS.

No child request, build, provider execution, Farm census execution, full suite,
kit edit, permission edit, marker/owner edit, Git/pin edit, or hub write was
performed. D130 SWAP/WAL remains on absolute hold. C0 contract and PLAN F
requirements are unchanged.

## Commands and results

Read-only commands used:

```text
sha256sum ORCH/bin/make-child-venv ORCH/bin/bench_store.py
python3.13 static AST/hash/archive-listing probe
git -C /home/user/peteromallet/astrid-agent archive --format=tar a4e016b6... | tar -tf -
git -C /home/user/banodoco/banodoco-workspace-runtime archive --format=tar 5e9ad1c6... | tar -tf -
git status --short --branch
```

All returned successfully. No product tests were run because this assignment is
source/static diagnosis only and explicitly prohibits build/provider/full runs.
