See the exact command record at `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m4-composition-e7-delivery-refresh/COMMAND`.

The delivery uses `git diff --binary --full-index --no-ext-diff --no-renames origin/main HEAD` plus `git bundle create ... origin/main..HEAD`; it does not use merge-history format-patch. The fresh archive proof uses `git archive`, `git apply --binary --check`, `git apply --binary`, and exact path/mode/blob comparisons.
