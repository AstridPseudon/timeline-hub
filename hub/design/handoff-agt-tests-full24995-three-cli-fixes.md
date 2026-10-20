# Handoff: Agent full24995 CLI fixture repair

Historical full agent-full-remotion12-s2-integration-1020143255-24995 is
classified in agent-full24995-classification.md. It has exactly three failures,
all the same stale fake-checkout seam after f5d0b4e0 changed implicit edit
preflight to _check_core():

- one asset forwarding test;
- two voice binding/gap forwarding tests.

The worker changed only the two named test files, adding _check_core = check
to their existing fake checkout fixtures. All forwarding/default/repeated-gap
assertions remain unchanged.

Proof: the two whole files pass (4 passed); old CLI neighbors and working copy
tests pass (254 passed); selected Ruff rules and git diff --check pass. No full
suite was rerun. Current-fix patch SHA-256 is
415744518d1223940e6e1588ebe9c6eee0a26250b7696063f36771ad387bd45b.
