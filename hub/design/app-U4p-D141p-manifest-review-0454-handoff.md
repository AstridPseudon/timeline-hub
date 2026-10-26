# U4p D141p handoff

PASS. The candidate is ready for the App merge queue.

The App candidate `dc1a86cf4797b6ca3799d9ad1dee7e7d949caf04` / tree `dd989783046aeff652486a1ba39db42aea86e201` has sole parent `8f278b91accec5852e39bb84822e99124fccb81d`. Its only changes are the authorized manifest and Astrid browser provenance metadata.

The manifest pins Agent `8585ed9c0404d0187b2ce70242d25114a32747c2`, tree `92a3ffdb5a8bf476e10bfa1bbda3e2856fb9938c`, and retains Runtime `6a011d58e69173d70e2e9bb3ac434ac8f9e87d8d` plus schema digest `sha256:867f3553ac0ff264300e5a2596b363cdb4c071842eb6570ad461c093d351708b`. The source checkout is clean, the installer User-Agent requirement is present, normal updater plans are repeat-idempotent, and vendor verification passes.

All 160 vendor payloads and every other App tree entry are exact to base. The unchanged installer acceptance tests pass under supported Node `v20.19.4`: 4/4 passed. No source, test, generated, pin outside the authorized metadata, kit, hub, or Git metadata writes were made; no service, queue, merge request, body, or collection operation was performed.

Recommended next step: merge this reviewed candidate through the App queue, preserving the exact source and Runtime identities above.
