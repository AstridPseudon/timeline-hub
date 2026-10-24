## Verdict: PASS for custody/counts/no-weakening; diagnostic NO-GO

- Retained run: `app-pin-860e9755-d78-watchdog-live-2001-1024200242-14383`, exit 1/188s. Preflight `27752` passed.
- Manifest pinned heads/trees:

  - App `860e9755c876ce510aabc5af0511ffe1886626f6` / `662f848af7db3cf30ebdc45adde1f562ce91d0dc`
  - Agent `22d00393f7d944f1d01505637ca00b1995c3e158` / `4a1a3a549a131e10e9a60b106491a6c5085e8fce`
  - Runtime `44917baf5976d6a655d582fafc63fde7b6cb242d` / `609c6e54f7283a992e51c6aef8cfc2f1bc5c3346`
  - Composition `635f4de06fda22a85fc2e4cfc764d0153a4c9f40` / `5ab5191a296980a0a6bcd1178ab6902d6478a148`

- Versions: Node 20.19.4, npm 10.8.2, `AstridRuntime/0.1 Python/3.13.16`, schema `sha256:867f3553ac0ff264300e5a2596b363cdb4c071842eb6570ad461c093d351708b`, provider `astrid-v1`, compiler `authoring-bundle-1`.
- Selected spec hash `c0624a04200c40acaf6866d270d9b9b9665b33173565ee709df384ddcdc0e797`; readiness hash `2b9723db262978ebbb410d5925163fe61c4a83f05f3b44fbbd524bc9df301593`. Before/after hashes match and are byte-identical to App860e. Harness/launcher are unchanged; watchdog option `2` is diagnostic-only.

JUnit exact counts:

- `d66/readiness.xml`: tests=1, failures=0, skipped=0, errors=0.
- `d66/p2-element.xml`: tests=1, failures=0, skipped=0, errors=1.

The error is native seed setup `transport_timeout`; the intended element gesture was not reached. No full-tour gate credit.

Safe artifacts:

- Stack: `d66/runtime-private/p2-commit-phase.stacks.txt`, mode `0600`, 4206 bytes, captured `2026-10-24 20:05:17.584Z`, SHA-256 `eb2e55e78734850ad08f7f36724f3e316e4535f8fec54591d6ac645796276f04`.
- Phase sink: `d66/runtime-private/p2-commit-phase.jsonl`, 108 lines, SHA-256 `8966b306726f91a805342fff0a1ed3b43317acda53c85218176bb47eeb77b3a9`.
- Bounds: request 1 recorded offsets 4556.035–7300.056 ms; request 2 17454.444–51952.355 ms; two summaries, untruncated, final phase `http_response`.
- The 2-second pending snapshot is not treated as hang proof. Runtime retains causal attribution.

Checks run:

- Read-only manifest/XML/source/hash/phase audit — PASS.
- `git diff --check` — PASS.
- `git status --porcelain=v1` — clean.
- No redundant suite, browser run, collector, replay, or product change performed.

The ephemeral source snapshot directory was cleaned up, but its manifest commit/tree and pinned Git object remain verifiable. Commit message and `DONE` marker were written.