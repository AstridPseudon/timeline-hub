# Review: current-public full wrapper custody

## Verdict

**REQUEST CHANGES — do not request the full suite yet.** Reviewed the exact
worker0927 commit `28420856da6b379d809d4f858e1243949b693670` and its
`scripts/full_coherent_public_current_integration.sh`.

## Blocking findings

1. **The final pytest process can import the checkout client instead of the
   private profile client.** The central test runner injects `PYTHONPATH=$PWD`
   before invoking the wrapper. The wrapper's profile-origin probe uses
   `python -I -B` (line 106), but the final `exec "$PROFILE_PY" -m pytest`
   (line 225) does not isolate or otherwise prove its import path. The current
   Agent checkout contains `astrid_runtime_client`; with the runner's
   `PYTHONPATH`, `import astrid_runtime_client` resolves to
   `.../agt-review-current-public-full-wrapper-exit-custody-0934/astrid_runtime_client/__init__.py`,
   outside the private profile. Its bytes currently match the Runtime-95
   client, but the origin is still an ambient checkout and this does not prove
   the eventual profile run has no inherited/old-client shadow.

   **Request:** make the final test process use only the selected private
   profile for product imports, and add a final-process origin check or an
   equivalent hermetic invocation. Preserve the actual pytest arguments
   (`-m pytest -q -n 3`) and normal temporary-directory behavior.

2. **The claimed coherent closure is not actually bound to the frozen
   closure or all three source checkouts.** Lines 140–175 check only that
   there are 166 `RECORD` files and that eight named distributions have the
   expected versions. Lines 187–201 check wheel-to-installed bytes, but do not
   bind the Agent wheel to c4b, the Runtime wheel to b92, or the client wheel
   to public95; a different wheel/profile with the same versions and 166
   records could pass. The 164 pinned names/versions/VCS revisions and their
   frozen digest are not compared. `banodoco_timeline_schema` is version-
   checked but not origin-checked. This leaves the exact closure and
   no-shadow requirements unproven.

   **Request:** compare the complete frozen 164-pin carrier, verify every
   RECORD target and origin inside the private environment, and bind product
   wheel contents to the exact c4b/b92/public95 source inputs (including the
   current Agent wheel identity), before allowing the final `exec`.

3. **The central-runner helper is committed but not registered or leased.**
   The source survives worker-worktree recycling: branch
   `tl/agt-m4-current-public-batch-full-profile-preflight-0927` contains the
   wrapper at commit `28420856d`, and `git cat-file` found it after the worker
   worktree was recycled. However, the lookup for
   `agent full-coherent-public-current-integration` in
   `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/tests/suites.conf`
   currently returns no entry, and no manager lease names the wrapper/profile
   inputs.

   **Request:** before any full request, add the named ORCH suite command that
   invokes `bash scripts/full_coherent_public_current_integration.sh` from the
   worker branch/recreated worktree, include the final private profile/wheel
   environment only once it exists, and create the manager lease protecting
   the wrapper source and profile/wheel paths for the complete run.

## Evidence run

- Exact identities passed read-only: Agent c4b/tree
  `d7796be264c341adbcb9765aae374b832dede144`; Runtime b92/tree
  `6abc2f117391de8e7e35c0283f575a002199894d`; Runtime client 95/tree
  `d3a290b407fa61e6ab2d476f50c068073f70df00`; source lock names client
  `95bd3c5f6d00e9bc8cc8cbe5ef510b68ed660f3c`; C13 marker
  `30da0a5e05d4529a2b97b3c1818cf9e15842d628`; C13 tarball SHA-256
  `9412ae25c306d5118241f4d631e8eecc6eef9b2fb5a98302d40938e9f6d54738`;
  Node `v20.19.4`; ffmpeg/ffprobe and VibeComfy present.
- `bash -n <(git show 28420856d:scripts/full_coherent_public_current_integration.sh)` — pass.
- Embedded preflight AST parse and
  `git diff --check c4b964f6a050edf63a4278d35717e46a88a80386 28420856d` — pass.
- Actual wrapper preflight, with profile/wheel unset:
  `SOURCE_ROOT=$PWD env -u FULL_COHERENT_PUBLIC_PROFILE_ROOT -u FULL_COHERENT_PUBLIC_AGENT_WHEEL bash <(git show 28420856d:scripts/full_coherent_public_current_integration.sh)` — expected exit **2**, all three setup failures reported, no pytest text/body reached. The worker recorded the storage gap as `2.733592987060547 GiB`; a later read-only invocation observed `2.8802223205566406 GiB`, so no build/install/request was attempted.
- Isolated dependency-only planted-child check (real wrapper source,
  disposable fake profile interpreter): child exit **37** propagated exactly;
  the same result held through a `pipefail` + `tee` pipeline and a subshell.
  A trapped SIGTERM reached the `exec`'d child and returned **143**.
- Wrapper scan found no skip/xfail/deselection/assertion weakening, no
  integration marker, no cache-provider override, no `--basetemp`, and the
  retained default command is exactly `exec "$PROFILE_PY" -m pytest -q -n 3
  "$@"`.

## Scope / not run

No product code, product blobs, or process-doc root files were changed. No
profile was built, no dependency/shared install was mutated, no pytest body or
collection was run, and no central suite/full request was made.

### Exact follow-up command after the above fixes and profile readiness

The ORCH named suite should ultimately execute the committed helper from the
recreated worker snapshot with the exact private paths, for example:

```text
env -i HOME=/root LANG=C.UTF-8 PATH=<pinned-node-and-system-path> \
  FULL_COHERENT_PUBLIC_PROFILE_ROOT=<private-c4b-profile> \
  FULL_COHERENT_PUBLIC_AGENT_WHEEL=<private-c4b-wheel> \
  bash scripts/full_coherent_public_current_integration.sh
```

This command was **not** requested or run.
