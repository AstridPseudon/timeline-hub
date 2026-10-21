# Land and select the fixed OMP producer

The delivery bundle contains the corrected OMP fork commit as a Git bundle. Push that exact commit to `peteromallet/oh-my-pi`, select its full SHA in the app manifest, and verify GitHub serves it before deploying the app. The app deployment is gated on the commit being available on GitHub. As with the selected Agent and Runtime commits, this fork commit must be available on GitHub before the app deploys. The configured-session-folder listing and recovery gap remains open until both the producer is pushed and the app manifest selects it.

The fixed commit is `9e282751c0059e37d2f6fbc14ffa0b450710bd23`, based on `9962a46db1e8340320a0f2fb276964f957985505`, with tree `2074d7a2e26cc954b5cf3d77e91f3efbb25ad34f`. The bundle is `omp-fork.bundle`; its advertised ref is `refs/heads/lead/omppin`. It preserves the reviewed commit ID and metadata.

## Push the bundled commit

Use a clean clone of `peteromallet/oh-my-pi` that contains base commit `9962a46db1e8340320a0f2fb276964f957985505`; the bundle has that commit as a prerequisite. Confirm the bundle ref, fetch it, and verify the exact commit and tree:

```sh
git bundle list-heads /path/to/omp-fork.bundle
git fetch /path/to/omp-fork.bundle refs/heads/lead/omppin:refs/heads/astrid-acp-session-fix
git show -s --format='%H%n%T' 9e282751c0059e37d2f6fbc14ffa0b450710bd23
```

The first command must show `9e282751c0059e37d2f6fbc14ffa0b450710bd23 refs/heads/lead/omppin`; the final command must show the commit and tree listed above. Then push the same commit ID:

```sh
git push origin 9e282751c0059e37d2f6fbc14ffa0b450710bd23:refs/heads/astrid-acp-session-fix
```

Verify the commit is available from GitHub before changing or deploying the app. Do not cherry-pick or amend it: the app pin and delivered bundle must resolve to the same commit ID.

## Select the landed producer

`tools.omp.source` is the only authoritative OMP source field. Set it to the full commit SHA:

```json
"omp": {
  "source": {
    "repo": "https://github.com/peteromallet/oh-my-pi",
    "sha": "9e282751c0059e37d2f6fbc14ffa0b450710bd23"
  }
}
```

Keep the app deployment gate closed until GitHub serves that commit and the app manifest contains this exact SHA. After the pinned source is deployed, run the update journey and check that conversations list and reopen after a cold restart, including configured external session stores and old OMP12 history. Remove the published-default known-gap note from `docs/testing/TESTING.md` only after these checks pass.

## Reproduce the focused native ACP tests

Use Bun **1.3.14**. The reviewed fork uses the unchanged frozen Bun lock with SHA256 `f08eab1fd7e0519e8b131697d6a35815fd71d9b0a61a8d70cc57b499bcba53ee` and native ABI **17.4.0**. In a clean checkout of the fetched commit, prepare the workspace and generated tool views, then check the lock:

```sh
bun install --frozen-lockfile --ignore-scripts --omit optional
bun run gen:tool-views
sha256sum bun.lock
```

Install matching native leaves before the real CLI tests. This Linux x64 example uses the integrity-pinned 17.4.0 archive. Other platform archive pins are in `QUALIFICATION.json`; native macOS and Windows were not executed in this qualification.

```sh
native_scratch="$(mktemp -d)"
curl -fsSL https://registry.npmjs.org/@oh-my-pi/pi-natives-linux-x64/-/pi-natives-linux-x64-17.4.0.tgz -o "$native_scratch/native.tgz"
printf '%s  %s\n' f380a65df2a2487b010314872b0d543dbbdc204a97b60551c4aaa5bf0f2dbd2b "$native_scratch/native.tgz" | sha256sum -c -
tar -xzf "$native_scratch/native.tgz" -C "$native_scratch"
mkdir -p packages/natives/native
cp "$native_scratch/package/pi_natives.linux-x64-baseline.node" "$native_scratch/package/pi_natives.linux-x64-modern.node" packages/natives/native/
rm -rf "$native_scratch"
bun test packages/coding-agent/test/acp-agent.test.ts packages/coding-agent/test/acp-session-dir-cli.test.ts
sha256sum bun.lock
```

The latest run passed **67 tests, 0 failed, 316 assertions across two files in 12.58s**. Both lock checks must retain the hash above. `QUALIFICATION.json` and `native-acp-session-tests.log` contain the run metadata and focused output. This qualification covers the stated native ACP/session tests; it does not claim the unrelated full-fork type/conformance gates, which have documented pre-existing optional-dependency/branding failures.

The live installer qualification also used this exact producer commit locally. It does not certify GitHub availability or the deployed app manifest; see the lead-agent installer report and its per-action evidence for reproduction details.

