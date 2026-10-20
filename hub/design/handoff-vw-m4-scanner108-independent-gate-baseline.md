# Scanner 1.0.8 independent gate baseline

Baseline review is against the exact 1.0.7 archive rejected by the Agent
policy review.

- archive SHA-256: `baf2fd28f96670b02e4dc63e21bc680e2ab0339a97671515d79ab91f9cbd3e27`
- archive size: 15,630 bytes
- extracted four-member flat copy hashes match the frozen flat handoff
- extracted test command: `/home/user/work/venv-agent/bin/python -I -B -m pytest -p no:cacheprovider --basetemp .../pytest-baseline -q .../baseline107/tests --agent-root /home/user/work/wt/vw-m4-scanner108-independent-gate`
- result: **40 passed in 5.67s**

Independent mutation review reproduced the known defect: malformed audio fade
durations and curve containers remain `status: complete`; malformed visual
values are only partially rejected. Free-form transition string IDs/mappings
remain allowed, while structurally malformed transition values fail closed.

No owner data, full suite, browser, renderer, listener, network, install, or
shared dependency mutation was used.
