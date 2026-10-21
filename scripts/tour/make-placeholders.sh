#!/bin/sh
# Regenerates the editor tour's placeholder media from the Lantern Valley frames.
#
# Inputs:  src/tools/video-editor/tour/assets/frame-1.webp and frame-2.webp (the start and end frames).
# Outputs: still-1.webp, still-2.webp (1280x720 soft night placeholders with a corner label),
#          video.mp4 (10 s, 1280x720, H.264 yuv420p, silent, 30 fps, +faststart: a slow drift of the start
#          still for 5 s, then of the end still for 5 s, joined).
#
# The frames come from the world's own harness (run once when the world changes):
#   cd astrid-shots/astrid/packs/rendering/worlds/lantern-valley
#   LANTERN_VALLEY_DEPS=<node_modules with three + esbuild> PLAYWRIGHT_DIR=<folder with playwright> \
#     node harness/capture.mjs --times 50,55 --sizes 1280x720 --out tour-frames-tmp
#   move the PNGs out, delete tour-frames-tmp, then cwebp -q 85 each PNG to frame-1.webp (50 s) and frame-2.webp (55 s)
#
# Requires ffmpeg, cwebp and python3 with Pillow (plus fontconfig's fc-match off macOS). Re-runnable: outputs are overwritten.
set -eu

HERE=$(cd "$(dirname "$0")" && pwd)
ASSETS="$HERE/../../src/tools/video-editor/tour/assets"
WORK=$(mktemp -d "${TMPDIR:-/tmp}/editor-tour-media.XXXXXX")
trap 'rm -rf "$WORK"' EXIT

W=1280
H=720
LABEL="$WORK/label.png"

# The label's face: Helvetica on macOS, otherwise fontconfig's default sans.
FONT=/System/Library/Fonts/Helvetica.ttc
[ -f "$FONT" ] || FONT=$(fc-match -f '%{file}' sans)

# Quiet corner label, drawn once and laid over every still.
python3 - "$LABEL" "$W" "$H" "$FONT" <<'PY'
import sys
from PIL import Image, ImageDraw, ImageFont

out, w, h, font_path = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), sys.argv[4]
font = ImageFont.truetype(font_path, 22)
text = 'placeholder'
img = Image.new('RGBA', (w, h), (0, 0, 0, 0))
draw = ImageDraw.Draw(img)
left, top, right, bottom = draw.textbbox((0, 0), text, font=font)
tw, th = right - left, bottom - top
pad_x, pad_y, margin = 14, 8, 36
x1, y1 = w - margin, h - margin
x0, y0 = x1 - tw - 2 * pad_x, y1 - th - 2 * pad_y
draw.rounded_rectangle((x0, y0, x1, y1), radius=8, fill=(12, 14, 22, 140))
draw.text((x0 + pad_x - left, y0 + pad_y - top), text, font=font, fill=(236, 230, 214, 200))
img.save(out)
PY

# Soft night still: heavy blur, desaturated, cooled toward night blue, plus the label.
still() {
  ffmpeg -hide_banner -loglevel error -y -i "$1" -i "$LABEL" -filter_complex \
    "[0:v]scale=$W:$H:force_original_aspect_ratio=increase,crop=$W:$H,gblur=sigma=36,eq=saturation=0.7:brightness=-0.12:contrast=1.05,colorbalance=bs=0.14:bm=0.06:rs=-0.03[bg];[bg][1:v]overlay=0:0,format=rgb24" \
    -frames:v 1 "$2"
}

# 5 s drift: a slow push-in with a gentle pan, from the still at 2x so the motion stays smooth.
video() {
  still_png=$1
  dst=$2
  ffmpeg -hide_banner -loglevel error -y -i "$still_png" -filter_complex \
    "[0:v]scale=$((W * 2)):$((H * 2)),zoompan=z='1+0.0004*on':x='(iw-iw/zoom)*0.5*on/150':y='(ih-ih/zoom)*0.5':d=150:s=${W}x${H}:fps=30,format=yuv420p[v]" \
    -map '[v]' -t 5 -an -c:v libx264 -preset slow -crf 28 -movflags +faststart "$dst"
}

for n in 1 2; do
  still "$ASSETS/frame-$n.webp" "$WORK/still-$n.png"
  cwebp -quiet -q 85 "$WORK/still-$n.png" -o "$ASSETS/still-$n.webp"
  video "$WORK/still-$n.png" "$WORK/video-$n.mp4"
done

# One 10 s shot: the two drifts back to back.
ffmpeg -hide_banner -loglevel error -y -i "$WORK/video-1.mp4" -i "$WORK/video-2.mp4" -filter_complex \
  "[0:v][1:v]concat=n=2:v=1:a=0,fps=30,format=yuv420p[v]" \
  -map '[v]' -an -c:v libx264 -preset slow -crf 28 -movflags +faststart "$ASSETS/video.mp4"

for f in still-1.webp still-2.webp video.mp4; do
  printf '%s  %s bytes\n' "$f" "$(wc -c < "$ASSETS/$f" | tr -d ' ')"
done
