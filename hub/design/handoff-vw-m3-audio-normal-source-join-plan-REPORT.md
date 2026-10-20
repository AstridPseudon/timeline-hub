# Normal-source PCM join proposal — complete, UNAPPLIED

Agent base `33b0a8385f2cd184f0e79544f78678bc0dbee0d7`. Three deliverable files in the branch's flat `design/` directory:

- `normal-audio-source-join.md`: exact normal-render/asset-server/Root lifetime, updated contract refs, owner work, acceptance commands and holds.
- `normal-audio-source-join.patch`: four inactive proposed additions, 101 helper lines + 180 test lines, reusing unchanged d2ad kernels. Applies cleanly to current base; NOT applied.
- `normal-audio-source-wiring.patch`: 14-line existing verified-block insertion against source candidate `435357aec`, NOT current integration; NOT applied. Uses existing validation/compiler, ExitStack and server.local_url. No nonexistent factory call or public DTO/flag/provider.

Harness should commit these three design artifacts only. Product/core/source/capture/provider/Runtime/pins unchanged. No git mutation/commit/checkout/merge/push.

Updated ratified Agent contract: `2c094da6f1e2d601e9433044d942865171a75294`, `hub/tl/agt-reviews-audio-mouth-scanner`, `design/audio-compile-contract.md` and `design/agent-review-viewing-20261020b.md`. Offset 350 is milliseconds, metadata-only; no .35 rescale. Public11 helpers supply rounded source clock and child rate. Occurrence speed stays metadata; Agent already folds occurrence gain, track gain stays downstream; curves honoured.

Read prior evidence: d2ad 22 passes, codec characterization 27, actual22 compiler reconciliation 138 PASS/5 RED. Those counts were NOT rerun here.

No transformed prepared-source factory found: current integration lacks verified_source.py; candidate 435357aec has original host mint and exact original-pair validation only. Service _segment_request replaces timeline_path while retaining original binding. Coordinator must compose the existing Python-only source path through the actual transformed pair. No authority is invented/reminted in this proposal.

Code-derived fade-phase counterexample: slicing a 0..2s clip at .5s changes source_from to .5 but retains fadeIn=.5. Recompilation restarts the fade at source .5 instead of preserving original gain 1. Path rebinding alone does not qualify the join. This is an owner dependency, not a proposed layered/window refusal.

AAC/MP3 debt retained: existing nonzero-start MP3 false refusal; absent-start ADTS and offset AAC +1024 show start_time alone unsafe. No kernel modification, new codec refusal, clock alignment or fallback. Package8/10 immutable; public11 adoption coordinated later.

## Exact verification

Working directory `/home/user/work/wt/vw-m3-audio-normal-source-join-plan`:

```sh
P=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-audio-normal-source-join-plan
sh "$P/cpu-guard.sh" env PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-agent/bin/python "$P/prepare-checks.py"
sh "$P/cpu-guard.sh" env -u NODE_OPTIONS -u NODE_PATH PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=$PWD:$P AUDIO_PROPOSAL_PROJECT=$P/proposal/remotion /home/user/work/venv-agent/bin/python -m pytest -c pyproject.toml -q -p proposal_import "$P/proposal/tests/packs/rendering/test_normal_audio_sources.py"
```

**Exit 0, 6 PASS, 0.58s**, pytest-clean-env.log. Extracted actual proposed Python adapter, existing AssetMaterializer, actual native Node/d2ad/public11 decode. Independently written stereo PCM16 -> full 30000-frame float WAVs, original 30000Hz/2 channels; rational .05 origins, unchanged props/registry/source, downstream gains, wrong Root asset URL/managed bytes, double apply, no-envelope no-op. Resolver only constructs contained URLs; no socket. Test-only proposal_import loads the unapplied module, grants no source authority and replaces no existing implementation.

Initial identical command without clearing NODE_OPTIONS/NODE_PATH: **2 PASS/4 FAIL**, existing probe_context correctly rejected ambient Node loader variables before decode. Cleaned test process environment; no policy patch. pytest.log retained.

```sh
sh "$P/cpu-guard.sh" /home/user/work/app/node_modules/.bin/vitest run --config "$P/vitest.config.mjs" --reporter=verbose
```

**Exit 0, 4 PASS, 1.03s**, vitest.log. Actual built public11 TimelineComposition/AudioTrack admits actual generated WAV metadata, preserves trim/rate/scalar gain, rejects forged origin/rate/envelope. Only media/frame primitives mocked; no HTTP fetch. Public admission does not compare source identity/content: wrong-WAV-under-matching-key/clock MUST be tested at the real host join before activation.

```sh
sh "$P/cpu-guard.sh" /home/user/work/venv-agent/bin/ruff check "$P/proposal/astrid/packs/rendering/rendering/renderers/remotion/normal_audio.py" "$P/proposal/tests/packs/rendering/test_normal_audio_sources.py"
sh "$P/cpu-guard.sh" node --check "$P/proposal/remotion/normal-audio-sources.mjs"
sh "$P/cpu-guard.sh" node --check "$P/proposal/remotion/tests/normal-audio-sources.test.mjs"
sh "$P/cpu-guard.sh" python3 -B "$P/package-proposal.py"
sh "$P/cpu-guard.sh" python3 -B "$P/verify-inputs.py"
git apply --check design/normal-audio-source-join.patch
# In $P/wiring-base, a scratch run.py read with git show 435357aec:
git apply --check /home/user/work/wt/vw-m3-audio-normal-source-join-plan/design/normal-audio-source-wiring.patch
git diff --check
# Each of the three new design files:
git diff --no-index --check /dev/null <design-file>
```

Final syntax/lint/patch/whitespace checks PASS. Ruff initially fixed one test import formatting issue, then passed; no logic change. No-index checks exit 1 for new-file differences with no whitespace diagnostics. Public11 SHA256 `dfa824a475737598477d98a2be2c2ad6ab9c3e6c8b0f967fad22e154afd74601` and all 77 extraction files verified; d2ad kernels unchanged; base exact; tracked product diff empty. Test aliases use advertised built exports only, native Node uses the same existing readonly extraction/App peers. No install/extraction/pin edit.

Every CPU batch checked absolute ORCH/QUIET.md and ORCH/managers/viewing/QUIET.md using own guard; markers absent. No release inferred.

## Hold and next steps

Bounded handoff COMPLETE; no worker blocker. Activation HELD for coordinator's real transformed-source composition, original fade phase, compatible decoder origin, coordinated public11 adoption and actual trusted normal-producer WAV positive. Existing ordinary ENVELOPE_UNRENDERED RED and strict-xfail vectors untouched; four App mismatches remain owner work.

Owner rebases the exact insertion onto the final source composition, adds actual normal-path served-WAV/asset/envelope/clock, forgery/double-apply, cleanup/authored-immutability, full/window/layer and codec positives described in the design, then runs the unchanged RED requirements. Do not merge/activate this proposal as normal-export green evidence.

No actual export/render, browser, socket, full/named/central service request, install, network, source certification or physical parity. No tests weakened/deleted/skipped/xfail-added. Worktree caches and external Vite cache/throwaway candidate copy cleaned; small proposed source/tests and verification scripts/logs retained for review.
