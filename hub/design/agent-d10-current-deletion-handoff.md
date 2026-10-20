# Agent D10 current deletion handoff

Source is current Agent d0a5072b (d0a5072bbe7b7ce9489f43aa0a81027ec400343b).
The uncommitted worktree tree is f162a705a5ef32df080d8d0f8219fbc639a51b22;
the exact binary patch SHA-256 is
b981568e0fe99fdb917b031618ed0746d243cc153016440c92ca25bfa583f1e6.

This port removes exactly the nine reviewed duplicate wrapper implementations
and their nine pack resource declarations:

- animations: fade, fade-up, scale-in, slide-left, slide-up, type-on;
- effect: text-card;
- transitions: cross-fade, fade.

Their element.yaml descriptors, schemas, defaults, IDs, source, packId, and
canonical pack:rendering owners remain. The retained
effects/audio-reactive-colour/component.tsx custom resource and all other pack
resources remain.

The host registry generator now obtains public membership from the installed
Composition package's resolveElementRegistries(DEFAULT_THEME) API, filters
source-less public entries without inventing a second precedence system, and
fails closed for missing non-public components. The bounded owner correction
keeps the source-less public text-card winner in the host map while routing
qualified local shadows through the existing owner selector. The catalog
generator uses the same public membership to preserve public renderability.

The nine public catalog rows have unchanged semantic fields. Normal
content-addressed revisions were regenerated:

| element | old revision | new revision |
| --- | --- | --- |
| animation/fade | sha256:d5c66e08523f9a52e58fdf0fdbb506665a46f6068e2ebb0984c2a1c54ab3bff3 | sha256:98ac929d20ef0e6e2cef8c9e6f485525ce76b66eafc0c0e2ba834dbdf0ab7c15 |
| animation/fade-up | sha256:b3f945f89233a264766a7b2f9eee45a1de381d07889709109d61c5506c89edca | sha256:ff2441e102e98e8bc7aa61faf524b7170f14a6cff57236e0e81858156bc3b5be |
| animation/scale-in | sha256:2833cc7a4d9d7c45cea70bc1e0c8c6a82d224cd7dfeb65ef1058a4250d73f9f5 | sha256:b53171551804e4579fd8cad219e400b6f24ed69b6585d6a27af17b1eb4c65456 |
| animation/slide-left | sha256:7bb58fe6873d000c55ca16e715117dad600edda4a5618c2b16328ac18c9adcf6 | sha256:86a8b45a6007b8f454aa628675f71f0d0c057affc224583b9e4a23d2aeea7783 |
| animation/slide-up | sha256:d3fc405ad86e70968bdfe84f34d8bb413b5360495c3b8d486cad68855fdc6a40 | sha256:09acf51ae8c9836b240d510c60847405b77cb77ee7ac117521e485755600b84c |
| animation/type-on | sha256:f6caf670755e590fdf1ba85e421631c9c3ec243ef325dc5f9c118f634a172e96 | sha256:e628b73e9165344e188a0ca9f5bf850223ce6c33c0cb0ac9a1dfd9a0d8e9920b |
| effect/text-card | sha256:05749d28c818f8894770884cf52933cceed0e58a6d7d8702033ab4b869d1304b | sha256:6575848081267d8ac02b802f109dd8fedb4bddb94469b914190f83b2e73be56f |
| transition/cross-fade | sha256:568fc1ad4404a8d317ecaf416eadfb2e195cda830a664e74b7c2871a6ff9216c | sha256:30fa91cf8af7aa9460e05e90a8f9bf058974d6f0164dd8ec34d412d54342bfe1 |
| transition/fade | sha256:df6f5140ce9a6b5b0b0a0d1a6118b53b15183de0beb9df3e5a3aa6da27649749 | sha256:e68bac9cac9d42bc5827e39e8266bbecabfbaf54c0cf7fe9c22fe6c2e7d031d3 |

Qualification:

- private Composition 0.0.13 overlay, pinned Node v20.19.4, artifact SHA-256
  9412ae25c306d5118241f4d631e8eecc6eef9b2fb5a98302d40938e9f6d54738;
- targeted command:
  PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=$PWD /home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider tests/packs/rendering/test_effect_registry_target.py tests/packs/rendering/test_remotion_element_generation.py tests/packs/test_composition_elements.py tests/core/test_editor_element_catalog.py tests/reshape/test_check_doc_references.py::test_committed_catalog_is_fresh_for_the_in_repo_packs;
  result: 24 passed in 56.41s;
- ASTRID_REMOTION_PROJECT_DIR=<private public13 overlay> ASTRID_NODE_EXECUTABLE=/home/user/work/toolchain/node-v20.19.4-linux-x64/bin/node PYTHONPATH=$PWD /home/user/work/venv-agent/bin/python scripts/gen_element_catalog.py --check;
  result: passed;
- git diff --check: passed.

Viewing/App next step: consume this exact Agent source tree and perform the
normal public13 vendor/provenance refresh for the final consumer. Do not
rewrite the catalog revisions, forge provenance, or rebind immutable captured
admissions/DocumentPins. This handoff does not claim a merge, browser/full
suite, release, or pixel/audio qualification.
