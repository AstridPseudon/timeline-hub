# Runtime OPS-App template export 1836 review 1840

## FAIL

The authentic environment export passes custody, but the suite-row export fails the exact payload requirement. The exported `handoff-runtime-OPS-App-template-export-1836-suite-row.txt` is a 709-byte regular file ending in the source LF and hashes to `e14e5ac850ba94ddadadd55b8b48ea3999fb06bc9ebc101c859d4413890ab944`, not the required `ffdb0b13c65f106d7b818208343feb3f438dfc943f4af57c5f612ddcf73dc036`. The validator payload excludes that LF; App import is expected to add one ordinary delimiter after receiving the LF-free payload.

The environment `handoff-runtime-OPS-App-template-export-1836-agent-remotion.env` is a 523-byte regular file with exact SHA-256 `e53a69a465e05976dcf7a781f420b1c7def64a13691f7a5f387f6a0609a6da02`. It compares equal to `ORCH/tests/agent-remotion.env` and custody1343's `evidence/agent-remotion.env`. Both artifact names are normal regular files, non-symlinks, and below 50 MiB. Row key/call-shape parsing, `bash -n` for source/export/custody env, and credential-marker scans passed.

Exact review evidence:

```text
cmp -s source_payload export_row                         # exit 1
cmp -s <(sed -n '56p' ORCH/tests/suites.conf) export_row # exit 0
cmp -s export_env ORCH/tests/agent-remotion.env          # exit 0
cmp -s export_env custody1343/evidence/agent-remotion.env # exit 0
```

The private extracted current embedded validator (`make-runtime` SHA-256 `9fc7f72a7d03fcb4618310ad57f5c9cf111b78a59b2c02caa702073d0951fd09`) accepted the real `remotion-env-nodes` source pair and stopped before builder, exit 0. The reviewed old validator is SHA-256 `5245f264336d65c4a5847d9e4f05734e77d25ede0dd35d64008e5a4c45aac0e6` and matches its timestamped backup; current validator matches custody1343's candidate. Runtime was read-only clean at `2a9e347ff0e1df1dedff5ab7b59ddb27dfe3129d9`; `git status` and `git diff --check` both exited 0.

No actual suite/env, installed script, Node/npm, network, P1 body, benchmark/build/install, pin/generated file, queue/daemon/provision action, or Git mutation was performed. C0v2 shapes/frozen34e references and the existing seven-argument exact-source route were only inspected. Do not import the row artifact; re-export the LF-free 708-byte payload before App proceeds. The env artifact may be retained unchanged. This is not benchmark-ready evidence.
