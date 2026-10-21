# D13 current nine-path preservation review

Verdict: APPROVE for the bounded source custody/security delta review only.
This is not approval of an installed launch, native Runtime, HTTP, renderer,
browser, wheel, profile, or full-suite qualification.

Exact identities reviewed:

- D13 port commit: `5be2918c45909abcf0c91b79b53a2ce73eed83b1`.
- D13 port tree: `218da96139901ced0a059cdce37146cb7fc314db`.
- Port parent/current: `a9f4cfdaee40f3382b51d6cdb291d7012be96b8c`, tree
  `93862f0accf8bbe2331ed551b69839b47f7b8e1b`.
- Reviewed donor: `6951c176f326e99f0e4d61c89233d1de49a9c05b`, tree
  `386fa1f8afe073edd08f31bd8c430ee9b86e1ab9`.

Allowlist and donor parity:

- `git diff --name-only a9f4cfdae 5be2918c` is exactly these nine paths:
  `astrid/core/contracts/runtime_orchestration.py`,
  `astrid/core/execution/generic_host.py`,
  `astrid/packs/rendering/actions/assemble_timeline/run.py`,
  `astrid/packs/rendering/pack.yaml`, `astrid/sdk/timeline/assembly.py`,
  `astrid/sdk/timeline/sync.py`,
  `tests/packs/video_editing/test_runtime_publication_chain.py`,
  `tests/sdk/test_timeline_assembly.py`, and `tests/sdk/test_timeline_sync.py`.
- Eight of the nine port blobs are byte-identical to the reviewed donor.
  `astrid/sdk/timeline/sync.py` has only the intentional current delta: the
  existing transcript-input materialization carrier and its two current call
  sites. The D13 sync hunk is unchanged from the donor.
- No generated contract, lock, artifact, or CLI surface changed. The exact
  current and port blobs are identical for `runtime.lock.json`,
  `artifacts.json`, and `cli-surface.json`.

Current preservation:

- Current presence (`b4762b7c4`), core-types, transcript, and WC8 size work are
  ancestors of current and remain in the port. The current files carrying
  those changes, including `astrid/sdk/timeline/document_diff.py`,
  `astrid/core/element/schema.py`, `astrid/sdk/timeline/native_source_inputs.py`,
  and `astrid/sdk/timeline_sheet.py`, are byte-identical from current to port.
- Current source/custody files are byte-identical from current to port:
  `astrid/sdk/host_bootstrap.py`, `astrid/core/source_identity.py`,
  `tests/sdk/test_host_bootstrap_source_identity.py`, and
  `tests/sdk/test_installed_runtime_source_identity.py`.
- The existing installed-origin guard remains: the current test at line 457
  refuses a profile whose `runtime_checkout` and `source_checkout` select
  different installed trees. The source probe still requires exactly the eight
  origins `host`, `child`, `action`, `client`, `sdk`, `runtime_protocol`,
  `runtime_protocol.platform`, and `astrid_runtime`, under the selected tree,
  with isolated `-I` execution and no ambient `PYTHONPATH` or
  `ASTRID_RUNTIME_CHECKOUT` authority.
- The approved c4a RECORD fence remains in the D13 fixture. Its six controls
  are retained: absolute path refusal, parent path refusal, symlink-component
  refusal, normal `dist-info/RECORD` acceptance, installed hash/size refusal
  after tamper, and installed package-byte refusal after tamper.

Assertions and test disposition:

- All current `test_timeline_sync.py` tests remain; the port adds the strict
  unknown-flight-kind fence test. The current publication-chain test names and
  original publication/render assertions remain. The old GenericHost
  publication-hook test retains its body and assertions and is marked strict
  `xfail` for the intentionally removed legacy hook, naming the required D13
  requester replacement. This is the required one-to-one expected-failure
  conversion, not assertion deletion.
- The registered native positive remains active in the port and adds the
  requester admission, managed proposal, producer guard, lost-ack/restart,
  ordinary render, media decode, and guarded-undo assertions. No current
  positive was converted to refusal or removed.
