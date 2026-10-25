# D118d facts

- The only repository change is `tests/sdk/test_timeline_capture_projection.py`.
- The current genuine source bootstrap creates the shot with `payload.items: []`; the retained fixture dereferenced the first item before this correction.
- Restored the reviewed D100 source-only setup: a registered `commit_timeline` call with a v2-shaped `doc.patch` sets the authored item list, checks `accepted`, reloads the canonical document, and leaves the original projection/canonical/pin/order/opaque/read-row/opener assertions unchanged.
- AST checks: all non-fixture functions are identical; the original `saved_closure` tail is identical; original assertions are preserved; test parameters and decorators are unchanged. The assertion count increases only by the setup acceptance guard.
- The change exactly matches the historical reviewed setup in commit `28081580dc95f02470d82ad81b826335d8e4bd09`.
- Frozen R4 candidate-sdk tip `11caf1d9de291d76f491cf69f7942606b7471d7a` does not contain the target test path, so no upstream exact-node comparison is claimed.
- The own failing-node check was not run because free space was `4821417984` bytes, below the required `5000000000`-byte floor.
