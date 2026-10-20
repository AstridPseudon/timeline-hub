"""Design-only registered declaration recipe and pure accepted-history fold.

Nothing here is installed in the product registry. Inputs to the fold MUST be
complete, scoped Runtime history, never client-supplied recorder claims.
"""
from __future__ import annotations

import copy

from jsonschema import Draft202012Validator

from astrid.sdk.timeline import commands
from astrid.sdk.timeline._command_state import CommandError, overlaps
from astrid.sdk.timeline.compiler import TimingInputs, WordBinding, compile_timing

OP = "clip.anchor"
PATH = ["app", "astrid"]
PARAMETERS = {
    "type": "object", "additionalProperties": False,
    "required": ["field", "declaration", "choice"],
    "properties": {
        "field": {"enum": ["on", "until"]},
        "declaration": {"type": ["string", "null"]},
        "choice": {"oneOf": [{"type": "null"}, {
            "type": "object", "additionalProperties": False,
            "required": ["source", "document", "word_ids"],
            "properties": {
                "source": {"type": "string", "pattern": "^occurrence:[^/]+/clip:[^/]+$"},
                "document": {
                    "type": "object", "additionalProperties": False,
                    "required": ["document_id", "version", "content_digest"],
                    "properties": {
                        "document_id": {"type": "string", "minLength": 1},
                        "version": {"type": "integer", "minimum": 1},
                        "content_digest": commands._SCHEMA["$defs"]["Digest"],
                    },
                },
                "word_ids": {"type": "array", "minItems": 1, "uniqueItems": True,
                             "items": {"type": "string", "pattern": "^word:[0-9a-f]{64}(?::[1-9][0-9]*)?$"}},
            },
        }]},
    },
}


def binding(bundle, target, args):
    choice = args["choice"]
    owner, clip = choice["source"].split("/clip:")
    occurrence = owner.removeprefix("occurrence:")
    placement = next(row for row in bundle["placements"] if row["occurrence_id"] == occurrence)
    pin = choice["document"]
    # This spike bounds the target to a parent clip; source identity is scoped.
    return WordBinding(("parent", "", target.removeprefix("parent/clip:")), args["field"],
                       args["declaration"], (occurrence, placement["shot_id"], clip),
                       pin["document_id"], pin["version"], pin["content_digest"], choice["word_ids"])


def declare(ctx, command):
    target, args = command["select"], command["args"]
    if not isinstance(target, str) or not target.startswith("parent/clip:"):
        raise CommandError("spike requires a parent clip")
    ctx.read(target, ["id"])
    ctx.object(target, ["app"])
    ctx.object(target, PATH)
    if args["declaration"] is None:
        if args["choice"] is not None:
            raise CommandError("clear has no word choice")
        ctx.clear(target, PATH + [args["field"]])
        return
    if args["choice"] is None:
        raise CommandError("word declaration requires an exact choice")
    choice = args["choice"]
    source = choice["source"]
    owner = source.split("/clip:")[0]
    ctx.read(owner, ["occurrence_id"])
    ctx.read(owner + "/shot", ["shot_id"])
    ctx.read(source, ["id"])
    asset = ctx.read(source, ["asset"])
    ctx.read(owner + "/registry", ["assets", asset, "media_id"])
    ctx.write(target, PATH + [args["field"]], args["declaration"])
    # Use the kernel to check scoped pin, word membership/order, text, source
    # window and maps. Timing reads are derived inputs, not authored guards.
    compile_timing(TimingInputs(ctx.state.bundle,
        sources=ctx.state.bundle["source_mapping"].get("pinned_documents", []),
        bindings=[binding(ctx.state.bundle, target, args)]))
    ctx.dependency("anchor.transcript", "transcript", choice["document"])
    ctx.dependency("anchor.choice", "entity", {"target": target, **copy.deepcopy(args)})
    ctx.bind("anchor.source", source, dependencies=["anchor.transcript", "anchor.choice"])
    ctx.record["bindings"][-1]["policy"] = "follow"


