# App2 parent media capture — independent review evidence

Verdict: **REQUEST CHANGES** for `3d47f353c4af3f97e4493b4dddad55da2e59ad8d`
over `2f8c6d89784f2823853844e96bddaa1b1ef95686`.

The actual TS-produced populated-registry command was accepted by frozen Agent
310 with identical command, record, reads, bindings, dependency pin, writes,
authored bundle, projection, inverse restoration, and replay. The exact five
field selection and detached verified media response remain basis-owned.

Two parity repairs are required before approval:

- Equal `parent.registry` and `parent.config.registry` containers with opaque
  data but no `assets` map crash in TS when the new alias is written to the
  second registry. Agent 310 creates the effective mirrored binding and keeps
  opaque data.
- Equal empty `parent.clips` and `parent.config.clips` arrays diverge after TS
  appends the birth. Agent 310 records the `parent.config.clips` derived write
  and keeps both arrays equal.

Minimal repair proposal (no product patch applied): carry the Agent-310
effective-parent-registry mirror behavior and the existing non-media parent-add
mirror update into the media executor. Preserve the Agent record/read/write
order, including the derived write; add only the two focused regressions.

The shared wiring proposal remains intentionally unapplied: current App media
producers still emit legacy rows/prepared-media commands and do not expose the
original five-field pin plus detached Runtime verification needed by this
helper. Manual recovery ADD remains App-owned and outside this row.