- The existing bounded evidence inventory of 82 passed, 2 deselected, and 1
  strict xfail, together with the six RECORD controls, is represented by the
  port. It was not rerun here because the task forbids native, HTTP, render,
  install, build, and full execution. The historical count is not relabeled as
  a qualification result for this exact tree.
- An installed-preflight test with missing environment/profile bindings is a
  failure condition, not a product pass. No missing-environment result is
  counted as evidence here.

Commands run in this read-only review:

```text
git rev-parse 5be2918c^{tree} 6951c176^{tree} a9f4cfdae^{tree}
  218da96139901ced0a059cdce37146cb7fc314db
  386fa1f8afe073edd08f31bd8c430ee9b86e1ab9
  93862f0accf8bbe2331ed551b69839b47f7b8e1b

git diff --name-only a9f4cfdae 5be2918c
  exact nine-path allowlist; status 0

git diff --check a9f4cfdae 5be2918c
  passed

git diff --name-status a9f4cfdae 5be2918c -- runtime.lock.json artifacts.json cli-surface.json
  empty

Byte comparisons of the four source/custody guard files and the current
presence/core-types/transcript/size carrier files
  all preserved; status 0

Byte comparisons of the nine port files against donor 6951c176
  eight identical; sync.py differs only by the intentional current transcript
  carrier hunk; status 0
```

No product test, build, install, native process, HTTP/socket, renderer,
browser, or full suite was run in this review.

Flat manager handoff for the next complete wheel/profile preflight:

1. Use exactly Agent `5be2918c45909abcf0c91b79b53a2ce73eed83b1`, tree
   `218da96139901ced0a059cdce37146cb7fc314db`; build one noneditable wheel
   into a private worker-owned destination. Do not use or mutate shared venvs,
   shared node_modules, the leased staging base, or a checkout as installed
   execution authority.
2. Install that wheel into a fresh private venv together with the manager's
   exact existing dependency closure and the matched Runtime/client pair:
   Runtime `b92d3e7a05eec65c142294ef4873edd059e9b31d`, tree
   `6abc2f117391de8e7e35c0283f575a002199894d`, and client/artifacts
   `95bd3c5f6d00e9bc8cc8cbe5ef510b68ed660f3c`, tree
   `d3a290b407fa61e6ab2d476f50c068073f70df00`. Record exact wheel hashes and
   package versions; do not infer or reuse stale Agent artifacts.
3. Produce only the existing four-field profile carrier: `profile`,
   `runtime_checkout`, `source_checkout`, and `runtime_environment`. Bind both
   checkout fields to the same private installed site-packages root and bind
   the environment to its private venv. Verify the selected interpreter is
   that venv's `bin/python`.
4. Before any product launch, run the selected interpreter with neutral cwd,
   `-I` and no `PYTHONPATH` or `ASTRID_RUNTIME_CHECKOUT`. Require all eight
   installed origins, exact selected-tree containment, no symlink component in
   profile paths or Runtime package trees, and the existing source/closure
   identity checks.
5. Verify Agent source archive/Git-blob parity against the exact commit/tree;
   verify the wheel SHA-256; verify every wheel and installed RECORD path is
   relative, nonempty, non-dot, non-parent, and non-symlinked; verify every
   recorded hash, size, and installed package byte. The six RECORD controls
   must pass, including the normal positive and all refusal cases.
6. Bind and hash the existing C13 tool closure without changing it: the
   manager-selected Node 20 executable, Remotion `agent-remotion-0013`, its
   package lock, browser executable, ffmpeg, ffprobe, node_modules, and font
   provenance/nonempty files. Require the existing source digest, tool hashes,
   private attempt-root write probe, and disk floor.
7. Run `test_d13_installed_native_preflight` only with the complete manager
   environment and exact private profile. A run with missing environment
   variables, missing Runtime origins, or a stale C13/Agent tuple must fail
   and must not be reported as a product pass. Keep native/HTTP/render/full
   qualification as a later separately authorized named run.
