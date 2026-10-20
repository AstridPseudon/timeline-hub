# PCM admission export — unreleased source proposal

**Complete as a source proposal; no release/adoption.** Base Composition `e80c46baf`. The complete two-file patch is [handoff-vw-m3-pcm-admission-public-export-proposal.patch](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-vw-m3-pcm-admission-public-export-proposal.patch); exact commands and diagnostics are in [handoff-vw-m3-pcm-admission-public-export-proposal-commands.md](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-vw-m3-pcm-admission-public-export-proposal-commands.md). No applicable AGENTS.md / CLAUDE.md / CONTRIBUTING was present in this worktree or its parent chain. PLAN, COMMON, current Viewing INBOX and the App blocker handoff were read.

## Need verified before editing

The exact immutable public12 graph has compile/apply/WAV, trim/rate and envelope validation, but no public source-admission function; private paths return `ERR_PACKAGE_PATH_NOT_EXPORTED`. The [handoff-vw-m3-pcm-admission-public-export-proposal-prerequisite.mjs](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-vw-m3-pcm-admission-public-export-proposal-prerequisite.mjs) replay proves that public fresh full-source PCM preparation succeeds identically for the matching record and all four forged records. `compileAudioEnvelope` ignores `render_source`; `validateAudioEnvelope` validates the envelope only.

Fresh preparation **already needs no new API when there is no prepared record**. It cannot meet this App brief's separate requirement to play the matching prepared URL and explicitly refuse its wrong-envelope, raw `.05` origin (expected `2/30`), wrong-rate and blob-URL variants. Ignoring those records and always preparing fresh would also ignore those required refusals. The public renderer's internal hook checks them, but adopting that renderer would replace the App readiness/retry owner; it is not a small admission adapter. This export is therefore needed for the specified prepared-source contract, not for PCM processing generally.

## Concrete change

`typescript/src/evaluation.ts` re-exports the **existing** `encodedEnvelopeSource` function and `EncodedEnvelopeSource` type. No implementation, validation or gain math changed; no hook, `envelopeKey`, root export, decoder, new type, DTO, renderer or save path was added. `audio-envelope.ts`, `use-audio-envelope.ts`, package.json and package-lock.json were verified byte-identical to HEAD. The existing helper checks envelope identity, exact source origin/rate and HTTP(S) scheme; this proposal adds no stronger provenance claim.

`typescript/tests/audio-envelope-admission.test.ts` adds seven tests through the evaluation barrel: exact full-source float WAV + matching positive, four individual strict refusals, existing canonical-key/missing/malformed/duck semantics, and a peer-denying import with browser/timer side-effect traps. A separate NodeNext probe compiles the **built public package entry**, including negative type assertions. A built public-entry runtime probe checks the same positive/four negatives, transitive peer freedom and untouched browser traps.

## Results

- Targeted admission + neighbouring evaluation tests: **16 passed**, 0 failed; seven are new.
- Explicitly requested existing Composition unit set: **69 passed**, 0 failed, 0 skipped. Combined distinct coverage: 76 tests. Sandbox subprocess-I/O qualification details and failed initial attempts are disclosed in the commands document.
- Test TypeScript compilation, generated-registry check, real `scripts/build.mjs`, public NodeNext type check and built-entry admission/purity probe: **exit 0** each.
- Clean private graph: **35,545 entries checked; zero additions, missing entries, changed file contents/modes or symlink targets**. [handoff-vw-m3-pcm-admission-public-export-proposal-graph-check.json](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-vw-m3-pcm-admission-public-export-proposal-graph-check.json). All scopes in our overlay were real directories; only leaf dependency symlinks were made. The first local audit classified executable files as plain files; corrected classification found no graph changes.
- Complete flat patch: forward check on a minimal original baseline and reverse check on this worktree **exit 0**; `git diff --check` **exit 0**.

## Handoff and limits

Orchestrator can review this concrete contract addition and decide its new public version before any release. **Immutable 0.0.11/0.0.12 bytes and consumer pins are unchanged.** Source and tests are on this proposal branch only; no integration merge. Flat copies of the two changed files accompany the patch.

After a separately authorized release/adoption, App can call this pure admission helper only when `render_source` is supplied; the no-prepared branch keeps its existing attempt lifetime and uses public compile/apply/WAV + rounded trim/rate for fresh preparation. App still owns decode/cancellation/retry/Blob cleanup, constant clip/track gain and readiness. None of that consumer implementation is claimed here.

No install, network, browser, render, listener/socket, central request, pack/archive, version/pin change or git mutation. No full integration suite or physical Player/export parity. Generated build/test output and the dependency overlay were removed from the worktree. No blocker to the assigned source proposal; public-contract/version approval remains the next orchestrator decision.
