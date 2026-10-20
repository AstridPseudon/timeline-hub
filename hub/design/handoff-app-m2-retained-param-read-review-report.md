# app-m2-retained-param-read-review

Completed the requested readiness review. **Candidate 0.2.7 is insufficient:**
it returns only `VerifiedDocumentObject`, while frozen027 native selected-PARAM
capture requires `(VerifiedDocument {pin, document}, selected object map)`.
No existing public retained document read was found in the reviewed candidate.
The public object read captures the exact document internally and discards it
from its return. Current `getDocument` cannot recover V1 after V2/removal.

Detailed source anchors, authority trace, object-ID discovery analysis, Runtime
test limitations and reconciliation are in the requested absolute design file:
`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/app-retained-param-read-review.md`.

- Reviewed App base `4f79aea853a53852f50456ac295588c19016f1f7`, frozen Agent
  `027bd16d96010544331c953c0e1014e161786e71`, Runtime candidate
  `8308cb9c153df3d7a5fdaf492af075be5b18e670` (client 0.2.7).
- The candidate's max10 tests use a local JSON `accepts()` helper and fixture
  provider, not native capture or Runtime `clip.set-params` acceptance.
- After a previous native PARAM, public history may supply the selected object
  ID through `params.snapshot`. Manifest-only/older-record callers lack that
  guarantee. Even granting the correct ID, the exact document remains missing.
- Wrote `notes/probe.py`: actual frozen native capture with complete published
  input shapes accepts 4→8 and rejects 16 under V1 max10. Removing the verified
  document refuses 8 even with correct object bytes. Missing object, object-as-
  document and removed-current-document substitutes also refuse atomically.
  Synthetic in-memory resource/receipt data tests shape validation only, not
  Runtime custody or a real build.

Exact final execution command:

```sh
PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-agent/bin/python /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m2-retained-param-read-review/notes/probe.py
```

Result: **exit 0, 8 bounded checks passed** (final run 1.73 seconds). The temporary
`git archive` source extraction is removed automatically. No Runtime/renderer
import, build, install, tsc, full/browser/socket/service/test-service run occurred.
Runtime tests were source-inspected only; live 0.2.7 reads, actual PARAM acceptance,
native end-to-end golden equality and App/browser qualification are UNRUN.

Verification: `git diff --check` produced no diagnostics; `git status --short`
was empty. `git diff --no-index --check /dev/null <file>` on the design, report,
probe and commit message produced no whitespace diagnostics (exit 1 denotes
the expected added-file differences). No temporary source extraction remains.

Decision: report the missing fact against the settled 03:31 decision; do not
invent an App authority or adopt an unfrozen candidate. Smallest next step is
Runtime/Agent owner reconciliation of the existing retained
`config_source(pin) -> VerifiedDocument` read with the existing native contract
and public object read, then normal artifacts/paired freeze and real public-read
native qualification. No route/schema/field/port/workaround is proposed here.

App product/adapter/generated files, pins, strict selected-PARAM refusals and
all original tests are unchanged. Both frozen pairs remain untouched. Writer
readiness is blocked on the owner reconciliation; this review task is complete.
