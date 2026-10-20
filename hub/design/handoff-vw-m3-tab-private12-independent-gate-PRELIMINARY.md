# Independent pre-browser gate: preliminary rejection finding

Not an approval. Awaiting producer frozen DONE/BLOCKED handoffs.

An independent read-only full snapshot of `/home/user/work/app/node_modules` found 35,618 physical entries, including 193 symlinks and 152 symlinks targeting their own containing package directory. Only five self-targeting links are in the six-entry authorized exclusion set; Composition/package is the sixth authorized exclusion. Therefore **147 retained self-targeting absolute links remain** under the ONLY-six rule.

Examples: `@acemir/cssom/cssom`, `@adobe/css-tools/css-tools`, `@babel/code-frame/code-frame`, each points absolutely back into `/home/user/work/app/node_modules` at its own parent package. Keeping these entries violates the private physical graph/no outside shared paths/no cycles requirement. Deleting or rewriting them would exceed the settled ONLY-six copy exception. This reviewer makes no expanded exclusion or repair decision.

Snapshot: `handoff-vw-m3-tab-private12-independent-gate-shared-before.json`, SHA256 of canonical entry map `4f318e4d09e07d8baad544c475662ef7aedb2900bafd658812c70bd571210ccb`. Detailed inventory: `handoff-vw-m3-tab-private12-independent-gate-links.json`. All links were inspected with lstat/readlink; none were traversed while snapshotting. No package/caches/source was modified.

No private candidate graph/controller is approved, no grant is issued, and no old failed capability is relabeled. This is artifact verification only; no Runtime, host certification, source certification, Player/export, pixel or audio parity claim.
