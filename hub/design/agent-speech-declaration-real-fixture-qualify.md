# Agent speech declaration / real-fixture qualification

## Scope

Qualified the remaining root Speech prerequisite only. The Agent source stayed at
`4048bec6bd1893ebb3bd435183127d52bacc560a` / tree
`4ddfa6d34b6cecd6f5a108145dae9853bf91815e`; the prior corrected
`generation.generate_speech` declaration remains the only product declaration
change. The normal catalog and artifact checks were already current, so no
generated catalog or artifact output was refreshed.

The proof uses Runtime commit
`c3d26567ff6fe4e20a959476d40aff90ad23a0ca` (tree
`f3ae49d38454ce73a9c91a954bb530b3ce51c122`) through the supported Runtime
checkout path. It does not alter the normal Runtime lock, generated client, or
raw84fc bytes.

## Evidence

1. Catalog/artifact checks:

   ```text
   python3 scripts/gen_tool_catalog.py --check       # passed; current
   python3 scripts/artifact_manifest.py --check      # passed; current
   ```

2. The exact three previously failing speech-action tests were rerun with
   `PYTHONPATH` and `ASTRID_RUNTIME_CHECKOUT` pointing at the C3d checkout:

   ```text
   env -i HOME=/root LANG=C.UTF-8 PYTHONDONTWRITEBYTECODE=1 \
     PYTHONPATH="$PWD:/home/user/work/wt/rt-pin-c3d26567" \
     ASTRID_RUNTIME_CHECKOUT=/home/user/work/wt/rt-pin-c3d26567 \
     /home/user/work/venv-agent/bin/python -P -m pytest -q -p no:cacheprovider \
     tests/packs/generation/test_generate_speech.py::test_speech_writes_wav_provenance_and_word_timing \
     tests/packs/generation/test_generate_speech.py::test_speech_moves_to_the_next_edge_endpoint_when_one_refuses \
     tests/packs/generation/test_generate_speech.py::test_speech_waits_and_asks_again_when_rate_limited
   # 3 passed in 0.28s
   ```

3. Added `tests/integrations/test_speech_publication_prerequisite.py`. Its
   bounded central named-lane run passed:

   ```text
   request-test agt-m2-speech-declaration-real-fixture-qualify targeted \
     --files "tests/integrations/test_speech_publication_prerequisite.py"
   # 1 passed in 19.71s
   ```

   The proof creates a temporary offline fixture pack and genuine one-second,
   8 kHz mono WAV. It then verifies SDK admission, the existing audio intent,
   the `generation.publish_v1` effect selecting the declared `speech` port,
   C3d's normal authenticated pack-host claim/settlement, CAS identity, the
   authorized reader's exact five-field selection, and verified WAV duration
   `1.0` seconds. The child executor has network isolation and makes no model,
   Speech, Edge, or external service call.

## Decisions and limitations

- C3d binds the daemon worker bearer to Runtime's `WORKER_ACTOR`
  (`astrid-pack-host`); the proof uses that existing actor constant rather than
  inventing an executor identity or lending credentials.
- C3d's media verifier reads intrinsic audio metadata from
  `generation.metadata.params`; the fixture supplies truthful `audio/wav` and
  `duration_seconds: 1.0` there.
- No outer workflow, full suite, broad91 replay, render, browser, TLS, or
  external provider call was run. No Runtime source or shared dependency was
  changed.
