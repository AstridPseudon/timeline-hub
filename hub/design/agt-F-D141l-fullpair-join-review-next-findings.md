# Independent findings

`PASS_EVIDENCE`. The exact current terminal pair is mechanically consistent and independently reconciled.

- Cut `agent-agent-core-full-1026100428-24814`: exit 1; XML hash `6710f7fe1b4b1a0b4d43614f0fe58d437b0b6fff76990e4a717022cef773fcd5`.
- Pristine `agent-agent-core-full-1026103030-25513`: exit 1; XML hash `9d36fcecf662cc9138cd30cb6ad674a57db30209b18593f29da08ed961792bba`.
- Concrete IDs: cut 9388, pristine 3082, matched 3018, cut-only 6370, pristine-only 64.
- Unnamed aggregate records are explicit null identities: 173 per side, reconciled from nested XML attributes. No historical aggregate IDs were fabricated.
- Classifications: 8991 `CUT_PASS_NOT_REG`, 19 `FAILS_BOTH`, 373 `N_A`, 5 `UNKNOWN`, 64 `PRISTINE_ONLY`; zero exact REG candidates.
- The five source-present cut-only non-PASS IDs remain `UNKNOWN`; source-absent cut-only IDs are `N_A` only with direct frozen-ref Git absence.
- Root labels and D134 clusters were checked against retained structure tables only. Source-limited bad-both rows remain bad-both and do not trigger Farm.

No repair, rerun, source edit, Farm run, or repository merge was performed.
