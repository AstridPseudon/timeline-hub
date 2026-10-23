# P3 common native seed handoff

Candidate on App `411ff10bd7043d55b4d83f2dfbbbd841af7b4806`: only `commitNativeSeed` in `tests/e2e/local/support/harness.ts` changes, +8/-6 lines. Native occurrence authored fields now use guarded normal `doc.patch`; the emitter receives a working bundle without injected derived `parent.occurrences`. Provider-managed identities and links remain untouched. All expected raw fixture construction, 21 Python assertions, request/receipt suffix and five P1/P2/P3 specification blobs are unchanged. Gate-5 remains `37caf28577d42fbe98afd2320dffa3c72e6e74b1`.

Independent Luna review approved. Existing targeted SDK suites: 57 + 44 passed. Pure App matcher/launcher controls: 8 passed. Exact changed-block SDK probe: 1 passed. Root/App/Node typechecks, scoped ESLint, preservation comparison and diff check pass. Probe has no captured media authority or fabricated acceptance and is not durable Runtime evidence.

**Required actual bounded normal-harness seed qualification remains unrun:** this worker is explicitly prohibited from service requests. Orchestrator/Farm must qualify the reviewed source against approved immutable Agent `8c355a48` / Runtime `cfa0af0d` and installed child/Remotion artifacts using the existing normal harness. Assert the full original raw closure and all receipt/base/manifest/origin checks before releasing P2 heavybody or counting P3 proof. No full/browser/journey/P1/P4/corpus/native14 body was run or requested. No product guard change or SDK defect is proposed.

Full commands, results, causal trace and limitations: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-P3-common-seed-sol-1433/report.md`.
