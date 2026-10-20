# Native frontend final gate — APPROVE

Approve candidate **`bdf883271fd522552c004706024ff04b1b6aa73f`** for bounded integration onto **`7970544bb17dfcf234bd1cc1bb55ab5d713decd8`**. No blocking finding, unreviewed scope, assertion weakening or PLAN disagreement. The combined patch is 19 paths; previously reviewed bases remain intact apart from the two requested fixes, stale-handle fencing and additive composition tests.

- Raw `clip_type` now accepts canvas x=600 as stored **x=100**, retaining scale=6 and original guards. Exported **`1e-06`** gutter now permits hold=1→2 while preserving its timestamp. Four unchanged original review probes pass.
- Private composition on current integration: **180 targeted tests passed**, plus the **4 original probes**. Mixed outbox tests prove exact A retry, original B claims, fresh B key, disjoint acceptance/relevant conflict, reverse-order draft preservation, and stale-handle refusal without recapture.
- History/recovery `5430a971`, trim `6a595224`, and latest timing fix survive. Existing Checkout methods remain unchanged; sheet retains client-aware retained-history lookup; CLI retains publication redo. Private composed tree: **`37a266d70d228316fa972413fb8603d8bd2b9692`**.
- Integrate with current history code: the sheet insertion patch needs two context lines adjusted for current `apply_sheet(..., client=...)` and `find_version(..., client=client)`. Regenerate `cli-surface.json` and `artifacts.json` from the combined code; both private checks pass. Do not replace overlapping files with the older candidate versions.

Verified actual central **18 passed in 81.09s** at candidate tree **`b3250fda18204300720baf403734a3a14f7cfffd`**, pinned Runtime **`94114269d1ce23ab3224d7eca5a85138ce2b5fed`**. This is development evidence, not current/final-tuple qualification. Verified the recorded **609 passed in 51.15s** and unchanged local-test/product sources; its local execution did not atomically record a whole-tree SHA. Did not rerun 609 or any full/HTTP suite.

Exact independent probe command (from the private composition; `PYTHONPATH` selects its source):

```sh
env PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD" /home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider -c pyproject.toml --basetemp=../pytest-tmp-probes ../notes/test_review_checkout.py ../notes/test_review_sheet.py
```

Result: **4 passed, 1 imported-marker warning in 2.56s**, exit 0. The complete exact 180-test command and generator checks are in the linked worker report; **180 passed in 30.66s**, exit 0.

No source fixes, shared dependency writes, Git mutations, pin/schema changes, legacy retirement or M2/AG03 closure. Next: history-preserving integration, then targeted central qualification of the safe tuple. No blocker.

Exact commands, outcomes, source identities and limitations: [worker report](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-review-native-frontends-final/notes/report.md).