def install(monkeypatch):
    """Test-local registry entry; the product's unknown-operation refusal stays."""
    registry, validate = commands.operations, commands.validate_command

    def registered():
        return {**registry(), OP: commands.Operation(PARAMETERS, declare, {"anchor": "follow"}, True)}

    def checked(command):
        if command.get("op") != OP:
            return validate(command)
        commands._VALIDATOR.validate(command)
        Draft202012Validator(PARAMETERS).validate(command["args"])
        if command["version"] != "1":
            raise CommandError("unsupported declaration version")

    monkeypatch.setattr(commands, "operations", registered)
    monkeypatch.setattr(commands, "validate_command", checked)


def fold(entries):
    """Reconstruct before/after binding state from authenticated ancestry only.

    Publication deltas and revision snapshots below are disposable memory, not
    a new persisted history store. An equal-text write still changes binding.
    """
    state, deltas, revisions = {}, {}, {}
    previous = None
    for entry in entries:
        publication = entry["publication_id"]
        if entry["previous"] != previous or publication in deltas:
            raise CommandError("incomplete binding ancestry", kind="history_unavailable")
        previous = {"revision_id": entry["revision_id"], "publication_id": publication}
        before = copy.deepcopy(state)
        if entry["intent"] != "recorded":
            if deltas:
                raise CommandError("unrecorded binding history", kind="history_unavailable")
        else:
            for record in entry["records"]["commands"]:
                command = record["command"]
                if command["op"] == "timeline.inverse":
                    combined = {}
                    for target in command["args"]["publications"]:
                        if target not in deltas:
                            raise CommandError("missing inverse binding history", kind="history_unavailable")
                        for key, (old, new) in deltas[target].items():
                            combined[key] = (combined.get(key, (old,))[0], new)
                    for key, (old, new) in combined.items():
                        if state.get(key) != new:
                            raise CommandError("inverse binding changed")
                        state[key] = copy.deepcopy(old)
                elif command["op"] == "timeline.restore":
                    candidates = revisions.get(command["args"]["revision_id"], [])
                    if not candidates or any(value != candidates[0] for value in candidates):
                        raise CommandError("restore revision has ambiguous binding provenance",
                                           kind="history_unavailable")
                    state = copy.deepcopy(candidates[0])
                else:
                    # Any declaration write (including unchanged values and
                    # ancestor replacement) invalidates the previous choice.
                    keys = set(state)
                    if command["op"] == OP:
                        keys.add((command["select"], command["args"]["field"]))
                    for key in keys:
                        if any(overlaps((key[0], tuple(PATH + [key[1]])),
                                        (write["ref"], tuple(write["path"])))
                               for write in record["writes"]):
                            state[key] = None
                    if command["op"] == OP and command["args"]["choice"] is not None:
                        args = command["args"]
                        expected = {"target": command["select"], **args}
                        choices = [d["pin"] for d in record["dependencies"] if d["key"] == "anchor.choice"]
                        transcripts = [d["pin"] for d in record["dependencies"]
                                       if d["kind"] == "transcript" and d["key"] == "anchor.transcript"]
                        bindings = [b for b in record["bindings"] if b["key"] == "anchor.source"]
                        if (choices != [expected] or transcripts != [args["choice"]["document"]]
                                or bindings != [{"key": "anchor.source", "ref": args["choice"]["source"],
                                    "policy": "follow", "dependencies": ["anchor.transcript", "anchor.choice"]}]):
                            raise CommandError("incomplete accepted binding capture", kind="history_unavailable")
                        state[(command["select"], args["field"])] = copy.deepcopy(args)
        keys = before.keys() | state.keys()
        deltas[publication] = {key: (before.get(key), state.get(key)) for key in keys
                              if before.get(key) != state.get(key)}
        revisions.setdefault(entry["revision_id"], []).append(copy.deepcopy(state))
    return state
