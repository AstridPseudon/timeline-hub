#!/usr/bin/env python3
"""Measure source-over fractions in the frozen MAIN image-cap stills.

This is an offline diagnostic, not a renderer or an opacity oracle.  The
opaque control and background must be captured at the same dimensions and
alignment as each measured still.  The PNG alpha channel is reported for
diagnostics only; the estimate always uses RGB source-over relationships.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from pathlib import Path
from typing import Any

import numpy as np
from PIL import Image


EXPECTED_SIZE = (1920, 1080)
EXPECTED_SOURCE_SIZE = (16, 16)
EXPECTED_SOURCE_RGB = np.array([240.0, 240.0, 240.0])
EXPECTED_FRAMES = (90, 105, 119)
MIN_CHANNEL_CONTRAST = 8.0
CONTROL_MATCH_TOLERANCE = 2.0


class MeasurementError(ValueError):
    """An input is unsafe or insufficient for a measurement."""


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise MeasurementError(message)


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _load_png(
    path: Path, *, expected_size: tuple[int, int], label: str
) -> tuple[np.ndarray, str]:
    _require(path.is_file(), f"missing {label}: {path}")
    try:
        with Image.open(path) as image:
            _require(image.format == "PNG", f"{label} is not a PNG: {path}")
            _require(
                image.size == expected_size,
                f"{label} dimensions {image.size} != {expected_size}",
            )
            _require(
                image.mode in {"RGB", "RGBA"},
                f"{label} mode {image.mode!r} is not RGB/RGBA",
            )
            return np.asarray(image, dtype=np.uint8).copy(), image.mode
    except OSError as exc:
        raise MeasurementError(f"cannot read {label}: {path}: {exc}") from exc


def _rgba(array: np.ndarray) -> np.ndarray:
    if array.shape[-1] == 4:
        return array
    return np.concatenate(
        [array, np.full((*array.shape[:2], 1), 255, dtype=np.uint8)], axis=2
    )


def _summary(array: np.ndarray) -> dict[str, Any]:
    values = array.reshape(-1, 4).astype(np.float64)
    return {
        "rgba_mean": [round(float(value), 6) for value in values.mean(axis=0)],
        "rgba_min": [int(value) for value in values.min(axis=0)],
        "rgba_max": [int(value) for value in values.max(axis=0)],
        "alpha_used_for_measurement": False,
    }


def _roi(array: np.ndarray, rectangle: tuple[int, int, int, int]) -> np.ndarray:
    x, y, width, height = rectangle
    return array[y : y + height, x : x + width]


def _validate_roi(
    rectangle: tuple[int, int, int, int], expected_size: tuple[int, int]
) -> None:
    x, y, width, height = rectangle
    _require(width >= 16 and height >= 16, "ROI is too small for a stable interior")
    _require(
        x >= 0
        and y >= 0
        and x + width <= expected_size[0]
        and y + height <= expected_size[1],
        f"ROI {rectangle} is outside {expected_size}",
    )


def _validate_inputs(
    source_rgb: np.ndarray,
    background_rgba: np.ndarray,
    control_rgba: np.ndarray,
    rectangle: tuple[int, int, int, int],
    expected_size: tuple[int, int],
) -> tuple[np.ndarray, dict[str, float]]:
    _validate_roi(rectangle, expected_size)
    _require(
        source_rgb.shape == (*EXPECTED_SOURCE_SIZE, 3),
        f"source dimensions/channels {source_rgb.shape} != (16, 16, 3)",
    )
    _require(
        background_rgba.shape == (*expected_size[::-1], 4),
        f"background dimensions/channels {background_rgba.shape} != {expected_size[::-1] + (4,)}",
    )
    _require(
        control_rgba.shape == background_rgba.shape,
        "control and background dimensions/channels differ",
    )
    _require(
        bool(np.all(source_rgb == 240)),
        "source is not the original uniform RGB240 image",
    )

    background = _roi(background_rgba[..., :3].astype(np.float64), rectangle)
    control = _roi(control_rgba[..., :3].astype(np.float64), rectangle)
    source = EXPECTED_SOURCE_RGB
    source_error = np.max(np.abs(control - source), axis=2)
    match = source_error <= CONTROL_MATCH_TOLERANCE
    source_match_fraction = float(match.mean())
    control_rmse = float(np.sqrt(np.mean(np.square(control - source))))
    contrast = np.max(np.abs(source - background), axis=2) >= MIN_CHANNEL_CONTRAST
    background_informative_fraction = float(contrast.mean())
    _require(
        source_match_fraction >= 0.98,
        f"opaque control does not match source (confidence={source_match_fraction:.6f})",
    )
    _require(
        background_informative_fraction >= 0.98,
        "background is uninformative against RGB240 source",
    )

    confidence = source_match_fraction * background_informative_fraction
    return source, {
        "source_match_fraction": source_match_fraction,
        "control_rmse": control_rmse,
        "background_informative_fraction": background_informative_fraction,
        "score": round(confidence, 6),
    }


def _quantization_interval(
    observed: np.ndarray,
    background: np.ndarray,
    control: np.ndarray,
    informative: np.ndarray,
) -> tuple[np.ndarray, np.ndarray]:
    """Return conservative alpha bounds for independent 8-bit ±0.5 inputs."""
    lower = np.full(observed.shape, np.inf, dtype=np.float64)
    upper = np.full(observed.shape, -np.inf, dtype=np.float64)
    for observed_sign, background_sign, control_sign in itertools.product(
        (-0.5, 0.5), repeat=3
    ):
        numerator = observed + observed_sign - (background + background_sign)
        denominator = control + control_sign - (background + background_sign)
        with np.errstate(divide="ignore", invalid="ignore"):
            candidate = numerator / denominator
        valid = informative & np.isfinite(candidate)
        lower[valid] = np.minimum(lower[valid], candidate[valid])
        upper[valid] = np.maximum(upper[valid], candidate[valid])
    return np.clip(lower, 0.0, 1.0), np.clip(upper, 0.0, 1.0)


def _measure_frame(
    frame_rgba: np.ndarray,
    background_rgba: np.ndarray,
    control_rgba: np.ndarray,
    rectangle: tuple[int, int, int, int],
) -> dict[str, Any]:
    observed = _roi(frame_rgba[..., :3].astype(np.float64), rectangle)
    background = _roi(background_rgba[..., :3].astype(np.float64), rectangle)
    control = _roi(control_rgba[..., :3].astype(np.float64), rectangle)
    denominator = control - background
    informative = np.abs(denominator) >= MIN_CHANNEL_CONTRAST
    _require(
        int(informative.sum()) >= 128,
        "control/background ROI has too few informative channels",
    )

    with np.errstate(divide="ignore", invalid="ignore"):
        ratios = (observed - background) / denominator
    values = ratios[informative & np.isfinite(ratios)]
    _require(values.size >= 128, "frame has too few finite RGB measurements")
    lower, upper = _quantization_interval(observed, background, control, informative)
    bounds_low = lower[informative & np.isfinite(lower)]
    bounds_high = upper[informative & np.isfinite(upper)]
    estimate = float(np.median(values))
    reconstructed = background + estimate * denominator
    residual = np.abs(observed - reconstructed)
    channel_fraction: list[float | None] = []
    for channel in range(3):
        channel_values = ratios[..., channel][informative[..., channel]]
        channel_fraction.append(
            round(float(np.median(channel_values)), 9) if channel_values.size else None
        )
    in_unit = float(np.mean((values >= -0.02) & (values <= 1.02)))
    return {
        "observed_fraction": round(estimate, 9),
        "channel_fraction_rgb": channel_fraction,
        "quantization_bounds": {
            "conservative_low": round(float(bounds_low.min()), 9),
            "conservative_high": round(float(bounds_high.max()), 9),
            "median_low": round(float(np.median(bounds_low)), 9),
            "median_high": round(float(np.median(bounds_high)), 9),
        },
        "informative_channel_fraction": round(float(informative.mean()), 9),
        "unit_interval_fraction": round(in_unit, 9),
        "residual_mean_abs_rgb": round(float(residual.mean()), 6),
        "residual_p95_abs_rgb": round(float(np.percentile(residual, 95)), 6),
        "rgba": _summary(frame_rgba),
    }


def measure_arrays(
    source_rgb: np.ndarray,
    background_rgba: np.ndarray,
    control_rgba: np.ndarray,
    frames: dict[int, np.ndarray],
    rectangle: tuple[int, int, int, int],
    *,
    expected_size: tuple[int, int] = EXPECTED_SIZE,
) -> dict[str, Any]:
    """Measure already-loaded PNG arrays; used by the CLI and self-calibration."""
    _, control_confidence = _validate_inputs(
        source_rgb, background_rgba, control_rgba, rectangle, expected_size
    )
    result = {
        "status": "MEASURED",
        "roi_xywh": list(rectangle),
        "control_confidence": control_confidence,
        "assurance": {
            "measurement_channels": "RGB only",
            "png_alpha_is_layer_opacity": False,
            "resized": False,
            "realigned": False,
            "frame_membership_rounded": False,
        },
        "frames": {},
    }
    for frame_number in EXPECTED_FRAMES:
        _require(frame_number in frames, f"missing required frame {frame_number}")
        frame = frames[frame_number]
        _require(
            frame.shape == background_rgba.shape,
            f"frame {frame_number} dimensions/channels differ from background",
        )
        result["frames"][str(frame_number)] = _measure_frame(
            frame, background_rgba, control_rgba, rectangle
        )
    return result


def _self_test() -> None:
    height, width = 64, 96
    rectangle = (8, 8, 80, 48)
    source = np.full((*EXPECTED_SOURCE_SIZE, 3), 240, dtype=np.uint8)
    background_rgb = np.empty((height, width, 3), dtype=np.uint8)
    background_rgb[...] = [32, 64, 96]
    background = _rgba(background_rgb)
    control = _rgba(np.full_like(background_rgb, 240))
    # The calibration path uses the same exact integer PNG quantization as an 8-bit capture.
    frames = {
        frame: _rgba(
            np.rint(background_rgb + fraction * (240 - background_rgb)).astype(np.uint8)
        )
        for frame, fraction in zip(EXPECTED_FRAMES, (1.0, 0.5, 1 / 30))
    }
    result = measure_arrays(
        source, background, control, frames, rectangle, expected_size=(width, height)
    )
    for frame, expected in zip(EXPECTED_FRAMES, (1.0, 0.5, 1 / 30)):
        actual = result["frames"][str(frame)]["observed_fraction"]
        _require(
            abs(actual - expected) <= 0.01,
            f"synthetic calibration missed {frame}: {actual}",
        )

    wrong_control = control.copy()
    wrong_control[..., :3] = [180, 180, 180]
    try:
        measure_arrays(
            source,
            background,
            wrong_control,
            frames,
            rectangle,
            expected_size=(width, height),
        )
    except MeasurementError:
        pass
    else:
        raise MeasurementError("wrong-color control was accepted")
    try:
        measure_arrays(
            source,
            background,
            background,
            frames,
            rectangle,
            expected_size=(width, height),
        )
    except MeasurementError:
        pass
    else:
        raise MeasurementError("uninformative control was accepted")
    try:
        measure_arrays(
            source,
            background,
            control[:, :-1],
            frames,
            rectangle,
            expected_size=(width, height),
        )
    except MeasurementError:
        pass
    else:
        raise MeasurementError("wrong-dimension control was accepted")
    try:
        measure_arrays(
            source,
            _rgba(np.full_like(background_rgb, 240)),
            control,
            frames,
            rectangle,
            expected_size=(width, height),
        )
    except MeasurementError:
        pass
    else:
        raise MeasurementError("uninformative background was accepted")
    print(
        "PASS: synthetic fractions 1, 0.5, 1/30; wrong-color, uninformative-control, "
        "wrong-dimension, and uninformative-background controls fail closed"
    )


def _parse_frame_args(items: list[str]) -> dict[int, Path]:
    result: dict[int, Path] = {}
    for item in items:
        frame_text, separator, path_text = item.partition("=")
        _require(
            separator and frame_text.isdigit() and path_text,
            f"invalid --frame {item!r}",
        )
        frame = int(frame_text)
        _require(
            frame in EXPECTED_FRAMES,
            f"unsupported frame {frame}; expected {EXPECTED_FRAMES}",
        )
        _require(frame not in result, f"duplicate frame {frame}")
        result[frame] = Path(path_text)
    _require(
        set(result) == set(EXPECTED_FRAMES), f"required frames are {EXPECTED_FRAMES}"
    )
    return result


def _write_json(path: Path | None, value: dict[str, Any]) -> None:
    text = json.dumps(value, indent=2, sort_keys=True) + "\n"
    if path is None:
        print(text, end="")
    else:
        path.write_text(text, encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--source", type=Path)
    parser.add_argument("--background", type=Path)
    parser.add_argument("--background-rgb", nargs=3, type=int, metavar=("R", "G", "B"))
    parser.add_argument("--control", type=Path)
    parser.add_argument("--frame", action="append", default=[], metavar="FRAME=PNG")
    parser.add_argument(
        "--roi", nargs=4, type=int, metavar=("X", "Y", "WIDTH", "HEIGHT")
    )
    parser.add_argument("--output", type=Path)
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    if args.self_test:
        _self_test()
        return 0

    try:
        _require(
            args.source is not None and args.control is not None,
            "source and opaque control are required",
        )
        _require(
            (args.background is None) != (args.background_rgb is None),
            "exactly one of background PNG or background RGB is required",
        )
        if args.background_rgb is not None:
            _require(
                all(0 <= value <= 255 for value in args.background_rgb),
                "background RGB must be in 0..255",
            )
        _require(args.roi is not None, "an explicit stable interior --roi is required")
        rectangle = tuple(args.roi)
        frame_paths = _parse_frame_args(args.frame)
        source, source_mode = _load_png(
            args.source, expected_size=EXPECTED_SOURCE_SIZE, label="source"
        )
        control, control_mode = _load_png(
            args.control, expected_size=EXPECTED_SIZE, label="control"
        )
        if args.background is not None:
            background, background_mode = _load_png(
                args.background, expected_size=EXPECTED_SIZE, label="background"
            )
            background_input: dict[str, Any] = {
                "path": str(args.background),
                "sha256": _sha256(args.background),
                "mode": background_mode,
                "size": list(EXPECTED_SIZE),
                "rgba": _summary(_rgba(background)),
            }
        else:
            rgb = np.array(args.background_rgb, dtype=np.uint8)
            background = np.broadcast_to(
                np.broadcast_to(rgb, (1, 1, 3)), (*EXPECTED_SIZE[::-1], 3)
            ).copy()
            background_input = {
                "rgb": [int(value) for value in rgb],
                "kind": "explicit constant RGB background; no PNG alpha",
                "size": list(EXPECTED_SIZE),
                "rgba": _summary(_rgba(background)),
            }
        frames = {
            frame: _load_png(path, expected_size=EXPECTED_SIZE, label=f"frame {frame}")[
                0
            ]
            for frame, path in frame_paths.items()
        }
        measurement = measure_arrays(
            source,
            _rgba(background),
            _rgba(control),
            {frame: _rgba(array) for frame, array in frames.items()},
            rectangle,
        )
        measurement["inputs"] = {
            "source": {
                "path": str(args.source),
                "sha256": _sha256(args.source),
                "mode": source_mode,
                "size": list(EXPECTED_SOURCE_SIZE),
                "rgba": _summary(_rgba(source)),
            },
            "background": background_input,
            "control": {
                "path": str(args.control),
                "sha256": _sha256(args.control),
                "mode": control_mode,
                "size": list(EXPECTED_SIZE),
                "rgba": _summary(_rgba(control)),
            },
            "frames": {
                str(frame): {"path": str(path), "sha256": _sha256(path)}
                for frame, path in frame_paths.items()
            },
        }
        _write_json(args.output, measurement)
        return 0
    except (MeasurementError, OSError) as exc:
        failure = {
            "status": "FAIL_CLOSED",
            "error": str(exc),
            "png_alpha_is_layer_opacity": False,
        }
        _write_json(args.output, failure)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
