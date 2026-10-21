# Agent Gate 1 fresh word/transcript frontends

Status: partial proof, with one current non-Python carrier gap.

## Scope and pins

- Agent candidate: `786ee084be2b87bcc2c18d1eaea09bb8a4faf710`.
- Runtime under test: successor `3dcae1836a609363135d07ee435ce9beea975504`.
- Agent normal client pin: `95bd3c5f6d00e9bc8cc8cbe5ef510b68ed660f3c`.
- The named suite guards the Agent base, Runtime import path, Runtime checkout, and normal client pin.

## Fresh setup

`tests/editing_conformance/test_gate1_fresh_word_transcript_frontends.py` creates a new isolated Realm through the existing managed-output settlement, project, document, and timeline APIs. It then uses accepted native commands to create one parent visual target, one source occurrence, one source clip, and one target media clip. No historical film, legacy composition writer, SQL, prepared provider, or fake accepted history is used.

The transcript is a fresh `media.transcript/v1` document for the settled media object. The measured carrier contains the exact `DocumentPin`, source occurrence/clip ID, and stable word ID. Assertions retain the source and target opaque values, exact parent registry, and the source word's rational interval inside the occurrence's half-open interval. Python covers accepted edit, restart/reload, inverse, and redo.

## Result

Named central lane `gate1-fresh-word-transcript-frontends`:

```text
1 passed, 2 xfailed in 4.60s
```

The Python adapter passes. CLI and sheet are strict xfails under one capability requirement: non-Python frontends must carry and hydrate the exact `clip.anchor` carrier. CLI command-file ingress currently attempts local command execution without hydrating the pinned transcript, and NativeSheet has no word-anchor carrier grammar. These are the same missing non-Python carrier capability; no product code was changed and the original requirement remains visible as strict xfails.

## Next step

Add exact carrier hydration/grammar to the non-Python frontend ingress, then remove the two strict xfail marks and require all three adapters to pass the same fresh fixture.
