# App Main95 prompt runner hash cause

## Decision

**APPROVE the corrected packet for central execution.** The final r46 source
is preserved unchanged. The mismatch was a stale packet pin, not process,
credential, source-guard, or selector drift. The packet now binds
`TIMELINE_MAIN95_PROMPT_RUNNER_SHA256` to the exact final runner hash
`sha256:d52ae2c084130bef6e2733da03088a7cfb8e516908e547645125e6d973cb2d42`.

No product PASS is claimed. Central preflight/list and the one browser actual
remain unrun.

## Exact comparison

Runner: `scripts/testing/main95-prompt-settings-integration.mjs`.

| Source | Commit | Exact blob SHA-256 |
| --- | --- | --- |
| Approved callback | `cd927abfa09b6f8571cfeb282763855af3e44541` | `c148574748970ccbbbacac5514b419a66731115b8736e89adf7ad45bfb827b9d` |
| r44 proof donor | `140431bd3a46a0c25b569013fe21aaff30c83050` | `b7d0732b02a533a091c76bb7a163376900725db1b5ac067979a638134800ed88` |
| Composed | `fb23bf75e0985c77b14c38f97776ca950f1b47bc` | `d52ae2c084130bef6e2733da03088a7cfb8e516908e547645125e6d973cb2d42` |
| Final r46 | `dfb96f10a3f33abcbef733ee55d9874e3aaeba01` | `d52ae2c084130bef6e2733da03088a7cfb8e516908e547645125e6d973cb2d42` |

The approved callback→donor diff is exactly:

- line 6: the comment changes from the existing SettingsAutoDisable journey
  to the distinct native settings-prompt journey;
- line 62: `SETTINGS_CASE` changes from the old scalar SettingsAutoDisable
  title to the exact native prompt title;
- lines 417–420: discovery error/log labels change from `settings-prompt` to
  `SettingsAutoDisable` wording in the donor’s composed descendants.

The donor→composed and composed→final comparisons show no selector or guard
change. Donor→final differs only at line 6 and lines 417–420: those harmless
comment/diagnostic labels were restored to `SettingsAutoDisable`. The actual
selector remains the prompt title at line 62. The spawned Node/Playwright
argv, one-test discovery cardinality guard, source pins, credential handling,
environment construction, overlay/restore checks, and all other process
guards are unchanged. The old `SettingsAutoDisable` text in these locations
is diagnostic wording only; it cannot select the old test because `--grep`
uses `SETTINGS_CASE`.

## First cause and packet correction

`b7d0732b…` was not the final source hash. It was the exact blob hash of the
r44 proof donor commit `140431bd…`; r47 carried that approved r44 packet pin
forward without recomputing the runner hash after the final composition. The
final composition commit `fb23bf…` and final r46 commit `dfb96f…` both contain
the same `d52ae2c…` blob. This is why the r47 HOLD was correct as a packet
identity check but does not require a source repair.

Updated packet:

`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/run-on-main-app-settings-prompt-current.md`

The packet is now `APPROVE`, pins the full final hash, retains the exact final
App commit/tree, Agent/Runtime/Composition/browser pins, prompt title, argv,
credential/environment guards, and explicitly does not replay the old
SettingsAutoDisable case.

## Evidence

- `node --check scripts/testing/main95-prompt-settings-integration.mjs` —
  PASS.
- `node --test scripts/testing/main95-prompt-settings-integration.test.mjs` —
  PASS, 1 file / 1 test.
- `git diff --check` — PASS.
- Exact blob hashes and zero-context diffs for all four requested commits —
  PASS.
- Existing r44 private-overlay Playwright `--list` evidence — PASS, exactly
  one prompt test and zero final failures; not rerun here.

No browser, Runtime door, current graph `--list`, actual/retry, build,
install, dependency-graph construction, localhost/live socket, or full suite
was run.
