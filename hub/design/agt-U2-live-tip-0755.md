# U2 live public-tip receipt

- UTC window: `2026-10-24T07:54:48Z`–`07:54:49Z`
- Exact `ls-remote` run once: returned `25359ed6877b9e13e07799bb2c9600fd143fde88`
- Local `origin/main`: same SHA
- Object: present; type `commit`
- Commit object: tree `f17171ac…`, parent `c416225f…`
- Exact ancestry check:
  `git -C /home/user/work/agent merge-base --is-ancestor 25359ed6877b9e13e07799bb2c9600fd143fde88 HEAD`
  → exit `1` (integration HEAD `3f7e63b0cf…`; merge base `74f3f7edba…`)

No network failure, retries, fetch/config/index writes, product changes, or tests. Ancestry acceptance is not met. `DONE` and commit message `chore(U2): verify live public tip` recorded.