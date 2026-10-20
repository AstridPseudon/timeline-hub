# Agent raw trim current pair

Date: 2026-10-20

## Composition

Composed only the reviewed-manifest candidate `ef56a3fd55dd1efa9f529e7caf6e32e0f36a0766`
and the disjoint-track-read candidate `9989adb34d55153424d3d71287dfe0d89688e770`,
both applied to the same base `f97b2b87688abb20280572a5fc23e4f69ec9e3f8`.
The duration-read fix `9bf503f98deb3051cb9caceeae3ea6a5ebd5f185` remains preserved
through that base. The two workers' additive changes to
`test_recipe_m2_clip_trim.py` are both retained.

The harness commit SHA is not available until worker exit. Pre-harness combined
identity:

- clean worktree tree: `7f43878c1f37abf1a8bef6d79b44df51d1ced50a`
- combined patch SHA-256 from `f97b2b87` to this worktree:
  `d1f913712bf5f465a635ed16948e90c34f592a19efdd78162c4f0abbc44c4144`
- candidate source tree before the additive delta:
  `4812245b80d2e8b4180c930b6d7bb8264524c8df`

Changed source blobs (SHA-256):

- `astrid/sdk/timeline/commit.py`
  `42b7088e509037d3b3f2baa393b685b10c001053c41779a5e8e9b14faa162ece`
- `astrid/sdk/timeline/sync.py`
  `57aa86f76a1820eadae976ec2c765594eb32c9c882fb46c97ad687fdc85fa1bc`
- `astrid/sdk/timeline/_trim_commands.py`
  `1baddedb63faa3f7e923d8cb5e51030a6982334c179f04b0a5bf8e02e221042b`
- `tests/editing_conformance/test_recipe_m2_clip_trim.py`
  `596afdd477b0a45d1ce364d67fd2ca88c076c2908311197eb79f8265f08a5589`
- `tests/editing_conformance/test_commit_runtime_raw_audio_trim.py`
  `36bb261752dbc7208b1f9b33699034f756009f7b05443e7bc8f5e5d9e6816dfc`
- `tests/sdk/test_timeline_sync_native.py`
  `881cfb52d0d3f9b0379bc57d6e93d50cfa07ad443a80df5c722d8aa00bd04329`

No Runtime files, custody/D13/private-carrier machinery, new pin/release,
latest-head or memo authority, or comprehensive journey changes are included.

## Exact Runtime pair

- inner reviewed Runtime 7d candidate: commit
  `7d1cfa6b1da0c50bb8a9d3430dcaa6272b20b55e`, tree
  `ac693097189637d3bd0fc3a39299d9b166758853`
- authorized named-suite outer Runtime tuple: commit
  `a0dca16975dfe8f5e762703b99d9791a16cf7fd7`, tree
  `4b7dd0fe44be973c344bab3de568eaf0bdd28476`

The existing exact-7d wrapper set `ASTRID_RUNTIME_CHECKOUT` to the inner 7d
candidate. It exercised only the two actual public HTTP cases: genuine WAV with
absent authored duration, and malformed bytes. The outer named suite supplied
the authorized a0 tuple.

## Evidence

Focused union of the 236-neighbor and 158-overlap lanes:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=$PWD /home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider --basetemp=/tmp/agt-m2-raw-trim-two-fixes-union tests/editing_conformance/test_recipe_m2_clip_trim.py tests/packs/timeline/test_cli_commit_trim.py tests/sdk/test_timeline_sync_native.py tests/sdk/test_timeline_sync.py tests/sdk/test_timeline_clip_trim_provider.py tests/editing_conformance/test_cli_trim_runtime.py
262 passed, 2 deselected in 49.39s
```

Existing exact-7d wrapper through the central test service:

```text
request: agt-m2-raw-trim-two-fixes-compose-native014-sockets-integration-1020181508-11875
2 passed, 3 marker-registration warnings in 4.43s; exit 0
```

The six Session authority controls are covered by the focused union, and the
two actual HTTP WAV/malformed cases are covered by the central wrapper. Ruff
and `git diff --check` passed on the composed source. The original historical
literal/comprehensive Runtime journey was not rerun; Runtime owns that single
authorized rerun after this new Agent SHA is available.

## PEER REQUEST from agent — 2026-10-20T18:21:45+00:00: final combined raw-trim source, retry original two nodes
Manager APPROVE bounded normal-private source27e823a5ddeb4f8995c436b44c8d42f728350919/tree7f43878c1f37abf1a8bef6d79b44df51d1ced50a, combines ef56 originalBASEmanifest read+9989 narrow consumed track fields on f97/9bf. 262focusedPASS +2actualexact7d WAV/malformedHTTP cases11875 (tested3f99tree differsONLYtemporaryrunner symlinkremovedafter). No schema/client/pin change; a0/f021 ordinary014 immutable. Exact source/tree/tuple design/agent-raw-trim-current-pair.md. KEEPcheckout agt-pin-27e823a5 requested.
Please rerun ONLY original historical-audio/literal-media failed nodes ONCE with yourgenuineWAVsetupacf80+observerfix and EXACTreviewedRuntime7d-compatiblecurrentcandidate; originalcommands/positiveassertions unchanged. If Runtimefixturetest source isnewerwithonlytestpatches, keepactualserver014artifactseparateexplicit. No comprehensive passingdoorcontrolrepeat/full. Label-only concurrenttrack edit mustrebase; consumedactive/kind/role/identity changes stillguardconflict. OriginalBASE+declaredmedia pin andBackendexactdurationread/singleFDguards unchanged. No clientduration orholdauthority. Returnexactcurrenttuple/result/remainingfailure.
NewC13pin isMERGED6f0cdc7d onpublic013 (sameRuntimeclientbytes),130boundedtests. Private014source27 retainsComp12 foritsqualifiedtuple; no relabelnew13. Separate D13process-group11line successor2PASS remainsUNMERGEDpendingindependentsecurityreview; no needpairit into rawHTTPtest.

Manager harness correction: Git final27e823a5 tree is 7f43878c1f37abf1a8bef6d79b44df51d1ced50a. Worker hand-computed8cc3 was wrong. Git diff from tested3f99 to FINAL7f438 shows ONLY deletion of temporary _test_raw_runtime_pair.py symlink; zero product/test changes. Exact source qualification remains valid on its same blobs; use final Git identity, not guessed hash.
