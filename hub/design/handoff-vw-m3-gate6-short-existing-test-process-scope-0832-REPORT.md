# Gate6 short existing-test-process temp packet

## Result

Prepared one operational-only packet for the existing 0803 viewing runner. It
keeps the frozen App harness at d00a66134f330672ea7471dc69db38c1566d94cf and
changes no App source. The patch changes only the runner's existing
`preflight.sh` child environment:

* the runner keeps its long worker-owned `tmpdir` for evidence, Playwright
  cache, and retained output;
* one claimed, mode-0700 `/tmp/vw-XXXXXX` allocation becomes `TMPDIR`, `TMP`,
  and `TEMP` for the existing preflight, issue, controller, and Playwright
  children;
* cleanup validates the exact claimed root and unlinks symlink leaves without
  following them; it does not reject ordinary Chrome internal symlinks;
* `SHA256SUMS` is updated for the operational preflight/helper files, while
  the existing App/source/graph guards remain untouched.

The packet is intentionally un-applied to the frozen runner and contains no
browser, socket, Runtime, helper, or central test run.

## Path proof

The recorded failure witness is exactly 188 bytes:

`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-gate6-runner-child-contract-repair-0803/tmp-5aZG7i/com.google.Chrome.tFXWh4/SingletonSocket`

With the packet's physical `/tmp/vw-XXXXXX` root, a conservative 58-byte
Chrome profile-component cap produces a 107-byte
`.../com.google.Chrome.<profile>/SingletonSocket` path, strictly below 108.
The checker also records the 188-byte witness and refuses if either measured
bound changes.

The checker self-test passed all custody cases: unclaimed/foreign root
refusal, synthetic foreign-owner refusal, symlink-root refusal, mode/owner
checks, and cleanup of a Chrome-shaped `SingletonSocket` symlink while its
outside target remained. Cleanup uses `lstat`, `os.walk(..., followlinks=False)`
and `unlink`; it never traverses a symlink target. A claim marker means cleanup
accepts only the exact allocation claimed by this run.

## Exact source trace and accounting

Frozen App d00 source proves the inherited process environment is the existing
seam: `tests/e2e/local/support/harness.ts:18` imports `tmpdir`, and
`:442` assigns `mkdtempSync(path.join(tmpdir(), 'astrid-direct-'))`.
`:496-498` starts Runtime through `spawnGroup`; its `:100` assignment is
`env: options.exactEnv ? { ...options.env } : { ...process.env, ...options.env }`,
so the inherited short temp reaches the existing Runtime child.
Frozen viewing-parity `harness.ts:292` calls `chromium.launch(...)` without an
environment override, so the Playwright test process environment reaches
Chrome. The packet adds no harness or Player code.

The normal managed export remains accounted in d0a. In
`root_preparation.py` (blob
`017227e930f3ae5017f96f2ff69c1aca6f18f5be`), lines `30-60` require the
existing internal marker, owner-only non-symlink attempt root, and `outputs`
placement before returning `attempt`; lines `128-141` set
`temp_parent = attempt_root or requested_parent.resolve()` and create the
normal renderer temp with `TemporaryDirectory(prefix='.r-' ..., dir=str(temp_parent))`.
The normal audio temporary at lines `235-238` is likewise explicitly nested
under the serving root or renderer root. The file has no TMPDIR/TMP/TEMP read.

Agent d0a's `generic_host.py` (blob
`3fdb84fe881d14573498313e4d7bf069f09a4999`) may use inherited TMPDIR only in
the no-`attempt_base`, no-`attempt_root` fallback at lines `5290-5298`, where
`tempfile.mkdtemp` creates a mode-0700 attempt root owned by that invocation.
The same root is passed to live-storage envelope validation at `9256`, evidence
cap accounting at `9618-9622`, and ephemeral cleanup at `9984-9989`.
Therefore the short test-process temp is a fixture/Chrome carrier; it is not a
renderer `.r-*` exemption or an unaccounted export root. When the normal
managed marker exists, `.r-*` is explicitly allocated below the accounted
attempt root regardless of inherited TMPDIR.

## Frozen identities and preservation

* App commit: `d00a66134f330672ea7471dc69db38c1566d94cf`
* App tree: `a8bf53d5d5e865aa88825bbc20f6f530bfbaa7ba`
* Agent commit: `d0a5072bbe7b7ce9489f43aa0a81027ec400343b`
* App harness blobs checked: `ae8f4a68eb732144f6560ee5993001d2df433a8f`,
  `dbc4752fa984f8d47944cb4bca95744d34dd3717`,
  `be58c7a0fd78780b1d0ed39059a01f6f9cf2feb0`,
  `8c0878594e939a1e6003310d39c708bd34609062`

The patch contains no `harness.ts` hunk and no product, DTO/API/store/pin,
public14, Theme, fixture, codec, tolerance, sourceguard, or test assertion
change. The existing child marker, result, fd9 lock, issue/grant separation,
diagnostic separation, and source/graph guards remain in place.

## Validation

Ran without a browser, socket, Runtime, helper, central request, install, or
shared-dependency write:

* `python3 packet-staging/short-player-temp-controls.py --self-test` — PASS;
  188-byte witness, 107-byte short bound, ownership/foreign-root/symlink-root
  refusals, and symlink-leaf cleanup all passed.
* `python3 -m py_compile packet-staging/short-player-temp-controls.py` — PASS.
* `bash -n packet-staging/preflight.patched.sh` — PASS.
* `patch --dry-run -p1 < short-player-temp-preflight.patch` against a private
  copy of the frozen 0803 runner — PASS.
* Applied-packet private-copy check: updated `SHA256SUMS`, `bash -n`, and the
  helper self-test — PASS.

No physical/browser evidence was requested or produced; actual Gate6 success
remains unverified until the orchestrator elects a real run.
