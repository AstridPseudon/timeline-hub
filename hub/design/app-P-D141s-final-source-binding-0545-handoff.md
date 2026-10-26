# D141s final builder handoff

Use the exact first pair only after the manager-owned normal App checkout has
been requested, materialized, detached, and read back at the pinned App
HEAD/tree. The planned path is `/home/user/work/wt/app-pin-4de54db1`; its
current absence is intentional and is not a verification failure or a source
receipt.

- target: `app-pin-4de54db1`
- repo: `app`
- selector: `p2-automatic-child-placement`
- normal suite: `d141g-p2-automatic-child-placement-4de54db1-submit`
- preflight suite: `d141g-p2-automatic-child-placement-4de54db1-submit-preflight`
- normal command: `normal-command.txt`, SHA-256 without newline
  `55da9058c938ce4ba362670b1322c49097441007d460677f6f5b2726c7f4c2aa`
- preflight command: `preflight-command.txt`, SHA-256 without newline
  `f20ab22c427e46fb06edbc2f91ea11ad27faf7a1b38c11abbc20895e465471a4`
- normal row: 1,022 bytes with one LF, SHA-256
  `c921243a9fbd154ed5ef16c27154212b6626e59748d7f3d34d5592fc38e32362`
- preflight row: 1,044 bytes with one LF, SHA-256
  `6d69ba5b21658c4f4acf5b6ecfd946089fd442b86bcb9683ac1b9dc63b9f6f83`

The Runtime pin is the actual final receiver source
`95d98f038320d5d46bd679ac000ab3e15825c935` / tree
`78df31d62c5b9ba4c84dee4ea346e43a767718c1`; Agent and Composition remain
`8585ed9c...` / `92a3ffdb...` and `635f4de0...` / `5ab5191a...`.
All eight pair summaries and full source facts are in `binding.json` and
`source-manifest.json`.

Normal D66 `--submit` is responsible for the later paired registration after
ordinary exact checkouts and receiver admission. It must compare registered
bytes to this genuine builder output before dispatching either paired part.
Do not force `full-e2e-timeline`, use direct `--run`, hand-edit the registry,
create a generic receiver/parser/framework, or touch the immutable 0459 receipt
and old held IDs. No body or actual proof is claimed by this handoff.
