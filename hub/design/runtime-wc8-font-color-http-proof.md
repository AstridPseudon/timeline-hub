# Runtime WC8 retained font/color HTTP proof

Date: 2026-10-21

## Result

Added one compact detached-sheet acceptance case to
`tests/editing_conformance/test_native_sheet_ordinary_runtime.py`. It reuses
the existing WC8 historical closure and retained `NativeSheet` basis, changes
the present `size`, `font`, and `color` cells together, verifies the literal
color quoting in the actual UTF-8 bytes, and sends one ordinary `/v1`
`clip.set-params` command. The case checks the original revision/publication
basis, exact command values and source, opaque/null/absent fields, parameter
order, sibling order/isolation, restart reload, and guarded inverse/redo.

The first central execution stopped before any commit on an over-specific raw
canonical-order assertion. The observed helper output was
`color=#25241F font=display opaque={"keep":[null,false,1,1.0]} size=32`; the
assertion was corrected to that actual order. The one qualifying corrected
execution passed. This is not a whole-WC8 deletion or merge claim.

## Exact qualification tuple

| Input | Identity |
|---|---|
| Agent base | `5ad4b7c26871c18ba01449a6d3c4d5bde6aa9a2b` |
| Central candidate source tree | `070a75eed14a85465269289e143fd5b26cbaab31` |
| Current Runtime server | `b92d3e7a05eec65c142294ef4873edd059e9b31d` / `6abc2f117391de8e7e35c0283f575a002199894d` |
| Published producer | `95bd3c5f6d00e9bc8cc8cbe5ef510b68ed660f3c` / `d3a290b407fa61e6ab2d476f50c068073f70df00` |
| Client / Runtime wire | `0.2.14` / `sha256:7d4afa05962b8cd61643213fc79cdde41e16046c4e2a777bd299b48af0f31816` |
| Ordinary raw schema | `sha256:6ba7b51e9518e7fb08b27ad5b7225855276b657d0adebf704dd853f699768f2d` |
| Artifact | `all76`, `sha256:54205b3ecb55038e416b31af936c9af26afa30dc1b05da16157ee4d861fe05ac` |

## Evidence

Central request ID:
`rt-m2-wc8-font-color-one-http-0805-rt-wc8-current14-integration-1021080840-13261`

Result: `1 passed in 4.30s`, exit `0`; exactly one node was collected and
the request used the relative selector:

```text
tests/editing_conformance/test_native_sheet_ordinary_runtime.py::test_current014_detached_font_color_uses_one_native_http_commit_and_guarded_inverse
```

The first request was
`rt-m2-wc8-font-color-one-http-0805-rt-wc8-current14-integration-1021080748-32412`;
it exited `1` in `3.37s` on the raw-order assertion before `apply_sheet` or
HTTP commit. Per the two-failure limit, no third central execution was made.

Local direct evidence: the retained sheet/native neighbors passed `97` tests
in `8.33s`, and `tests/editing_conformance/test_native_sheet_current.py`
passed `38` tests in `7.29s`. Preflight passed exact imports, Runtime health,
client/wire, `all76`, ordinary `6ba`, private `RealmStore` isolation and one
marked-node collection. A first private health witness failed only because it
had not initialized its private realm; the corrected normal initialization
passed.

No full, browser, renderer, install, generation, direct-socket, old HTTP
case, or whole-file central run was performed.

## Independent review limit

The independent source review is `HOLD`, not `APPROVE`. It found that the
converted unknown-neighbor refusal appends `unknown=label` after the `# ref`
suffix, so it exercises malformed binding rejection rather than the required
unknown-field refusal. That separate worker recommends placing the token
before the suffix and rerunning its focused tests. No merge or source-safety
approval is claimed here.
