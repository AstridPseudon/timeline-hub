# G5 redo reproducer source — design report

Status: source authored, execution intentionally **NOT RUN** in worker
`agt-G5-redo-reproducer-source-1534`.

The standalone source and manifest are:

- `agent-G5-redo-reproducer-1534-7e4b.py`
- `agent-G5-redo-reproducer-1534-7e4b.manifest.json`

Source SHA-256: `153be3ff0db9e473bde9289e9964ea7900e8666713073677a8d4251c42c91740`.
Manifest SHA-256: `b7807cc6f5a6a4d77b727308666c4332fb4f8789bd1c85dadd2d7a4a15ca1388`.

The source is pinned to Agent `91ac58a9fc6f1f752be16c0e4b8a1bf17095acee`
and Runtime `9ce4242bc01f100bab9efc51032a73985cefb2b2`; it checks those heads
at runtime and checks the unchanged public target body hash
`c2711a2d10765828694ee1906d75bdf62a91ed6ac0bbef8e4cb0d823e48ec30d`.

It reuses the exact public fixture, verifies current closure pins, performs
normal forward and whole undo, then constructs normal public redo. It captures
the exact v2 request and full reply/error, provider throw traceback locals,
guard `ref/path/base/theirs`, Runtime port history/read/prepared boundaries,
accepted records/bindings/effects/dependencies/undo steps, canonical documents,
source/native pins, SQL no-write snapshots, and loaded origins. It retains the
later-overlap refusal predicates even if redo stops first.

No global tracing, semantic monkeypatch, cache injection, waiver, product
change, test change, Git write, or blind retry is present.

Exact execution command and expected artifacts are recorded in the manifest.
No behavior result is claimed until independent fidelity review and the single
manager-owned live diagnostic run.
