## Report

- Updated only `caller-publication.py` and `caller-custody.json`.
- Bound P2 to source `d6ed8cbda122d810d5836ebfce3c56c10e76e9b4`, tree `542b772e6deed676b917f857708445b7d37a5aa8`, with both authentic parents.
- Rebound P2 App/tree/parent fields and refreshed all 60 decoded source/body guards.
- Preserved P3 row byte-exact (`23226c27…a7a3bf0`), 247 outsider rows, 465609 bytes, outsider digest `9acf76…1e2e8`.
- Retained Agent333/Runtime37eb, child1016/key188546, Remotion0258, wire fields, and fail-closed controls.
- Status remains `PREPARED`; authorization remains `NOT_GRANTED`.

Tests:

- `python3 -m py_compile caller-publication.py` — PASS
- `python3 -m json.tool caller-custody.json` — PASS
- Read-only source custody/body/guard validation and `bash -n` — PASS
- `git diff --check` — PASS
- Publication correctly refuses because `/home/user/work/wt/app-P2-final-pure-integrated-1036` was recycled; no READY or installation claim made.

Source report/ref remains terminal PASS with 695/695 tests, 67/67 popup tests, 30/30 Gate5 controls, and 11/11 diagnostics. Next step: recreate the separate clean source checkout, rerun publication, then perform independent review.