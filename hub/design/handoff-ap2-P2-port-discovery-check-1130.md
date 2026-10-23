# Handoff: ap2-P2-port-discovery-check-1130

**PASS — bounded missing-acceptance check only.** On actual App HEAD
`be8f4296c17193454a18866a4e91176fbad8a673`, the existing
`playwright.auto-real-proxy.config.ts` listed exactly one original selector
with exit 0 under the 10-second timeout. The listed selector is the real
automatic image-placement journey at `auto-real-proxy.spec.ts:579`.

Port identity is intact: parent spec blob `4564e8a…`, current/reviewed spec
blob `fea6ba47e59c2a302a70c4162699af2ae4b339d6`; the port commit changes only
that spec, passes diff/EOF controls, and leaves the worktree clean. Existing
normal34e Runtime (`34eac004…`) and private 819acf Composition (`0.0.14`, 80
files, private required subpaths) identities pass read-only checks.

The independent 1118 evidence and its supplemental 4-known-vs-7-baseline,
0-introduced typing comparison are reused, not rerun. No semantic review,
author-test/source change, global matrix repeat, browser/body/HTTP/full/build/
service/request-test/native14/ops run, or acceptance credit was performed.
