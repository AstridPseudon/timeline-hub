# Visual seam picture and continuity lanes

The immutable parent composition's `config.app.visualSeamContract` carries
authored seam policy. Publish changes through `publish_parent_composition`
with `expected_head`; never rewrite pinned child revisions in storage.

Picture is inferred from the track and clip type; no declaration is needed.
Any clip type on a visual output lane counts as picture, including a custom
renderer's opaque types, except known overlay/effect types and effect, animation
or transition element references. Built-in picture types also count on a lane
that `continuityTracks` or a canonical occurrence names. Source and audio
lanes, disabled clips and text cannot satisfy child picture coverage. The
metadata analyser does not execute custom renderers or verify their pixels. A
legacy `pictureTracks` key in a stored policy is ignored; it is preserved
byte-for-byte and never read.

`continuityTracks` selects lanes requiring strict gap/overlap checks. Picture
coverage is the union of a child's active picture spans, independent of this
selection. For a composition whose parent shot lane is `picture` and whose
custom layered child picture is on `plate`, a policy can use:

```json
{"continuityTracks": ["picture"]}
```

Custom picture timing remains opaque in the report. Its cut represents its
activation; independent auxiliary activations and known motion/phase/source
cues still require acknowledgement. Store boundary declarations in `intents`,
keyed by the decimal frame. Use the report's `canonicalContext`, the current
`disclosureVersion` as `contextVersion`, and the intended `kind`. Hard cuts and
transitions carry no cue acknowledgement. `synchronized` acknowledges only
the exact named `canonicalCueIds` in `participants`; relevant edits invalidate
the context. No intent exempts structural gaps or overlaps.
