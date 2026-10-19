# Visual seam picture and continuity lanes

The immutable parent composition's `config.app.visualSeamContract` carries
authored seam policy. Publish changes through `publish_parent_composition`
with `expected_head`; never rewrite pinned child revisions in storage.

`pictureTracks` declares visual output lanes whose custom clip types supply
picture. Built-in picture types continue to work without a declaration.
Unknown types on other lanes remain opaque auxiliary elements. Source/audio
lanes, disabled clips, text, known overlay/effect types and effect element
references cannot satisfy child picture coverage through this declaration.
The metadata analyser does not execute custom renderers or verify their pixels.

`continuityTracks` selects lanes requiring strict gap/overlap checks. Picture
coverage is the union of a child's active picture spans, independent of this
selection. For a composition whose parent shot lane is `picture` and whose
custom layered child picture is on `plate`, a policy can use:

```json
{"continuityTracks": ["picture"], "pictureTracks": ["plate"]}
```

Custom picture timing remains opaque in the report. Its cut represents its
activation; independent auxiliary activations and known motion/phase/source
cues still require acknowledgement. Store boundary declarations in `intents`,
keyed by the decimal frame. Use the report's `canonicalContext`, the current
`disclosureVersion` as `contextVersion`, and the intended `kind`. Hard cuts and
transitions carry no cue acknowledgement. `synchronized` acknowledges only
the exact named `canonicalCueIds` in `participants`; relevant edits invalidate
the context. No intent exempts structural gaps or overlaps.
