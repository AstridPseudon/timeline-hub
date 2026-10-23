# P1/D25 mounted event adapter handoff

Proof added a test-only pre-title collector on App base `b221388d3` / tree `5ce46b64b63862f103379df3f3d74982e4ef461a`. It opts in before navigation, listens for `timeline:save-diagnostic`, safely projects finite allowlisted detail, caps records, and enriches the existing early-file/continuation artifact. The original two chain bodies remain byte-exact (`4b04ad7e...` and `2f750118...`).

Targeted evidence is green: safety Node TAP 19/19; root/App/Node TypeScript; scoped ESLint; Playwright list exactly 2; diff check and outside-file check. No browser/service/full run was performed.

The producer handoff still lacks final typed source/sample/review and authoritative literal scope/type/nested keys. Before any real-emitter qualification, App must publish that small interface/source hash; align the isolated constants/projection then re-run targeted checks. Do not treat this adapter as whole-P1 GO or causal proof.
