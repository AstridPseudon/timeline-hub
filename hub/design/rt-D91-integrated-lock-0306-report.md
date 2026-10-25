## Report

- Prepared exact D91 tuple:
  - Agent `562ee30b6e…`, Runtime `6634a17f…`, App `24865fa2…`, Composition `635f4de0…`.
  - Reviewed test blob matched `00c1ccc5…`; 10 selectors preserved.
- Installed one CAS-protected D73 row; unrelated registry bytes remained identical.
- Controls passed: positive exit `17`, one body call; poison exit `1`, zero body bytes.
- Submitted service `agent-d91-integrated-lock-0306-1025030907-9472`.
- Result: failed before pytest because mutable Agent path had moved to `7f4ea9ce…` instead of authorized `562ee30b6e…`. No XML, collection, or test body ran.
- Preserved prior 9031 unchanged. No product/test changes; worktree clean. Evidence is 252 KB.
- Commit message and `DONE` marker created.

Blocked by absence of an immutable checkout for the authorized Agent commit. Next step: provide that exact checkout, then submit one fresh authorized body.