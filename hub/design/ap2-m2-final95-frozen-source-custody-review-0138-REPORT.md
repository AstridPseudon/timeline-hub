# App final95 frozen-source custody review

## Disposition

**APPROVE** the worker 0125 App source-binding fix and the current helper set
for the parent qualification command below. The final95 parent role binds the
actual frozen composed App source, not the older 10fa pin branch. No product
code was changed.

HOME remains the sole owner of the live final95 bootstrap create/init/retry/
restart/undo proof. I reviewed its constants only and did not launch that
proof or any actual gate. The retained `4657` bootstrap result remains
unqualified as recorded in current HOME status.

## Closed source profile

The current `final95` role table is closed as follows:

| role | App commit | App tree |
| --- | --- | --- |
| `parent` | `25155ccb22728780a3ecd6379a929cad75cc1400` | `972d2ed2e4f85f334eb9f2e6ca40d9bfbce9eac7` |
| `bootstrap` | `dfdbef10f9d8ccf1a630f000cd076023918ead8a` | `33674ef4bbaa4b043baed77492621095cccc28f7` |

The parent commit was obtained through `bin/request-checkout` as the
immutable detached checkout `/home/user/work/wt/app-pin-25155ccb` and
verified clean. Its HEAD and tree exactly match the parent role. The four
App pin files match both the parent candidate and approved App pin commit
`10fa2ff9a8216604aa39e3584f89dc9e7a09080a`:

```text
runtime.lock.json                                      770352eaf1d015e90fca0ed2f1893749b73b69356ca82a7223b2573276fe485e
src/integrations/runtime/generated-contract-metadata.ts 4cd934d868eafd5ab82578da2232f1ee13f04d83c9314b3473b75bd951570044
src/integrations/runtime/generated.ts                  c575f183b6486dd07e8ec798f5a46bff4c9ffc0918892b189c1a433b9f80762d
src/integrations/runtime/timeline-commit-types.ts      f8cbbbbc48713a308c2ac2e2e977d08525c4280ef4dc93cd3e8d842245394564
```

The bootstrap constants match the independently approved bridge-base source
review. They are not substituted for the parent source in the parent lane.
Unknown final95 roles refuse before source preparation. The old202 profile
still defaults to its historical tuple and bypasses the final95 App-root
guard; its compatibility probe passed.

## Preserved dependency and source checks

Read-only checks passed for:

- Agent `6efc81500a0e0688c2bb41e736503f0fc3e04abb`, tree
  `2ed2b8a12b5b3391ca221ba6ff05390f71a73556`.
- Runtime/producer `95bd3c5f6d00e9bc8cc8cbe5ef510b68ed660f3c`, tree
  `d3a290b407fa61e6ab2d476f50c068073f70df00`.
- Runtime manifest: 76 artifacts, manifest SHA
  `a902387c6a2315374f7e73511feea47da30191aba831b48820b3864b773a532d`.
- Artifact package: `sha256:54205b3ecb55038e416b31af936c9af26afa30dc1b05da16157ee4d861fe05ac`.
- Raw edit-command schema `6ba7b51e9518e7fb08b27ad5b7225855276b657d0adebf704dd853f699768f2d`, byte-equal between Agent and Runtime.
- Locked public13 graph: version `0.0.13`, archive SHA
  `895c628ab0727c8975247310fd0319b0f546a8d032a57072c9e364e20965ca30`.
- Preserved source/import/collection checks using the exact Agent/Runtime
  checkouts: PASS; the required parent-media test collected.

## Guard probes

Using the current `normal014-source-common.sh` guard with
`NORMAL014_PROFILE=final95 NORMAL014_APP_SOURCE=parent`:

- exact immutable parent checkout: **PASS**;
- missing App root: **REFUSED**;
- dirty copy of the exact parent (private temporary copy only): **REFUSED**;
- foreign current worker root: **REFUSED**;
- unknown source role: **REFUSED**.

Both runner entry points also refused the foreign root during `preflight`
before source preparation, installation, browser, or network work:

```text
normal014-app-central.sh foreign preflight: REFUSED before preparation
normal014-parent-media-central.sh foreign preflight: REFUSED before preparation
```

The shell syntax check for all three normal014 helpers passed.

## Commands and results

```text
sh -n design/normal014-source-common.sh design/normal014-app-central.sh design/normal014-parent-media-central.sh
  PASS

NORMAL014_PROFILE=final95 NORMAL014_APP_SOURCE=parent sh -c '. "$1"; verify_app_source "$2"' sh normal014-source-common.sh /home/user/work/wt/app-pin-25155ccb
  PASS (exact parent)
same guard invocation with missing, dirty-copy, and current integration roots
  REFUSED in all three cases

NORMAL014_PROFILE=final95 NORMAL014_APP_SOURCE=parent AGENT=/home/user/work/wt/agt-pin-6efc8150 sh -c '. "$1"; verify_artifacts "$2" "$3"' sh normal014-source-common.sh /home/user/work/wt/rt-pin-95bd3c5f /home/user/work/wt/rt-pin-95bd3c5f
  PASS: verified artifacts=76; manifest and raw 6ba schema matched

PYTHONDONTWRITEBYTECODE=1 PYTHONPYCACHEPREFIX="$TMPD/pycache" NORMAL014_PROFILE=final95 NORMAL014_APP_SOURCE=parent NORMAL014_PYTHON=/home/user/work/venv-app2-native/bin/python sh -c '. "$1"; verify_python_imports_and_collection "$2" "$3" "$4"' sh normal014-source-common.sh /home/user/work/venv-app2-native/bin/python /home/user/work/wt/agt-pin-6efc8150 /home/user/work/wt/rt-pin-95bd3c5f
  PASS: required parent-media test collected

NORMAL014_PROFILE=final95 NORMAL014_APP_SOURCE=parent TMPDIR="$TMPD" bash normal014-app-central.sh preflight "$FOREIGN"
NORMAL014_PROFILE=final95 NORMAL014_APP_SOURCE=parent TMPDIR="$TMPD" bash normal014-parent-media-central.sh preflight "$FOREIGN"
  REFUSED before preparation in both runners
```

## Exact helper hashes

Worker 0125 reported these binding-fix after-hashes:

```text
design/normal014-source-common.sh       3b2018de1fbc123135590c37d4b17e995fd194fc39089b793e3f1b82e742bd56
design/normal014-app-central.sh         65ea14c97c8bafccb53ae3ccc7054c380f409f211281ca46afbcaeed23e7f30f
design/normal014-parent-media-central.sh 1d2ebce742bab9a20a911baedab8e7e318e82d6f1043f7f554949855acf646fd
tests/suites.conf                       9bb3b11d4e7292adb4ca9ca40203a86eeb815911a5896c1a23ccca2a3f39fbc7
```

The current source-common, parent-media, and suites hashes match exactly.
The app runner has the separately reviewed 0132 required-case verdict guard
applied after 0125, so its current approved hash is
`c18d79205ca3b6af4a679ecef9cba0c11a1c3afee23b1daa56d95f109bedbf20`; the
0125 binding content remains present. This is an additive reviewed change,
not a custody mismatch.

## Ready parent command

Do not run it as part of this review. The ready command for the later actual
parent qualification is:

```sh
NORMAL014_PROFILE=final95 NORMAL014_APP_SOURCE=parent \
  bash /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/normal014-parent-media-central.sh \
  run /home/user/work/wt/app-pin-25155ccb
```

No browser, socket, full suite, package installation, new virtualenv, or
actual gate was run. Temporary probe copies and private bytecode output were
cleaned on exit; shared dependencies, artifacts, and virtualenvs were not
modified.
