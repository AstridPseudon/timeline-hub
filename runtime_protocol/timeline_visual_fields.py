"""Pre-publication checks for visual references the installed composition draws."""
from __future__ import annotations

import math
from collections.abc import Mapping

from .errors import ValidationError


_ANIMATION_PHASES = {
    "fade": frozenset(("entrance", "exit")),
    "fade-up": frozenset(("entrance",)),
    "scale-in": frozenset(("entrance",)),
    "slide-left": frozenset(("entrance",)),
    "slide-up": frozenset(("exit",)),
    "type-on": frozenset(("entrance",)),
}
_TRANSITIONS = frozenset(("cross-fade", "fade"))
_EASING = {
    "linear": "linear",
    "in": "in", "ease-in": "in",
    "out": "out", "ease-out": "out",
    "in-out": "in-out", "inout": "in-out", "in_out": "in-out", "ease-in-out": "in-out",
    "step": "step",
}
_TYPE_ON_PARAMS = frozenset(("durationFraction", "showCaret", "startFrame"))


def _motion_curve(value):
    return _EASING.get(value.strip().lower()) if isinstance(value, str) else None


def _animation(ref, phase, path):
    if isinstance(ref, str):
        identity, duration, easing, params = ref, None, None, {}
    elif isinstance(ref, Mapping):
        identity = ref.get("id")
        if "type" in ref or "duration" in ref:
            raise ValidationError(f"{path} uses unsupported animation fields; use id and durationFrames")
        if set(ref) - {"id", "durationFrames", "easing", "params"}:
            raise ValidationError(f"{path} contains unsupported animation fields")
        duration = ref.get("durationFrames")
        easing = ref.get("easing")
        params = ref.get("params", {})
        if duration is not None and (isinstance(duration, bool) or not isinstance(duration, (int, float))
                                     or not math.isfinite(duration) or duration <= 0):
            raise ValidationError(f"{path}.durationFrames must be a positive frame count")
        if easing is not None and not isinstance(easing, str):
            raise ValidationError(f"{path}.easing must name a supported motion curve")
        if not isinstance(params, Mapping):
            raise ValidationError(f"{path}.params must be an object")
    else:
        raise ValidationError(f"{path} must be an animation id or reference object")

    if not isinstance(identity, str) or not identity:
        raise ValidationError(f"{path}.id must be a non-empty animation id")
    phases = _ANIMATION_PHASES.get(identity) if isinstance(identity, str) else None
    if phases is None:
        raise ValidationError(f"{path} references unsupported animation '{identity}'")
    if phase not in phases:
        raise ValidationError(f"Animation '{identity}' is not supported in {phase}")
    for value in (easing, params.get("easing")):
        if value is not None and _motion_curve(value) is None:
            raise ValidationError(f"{path} uses unsupported easing '{value}'")
    if (easing is not None and params.get("easing") is not None
            and _motion_curve(easing) != _motion_curve(params["easing"])):
        raise ValidationError(f"{path} has conflicting easing values")
    allowed_params = _TYPE_ON_PARAMS | {"easing"} if identity == "type-on" else {"easing"}
    if set(params) - allowed_params:
        raise ValidationError(f"{path} contains unsupported parameters")
    if identity == "type-on":
        for key in ("durationFraction", "startFrame"):
            value = params.get(key)
            if value is not None and (isinstance(value, bool) or not isinstance(value, (int, float))
                                      or not math.isfinite(value)):
                raise ValidationError(f"{path}.params.{key} must be finite")
        if "showCaret" in params and not isinstance(params["showCaret"], bool):
            raise ValidationError(f"{path}.params.showCaret must be a boolean")


def _transition(ref, path):
    if isinstance(ref, str):
        identity, duration, params = ref, None, {}
    elif isinstance(ref, Mapping):
        identity = ref.get("id", ref.get("type"))
        if "id" in ref and "type" in ref and ref["id"] != ref["type"]:
            raise ValidationError(f"{path} has conflicting transition identifiers")
        if set(ref) - {"id", "type", "duration", "durationFrames", "params"}:
            raise ValidationError(f"{path} contains unsupported transition fields")
        if "duration" in ref and "durationFrames" in ref:
            raise ValidationError(f"{path} has conflicting transition duration units")
        duration = ref.get("durationFrames", ref.get("duration"))
        params = ref.get("params", {})
        if duration is not None and (isinstance(duration, bool) or not isinstance(duration, (int, float))
                                     or not math.isfinite(duration) or duration <= 0):
            raise ValidationError(f"{path} duration must be a positive finite value")
        if not isinstance(params, Mapping):
            raise ValidationError(f"{path}.params must be an object")
    else:
        raise ValidationError(f"{path} must be a transition id or reference object")
    if not isinstance(identity, str):
        raise ValidationError(f"{path} must name a transition")
    identity = "cross-fade" if identity == "crossfade" else identity
    if identity not in _TRANSITIONS:
        raise ValidationError(f"{path} references unsupported transition '{identity}'")
    if set(params) - {"easing"} or params.get("easing", "linear") != "linear":
        raise ValidationError(f"{path} has unsupported transition parameters; incoming opacity supports easing=linear")


def validate_timeline_visual_fields(document):
    """Refuse visual references that would fail or be ignored by the pinned renderer."""
    def clip(value, path):
        if not isinstance(value, Mapping):
            return
        for phase in ("entrance", "exit"):
            if phase in value and value[phase] is not None:
                refs = value[phase] if isinstance(value[phase], list) else [value[phase]]
                if not refs:
                    raise ValidationError(f"{path}.{phase} must contain an animation reference")
                for index, ref in enumerate(refs):
                    _animation(ref, phase, f"{path}.{phase}[{index}]")
        if "transition" in value and value["transition"] is not None:
            _transition(value["transition"], f"{path}.transition")

    def visit(value, path="$"):
        if isinstance(value, Mapping):
            for key, child in value.items():
                if key == "clips" and isinstance(child, list):
                    for index, item in enumerate(child):
                        clip(item, f"{path}.clips[{index}]")
                else:
                    visit(child, f"{path}.{key}")
        elif isinstance(value, list):
            for index, child in enumerate(value):
                visit(child, f"{path}[{index}]")

    visit(document)
