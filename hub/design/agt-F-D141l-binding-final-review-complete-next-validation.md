# Validation

Fresh direct acceptance execution:

```bash
PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-agent/bin/python -P /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-F-D141l-binding-final-next/evidence/check-source.py check
```

Result: exit `0`. Fresh stdout is retained in `checker.stdout` and fresh stderr
in `checker.stderr` in this evidence directory. The stdout record is:

```json
{"control_status": "PASS", "pair_status": "READY_SOURCE_D141aa_NOT_RUN_LIVE", "admission_cases": 10, "lifecycle_cases": 38, "controller_route": "isolated request-test -> queue actor -> wait-test", "log": "/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-F-D141l-binding-final-next/evidence/private-control-logs/check-1793008726782191470.json"}
```

The fresh control log independently contains 10 native-admission-expression
cases. Its unchanged tiny controls are `positive exit=17 calls=1` and
`poison exit=1 calls=0`. Exact hashes:

```text
check-source.py 3add53f0c0f75c8f877757ec860924cd3085d8ea9cd88c9cd18b93afbabcbba2
source-manifest.json 62a814f708e3238eea7006220490699e9ca3ec99258c9548e8c240fa2622aef4
checker.stdout 135525af7c71a421b8c86dbe448cbcf296b1b1e661ee33a86a2cbce801508a08
checker.stderr e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
control-log 895b5feea43e7102499feb3239bd110b12d3386f1f1c18a5500dc3025f08560d
publication-record e436576284add9d6624d266b288c963393559778e223b8f7353c0217ed1da8ef
```

The required own sampler used 5-second intervals and a 4,000,000,000-byte
stop threshold. During the checker it recorded available bytes from
4,613,914,624 down to 4,610,801,664, all above the threshold; the complete
trace is retained in `disk-trace.txt`.

No product or source test suite was applicable or run. No live service action
was run. The prior syntax/AST/JSON/hash conclusions remain inherited and the
historical subject trace gaps remain explicitly unverified rather than
backfilled.
