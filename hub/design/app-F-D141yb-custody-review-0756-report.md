# F D141y-b independent custody review

Verdict: **FAIL_CUSTODY**.

The fixed source tuple is authenticated and clean. The retained original 0741
record proves one exact canonical `delivery-build --dry-run` invocation and
partial Agent/Runtime output, but it does not prove a terminal command exit,
App/Composition result, child reaping, or a complete delivery result. The
wrapper's harness exit `0` is not a build PASS.

## Proven facts

- Tuple JSON SHA-256: `63cd645e36569256fad04837b4f32927e1d84ca81186b49315cc18e91c294643`.
- App `82e9e13ddf1d7ec6c736521b2eb091dca9877598`, tree
  `6a6e49eb4461b5ca1a7fa1247653bc794f26d710`.
- Agent `ecdc242ed9b673f641759ecf029f95e89a2c6f92`, tree
  `d362fe9dfdbd0c1fc8e0739c193ed2b74a7d2735`.
- Runtime `95d98f038320d5d46bd679ac000ab3e15825c935`, tree
  `78df31d62c5b9ba4c84dee4ea346e43a767718c1`.
- Composition `635f4de06fda22a85fc2e4cfc764d0153a4c9f40`, tree
  `5ab5191a296980a0a6bcd1178ab6902d6478a148`.
- The captured original command has invocation count one and the exact
  production argv shown in `original-command-extract.txt`; its tuple SHA
  argument is the tuple hash above. No retry, subset, replay, or alternate
  invocation is credited.
- Raw stdout is 165 bytes, SHA-256
  `9dca8647b52b5d09c4eb5b6253fa8c8bbc1494070cca3a01165276763ea57350`.
  It contains only Agent `PASS in 29s; 1 patch(es)` with tree
  `d362fe9dfdbd`, and Runtime `PASS in 7s; 1 patch(es)` with tree
  `78df31d62c5b`.
- Raw stderr is zero bytes, SHA-256
  `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`.
- The original trace starts at `07:43:11.214010258Z` with
  `4592930816` bytes and records `3930136576` bytes at
  `07:43:36.304196498Z`, below the `4000000000` stop. Dispatch admission was
  `4594692096` bytes. The continuous trace therefore crossed the stop during
  the invocation; the later normal stop acknowledged pid `3209`.
- Wrapper pid `3191` reached finalize at `07:43:59Z` and reports harness rc 0.
  That is wrapper custody only. There is no retained original
  `raw-command.exit`, `command.json`, `results.json`, `report.md`, `DONE`, or
  sampler lifecycle receipt. Main's genuine descendant/process-audit receipt
  was not available to this review. Original command exit and child reaping
  are therefore **UNKNOWN**.

## Build accounting

Agent and Runtime partial lines are retained as actual one-patch/tree matches;
they do not establish whole-run success. App and Composition are **UNKNOWN**.
No genuine retained evidence proves complete patch, tree, bundle, or apply
checks for any repository after interruption. In particular, the 0741 record
does not support a ZIP, publication, final build, or whole-run PASS.

The canonical source places `preflight_all` before staging/work-root creation
and before the per-repository `build_repo` loop. This review used that source
only to classify what the retained partial output can and cannot prove; it did
not invoke it.

## Limits and disposition

The original parent log and private staging remain Main INPLACE/KEEP and were
not physically transferred. SAFE transport was byte-checked; it is not a
physical replay or a substitute for missing terminal artifacts. Tests,
typecheck, lint, browser, import, generator, cleanup, staging writes, final
build, ZIP, and product work were **NOTRUN**. The independent sampler in this
review is present-time evidence only: it remained above 4 GB, received TERM,
wait returned 0, and it was reaped; it does not establish any original 0741
sampler fact.

The prior 0710/0719/0724/0729 limits remain immutable: an ordinary refusal or
honest correction is not a delivery qualification, and present-time sampler
observations never repair historical custody. Next step is Main's genuine
host process/descendant receipt and, separately, a newly authorized complete
F-final run; do not upgrade 0741.
