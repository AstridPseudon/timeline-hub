## Verdict: FAIL — do not apply

Finding 1 — the new-origin assertion is invalid.

The patch asserts `new URL(request.url()).origin === harness.runtimeUrl` at proposed-v2.patch lines 79 and 93. Browser requests use the fixed Runtime door origin; `harness.runtimeUrl` is the Runtime daemon’s dynamically changing upstream port. Therefore this assertion will fail and cannot prove delivery to the restarted Runtime. The smallest fix is to assert the door’s current discovery/upstream target through an explicit harness observation, without rewriting the request URL.

Finding 2 — artifact diff check fails.

`git diff --no-index --check /dev/null proposed-v2.patch` reports trailing whitespace at patch lines 55 and 74. Remove those spaces and refresh the patch hash/evidence.

Protected hashes verified:

| Region | Before | Virtual after |
|---|---|---|
| Full source | `a6468188ff21c4fd8bd397ff242b0260ee92ab6f2f90ac94786973eaf3c1e99a` | `fe8a4666b73c8529dbafa813cf30ee289991093a22b0bd1499c7b1cea311b4b3` |
| `faultFirstCommit` | `0ac6ab0f91cfc9fee0136ec90f408584e2a7755f245b7aea2f85f06c8c316c31` | `fff97e9377fb6eae2d08a948a17d1af9055063ee58efad3b3fd763d1db416286` |
| P3 restart/recovery block | `119b31fefb43b2d42f79f055e92bdf6de51bb800ea0273b104c235030754b9ba` | `f90fcde5ee573782a03e06e9d8f1334aa27fe46cabe1797368a9a50b4ab690f3` |

Patch hash: `16758b68c4089a0f61f008b6cb51fd1bd9e1895706c825fc8ebcdc8168847f14`.

Checks:

- `git apply --whitespace=error --check proposed-v2.patch` — PASS
- Node20 Gate5 controls — PASS, 3/3
- Virtual Node20 ESLint — PASS
- Virtual TypeScript comparison — no new diagnostics
- Author’s private lifecycle controls — reported 2 positive and 4 negative schedules passing; not independently rerun because the script was not retained as a tracked artifact
- No browser, service, original P3, full suite, or product source changes performed

The worktree source remains unchanged.