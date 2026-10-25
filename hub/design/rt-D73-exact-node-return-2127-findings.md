# Findings and dispositions

| Finding | Disposition |
| --- | --- |
| Launcher received `-o` before pytest module mode. | Fixed in both private rows: `-m pytest -q` is first. |
| Fixed request ID and fixed/shared XML paths could overwrite per-ID output. | Fixed: rows derive the ID from the runner-owned `D66_OUTPUT_DIR` and place XML beneath that directory. |
| Frozen selected/fork origins carry old launcher `cec561…` and the wrong environment behavior. | Fixed by admission guard: only launcher SHA `9f668e…` is eligible; old origins are explicitly rejected. |
| Agent 22bf source does not contain the reviewed selected-file tuple. | Explicit not-ready census; the source guard rejects its `6d7ba762…` selected hash. |
| Selected4/fork receipts, manifest, suite installation, and fresh result receipts are absent. | Explicit missing inputs in readiness; no executable route is claimed ready. |
| Positive-17 one-call and poisoned-source zero-call controls. | Private `--controls` path invokes the reviewed focused control test only after receipt-bound source admission; no fresh control claim was made here. |

No central config, runner, kit, source, pin, product, or test file was
modified. No behavior expectation was weakened or deleted.
