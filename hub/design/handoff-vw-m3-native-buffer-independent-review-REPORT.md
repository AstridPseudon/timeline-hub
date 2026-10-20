# Independent review: native RGB decoder buffer fix

Verdict: PASS / qualified for integration.

Candidate source: `tl/vw-m3-frame-native-buffer-fix` at
`4360c7591819425b0163cdc907ee54b1ee56860d` (parent `1ba0800af20bd8bcb51439c0c977d486f645b43d`).

## Scope review

The parent-to-candidate diff contains exactly these two files:

- `tests/e2e/timeline/viewing-parity/frames.ts`
- `tests/e2e/timeline/viewing-parity/directframes.test.ts`

`compare.ts` is unchanged. The 640x360 comparator dimensions, channel bound
`> 2`, and outside-pixel fraction `.001` remain unchanged. No codec, profile,
resize, source fixture, product, browser, render, socket, or full-suite change
was introduced.

`decodeRgb()` now rejects missing/non-positive/non-safe probe dimensions, checks
the safe RGB byte arithmetic, refuses frames over `256 * 1024 * 1024` bytes,
derives `maxBuffer` from the probed `width * height * 3` plus 1024 bytes, and
still requires the returned stdout to have exactly the expected byte length.
Probe and ffmpeg failures propagate; there is no partial-output acceptance or
fallback that could hide truncation. The buffer is bounded at roughly 256 MiB
plus the explicitly named 1 KiB headroom, so this does not create an unbounded
memory path.

## Independent reproduction

I archived the parent and candidate source files into a private graph and used
real read-only leaf links to the already-installed packages; no shared
`node_modules`, cache, runtime, or worktree files were written. With real
`ffmpeg`/`ffprobe`, a generated 1920x1080 `testsrc2` PNG and FFV1/RGB24 MKV
produced:

- Red-before (parent): both `decodePlayerCapture()` and `decodeExportFrame()`
  failed with `RangeError`, code `ERR_CHILD_PROCESS_STDIO_MAXBUFFER`, message
  `stdout maxBuffer length exceeded`.
- Green-after (candidate): both decoded as `1920x1080`, each with exactly
  `6,220,800` RGB bytes; the Player and export byte buffers were identical.
- The candidate's unchanged comparator rejected both native-size frames as
  invalid Player/export dimensions, preserving the 640x360 contract.

A missing-input probe independently failed at `ffprobe` with command exit code
1, not at the stdout max-buffer path and not as an accepted frame.

## Tests

- `XDG_CACHE_HOME=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-native-buffer-independent-review/private-graph/cache-targeted node --import tsx --test tests/e2e/timeline/viewing-parity/directframes.test.ts tests/e2e/timeline/viewing-parity/compare.test.ts tests/e2e/timeline/viewing-parity/media.test.ts`
  — PASS, 3 file-level subtests, 0 failures. This was run from the private
  source/dependency graph and includes the generated 1920x1080 PNG/lossless
  regression.
- `XDG_CACHE_HOME=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-native-buffer-independent-review/private-eslint-cache ./node_modules/.bin/eslint tests/e2e/timeline/viewing-parity/frames.ts tests/e2e/timeline/viewing-parity/directframes.test.ts --report-unused-disable-directives --max-warnings 0 --no-cache`
  — PASS.
- `git diff --check 1ba0800af..tl/vw-m3-frame-native-buffer-fix` — PASS.

No full suite, browser, render, socket, install, or remote/integration action
was run or requested. No concrete defect or follow-up patch is proposed.
