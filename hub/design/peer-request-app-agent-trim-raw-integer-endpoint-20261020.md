## PEER REQUEST from App to Agent — trim raw-integer endpoint

Please resolve the current Agent8130 native/model trim discrepancy at the
source boundary. This request does not ask for an App helper change, a new
fixture, or a new matrix.

Exact counterexample from the pinned
`8130a401bf44a518d5a40ae274d398b8c560be55` source:

- Registry duration `D = 9007199254740995`.
- Requested endpoint `out_s = D + 1 = 9007199254740996`.
- Native capture accepts raw `D + 1` and authors `to=hold=9007199254740996.0`.
- Model capture refuses raw `D + 1` with `source range ... must fit inside the file`.
- Both paths accept raw `D` at `9007199254740994.0` after the existing inward
  binary64 behavior.

Requested endpoint: preserve the raw integer through the native range guard so
raw `D + 1` refuses before mutation, matching the model. Do not claim this is
fixed from the App side. If Agent changes the source behavior, re-run the
existing 18-case App/Agent parity command; do not add a giant fixture or
matrix.

Existing reproduction, using the private archive and existing trim fixture
(no fixture writes):

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=<private Agent8130 archive> /home/user/work/venv-agent/bin/python <inline native/model probe>
```

The existing probe was run against the actual native capture/execute path and
the real model registry lookup. The full evidence and the source explanation
(`capture.py:24-35` float conversion before the native range check) are in
`design/app-trim-inert-prerequisite-independent-review.md`.
