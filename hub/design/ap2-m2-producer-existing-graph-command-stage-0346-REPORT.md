# AP2 M2 producer existing-graph command stage

## Result

Prepared one new named suite, `ap2-m2-producer-existing-graph-command-e2e-integration`, without changing the existing producer suite. It uses `sh scripts/testing/run-producer-public13-list.sh "$PWD"`.

The durable runner reuses the existing public13 attachment runner:

```text
/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-public13-effective-build-attachment-fix/public13-integration-runner.sh
```

It does not copy the App or create/install another graph. A private `npm` forwarder preserves the existing wrapper's hosted build command, then forwards its hard-coded ordinary child to:

```text
node_modules/.bin/playwright test --config playwright.producer-ownership-current-pin.config.ts tests/e2e/local/producer-ownership-current-pin.spec.ts --list
```

The forwarder rejects zero-test output and preserves a nonzero child return code. The existing wrapper continues to own graph attachment, frozen Agent and Runtime checkout creation, private package graph/cache/TMPDIR paths, cleanup, and hosted-build failure propagation.

## Exact source and controls

- App approved body: commit `36dd91257fd13dcad0d58b48c790caa5063b4c8c`, tree `d908845dbc8e5ebf96698d08621557e904f20c52`.
- App source base: commit `4ef89267f00d193273441ff6dbb955f30d27d708`, tree `8c7393050ded32854503dfb7719a102b5dec94eb`; central final test snapshot tree was `0a4e6e46b080843902624eeadd7c288bb5f5d928`.
- Selector config SHA-256: `5b880ceff883abce2575a3a85aaa4eda69d3bcb848768ff0e91f337d50cca4c0`.
- Producer body SHA-256: `d91d0c1cce22f68119cd30fcb0a288346474b0ad4b64c84dcee3b730fa468d89`.
- Producer helper SHA-256: `50cbe5341f24c9a1ecc999018e2c6d975380a3440570abce151f9173c9752016`.
- Existing public13 wrapper SHA-256: `40c25724b502ce5582caf04c6ebf44ab89a509b5f3d629876d599f57c3e5fa7a`.
- New forwarding runner SHA-256: `d382db5b7ddcd9d5dc2420666d340cd2ff7ea97a6f3a1521e4f455a29bbb0354`.
- Agent: commit `8130a401bf44a518d5a40ae274d398b8c560be55`, tree `236c3e57e0265c52b81ba8085de3193026176bff`.
- Runtime: commit `2c4ac180c2220bdad966bc01e95ad230e99ce26a`, tree `7ab412cc4bcbe517efcfa806e092336390312e18`.
- Runtime producer manifest: `sha256:6f000bc615a9cb24fb00cc69a97af75eae71006ebfe87e3caa272fcdbbb1af56`, exactly 75 artifacts.
- Protected graph archive SHA-256: `895c628ab0727c8975247310fd0319b0f546a8d032a57072c9e364e20965ca30`.
- Public13 Composition tarball SHA-256: `9412ae25c306d5118241f4d631e8eecc6eef9b2fb5a98302d40938e9f6d54738`, exactly 77 regular members.
- Protected graph package SHA-256: `7c806b078b00bba1593336c49a3d2953b3f8f7afc7fa9919f6d5d7ccc7c1aa61`.
- Protected graph `dist/evaluation.js` SHA-256: `e27ed545e9e0c28cf863e7bccd4a720f61e1002e04f2946dd3afca5e5f478155`.

The runner verifies these together with clean frozen sources, exact App/body ancestry, selector/spec/helper hashes, protected graph realpath, Composition version, and public13 tarball/member count.

## Evidence

Central named suite request:

```text
request-test ap2-m2-producer-existing-graph-command-stage-0346 ap2-m2-producer-existing-graph-command-e2e-integration
```

Result: `...-1021034858-18751`, PASS, exit 0, 59 seconds. The central log reports the public13 resolver probe PASS, hosted build PASS, and:

```text
Total: 1 test in 1 file
```

Targeted local checks:

```text
sh -n scripts/testing/run-producer-public13-list.sh                 # PASS
git diff --check                                                   # PASS
node_modules/.bin/playwright test --config playwright.producer-ownership-current-pin.config.ts tests/e2e/local/producer-ownership-current-pin.spec.ts --list  # exactly 1
```

Private negative controls all passed: wrong graph realpath rejected; wrong Agent source tree rejected; `Total: 0 test` output rejected; and a failing forwarded child returned status `1` unchanged.

No browser, localhost/socket journey, producer body, actual gate, or full suite was run.

## Scope and callers

Only the test runner and central test-service allow-list received changes. No product, pin, generated, bootstrap, dependency, graph, or test-body file changed. The existing producer suite line was not mutated.

The new runner has one caller: the new named suite line. Existing production callers remain unchanged: transcript regeneration through `transcriptLaneExtension` / `buildTranscriptCaptionPatch`, and scene movement through `scenePhaseMarkersExtension` / `moveExistingShotsToMarkers`, registered by `localExtensions.ts`. No new product caller is claimed.

## Recommended next step

After separate authorization, run the same named suite with an actual forwarded journey command. This preparation proves only protected public13 attachment, source identity, hosted build, and one-test collection.
