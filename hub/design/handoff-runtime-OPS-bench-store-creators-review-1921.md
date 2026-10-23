# OPS-bench-store creators return 1912 — independent review 1921

**SOURCE: FAIL. Combined behavior: FAIL / UNQUALIFIED / STOPPED.**

The creator source fixes the two independent1908 findings in substance. The
child maker passes exact verified `.provision-report` bytes as `report: str` to
the core registration callback, while the core projection interface owns the
fixed `tests/provision/<validated registration name>.txt` transaction. Created
and managed-reused receipts verify the retained report and public projection,
include the actual raw report SHA256, and distinguish requested Agent/backend/name
from actual retained source markers. Legacy reused receipts add
`status=passed` only after the unchanged full verifier succeeds. D21c custody
retains the full Agent SHA + Runtime backend SHA + generated client file/digest
tuple; Remotion runtime identity remains keyed by the Remotion tree.

The exact existing Proof grep parser fixture passed for both created and reused
receipts, including false-tuple, failed-status, malformed-byte, missing-cache,
report-tamper, and missing/changed-public-projection controls. Static review
found no fabricated PASS, weaker custody, out-of-transaction public report write,
arbitrary projection path, or lost original child verifier. The production shape
remains audit/request writer → dispatcher positional call → maker → `Store.ensure`.

SOURCE PASS is nevertheless withheld for packet-integrity failures:

1. The new hash manifest is stale for `make-child-venv.sh`,
   `make-child-venv.patch`, `test-receipts.py`, and `validate-packet.py`.
   `sha256sum -c` fails those four entries; the old1850 manifest passes, while
   `artifact-summary.json` records different current hashes.
2. `validate-packet.py:45` extracts the first `IDENTITY_SCRIPT='` occurrence,
   which is the embedded Store Python literal at staged maker line 199 rather
   than the shell assignment at line 319. Its embedded identity compile fails
   with an unterminated-string `SyntaxError`.
3. Against the current installed inputs, `make-child-venv.patch` applies but
   does not cmp the staged source. The other three replay/cmp checks pass.

Scoped checks: exact receipt fixture PASS; all four `bash -n` PASS; Store,
verifier, relocation, provenance and distribution embedded compile PASS except
the validator's broken identity extraction; the two permitted evidence Python
files `py_compile` PASS; new manifest FAIL; old1850 manifest PASS; Runtime
status empty and diff-check PASS; no product suite applies. Scratch remained
below 10 MiB.

No product/test/generated/pin/Git/live kit/config/queue/bench/install/provision/
network/chmod/cleanup change was made. Prohibited combined adapter creation,
readonly publication/deletion, HOST/test-service qualification and full suites
were not run. Combined **FAIL / UNQUALIFIED / STOPPED** is retained. See the
worker report for exact commands and hashes.
