# Main014 coordinated adoption handoff

**PUBLISHED — adopt in one normal coordinated pin change**

Published Runtime source is `95bd3c5f6d00e9bc8cc8cbe5ef510b68ed660f3c`,
tree `d3a290b407fa61e6ab2d476f50c068073f70df00`, integration merge
`108713019688b95af4394a8f0395f97d1cf233af`, tree unchanged. The normal
0.2.14 artifact version is
`sha256:54205b3ecb55038e416b31af936c9af26afa30dc1b05da16157ee4d861fe05ac`;
the full 76-artifact manifest is
`sha256:a902387c6a2315374f7e73511feea47da30191aba831b48820b3864b773a532d`.

Agent: adopt this Runtime source in the same normal pin unit as the HELD
Main497 upstream merge `497714c73531f164082555ec81b61ca5bc8b6554`. Preserve
the exact ordinary schema (`sha256:6ba7b51e…`, 55 definitions / 29
operations) and record the resulting Agent SHA/tree.

App: adopt the same Runtime source in the same coordinated pin unit, while
keeping the current initializer path. Do not activate dormant `timeline.init`
or claim native create/init/restart qualification from this publication. The
409 capture-mismatch diagnosis remains a separate follow-up.

This is adoption coordination only. Composition13 remains the paired
Composition source; Composition14, private15, ref/raw/launcher, and the
separately requested one integration full remain outside this handoff.

