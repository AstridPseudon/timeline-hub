"""Bounded replacement of one extension-owned project-data entry."""

from __future__ import annotations

import json
import re

from ._command_state import CommandError

_EXTENSION_ID = re.compile(r"^[a-z][a-z0-9_-]*(?:\.[a-z][a-z0-9_-]*)*$", re.IGNORECASE)


def _validate_target(target):
    if (
        not isinstance(target, str)
        or len(target) == 0
        or len(target) > 128
        or _EXTENSION_ID.fullmatch(target) is None
    ):
        raise CommandError("project-data.write requires an explicit extension target")


def project_data_write(ctx, command):
    """Replace exactly one key in the parent timeline's ``config.app`` map.

    The project catalog is deliberately outside the authoring bundle and is
    not reachable from this command.  Opaque JSON, including object keys that
    are special to JavaScript, remains ordinary authored data in Python's
    object model.
    """
    if command.get("select") != "parent":
        raise CommandError("project-data.write requires the parent timeline scope")
    args = command["args"]
    target, key, value = args["target"], args["key"], args["value"]
    _validate_target(target)
    if not isinstance(key, str) or not key.strip():
        raise CommandError("project-data.write requires a non-empty project-data key")
    if args.get("mode") != "replace":
        raise CommandError('project-data.write only supports mode "replace"')
    try:
        json.dumps(value, allow_nan=False)
    except (TypeError, ValueError) as exc:
        raise CommandError("project-data.write value must be finite JSON") from exc

    ref, path = "parent", ["config", "app", target, key]
    # Containers are part of the authored scope.  Recording them when they
    # are first created lets inverse restore absent/null target containers
    # exactly; existing namespaces are touched only at the requested key.
    ctx.object(ref, ["config"])
    ctx.object(ref, ["config", "app"])
    ctx.object(ref, ["config", "app", target])
    ctx.write(ref, path, value)


PROJECT_DATA_INTENT = {}
