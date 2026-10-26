# F/D141b validation

## Verdict

`FAIL` for candidate commit
`6274c362f902632a99ab0f676ad458ace08f550b`.

## Commands run and results

- `git -C /home/user/work/agent show 6274c362f902632a99ab0f676ad458ace08f550b:evidence/command.sh | bash -n` — exit 0.
- `git -C /home/user/work/agent show 6274c362f902632a99ab0f676ad458ace08f550b:evidence/source-manifest.json | jq empty` — exit 0.
- `git -C /home/user/work/agent show 6274c362f902632a99ab0f676ad458ace08f550b:evidence/admission.json | jq empty` — exit 0.
- `git -C /home/user/work/agent diff --check c585cb2aa73c5298d474e614cb2144f58f27e605 6274c362f902632a99ab0f676ad458ace08f550b` — exit 0.
- Read-only `git rev-parse HEAD HEAD^{tree}`, `git status --porcelain --untracked-files=all`, and receipt checks for `/home/user/work/wt/agt-pin-8b6ed211`, `/home/user/work/wt/rt-pin-fa9cd546`, `/home/user/work/wt/app-pin-7ca61bb3`, and `/home/user/work/wt/vw-pin-67b8aa3d` — all four exact SHA/tree pairs and clean statuses matched the packet.
- Read-only frozen source checks against the recorded four repository origins and frozen commit objects — all four commit objects existed and their trees matched the recorded trees.
- Read-only `git ls-tree` membership check for the 17 roots — all present.
- Read-only `git cat-file -e` and `git ls-tree` checks for the five approved absent roots — all five absent (`cat-file` exit 128, zero tree lines).
- Read-only command inspection for `-n 3`, cleared `addopts`, disabled cache provider, timeout 45, exact source cwd/PYTHONPATH, gate markers, source-before/source-after, and body-only TERM — all required tokens present.
- Read-only `test -e` checks for the command publication path named by `service-row.txt` and its containing evidence directory — both absent after author worktree recycle; the row's hash guard is therefore not executable until exact publication.

## Scope limits

No product imports, pytest, collection, preflight controls, service request,
suite installation, socket, or comparator body was run. No source/code,
checkout, branch, shared dependency, or other worker worktree was modified.

## Blocking semantics

The command's body redirects stdout and stderr together, has no successful
exit-code witness, ignores monitor return 97, and does not carry the separate
4.6 GB source floor. It records interpreter identity without asserting it.
These are command-level acceptance failures, independent of the retained
provenance and root-list passes.
