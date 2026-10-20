# PCM peer-topology guard — READY held

Preparation only. The PCM freeze remains **HELD pending lead restore**. No
manager grant, new baseline, graph repair, substitution, browser, socket,
renderer, install, or central run was performed.

The guard reconciles the existing served-PCM controller with the independent
shared-graph audit. Its borrowed graph check reads the retained root-smoke
manifest below, verifies that manifest's frozen SHA-256, inventories the live
graph with bounded cycle detection, and requires exact equality of every file
digest and symlink target. It therefore refuses both the observed 106 added
package-directory self-links and any non-cyclic topology drift.

Retained baseline:

```text
/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-vw-m3-root-smoke-central-ready-prepare-pre.json
SHA256 2387ebb5e0beaf9b5c0eea064edf0d9e1425059f05f39e9cb31fea064a5414ed
graph entries 21495 (21462 files, 33 link records)
```

Flat artifacts:

```text
handoff-vw-m3-pcm-peer-topology-guard-controller.py
handoff-vw-m3-pcm-peer-topology-guard-test_normal_audio_served_sources.py
handoff-vw-m3-pcm-peer-topology-guard-guard-regressions.py
```

The copied PCM fixture remains unchanged: seven whole-scope cases and two
phase cases, including the public-77/native-helper/Node/source pre/post and
finally-controlled paths. The six historical Remotion/Player file hashes
remain a profile-local check; no Agent/App profile equality was introduced.

