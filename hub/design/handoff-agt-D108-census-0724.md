# F-D108 census return — source-only derivative

This is the Agent-owned derivative of the D108 census result. It does not
replace the Runtime-authored crosswalk. The amended Runtime files were saved
under the return worker's evidence directory and restored to their exact
logged preimage bytes.

## Exact accounting

The selector sets are the pinned git-object-only AST sets from the prior
census evidence: fresh Agent `08e6b905114a3ee2b05c3e7980421f26b4abf15c`
minus captured Agent `d6294843286c18e57af3c1874cf1996be42212d2`.

| set | exact operation | count | SHA-256 of sorted selector lines plus final newline |
|---|---|---:|---|
| raw | fresh upstream minus captured | 105 | `99a03feaf7d0343ad08837609df17bdd19b0af88ce671ef50bd4fb85b63c0714` |
| declared | raw minus approved D18 scope exclusion | 104 | `468170f22ffa162ad5543ff70f9c72aecb084b4f8f54cc9dbc1d5fc6bd40f912` |
| reconstructed | raw minus D18 and Windows registration | 103 | `235833c98214b57d7255cb422e1d0340d9d0b386e679cb475e86449428fcf310` |

`declared - reconstructed` is exactly:

`tests/test_installer_windows_tasks.py::test_register_scheduled_task_accepts_rendered_xml_string`

## The two identities

### D18 child bridge

`tests/core/execution/test_generic_host_child_bridge_d18.py::test_output_above_persisted_retention_budget_is_refused_before_any_read`

- Raw membership: yes; declared membership: no; reconstructed membership: no.
- Disposition: approved D18 scope exclusion, not retirement.
- Fresh file blob: `9ac7292e50831c29002a94d2d13be48a7c4780f7`.
- Fresh function SHA-256: `a591a4fa5540daeac8df031f4b16ddb16d1fd2513798fdd3eef18d224efc9848`.
- Captured current file blob: `4f3da5e83c4413c9a44a7d1a2329032a44f7de10`.
- Current renamed selector: `test_materialization_rejects_above_persisted_retention_budget_before_reread`, function SHA-256 `5cb6e6811fab503b754cffc9a92689f90df08317aaec55659bf60b588f841485`.
- The predicates are not exact-equivalent: the fresh selector refuses at identity dispatch before `get_object`; the current selector reads the descriptor before refusing reread.
- Approval sources: the three D18 documents named in the JSON handoff.

### Windows Task Scheduler registration

`tests/test_installer_windows_tasks.py::test_register_scheduled_task_accepts_rendered_xml_string`

- Raw membership: yes; declared membership: yes; reconstructed membership: no.
- Fresh file blob: `ef1b2ca9d7b95056826baf1323394dbf15f2a913`.
- Fresh function SHA-256: `deb4ceb835cb0cfcc3ad596214293b7cdc68356cf35d5e4c2cf2b63a1f52797d`.
- Current file is present at the captured blob `be0dc5e501f2b75f4e1d63596e2b0304a8a997bc`, but the registration selector is absent. The current file does contain the sibling cleanup selector `test_task_cleanup_preserves_powershell_success_and_failure`.
- The cleanup selector's preserved full-function SHA-256 is `277c9825fd2c69ee415d6f16650ac92a4037472792fcd954feb978f35c239120`.
- No approved exclusion, retirement, or source-only equivalent was found. Both Windows selectors remain required for F-final; no Windows body was run.
- Installer decisions checked: `rt-D72-installer-review-1722.md` and `peer-runtime-to-agent-20261024T1750Z-installer-reviewed-D77.md`.

No durable source corruption is proven. The proven issue is the one-selector
reconstruction/accounting gap. No product, test, ledger, pin, generated, or
source files were changed.

