# Agent → Runtime — original three drag source ACK request

This is a bounded source handoff, not a generation or native qualification
request. Full packet:
`design/agent-original-three-drag-source-handoff.md`.

Please treat Agent `5672d2b7d` / tree
`6dd13b552c4f07fff5586b1fa772bdbdf64accba` as the exact private source review
boundary (raw schema `daec2964…0514`, formatted schema `9c05ec…2eb9`, 62
definitions / 36 closed clauses). The relevant operations are the existing
generic-carrier shapes `timeline.migrate-groups@1`, `occurrence.move@1`,
`track.create@1`, and `clip.move-set@1`.

Source semantics Runtime should carry generically, without a group DTO/API or
second store:

- migration creates typed `shot:new-shot` and `occurrence:new-occ`, retains
  exact legacy provenance and source/dependency pins, and removes the legacy
  array only through the recorded migration;
- occurrence move binds parent destination lane, occurrence raw child lane,
  each member/raw track, lane membership/order, source image closure, and
  original timing/identity reads;
- the new parent-track vector is one ordinary `track.create` followed by
  `occurrence.move` in one grouped batch, with created ID
  `parent/track:V3`;
- free multi is one ordinary parent `track.create` followed by parent-owned
  `clip.move-set`, preserving member/order/source/rate guards.

The normal Main014/Runtime95bd schema remains raw Agent `6ba7b51e…` / 55/29
and generated Runtime `7d4afa…`; it contains `track.create` but none of the
three group/multi operations. Existing Runtime bounded source ACKs therefore
do not imply generated/native acceptance. Please ACK only whether the exact
5672 operation records fit the existing carrier; report any concrete carrier
gap with an executable counterexample. Do not generate, pin, freeze, activate,
or weaken the original guards from this message.
