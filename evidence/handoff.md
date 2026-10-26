# D141h Runtime handoff

Runtime obligations are complete:

- Target15 genuine normal ID: `rt-pin-fa9cd546-full-d141-pristine-targeted15-1026044256-11121`; exact 15/15 PASS on Runtime `fa9cd546` with Agent `8b6ed211`, normal `/home/user/work/venv-runtime/bin/python -m pytest -q -n3`, exit 0.
- Existing authorized P5 ID: `runtime-d141-p5-cut-1026013331-6934`; exact 38/38 PASS on Runtime `6a011d58` with Agent `28e56cac`, exit 0. Original identity and source origins were preserved; it was not relabeled freeze2 and was not reissued.
- Targeted15 registry row was appended disjointly through the locked atomic CAS route. Old full-pristine row `8912` and the cancelled `19479` obligation were not reissued; App admission remains paired-kit pending and untouched.
- Receipt attachments use only the installed validator-supported per-job interface. Both service directories are KEEP-retained and raw trace/witness/receipt files are mode `0600` under mode `0700` directories.

The exact raw XML, logs, summaries, trace files, runner exits, and monitor sidecars remain in the central service result directories. Evidence in this worktree records their exact paths/IDs/hashes without copying those artifacts. No unmeasured GO is claimed beyond the two terminal service results above.
