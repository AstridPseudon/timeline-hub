# D141f independent witness/custody review

Verdict: **PASS — author 0209 remains `NOT_QUALIFIED`.**

The exact three required App normal journeys were independently checked at their retained test roots. Their authenticated manifests and request/summary hashes match the author packet and the exact source tuple. None contains an `available_bytes` or equivalent disk sample before body start, after body completion, or as a continuous trace. The P1 and parent-move journeys terminally passed; automatic child placement terminally failed its guarded Undo-history assertion. Those functional outcomes do not create disk custody evidence.

The search covered each exact run's request, runner, bench lease, result, snapshot, D66 manifest/collection, readiness, JUnit, terminal status/exit/summary, and runtime-private logs. It also covered the D66 plain-stack source/tests, central test-runner admission and dispatch paths, worker controller/source-guard records, original admission/terminal receipts, the queued `...18617` request, and retained old immutable log/design witnesses. This is not a narrow absence claim.

The retained Runtime D89d witness is the only credible paired numeric observation found outside the App packet: `5,190,156,288 -> 4,430,635,008` bytes, bracket delta `759,521,280`, with disk-start hash `05e055...e9f8` and disk-stop hash `642489...0132`. It is explicitly excluded: it belongs to `runtime-full-d141-cut-1026005231-18778`, not an App normal journey; it is a start/end bracket rather than continuous same-body sampling; and its underlying retained test root is absent. It cannot establish App's same-kind body drop or be substituted for `X`.

Likewise, the App source-only admission values (`4,771,422,208` in the author measurement and `5,433,016,320` in the controller admission), later source-only values, and queued `18617`'s `4,793,532,416` diagnostic are not body observations. No body drop is inferred from queue state, source admission, or endpoint values. The queued request remains `NOTRUN` and unchanged. The newer App source `5fe` is not used to retarget the exact `867` runs.

Therefore `X` is unavailable and the settled fallback remains:

```text
X = unavailable
floor = MAX(4,600,000,000, 4,000,000,000 + X + 200,000,000)
selected floor = 5,000,000,000 bytes
stop = 4,000,000,000 bytes
```

No source, kit, registry, queue, request, snapshot, Git metadata, pin, hub, test, sampler, watcher, or instrumentation was changed. No heavy work was run. The production request/reply contract and original tail/assertions remain untouched.
