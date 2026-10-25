# F-D86 protected source review

## Bases and exact source identities

- True baseline: `993e1e9d98463a1bfa35c611d45dd7b21e32e783`; both candidates have this direct parent and the two candidate commits have no additional ancestry.
- Parent candidate: `2f935f6d4d7952d5210b2243bf2f5f9039a3222e`; changed blob `ff5493dc43b563832f4ea2a15e544e3b3d080afe`; file SHA-256 `685f6168fa378b9269a2e605e5bec4643a413b856e2782a786bbe4e7dfbd9fcf`.
- Numeric candidate: `ec76fa69e6cc8af424ec397512b9422968b7eaf5`; changed blob `01319dc1028aeac266ee483beb7ebe80d1b53d5c`; file SHA-256 `134a851d76cd0058723f531573128eb13a7b14a2336e4be3ab0ed6bafa37c33e`.
- Baseline parent-swap blob `66ba1bf4c77da3a008f762df749c74866e0e77dd`, SHA-256 `2bde457aa4f5313e98119aadfa2fd3fe6f4feb648f8f6274096b8d6dc4897222`.
- Baseline numeric-move blob `65f96adc766471cd753c12c537cf00796ee83c3f`, SHA-256 `51f6df318fbba81f66512c94a9ce60ef6eda6d930e3c8c27c5fe6ab8e4a2cca1`.
- `test_commit_runtime_numeric_params.py` is unchanged: blob `49281cbfb114ec9893d5cfc8ab961b1c05fd8062`, SHA-256 `8f1020a2ce363abbc11f7fc47b8287a48f963c7d4de3a88b5e5f86a757f6788c` on baseline and numeric candidate.

## Parent swap mapping

- The retired cross-interpreter historical seed, hard-coded historical Runtime checkout, seed JSON, and direct current-realm reconstruction were removed.
- `editing` delegates to the existing occurrence-media fixture with the exact `swap` operation, `parent` owner, image/video parameter, and parent `source_bytes`; that fixture performs the current bootstrap, real media admission/selection, native capture, and registered `astrid` provider acceptance through `commitTimeline`.
- `http_editing` keeps the original two owner selectors (`parent`, `occurrence:occ-a`) and the exact image source path.
- The new local body supplies the complete C0 envelope: scope/base pair, nonempty commands, label, one contiguous step with command ordinals and semantic patch field, `fields`, request reads, dry-run, source, rationale and group ID. Idempotency remains passed by the existing commit/client callers.
- All six test-function ASTs, decorators, signatures, assertions, raises and branches are identical after location stripping. Family selectors remain the assigned 12: two accepted/retry/undo/redo, four lifecycle-race, four history/rebase/ABA, and two authenticated HTTP owner selectors.
- No retired publisher, synthetic accepted record, SQL/history fabrication, guard bypass, or unsupported emitter membership was added.

## Numeric mapping

- The fixture now selects `vendored_runtime_commit()`, builds the real precut film fixture, and registers `load_timeline_commit_provider('astrid')` before setup submission. Setup is a native `capture_clip_set` submitted through `commitTimeline`; no direct publication or synthetic history remains.
- Parent target remains `parent/clip:music-bed`; occurrence target remains `occurrence:occurrence-1/clip:clip-1`. The occurrence setup retains the original independent `hold=0.25`; parent hold is read from the target. The authored values retain exact representations: `start` parameter values `(0, 0.0, 0)`, opaque list `[None, False, 1, 1.0]`, boolean `fixed_start=True`, and numeric `for` values.
- The native move command, original five assertions, decorators, signature, and all three `(start,on)` cases across both scopes are preserved. The unchanged numeric-params neighbor still has its original five before/after cases and both refs and imports the migrated fixture.
- The nine assigned numeric selectors remain six move selectors plus three numeric-params selectors.

## Verdict

- `2f935f6d4d`: `PASS_SOURCE`.
- `ec76fa69e6`: `PASS_SOURCE`.

No test collection, test/helper/fixture execution, service, browser, build, render, or exploratory fixture probe was used as evidence.
