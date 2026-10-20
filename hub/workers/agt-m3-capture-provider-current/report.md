Implemented the pure provider hook, verified-source host handoff, and complete saved-expansion reopen. Duplicate verifier and current pins remain intact.

- Direct checks: 34 provider, 9 golden, 33 host, 80 neighbor, 23 closure, and 59 scene-source tests passed.
- Central capture: 23 passed, 4 existing xfails. Two unrelated M1 cases failed the current-Runtime/client-pin handshake.
- Central scene setup errors were resolved by supplying the fixture’s dependency override for the direct rerun.
- Runtime’s independent 20-case pairing remains the next step before verifier deletion.

Source tree: `525bdabe863a42bc177f5ff331560133f77ce634`. Commit message and `DONE` written.

[Exact commands, results, limitations, and handoff](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/agent-capture-provider-current.md).