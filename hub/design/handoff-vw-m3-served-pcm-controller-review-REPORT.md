# Served PCM controller/fixture review

## Verdict

**DEFECTS — do not spend the central run grant until the controller hardening below is applied.**

The whole-source fixture itself is otherwise APPROVE-ready for one central run after the
normal-PCM producer has a final committed SHA and the manager supplies the approved stable
public12 project. It is correctly bounded to seven cases. The window/layer cases must remain
ordinary RED and must not be included in a `whole` claim until the source-owner join exists.

## Findings

### D1 — source freeze is incomplete before and after the run (required)

`handoff-vw-m3-pcm-served-source-fixture-controller.py:30-33` compares the Git tree and
`git diff --name-only HEAD`, but `git diff` does not report untracked files. A central snapshot
with an untracked import/helper can therefore pass the advertised “exact approved producer
source tree” check and still affect `PYTHONPATH` imports. The controller also exits directly
from the pytest subprocess (`:91-95`) and never rechecks the source tree or approved project
helper/package bytes afterwards.

Minimal correction: add a clean-tree assertion using
`git status --porcelain=v1 --untracked-files=all` (empty), and run the same source-tree,
helper-byte, dependency/package, and environment postflight in a `finally` after pytest.
Preserve the pytest return code while reporting a postflight failure. This is a controller-only
fix; no product or test expectation needs changing.

### D2 — returned URLs are not pinned to the fixture’s actual server (required hardening)

`handoff-vw-m3-pcm-served-source-fixture-test_normal_audio_served_sources.py:33-42` checks
only `http` and hostname `127.0.0.1`. It does not assert that the URL port is
`server.port`. The later staging-path check proves the URL path names a file in the intended
staging tree, but a different loopback listener serving the same bytes would still satisfy the
HTTP/PCM assertions.

Minimal correction: pass the live server port into `_get` and assert
`parsed.port == server.port` for both original and prepared URL reads. Keep the existing
`path.relative_to(attempt)` and `body == path.read_bytes()` checks. This makes “actual
host-served WAV from this invocation server” explicit without adding an auth protocol or
localhost grant.

## What passed review

- Positive cases call the actual `prepare_normal_audio_sources` product module from the
  source snapshot, with the actual `AssetMaterializer` and `InvocationAssetServer`; there is
  no fake source factory, mocked HTTP, custom authority setter, DTO, or self-written positive
  attestation.
- The fixture first GETs each original URL and compares its bytes with the managed source,
  then GETs each returned prepared URL while the server and attempt directory are live.
  It binds the returned path to the actual server staging file and checks exact response bytes.
- The native oracle validates float32 WAV format, stereo channels, native 30000 Hz rate,
  complete 60000-frame output, every sample against an independently calculated fade ramp,
  and unequal source content for the two assets. It also swaps the two same-clock/envelope
  WAV bodies and requires the independent oracle to reject the swap.
- Forged `render_source`, wrong registry URL, missing asset, changed staged bytes, wrong
  managed digest, and double preparation are rejected before accepting output. Inputs,
  registry, opaque data, clip/track gain, trim/rate, and source metadata remain unchanged.
- Batch failure removes only the helper-owned batch and leaves the attempt sibling. Success
  and interruption remove attempt WAVs before 404 checks; server shutdown checks port/thread;
  materializer cleanup removes only its own staging tree and preserves managed originals and
  the unrelated outside sentinel.
- The fixture does not override `allowed_origin`; it uses the existing invocation server
  policy, which only emits CORS for its exact existing `http://localhost:3000` renderer origin.
  The urllib reads send no `Origin`, and the controller adds no localhost/auth grant.
- The controller preserves the inherited `HOME`, `LANG`/`LC_*`, `PATH`, and `TMPDIR` values
  in its child projection, only prepending the approved Node directory and adding the explicit
  source/project variables. It does not alter the parent environment or use HOME as a data
  root.

## Ordinary RED prerequisites

The two parameterized cases in
`test_slice_retains_original_phase_on_actual_http_until_source_owner_joins` (`window` and
`layer`) are correctly ordinary RED, not skips or xfails. Before granting `with-phase`, the
Agent source owner must:

1. retain each actual original compiled occurrence clip before `_segment_request`;
2. carry the trusted original/current pair through source validation and serialization;
3. invoke the producer with that actual mapping, never reconstructing it from
   `app.astrid_slice_origin`, IDs, bounds, or caller metadata; and
4. preserve the same served-WAV/native-byte assertions through the real caller.

The exact required source transform is the contract already recorded in
`design/audio-compile-contract.md` and the normal-source handoff: derive rounded public
`q0/q1`, child playback rate `r`, compile the original envelope once, and translate all
keyframes by `-(q1-q0)/r` in disposable derived props. Do not add a refusal, skip, xfail,
second compiler, tolerance widening, or authored write.

## Minimal central grant after D1/D2

- final committed producer SHA (not the current uncommitted candidate);
- one approved existing installed public12 project whose three helper files match the final
  source and whose archive/77-member, React 18.3.1, Remotion/media/layout-utils 4.0.509,
  and Node 20.19.4 preflight passes;
- the exact Node executable path;
- one named suite registration using `--scope whole`; and
- one central request/wait invocation from `READY.md`.

Do not grant `with-phase` until the four prerequisites above are proven. A `whole` pass does
not close phase transport, normal-route admission, `_execute_remotion_locked`, Player/export
parity, or full-render claims.

## Pure review checks run

- `/home/user/work/venv-agent/bin/ruff check <flat fixture> <flat controller>` — PASS.
- Python AST parse of both flat `.py` files — PASS.
- `git apply --check handoff-vw-m3-pcm-served-source-fixture-UNAPPLIED-tests.patch` — PASS;
  patch remains unapplied.
- `git diff --check` in this review worktree — PASS; worktree had no product changes.

No listener, browser, network, full suite, central test service, or fixture execution was run.
