# P2/A3 protected review — FAIL

Reviewed cumulative delta `bbba1990` + `ec78b6be` against clean `c101477597`.

Findings:

- `assertNativeCommandShape` validates reads, selections, expect, authorship, and bindings structurally only. Wrong paths, keys, scopes, values, or relationships can pass.
- `assertNativeStepShape` accepts any nonempty structurally valid patch/dependencies; it does not anchor operation, path, before, or after to the inverse target or canonical before/after state.
- `assertNativeRecorder` echoes authoritative command reads/selections and only checks write cardinality plus generic state shapes. Write paths, refs, after-values, derived effects, and bindings are not independently source-derived.
- `acceptedPost` and `historyFor` fabricate reply/history records from observed request/result data, so the controls are expected-from-observed rather than independent.
- Native accepted replies do not independently verify canonical document/digest against the actual Runtime readback.

Retained predicates are present for doc.patch atomic/omitted-reads/nonempty-patch behavior, asset/element/placement canonical changes, registry/config/manifest/sibling isolation, legacy-route absence, reload, and guarded Undo. They do not cure the incomplete native authoritative oracle.

Evidence:

- `git diff --check c101477597 ec78b6be2386550ee5709adb8d1ebe90bead64cb` — passed.
- Worktree remained clean.
- No acceptance, TypeScript, ESLint, browser, merge-request, or submission run was performed because this review failed before application.

No patch was applied; no blobs were applied; no normal receipt or actual submission ID exists. `DONE` and the P2 commit message were written.