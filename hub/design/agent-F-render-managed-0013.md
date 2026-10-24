## Report

Implemented `tools/run-render-cohort-0013.sh` and added one named service row: `render-cohort-0013`.

Preflight passed:

- Exact 21 nodes derived from retained 267-failure archive: 14 direct, 6 conformance, 1 export adapter.
- Frozen Agent c36/source hashes, Runtime tree 6047, installed child/profile `819acf`, RECORD/direct_url, registry, fonts, ffmpeg/ffprobe verified.
- `bash -n` and `git diff --check` passed.
- No product, test-body, pin, profile, registry, or dependency changes.

Targeted service run:

`agt-F-render-managed-0013-render-cohort-0013-1024002017-31761`

Result: 16 passed, 5 failed in 289.20s.

Failures were all Three.js cases because the service `PATH` omitted `node`/`npx`; longreprs confirm `required binary is unavailable`. No backend fix was attempted and the body was not retried. All phase outcomes and longreprs are retained in the worker evidence.

Preflight snapshot identity quirks were repaired harness-only using the existing synthetic-snapshot parent rule.

Commit message written: `test(agent): F managedrendercohort`. DONE marker created.