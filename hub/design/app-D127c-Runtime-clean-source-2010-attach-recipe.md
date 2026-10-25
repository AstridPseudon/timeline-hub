# D127c Runtime source attach recipe

Use the harness-created commit on branch `tl/app-D127c-Runtime-clean-source-2010`.

Verify the two files in `/home/user/work/wt/app-D127c-Runtime-clean-source-2010`:

```sh
git -C /home/user/work/wt/app-D127c-Runtime-clean-source-2010 show HEAD:tests/helpers/p2_commit_phase_capture.py | sha256sum
git -C /home/user/work/wt/app-D127c-Runtime-clean-source-2010 show HEAD:tests/test_p2_commit_phase_capture.py | sha256sum
```

Expected SHA-256 values are `095c252b111a6d43cb5b4b9ed284b5a445b8b6fe69ca0ad4ee6950f1383c352d` and `ee789ec10738e1d9f3a2aae92c15b6d49cc86ad4f3c6e0e7cafc5fe5c883cf88`, respectively. The carrier is source-only and must remain held for the final Appguard/coupled binding pass. Do not run activation or request a merge from this worker.
