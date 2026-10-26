# D141l independent review: FAIL

One blocking finding was found.

## D141L-F1 — retained admission was incorrectly excluded

The author reports `X = null`, `NOT_QUALIFIED`, and the default heavy floor of
`5,200,000,000` because the retained controller admission predates the body.
That interpretation conflicts with the explicit MAIN05:20 decision: the retained
controller admission `5,433,016,320` may be the bracket start when paired with a
retained in-run observation. It is the same controller, same `/home/user/work`
mount, and the normal full body begins at `00:43:38Z`, after the recorded
admission at `00:42:39.754967Z`.

For normal run `app-full-1026004326-12174` (source
`867cb2737af1b46dc608c7cd37c349e920fe9422`, tree
`2b44a46ca51d880c6a00da4c19aa8629b55eb7dd`), the retained minimum is the exact
table row `4,839,120,896` at byte offset `1157219` in
`managers/app/rounds/20261026T0035Z.log` (source SHA-256
`720b56d6f058d8aa5ed7770b1e2e5c54a5703ebb68a6403edccfc7a8f6e4302d`), observed
at `00:48:37Z`. Therefore:

```text
X = 5,433,016,320 - 4,839,120,896 = 593,895,424
floor = max(4,600,000,000, 4,000,000,000 + 593,895,424 + 200,000,000)
      = 4,793,895,424 bytes
```

The ordinary in-body bracket `5,055,897,600 - 4,839,120,896 = 216,776,704`
is smaller and is not cherry-picked. The pristine run was also checked: its
lowest timestamped in-body row is `4,938,567,680` at offset `1276493` in
`20261026T0110Z.log`, observed at `01:15:43Z`; its timestamped bracket is
`11,431,936` bytes. It does not exceed the corrected normal-run bound. No
continuous-peak claim is made. The unobserved intervals before the first sample,
between samples, and after each minimum remain disclosed.

## Separate service-format limitation

The installed validator is unchanged and requires exactly two manager-owned
witness files, each with original bytes `Avail\n<strict decimal integer>\n`.
The retained sources contain only multi-line `df -B1` table rows with a
`Filesystem` header; the retained originals contain no supported two-line
`Avail` witness. Converting a table row would create a new derivative and is not
accepted as historical custody. Thus the corrected bound is source-qualified
under MAIN but cannot currently be attached as an executable receipt through the
normal validator route. No receipt, live ID, or derivative witness was created.

## Other checks

The Composition base head/tree is byte-exact as requested. The two full-run
commands, source heads/trees, run intervals, table-row hashes/offsets, installed
`test-run` and `d141-validate-receipt.py` hashes, arithmetic, gaps, and the
current source-only admission were reproduced. C0 request/reply shape and the
D130/D141 stop were not changed. No product, test, kit, body, pin, queue, or Git
state was mutated.
