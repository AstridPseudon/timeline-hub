# FAIL — finite owner fixture cannot execute in this namespace

The one complete derivative command exited **1**, after actual positive construction and the corrected stale-upstream negative passed. `os.chown(wrong_owner_root, 65534, -1)` then raised `OSError: [Errno 22] Invalid argument` before the source-owner guard ran. `/proc/self/uid_map` and `gid_map` both contain only `0 0 1`; UID65534 is unmapped. This is an observed fixture setup failure, not evidence of a production defect or a safety/classifier refusal.

F1 isolation: UUID/exclusive run and invocation/service/direct-stage roots added; positive and stale lifecycles each used their own preserved trace. No trace collision.

F2 stale origin: independently advanced private `origin/main` while preserving the recorded old base; both values emitted before invocation. The exact D68 reason `agent recorded upstream base is not current origin/main` was observed. No repository was staged for this negative.

F3 observation: real caller returned2 and emitted a FAIL diagnostic; wrapper FAIL reason and empty repo/stage/builder evidence matched. Exception-only/no-receipt assumptions replaced by exact phase-specific expectations. No arbitrary failure qualifies.

F4 stage owner: derivative replaces global shared `os.geteuid` patching with real private ownership fixtures, separate precise D68 and actual-caller entrypoints, and prior real source validation. **Unverified:** the earlier source-owner fixture fails to acquire its intended owner, so neither stage-owner branch ran. Wrong-source-mode, both stage modes/owners, wrong App base/tree, dirty/symlink/ref-drift controls remain unexecuted.

No second heavy, unchanged33 rerun, cleanup, retry, source alteration, installation or publication was performed. Complete checker qualification is FAIL; no installation. A subsequent authorized correction should use a reviewer-approved narrowly scoped owner-metadata fixture compatible with a root-only UID map, preserving actual source ownership validation and exact stage guard phase. Production changes are not indicated by this evidence.
