---
name: fresh_vignette_029
description: Apply a static radial vignette that darkens the outer edge of a clip.
---

# Fresh Vignette 029

`fresh_vignette_029.vignette` is a timeline modifier for darkening image edges.
Set `strength` from `0` (no change) through `1` (black at the outer edge).
The modifier keeps the clip's existing bounds, alpha, and support. It uses the
clip's known rectangle and does not add a timeline overlay or change timing.
