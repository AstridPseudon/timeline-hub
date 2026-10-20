# Runtime raw-media base-eligibility contrast

## Decision

The Agent HOLD is a real Runtime eligibility regression in `b73139121169b72a2af9371f7808999ee91a1471`; it is not a raw-reader, CAS, constructor, provider-protocol, or fixture-selection artefact. The required contract is the intersection of both predicates:

1. the exact two-field `MediaPin` is declared by the original request; and
2. the same pin is present in the authenticated request's exact `base_revision_id` closure.

The active `rt-m2-raw-base-eligibility-fix` should restore the e220 base-closure check before memo lookup, descriptor open, or metadata return, while retaining b731's descriptor-stable reader and acceptance-time recheck.

## Immutable source identity

| source | commit | tree | archive SHA-256 | `timeline_commit_port.py` blob |
| --- | --- | --- | --- | --- |
| approved e220 | `e220670e40e196fb8f37dd8ce5d558fe0f6adf1c` | `6f802e315a7a447fa8d8245bf6f30963da6bb4f2` | `c5dbdab3a7415dd9da20e86b4383033edf5d1b6e216a42a674f672879b1f9e4a` | `d180708bc270f16f81dce5e2eb345b49232302bf` |
| candidate b731 | `b73139121169b72a2af9371f7808999ee91a1471` | `2c9452aea8ef0c65d2ef2e902f46a91fa4409ee7` | `c683b2a674cb8ab2f2cd3ecd4ab9baee6ab18942953f7ad6f7d097ac38a81625` | `a393aff1c8a21ef9d8131ebee72f0b00ddff3496` |

Both immutable archives reported the same protocol identity:

- provider: `astrid-v1`, interface version `1`;
- provider contract/schema digest: `sha256:8de823011a121359b9ad021e283b45afb6baeabc8a154a02bd086d1260a8b8f4`;
- `contract/manifest.json` SHA-256: `75dc4d088d6647af9f0aa3f7f4a1a30e65195f85b81f81f7b354fd7e418f6d14`;
- `contract/component-manifest.json` SHA-256: `1ad76db27c1d9716bb234f811bf63e1f5898cb3d5f9b835a821765e6cad895e5`;
- `contract/artifacts.json` SHA-256: `129abdbbf1f877643618b5290b39a5dd9225ba95b4c8fe8f2bb005ea4cf85497`.

The fresh-import `__file__` values were the archive-local files:

```text
/tmp/rt-raw-base-contrast.wpjAhF/e220670e40e196fb8f37dd8ce5d558fe0f6adf1c/runtime_protocol/timeline_commit_port.py
/tmp/rt-raw-base-contrast.wpjAhF/b73139121169b72a2af9371f7808999ee91a1471/runtime_protocol/timeline_commit_port.py
```

The archive and fixture directories were removed after the probes.

## Actual construction probe

For each archive, a fresh Python process imported only that archive through `PYTHONPATH`, initialized a normal temporary `RealmStore`/`RuntimeService`, registered a protocol-valid provider, created the empty timeline through the normal service API, ingested a real WAV into the same project *after* the base bootstrap, and submitted a valid `clip.add` request. The row's preserved opaque field recursively declared the exact raw pin, so the request exercised the real constructor's `objects(request["commands"])` path. The provider called `port.media_info(pin)` and then returned a controlled refusal only after a successful read; it did not mock the port or reader and did not fabricate SQL/history.

The service construction path was the real:

```text
RuntimeService._execute_timeline_commit()
  -> timeline commit coordinator
  -> port_factory()
  -> RequestCommitPort(self, commits, bound_context, check)
  -> provider.commit(provider_context, port)
  -> RequestCommitPort.media_info(pin)
```

Results for the same probe:

| source | port construction | post-base same-project managed pin |
| --- | --- | --- |
| e220 | `RequestCommitPort`; provider entered; `read_result` stayed unset | raised `RuntimeErrorBase`, reason `dependency_unavailable`, message `media info requires an exact base-closure media pin` |
| b731 | `RequestCommitPort`; provider entered | returned `{"object_id": "sha256:d2e105a5563128a84ea9b333e453efadd179e94bff8f194ac11230738fc80130", "media_type": "audio/wav", "size": 32044, "duration_seconds": 2.0}`; provider then returned its controlled `probe_complete` refusal |

The same project ownership was real: the object was created by `RuntimeService.ingest`, and the read reached `MediaReads.media_info` rather than failing ownership. The 2.0-second value is the WAV header derived by the immutable reader; it is not a caller-supplied duration.

## Exact source cause

The constructor and downstream reader are not the cause:

- `RequestCommitPort.__init__` is AST-identical in both archives (SHA-256 `391d7148cc9b4d2b34a565d920705a41d5473e72dd6d80f6c9c0afde9ad1d97b`), including `self.__declared = list(objects(self.__request["commands"]))` at lines 126–126.
- `RuntimeService._execute_timeline_commit` is AST-identical (SHA-256 `e3d32b525a25cecf33bf9bdf39a79420a084d2a88ffde477b8cb9cfc9edde72a`), including the `RequestCommitPort` factory at lines 2456–2458.
- `MediaReads.media_info` is AST-identical (SHA-256 `55490eb7287d2afb241778b2977ea80c3f5762cdd940078fd9ec7feb332d56a9`). It performs project ownership lookup, one CAS descriptor open, `_verify_open_file` before and after WAV parsing, and returns only verified header metadata.
- `_verify_open_file` is AST-identical (SHA-256 `b9c7def041d3e025a2231475232a3dbf912be5b570a58e3943f8ee0a62f067f8`).

Only `RequestCommitPort.media_info` differs:

- e220 lines 285–301 validate the exact pin, load the original `base_revision_id` closure, require membership in `base["dependency_manifest"]["media"]`, then memoize/read;
- b731 lines 279–288 only require `pin in self.__declared`, then memoize/read.

Thus the earlier mechanical statement that the raw reader is identical is correct but insufficient: the source-selection helper changed the authority context before the identical reader is reached. A recursively declared pin can be same-project-owned and still be absent from the original accepted base. b731 admits that pin; e220 refuses it.

## Controls and limits

The existing exact-base positive test was run from a fresh archive for each source:

```text
PYTHONPATH="$archive" PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-runtime/bin/python -m pytest -q -p no:cacheprovider tests/test_timeline_raw_audio_port.py -k 'reads_exact_base_pin_and_wav_header'
```

Result: **1 passed, 6 deselected** for e220 and **1 passed, 6 deselected** for b731.

No full/wide suite, HTTP/browser/CLI journey, native Agent pair, SQL/history fabrication, new fixture file, public API/schema/ABI, or product source edit was used. The negative probe used the real service/constructor; the only provider code was a protocol-valid observation harness whose final refusal prevented unrelated candidate-acceptance semantics from confounding the eligibility read.

## Handoff

Keep the ordinary014 raw-media compose and native Agent/Runtime pair on HOLD until the eligibility fix has a committed SHA/tree. The fix should add/retain one permanent real-ingest counterexample plus the exact-base positive control, with the guard before memo/descriptor/CAS read and without broadening authority to current head, observed closure, command arguments, or same-project ownership alone.
