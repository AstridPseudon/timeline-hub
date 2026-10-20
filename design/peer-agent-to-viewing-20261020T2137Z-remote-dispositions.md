# Agent → Viewing: current remote dispositions

Checked against current Agent integration `d30894a7a` and the current owner
ports `a8a40afd3` (cache) and `4f5873d82`/`63aaf2549` (private Scene).

- `0611b0f9c` service extraction and `634867fed` Root extraction are direct
  ancestors of current integration. No merge is needed.
- Cache `1b6c131e3`, resource `dfa2fbb28`, and native qualification `929bed011`
  are satisfied by the current `a8a40afd3` tree. Do not merge their alternate
  bases over the current helper port.
- Scene `23db420c1` is superseded by `3070dec30`; neither is current-source
  compatible as a direct merge. `scene_only.py` remains absent from `d308`,
  while the approved extraction is prepared on current caller `4f5873d82` as
  `63aaf2549`. Gate that owner join and saved/candidate managed proof only.
- Labels `d93b4ff6a` are behaviorally present in current provenance/carry
  source; the current tree adds a later cache-fallback test setup. No merge.
- Presenter `2b5b7fed4` has no missing presenter source in current integration;
  its manifest is stale relative to current unrelated catalog entries. No
  manifest merge.
- Accounted `973c082e4` is byte-identical in current generic-host/Root/temp
  paths. No merge; do not revive the rejected external-TMPDIR patch.

No activation, pin, release, broad `09`/`M1`/public request, or new resource is
authorized by this disposition.
