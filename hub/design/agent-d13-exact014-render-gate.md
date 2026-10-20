# Agent D13 exact014 render gate

The owned named suite `registered014-render-integration` was added for the
staged014 Agent consumer (`65c87dd5`, tree
`78fafd290c7bd61e98e82539fba62d9d96a33dfe`). It combines the existing
registered-native render lane's `env -i` current Node/Remotion/read-only peer
profile with `ASTRID_RUNTIME_CHECKOUT=/home/user/work/wt/rt-pin-a0dca169`
(Runtime `a0dca169`, tree `4b7dd0fe44be973c344bab3de568eaf0bdd28476`) and
the production `venv-agent-child-s2` helper. Its command targets only the
integration tests in `tests/packs/video_editing/test_runtime_publication_chain.py`.

Qualification request:
`agt-m2-d13-exact014-render-gate-registered014-render-integration-1020155702-1130`.

The canonical proposal positive passed. The real render positive completed
the settled proposal/requester outbox, lost-ack restart exact retry,
revision-pinned normal render, CAS MP4, `ffprobe` decode, and undo assertions,
then failed during `host.shutdown()` with
`CustodyError: CPU attempt cleanup remains unresolved`. This is a custody
teardown contract failure after render, not the earlier missing Remotion
environment failure. No donor result, fallback server, skip, xfail, or
product rework was used. D13 remains held pending an owning-manager decision
on that contract gap and a fresh exact-tuple pass.
