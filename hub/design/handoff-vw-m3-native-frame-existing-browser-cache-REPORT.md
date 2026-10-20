# Native fresh-PNG existing-cache handoff

## Verdict

**BLOCKED before browser setup.** The permitted existing `remotion/shared-browser.mjs` cache seam was prepared and exercised in an owned `0700` HOME. Its versioned lookup selected the installed Chrome honestly when given the admitted project root, with no explicit browser environment override. The native worker's actual no-argument lookup returned `null` on the reviewed source, so this worker did not launch a browser or claim a PNG.

The precise source blocker is unchanged and outside this task's ownership:

1. `remotion/src/astrid-frame-worker.mjs` calls `sharedBrowserExecutable()` without a project-root argument.
2. `remotion/shared-browser.mjs` derives its default project root as the parent of the module directory. In the admitted project layout, `@remotion/renderer/package.json` is under `ASTRID_REMOTION_PROJECT_DIR/node_modules`, not that parent, so the no-argument version lookup is null and the cache candidate is never selected.
3. `astrid/core/execution/remotion_host_session.py::HostRemotionSession._start` projects HOME/LANG/LC/PATH and drops the explicit `ASTRID_REMOTION_BROWSER_EXECUTABLE` selector as well.

Repairing that carry or inventing a private parent alias/source factory would violate the task boundary. The existing cache seam is therefore not honestly sufficient for this native run until the Agent core forwarding work lands.

## Frozen evidence

- Source fingerprint: `196b7ba77f6ef4ced08633267260a8f4c35a00de2d51cb56e9ed1a1313a1413a`
- Controller SHA256: `93ee44ac0b041b6a6a0f976fe212e768841e0287e1380e0c36e0cf0ac30cb088`
- Manifest: `handoff-vw-m3-native-frame-existing-browser-cache-manifest.json`
- Agent source: 3,080 files
- Runtime: commit `2c4ac180c2220bdad966bc01e95ad230e99ce26a`; archive SHA `eed22a1b0d1af2045f823ec9f71dbd7cd862ba7935edfd5199171656e3ff1669`
- Clean peer graph: 21,455 entries (the separately replaced public12 package is excluded from the peer comparison)
- Composition public12: 77 member files; archive SHA `0a7b61529099ce994f807c6d7b1078303a09e7c0219144cc4b07467977f0f1a3`
- Node: SHA `43d6cf63f2a460b463eba6b19df5e9a259771c56f11b5130e04178a15bb99490`
- Chrome: `/opt/google/chrome/chrome`, version `155.0.8059.84`, executable SHA `cb19b59995072b86cc7f887b3b1c7ab1f63518a7f2ed9f0d33249e1a040e2c76`
- Chrome tree: 255 entries, SHA `5b9b48fad617dc414d4a18ccfe9c7933c7bc4a8efd78c70d4f7a9e853808de0e`
- Remotion renderer package version used by the cache layout: `4.0.509`

## Exact checks

```text
node --test remotion/tests/shared-browser.test.cjs
PASS: 1 file / 1 test

PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD" /home/user/work/venv-agent/bin/python -B -m pytest -q -p no:cacheprovider -o addopts= tests/packs/rendering/test_scene_source_carry.py::test_native_caller_binds_actual_frame_session_to_admitted_project tests/packs/rendering/test_native_fresh_export_label.py -k 'not one_fresh_saved_frame'
PASS: 1 passed, 5 skipped, 1 deselected in 3.89s

PYTHONDONTWRITEBYTECODE=1 python3 -B handoff-vw-m3-native-frame-existing-browser-cache-controller.py preflight --source /home/user/work/wt/vw-m3-native-frame-existing-browser-cache --node node
PASS: stable fingerprint and cache resolution; native no-argument result null.

PYTHONDONTWRITEBYTECODE=1 python3 -B handoff-vw-m3-native-frame-existing-browser-cache-controller.py capture --source /home/user/work/wt/vw-m3-native-frame-existing-browser-cache --node node --reviewed-sha256 196b7ba77f6ef4ced08633267260a8f4c35a00de2d51cb56e9ed1a1313a1413a
EXPECTED exit 1: refused before browser setup with the precise no-argument/cache/core-forwarding reason above.

git diff --check
PASS; worktree clean.
```

The Python fresh-label physical test `test_one_fresh_saved_frame_exports_retained_revision` was collected only by name in the handoff; it was not executed. No browser, daemon, socket, live capture, download, install, network, full suite, or shared dependency/cache mutation occurred.

## Next step

Agent core owner must carry the already-admitted browser selector through the native host projection (or make the existing helper's normal no-argument project-root lookup resolve without an alias). After that change, refresh all source/controller fingerprints and obtain independent review plus a fresh grant before attempting the one-frame proof. Do not reuse this blocked fingerprint.
