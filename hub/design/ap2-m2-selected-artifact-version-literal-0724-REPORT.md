# App2 M2 selected final95 artifact-version literal correction

## Result

Copied the immutable a92fded8 runner into the worker-owned artifact directory:

```text
/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-selected-artifact-version-literal-0724/artifacts/run-owned-selected-final95.sh
```

The copied runner now derives `ARTIFACT_SHA` from
`Runtime95:contract/artifacts.json` programmatically at initial binding and
again when restoring the selected tuple. The real `run` dispatch independently
re-derives and compares the artifact version immediately before the existing
launch boundary. A planted invalid artifact version is covered by a negative
control against that same guard. The original four custody fixes, actual-path
stub/list/cleanup controls, source guards, helper guards, and pins were not
changed.

The App worktree has no source or test diff. The worker-owned runner changed
only outside the repository, as requested.

## Evidence

Programmatic literal command:

```sh
python3 -c 'import json,subprocess; print(json.loads(subprocess.check_output(["git","-C","/home/user/banodoco/banodoco-workspace-runtime","show","95bd3c5f6d00e9bc8cc8cbe5ef510b68ed660f3c:contract/artifacts.json"]))["version"])'
```

Output:

```text
sha256:54205b3ecb55038e416b31af936c9af26afa30dc1b05da16157ee4d861fe05ac
```

Generated final tuple from committed source objects:

```text
App HEAD/tree:       ba02c8f246ec61cd65d178a1ada686788df3fdab / 7fe8c15b56da9944ae31e8273d41d3ceb21b3677
Agent HEAD/tree:     6efc81500a0e0688c2bb41e736503f0fc3e04abb / 2ed2b8a12b5b3391ca221ba6ff05390f71a73556
Runtime HEAD/tree:   95bd3c5f6d00e9bc8cc8cbe5ef510b68ed660f3c / d3a290b407fa61e6ab2d476f50c068073f70df00
Producer HEAD/tree:  95bd3c5f6d00e9bc8cc8cbe5ef510b68ed660f3c / d3a290b407fa61e6ab2d476f50c068073f70df00
artifact version:    sha256:54205b3ecb55038e416b31af936c9af26afa30dc1b05da16157ee4d861fe05ac
manifest/count:      a902387c6a2315374f7e73511feea47da30191aba831b48820b3864b773a532d / 76
schema:              6ba7b51e9518e7fb08b27ad5b7225855276b657d0adebf704dd853f699768f2d
App lock:            770352eaf1d015e90fca0ed2f1893749b73b69356ca82a7223b2573276fe485e
App metadata:        4cd934d868eafd5ab82578da2232f1ee13f04d83c9314b3473b75bd951570044
App generated:       c575f183b6486dd07e8ec798f5a46bff4c9ffc0918892b189c1a433b9f80762d
App types:            f8cbbbbc48713a308c2ac2e2e977d08525c4280ef4dc93cd3e8d842245394564
App schema:           f52b82024ecd44a5e6c9c68d5cb326d50d70efe9aaad6f8ac6352ea1c87b97b1
```

The runner checks that committed App schema hash as part of the retained
App/runtime lock controls.

Commands:

```text
sh -n <worker-owned runner>                                  PASS
python3 static artifact-binding/delta review                  PASS
git status --short --untracked-files=all (App worktree)       clean
sha256sum <worker-owned runner>                               dcda1b820fa2feb68db6ae99b56cdc8cd4277016c3eaf939a5ded423c9b25ee0
```

The custody control hashes remain `d9a691dcaafd7d544a467445a3a020a9ad3d02afc1d527870f00be6948fea848`,
`1d2ebce742bab9a20a911baedab8e7e318e82d6f1043f7f554949855acf646fd`, and
`a959de6e0041f0d8ee28b949a19f5add97d7fb5de27714da6beaad15abd6ce4f`.

## Decision and limitation

The supplied a92fded8 runner already contained the authoritative `...fa30dc1b...`
value. The stale `...fa30db1d...` and `...fa30db1b...` variants were in the
prior report, which is why this was treated as a literal/binding correction,
not a release or pin decision. The old preflight validated the runner’s own
declared variable against the manifest, but it never validated the report’s
separate emitted literal and had no independent post-restore real-dispatch
assertion. Deriving from the immutable manifest removes that duplicate source
of truth; the new dispatch check closes the boundary immediately before launch.

No preflight, module/startup, browser, build, daemon, socket, full suite,
install, or actual product run was performed. The planted refusal and the
real-dispatch check are statically reviewed but runtime-unverified under the
explicit no-actual constraint.

## Next step

Use the worker-owned runner for the separately authorized central actual, with
the existing immutable source and keeper pair. That run should retain the
new `artifact_version` trace immediately before `launch`.
