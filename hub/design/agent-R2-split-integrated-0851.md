# R2 split inverse integrated proof

Result: **PASS, bounded Agent proof**.

Integrated `HEAD` is `2e12b49ba61bc68a982a1cdc9d2d012036c9b720` with tree
`6f7649a4e0b8f1d936dc94a5fa0bb7c5fb3db276`, after the home merge of reviewed
`f7fcb72827405ea938555db92827a5095f02a3a5`. The merge diff from
`e837e18c5` has exactly two paths: the five production lines in
`astrid/sdk/timeline/inverse.py` and
`tests/editing_conformance/test_inverse_clip_mirrors.py`.

The exact source and 35-case regression file match the independent review:

- `inverse.py` blob `5b462b4fc5803cc396a5ce195ac0f5ec4b6f71e8`, SHA-256
  `267b1b1589c0254345a13bf802df8b40301f70020389c223c91f4b14808f336d`.
- `test_inverse_clip_mirrors.py` blob
  `e5e0cb49092b331a8c2e451296c182c503ecba4f`, SHA-256
  `7cec273a0fe7bd73be794e11bc54bbd1f222455112bb9b3d87e9e08b4f474b81`.

R1 commit `d462103985e3d4c4591ed76c5d5f261b2398fb36` and P4 commit
`f816d71d98716418e38fd5668e9c57cbc849e26b` remain ancestors. The current P4
test blob is `afc9c112527692536a065de8cdbfc7a25c19bc26`.

Required acceptance, run exactly with the specified Agent/Runtime environment:

```text
206 passed in 39.62s
```

Static checks also passed: scoped Ruff; vendor lock (`ok runtime.lock.json`);
artifact manifest (`artifacts.json is current`); and `git diff --check`.
Reviewed unchanged-tree evidence is reused for baseline Ruff `2149/2149` and
Mypy `1912/1912`.

The qualification is intentionally narrow. It proves the existing
`apply_inverse` production caller's Agent mirror repair and provider undo
behavior, including strict guards/history, derived writes, physical bindings,
effect ranges, ABA and surviving-consumer refusal. It does not claim full
Runtime authorization: the prior real-annotation matrix remains 53/58, with
five whole multi-step inverse candidates blocked by intermediate image
binding. No workaround or weakened expectation was used, and no rerun was
authorized before a meaningful Runtime fix. HTTP/P1, P4 HTTP, native14,
crash24, browser duplicate, and full-suite evidence remain unclaimed.

See the worker report for the exact command and path-level evidence:
`workers/agt-R2-split-integrated-0851/report.md`.
