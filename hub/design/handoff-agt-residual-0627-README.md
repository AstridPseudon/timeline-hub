# F-D86 residual source-delta routing

This is a source-only routing result for the exact 30 original selectors in
actual9211 (word11 96--106, scalar11 119--129, ownedmove8 130--137).
Historical source commits and receipts are retained verbatim in
`handoff-agt-residual-0627-routing.tsv`; `source0329` is only a legacy owner
reference and is not reported as a new finding.

## Ready selector subset

The only new, relevant source edges at an original first boundary are:

- IDs 102 and 103: the retained-input tests import and call
  `native_word_anchor_fixture.seed` (test file lines 86 and 91). The old
  boundary was the fixture's `clip.add v1 does not support on` at
  `_clip_commands.py:49`. That fixture has since changed through the reviewed
  literal-birth, current-Runtime selection, mirror, and guarded timing source
  changes (`b2cb772852`, `a8bf1e51c6`, `5e9acf59d2`, `5554fe792b`). Current
  fixture hash: `f70d2e9c...ddeddac`. This is source readiness only; it does
  not claim a passing behavior result or cure.
- IDs 130 and 131: the exact original first-boundary assertions/caller setup
  changed in the owned-oracle merge `b8a48a91b0`. ID 130 is the status
  assertion at line 174; ID 131 is the prepared-video Runtime pin/caller at
  line 249. Current hashes are `7f1860c3...22bae70` and
  `4cc89a0a...0cdc2c`, respectively. This is source readiness only; it does
  not claim behavior qualification.

`selectors.txt` contains only these four exact selectors. No original input,
topology, opaque value, assertion, refusal, retry, inverse, ABA, or no-write
guard was changed by this routing work.

## Explicit remainder routing

- IDs 99 and 101 are `RETIRED_D95_LEGACY_SCOPE`; they remain separate from
  new refusals and are not ready.
- IDs 102 and 103 are the sole word READY_DELTA rows. IDs 96--98 remain HOLD:
  D90 changed shared `inverse.py` (`06bd41f...`) but no exact family-specific
  source edge reaches their Runtime service first boundary. ID 100 remains
  HOLD for Runtime's moved-head/private sequential physical proof. IDs
  104--106 remain HOLD with `EXACTMISSING`: their Gate1 assertion has no named
  current source/caller delta.
- Scalar IDs 119--129 remain HOLD. Their selected Agent source files retain
  the historical scalar source (`721189cbc8...`); D101 and D90 are shared or
  later dependencies, not an exact new source at the recorded first boundary.
  IDs 119--121 therefore remain Runtime-owner `service.py:2347`; IDs
  122--128 remain Agent-owner `commit.py:1467`; ID 129 remains the Agent
  provider/source seam. No body retry is implied.
- Owned IDs 132--137 remain HOLD with `EXACTMISSING`: the current owned
  helper path is still the historical `73998ac...` producer/caller seam for
  those Runtime `service.py:2518` failures. The current oracle change is
  specific to IDs 130--131 and does not transfer to these rows.

The current D101 Agent/Runtime pair, word oracle657, and D90 inverse source
were checked by exact path/caller trace. None adds a ready edge to the held
rows above. M1scope0613 remains a separate pending dependency. Already
qualified numeric6/fourR2/P4 are excluded.

## Static evidence

No imports, tests, collection, helpers, fixtures, probes, services, package
installs, or full suites were run. Evidence is limited to AST/source/hash
inspection and the checks reported by the worker. The report makes no product,
authority, retirement, or behavior claim.
