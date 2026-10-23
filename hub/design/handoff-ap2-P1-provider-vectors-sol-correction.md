# AP2 P1 provider-vector correction

Status: **NOT MERGEABLE** pending the Agent R1 membership/order guard fix.

Base SHA: `edcd1b2baea3919c7730725d0df154e7d8c9447f`

The bounded packet changes only the permitted request fixture and P1 tests. It
now submits all five trim effects (`from`, `to`, `hold: 17 -> 4.0`, and tagged
removals of `app.astrid.for` and `app.astrid.until`), and all four child vectors
use the verified physical `internal-revision:ir` root with
`clips/id:c/...` paths. The provider tests project the fixture bundles into a
complete canonical closure in memory, then run the real R1 executor and the
detached Runtime commit service. The two occurrence aliases remain one shared
physical child; no implicit fork is introduced. Fixture/source bytes and SHA
values remain unchanged.

## Original vector dispositions

| Vector | Disposition |
| --- | --- |
| `trim-internal-clip-window` | PASS direct R1 and service. Exact native outcome retained, including hold and both authored metadata removals; opaque values preserved. |
| `created-track-and-clip-list-inserts` | PASS direct R1 and service. Existing list order, opaque values, and inverse evidence retained. |
| `params-absent-to-explicit-values` | PASS direct R1 and service. Physical child path, absent guard, exact opaque values, JSON reload, and shared-child result pass. |
| `params-null-to-object` | PASS direct R1 and service. Explicit null remains distinct from absent and is replaced with the exact object. |
| `params-remove-and-preserve-opaque` | PASS direct R1 and service. Remove-versus-null is exact; opaque, `x`, and `y` siblings survive JSON reload. |
| `disjoint-field-merge` | PASS direct R1 and service/replay. A competing `y: null -> false` commit lands first; stale `x: 1 -> 2` lands with the historical service status `rebased`, preserves `y: false`, and yields the exact merged payload. |
| `same-field-refusal` | PASS. Stale `from` edit remains `value_conflict`; head/history remain unchanged. |
| `ordered-list-move-and-order-refusal` | Move/order case passes. The required stale membership-removal case remains red because current R1 returns `value_conflict`, not contract-required `selection_changed`; the assertion is intentionally retained. |

## Evidence

Required bounded command:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.:/home/user/work/runtime ASTRID_RUNTIME_CHECKOUT=/home/user/work/runtime /home/user/work/venv-app2-native/bin/python -m pytest -q tests/sdk/test_p1_doc_patch_provider.py tests/sdk/test_p1_doc_patch_requests.py tests/sdk/test_p1_case_corpus.py
1 failed, 41 passed, exit 1
```

Exact remaining failure:

```text
tests/sdk/test_p1_doc_patch_provider.py::test_provider_refuses_stale_same_field_membership_and_order[ordered-list-move-and-order-refusal-intervening2-selection_changed]
E       AssertionError: assert 'value_conflict' == 'selection_changed'
E         - selection_changed
E         + value_conflict
```

```text
/root/.local/bin/ruff check tests/sdk/test_p1_doc_patch_provider.py tests/sdk/test_p1_doc_patch_requests.py
All checks passed!

/root/.local/bin/mypy --follow-imports=silent tests/sdk/test_p1_doc_patch_provider.py tests/sdk/test_p1_doc_patch_requests.py
Success: no issues found in 2 source files

git diff --check
clean (no output)

Fixture/source provenance check: 1 passed, 2 warnings.
```

No full, browser, socket, or H3 run was performed. Provider/direct-service
evidence is not HTTP/App/H3 proof; full H3 remains NO-GO.

## Remaining owner need

Agent R1 must check collection membership/order dependencies before the item
value guard during stale replay, so removal of `clip-b` returns
`selection_changed`. The same-field stale edit must continue returning
`value_conflict`. After that provider correction, rerun the exact bounded
command above and retain the original successful vector assertions.
