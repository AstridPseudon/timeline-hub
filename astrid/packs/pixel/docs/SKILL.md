---
name: pixel
description: >
  Snap generated images to a pixel grid, remove flat backgrounds into hard-alpha
  cutouts, and join ordered managed-image poses into a shared-grid sprite strip.
---

# Pixel — Agent Guide

## When to Use This Pack

Use this pack when a generated image should become true pixel art (hard
edges, one colour per logical cell, optional brand palette) or needs a
transparent cutout. Typical source: Codex `gpt-image` output, which looks
pixelated but has soft edges, non-integer block sizes, and an opaque background.

Do not use it to generate images (use `generation`) or to smooth or upscale art
(`generation.generate_image_upscale` smooths edges, which is the wrong direction).

## Entrypoints

Both actions take a media handle as `image`: a generation output row
(`gen.output("generated_images")`), `"run:<run_id>/generated_images#n"`, or the
`"sha256:<digest>"` of a file you imported with `python3 -m astrid media import`.

```python
import astrid.sdk as sdk
from astrid.sdk import AstridClient

with AstridClient.open_from_launcher() as client:  # sdk.invoke needs an explicit client
    snapped = sdk.invoke("pixel.snap", kind="action", project="almost-ready", client=client, wait=True,
                         inputs={"image": "run:<run_id>/generated_images#0", "grid_width": 48, "grid_height": 48, "fit": "none"})
    cutout = sdk.invoke("pixel.cutout", kind="action", project="almost-ready", client=client, wait=True,
                        inputs={"image": "run:<run_id>/generated_images#0", "mode": "flat", "grid": "48x48", "fit": "none"})
    native = snapped.output("native")  # a handle: pass it on, or client.media.read_bytes(native["digest"])
```

Invocations are admitted as tasks. Identical inputs reuse the existing task,
so after a fix re-run with `python3 -m astrid tasks retry <task-id> --project almost-ready`.

Pass `crop` as JSON text containing {x, y, width, height} in source pixels to
either action to cut a region first, for example a character pose out of a
reference sheet.

## Actions

| Action | What it does |
|---|---|
| `pixel.snap` | Mode-downsamples onto an explicit grid (`grid_width`/`grid_height`, `fit`) or a detected lattice (`auto_grid`). Optional `palette` (`astrid` preset or hex list) or `max_colors`. Outputs `native` (grid size), `preview` (scaled), `report`. |
| `pixel.cutout` | Removes a background (`chroma`, `flat`, or `luma`) into hard alpha. Optional `grid` snaps first so alpha is per logical pixel. Trims, drops specks. Outputs `cutout` (RGBA) and `report`. |
| `pixel.strip` | Aligns ordered cutout poses, snaps them to one shared grid and palette, and writes a strip plus `am-sprite` metadata. |

## Choosing a grid

- Already-pixelated sprite on an exact lattice (for example a 4x upscale): `auto_grid: true`.
- gpt-image output: the blocks are non-integer, so auto detection is often
  unreliable. Pick the grid from the sprite's block size, for example 1254 px ÷ 26.1 px
  = 48 cells. The `report.grid.*.hint` field of an `auto_grid` run suggests a block size.
- Use `fit: none` when the grid already matches the aspect; `contain` for cutouts so
  the whole subject survives.
