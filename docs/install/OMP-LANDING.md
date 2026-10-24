# Land and select the fixed OMP producer

Astrid defaults to `@oh-my-pi/pi-coding-agent@18.12.6`. The npm release still
has the configured-session-folder listing and recovery gap. The reviewed fork
ports `9e282751c0059e37d2f6fbc14ffa0b450710bd23` onto upstream `v18.12.6`
(`45c35e40c46166dc726ccc52f5d27f40f2449f99`). It preserves explicit stores for
ACP list, load, resume and fork, and keeps legacy string message history readable.

The delivery artifact is `omp-fork-18.12.6.bundle`, advertising
`refs/heads/astrid/18.12.6`. Release owners must push the exact bundled commit to
`peteromallet/oh-my-pi`, select its full SHA in the app manifest, and verify GitHub
serves it before deploying the app. This gate also applies to the selected Agent
and Runtime commits. Astrid never patches the selected producer during install.

## Push the bundled commit

In a clean clone containing upstream `v18.12.6`, inspect and fetch the bundle:

```sh
git bundle verify /path/to/omp-fork-18.12.6.bundle
git bundle list-heads /path/to/omp-fork-18.12.6.bundle
git fetch /path/to/omp-fork-18.12.6.bundle refs/heads/astrid/18.12.6:refs/heads/astrid/18.12.6
git show -s --format='%H%n%T%n%P' astrid/18.12.6
git diff v18.12.6 astrid/18.12.6 -- packages/coding-agent
```

Verify the advertised SHA matches the fetched commit, its parent is the upstream
tag above, and its diff contains only the session-store fix, regression tests,
fixtures and changelog. Then push that commit unchanged:

```sh
git push origin astrid/18.12.6:refs/heads/astrid/18.12.6
```

Verify GitHub serves that full SHA before selecting or deploying it. Do not
cherry-pick or amend the delivered commit: the manifest and bundle must resolve
to the same commit ID.

## Select the landed producer

`tools.omp.source` is the only authoritative OMP source field. Set it to an object
with `repo: "https://github.com/peteromallet/oh-my-pi"` and `sha` equal to the
full 40-character commit SHA printed above. Keep the app deployment gate closed
until GitHub serves that commit and the manifest selects it.

After deployment, run the update journey and check that conversations list and
reopen after a cold restart, including configured external stores and old OMP12
history. Remove the published-default known-gap note from
`docs/testing/TESTING.md` only after those checks pass. A saved model that no
longer resolves is rejected by 18.12.6; Astrid tells the user to start a new chat
and retains the saved transcript.

## Reproduce the focused native ACP tests

Use Bun **1.3.14**. The frozen lock SHA256 is
`6e330e18ca780dfccd6b6161818c204155f4c2cefce482bfead3e8315406a048`;
the native release is **18.12.6**, reported by `__piNativesBuildVersion()`.
Prepare a scratch HOME and `PI_CODING_AGENT_DIR` before running the CLI. In the
fetched checkout, install and generate the tool views:

```sh
bun install --frozen-lockfile --ignore-scripts --omit optional
bun run gen:tool-views
sha256sum bun.lock
```

Install matching native leaves before real CLI tests. The Linux x64 archive is
pinned below; every supported target's URL, SHA256, SRI and filenames are in
`astrid/installer/omp/recipe.json` in the agent repository.

```sh
native_scratch="$(mktemp -d)"
curl -fsSL https://registry.npmjs.org/@oh-my-pi/pi-natives-linux-x64/-/pi-natives-linux-x64-18.12.6.tgz -o "$native_scratch/native.tgz"
printf '%s  %s\n' 16c79fdc9783c7eb08ffd48867771eae792f6c0377a5eb5fc5ebb5e84ac5e931 "$native_scratch/native.tgz" | sha256sum -c -
tar -xzf "$native_scratch/native.tgz" -C "$native_scratch"
mkdir -p packages/natives/native
cp "$native_scratch/package/pi_natives.linux-x64-baseline.node" "$native_scratch/package/pi_natives.linux-x64-modern.node" packages/natives/native/
rm -rf "$native_scratch"
bun test packages/coding-agent/test/acp-agent.test.ts packages/coding-agent/test/acp-session-dir-cli.test.ts
bun test ./packages/coding-agent/test/acp-*.test.ts
sha256sum bun.lock
```

Both lock checks must retain the hash above. The former 17.4.0 producer's
qualification does not qualify this release, GitHub availability, or a deployed
manifest. Native macOS and Windows require separate qualification.

To refresh the build recipe from a reviewed commit, run in the agent checkout:

```sh
python scripts/refresh_omp_recipe.py --producer-repo /path/to/oh-my-pi \
  --candidate astrid/18.12.6 --version 18.12.6 --bun-version 1.3.14 \
  --cache /path/to/native-archives
```

The script emits the installer's build closure only. It verifies native archives
against registry SRI and records their SHA256; it does not generate a downstream
patch or select the user's producer.
