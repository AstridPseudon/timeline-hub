# Corrected D09 partial-mouth physical-equivalence preparation

Prepared a test/controller-only extension against the independently approved
Agent presenter source `ee71010a0947edcbbacbf8178e5fee11ab6bab3d`.

The handoff preserves the existing explicit `{x:151,y:104,w:19}` four-still
fixture and its 799-pixel old/public crops, 387-pixel erase control, unchanged
strict `>2%` statistics, and padding controls. It adds only the partial raw
input `{x:151,y:104}` with omitted size and two fresh frames `[0,3]`. The new
case requires both old/private and public compatibility crops to be
`(298,202,339,219)` with area 697, byte-identical pixels, and identical
`_diff_fraction` statistics. Its copied-image negative changes exactly 20
pixels and requires `20/697 > 0.02`; it does not use a 799 denominator or
normalize the raw input to size 19.

The missing-default and malformed inputs remain pure registered-source
assertions in the exact `ee71010a0` scene test: both report no inspection/
unknown, and neither is captured or given a fabricated positive. No product,
registry, root manifest, private crop, or statistics code was changed.

Artifacts:

- `handoff-vw-m3-mouth697-physical-controller-prep.patch`
  (`sha256 9624922e36ff9668d2458704368a16ea87d4e82551959e46d9e0b197ca122d5c`)
- `handoff-vw-m3-mouth697-physical-controller-prep-manifest.json`
- `handoff-vw-m3-mouth697-physical-controller-prep-COMMAND`
- `handoff-vw-m3-mouth697-physical-controller-prep-READY.sh`
- `handoff-vw-m3-mouth697-physical-controller-prep-run-central.py`

The controller uses a fresh manager grant and one-shot `RUN_STARTED`, a private
0700 temporary directory, the viewing browser flock, a 10 GiB floor plus temp
budget, full source/dependency/browser pre/post hashes, the read-only f816
graph and six peer hashes, immutable public12 77-file archive, Node20.19.4,
and Chrome155. It runs only the new partial test; it does not run the old
rejected default/partial controller.

## Offline checks

- `ast.parse` / `compile` on the controller and new Python test — PASS.
- `python3 -m json` equivalent parse of the manifest — PASS.
- `/opt/node22/bin/node --check` on all three staged `.mjs` files — PASS.
- `bash -n handoff-vw-m3-mouth697-physical-controller-prep-READY.sh` — PASS.
- `git -C /home/user/work/agent apply --check --whitespace=error-all <patch>` — PASS.
- `git diff --check` in the Composition worktree — PASS; worktree remains clean.
- Source-hash values were independently read from `ee71010a0`; public12 archive
  hash is `0a7b61529099ce994f807c6d7b1078303a09e7c0219144cc4b07467977f0f1a3`.

No browser, render, socket, central test, install, network, full suite, source
activation, or root-manifest regeneration was run. The central two-still
pixel result is therefore unverified and awaits independent review plus a
fresh manager grant. The stale root-artifact condition remains a named limit;
this is not admitted-host, Runtime, or Gate 7 evidence.
