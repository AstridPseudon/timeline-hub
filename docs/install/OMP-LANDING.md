# Land the native OMP session correction

The release owner lands this patch on `peteromallet/oh-my-pi` or republishes the corrected producer, then selects that exact producer in Astrid's install manifest. This delivery performs no push or publication. Astrid does not apply this patch during installation.

Until the owner changes that selection, the manifest defaults to published `@oh-my-pi/pi-coding-agent@17.4.2`. That release has the configured-session-folder listing/recovery gap documented under Known gaps in `docs/testing/TESTING.md`. Live ACP and installer history-retention qualification in this delivery use the explicitly selected, locally built fixed producer; they do not qualify the published default's session-folder behavior.

## Apply

The delivery folder contains `0001-preserve-native-acp-session-stores-and-legacy-history.patch`, its tests, `QUALIFICATION.json` and the focused test log. Use a clean fork checkout at the exact reviewed base:

```sh
git switch -c astrid-acp-session-fix 9962a46db1e8340320a0f2fb276964f957985505
git am /path/to/deliver/omp/0001-preserve-native-acp-session-stores-and-legacy-history.patch
```

The reviewed source commit is `9e282751c0059e37d2f6fbc14ffa0b450710bd23`. Applying the patch may create a different commit ID; select the resulting full commit after landing. `QUALIFICATION.json` records the reviewed Git tree and patch checksum for comparison.

Production changes are limited to native ACP options, listing/recovery store selection, and saved user string-content normalization. Tests cover explicit/private store isolation, list/load/resume/fork, cold CLI restart, a genuine OMP12 transcript, and a pruned recorded working directory. No session directory is moved or reset.

## Test

Use Bun **1.3.14**. The reviewed fork uses the unchanged frozen Bun lock with SHA256 `f08eab1fd7e0519e8b131697d6a35815fd71d9b0a61a8d70cc57b499bcba53ee` and native ABI **17.4.0**. In a clean build environment, prepare the workspace and generated tool views:

```sh
bun install --frozen-lockfile --ignore-scripts --omit optional
bun run gen:tool-views
sha256sum bun.lock
```

Install the matching native leaves before running the real CLI tests. This is the Linux x64 example; other platform archive pins are in `QUALIFICATION.json` and were not natively qualified here:

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

The reviewed result is **67 passed, 0 failed, 316 assertions across two files in 9.54s**. Both lock checks must retain the hash above. The full owner-fork type/conformance gates have pre-existing optional-dependency/branding failures; this result claims the stated native ACP/session tests only.

## Select the landed producer

`tools.omp.source` is the only authoritative OMP source field. Remove the older OMP `version`/`repo` fields. The published default is:

```json
"omp": {
  "source": "@oh-my-pi/pi-coding-agent@17.4.2",
  "_comment": "See LANDING.md: select the fixed producer after owner landing."
}
```

After landing, select the fork's exact full commit:

```json
"omp": {
  "source": {
    "repo": "https://github.com/peteromallet/oh-my-pi",
    "sha": "REPLACE_WITH_THE_FULL_40_CHARACTER_LANDED_COMMIT"
  }
}
```

A fork source build currently requires the reviewed 17.4.0 package/native ABI and unchanged frozen lock. It builds the selected source directly, without a downstream patch, with private build configuration and integrity-pinned native assets. A remote GitHub source needs no system Git. For a developer qualification, `repo` can instead name an absolute local Git repository or local `file://` URL; the full commit must exist there. This delivery's local fixed source is `9e282751c0059e37d2f6fbc14ffa0b450710bd23`.

If the owner republishes a corrected npm package instead, replace the source string with its exact `name@version`; do not use a range or tag. `install-manifest.patch` in the delivery folder shows the default field replacement in the app manifest. Update the app's agent/Runtime pins to the final lane SHAs from `REPORT.md` separately.

After changing the source, run the normal update journey and the history checks in the tester guide, including list/reopen after a cold restart, explicit external stores, old OMP12 history, kept-workspace reinstall and cleanup. Until that selected producer passes, retain the published-default known gap in the tester guide.
