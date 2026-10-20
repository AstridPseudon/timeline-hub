Implemented in [astrid/sdk/remote.py](/home/user/work/wt/agt-m2-private952-reload-source-shape/astrid/sdk/remote.py).

- Canonicalized reloaded `_source_closure` rows using existing image fieldsets.
- Preserved raw GET envelopes, payloads, pins, ordering, identities, and history.
- Classified all six failures as outer `created_at`/duplicate-manifest decoration only.
- No pin or public integration changes.

Tests:

- Native six-case reload: `6 passed`
- Native ingress file: `40 passed`
- Non-socket neighbors: `49 passed, 4 deselected`
- Socket-dependent central run: queued due service capacity; unverified.
- `git diff --check`: passed.

Recorded `commit-msg`, `commit-msg.txt`, and `DONE`.