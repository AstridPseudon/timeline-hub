# D118d independent protected review

## Verdicts

- Source semantics: PASS. The author commit changes only `tests/sdk/test_timeline_commit_graph_roots.py`, adding the current v2 label, one step envelope, `merge: fields`, and request `reads: []` to the existing Runtime request. The complete test-function, assertion, decorator, input, case, and patch ASTs are conserved.
- Own nine functional proof: FAIL. The one mandated exact-nine run executed once on the clean qualified Runtime pin and all nine cases failed before their intended assertions because Runtime rejected the prepared canonical document: `occurrences[2].gain` is `null`, while the pinned PreparedCommit schema requires a number. This is a current Runtime/fixture schema incompatibility, not an authored graph-root assertion failure, but it prevents functional proof.
- Full core: PENDING. No full suite was requested or run.

## Scope and custody

- HEAD: `94ac9347b64e0aaf5fb71443cc500fd57e80aa72`.
- Runtime pin: `/home/user/work/wt/rt-pin-5e9ad1c6`, commit `5e9ad1c6f74241d8771d3284fdd2ce7a214fd344`, tree `de2954a0ceadb4455903d9abdfec3b773318a50f`; clean at admission.
- Upstream `92443771676ef2bbb547d0a103d708fa8bec4c63` does not contain the target file.
- The test uses `RuntimeService.register_timeline_commit_provider(load_timeline_commit_provider('astrid'))` and calls the canonical `commit_timeline` route with the v2 envelope. No offline acceptance or forged accepted record was used.

## Functional result

The exact nine node IDs from the author facts were run with the mandated command, `-p no:cacheprovider`, timeout 45 seconds, and the required runtime pin. Admission was at 5,017,751,552 free bytes. Result: 9 failed in 14.18 seconds. All nine share the same safe failure frame: `runtime_protocol.errors.ValidationError: invalid PreparedCommit: None is not of type 'number'`, at the prepared canonical document path `parent_revision.payload.occurrences[2].gain`.

## No source edits

No product or test source was edited by this review.
