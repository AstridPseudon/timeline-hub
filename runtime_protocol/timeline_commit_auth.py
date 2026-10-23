"""Authenticate provider annotations against sealed requests and recorded boundaries.

This module consumes provider observations; it never executes submitted edits.
Command execution, conflict detection and inverse construction belong to Agent.
"""
from __future__ import annotations

import copy
import hashlib
import re

from .timeline_commit_producer import value_equal
from .timeline_commit_validation import digest
from .util import canonical_json


def require(condition, message):
    if not condition:
        from .timeline_commit_store import reject
        reject("invalid_records", message, status=422)


def images(document):
    return {"parent": document["parent_revision"], **{
        "shot-revision:" + row["revision_id"]: row for row in document["shot_revisions"]}, **{
        "internal-revision:" + row["revision_id"]: row for row in document["internal_timeline_revisions"]}}


def normalized_path(ref, path):
    if ref == "parent" and path[:1] in (["clips"], ["registry"]):
        return ["config", *path]
    return list(path)


_TEXT_BINDING_REF = re.compile(
    r"occurrence:([^/]+)/text-binding:(prompt|voiceover_script|transcript)"
    r"(?::([a-z][a-z0-9-]{0,63}))?\Z"
)


def _text_binding_key(kind, slot):
    return kind + (":" + slot if slot is not None else "")


def _text_binding_members(owner, rows):
    require(isinstance(rows, list), "provider text-binding collection is absent or malformed")
    members = []
    for row in rows:
        require(isinstance(row, dict) and isinstance(row.get("kind"), str)
                and (row.get("slot") is None or isinstance(row.get("slot"), str)),
                "provider text-binding collection has an invalid identity")
        member = owner + "/text-binding:" + _text_binding_key(row["kind"], row.get("slot"))
        require(member not in members, "provider text-binding collection has an ambiguous identity")
        members.append(member)
    return members


def _text_binding_site(boundary, ref):
    collection = ref.endswith("/collection:text-binding")
    if collection:
        owner = ref.removesuffix("/collection:text-binding")
        owner_match = re.fullmatch(r"occurrence:([^/]+)", owner)
        require(owner_match is not None, "provider text-binding collection is outside its authenticated boundary")
        if owner_match is None:
            raise AssertionError("unreachable text-binding collection alias")
        occurrence, kind, slot = owner_match.group(1), None, None
    else:
        match = _TEXT_BINDING_REF.fullmatch(ref)
        require(match is not None, "provider text-binding alias is outside its authenticated boundary")
        if match is None:
            raise AssertionError("unreachable text-binding alias")
        occurrence, kind, slot = match.groups()
        require(kind == "prompt" or slot is None,
                "provider text-binding alias has an invalid slot")
    owner = "occurrence:" + occurrence
    rows = boundary.get("parent", {}).get("payload", {}).get("occurrences", [])
    matches = [row for row in rows if isinstance(row, dict) and row.get("occurrence_id") == occurrence]
    require(len(matches) == 1, "provider text-binding occurrence is outside or ambiguous in its boundary")
    shot_ref = "shot-revision:" + str(matches[0].get("shot_revision_id"))
    require(shot_ref in boundary, "provider text-binding occurrence has no authenticated shot")

    bindings = boundary[shot_ref]["payload"].get("text_bindings", [])
    require(isinstance(bindings, list),
            "provider text-binding collection is malformed")
    for row in bindings:
        require(isinstance(row, dict) and row.get("kind") in {"prompt", "voiceover_script", "transcript"}
                and (row.get("slot") is None or isinstance(row.get("slot"), str)),
                "provider text-binding collection has an invalid identity")
    if collection:
        _text_binding_members(owner, bindings)
        return shot_ref, ["text_bindings"]
    identity = _text_binding_key(kind, slot)
    matching = [row for row in bindings
                if _text_binding_key(row["kind"], row.get("slot")) == identity]
    require(len(matching) <= 1, "provider text-binding alias is ambiguous in its boundary")
    return shot_ref, ["text_bindings", "kind:" + identity]


def site(boundary, ref, path, continuations=None):
    """Resolve root and native aliases in one authenticated closure image."""
    path = list(path)
    if ref == "timeline":
        return ref, []
    if ref in boundary:
        return ref, normalized_path(ref, path)
    if ref.startswith(("shot-revision:", "internal-revision:")) and continuations:
        seen = set()
        while ref not in boundary and ref in continuations and ref not in seen:
            seen.add(ref)
            successors = continuations[ref]
            require(len(successors) == 1, "provider source has ambiguous authenticated successors")
            ref = next(iter(successors))
        if ref in boundary:
            return ref, path
    if "/text-binding:" in ref:
        binding_ref, binding_path = _text_binding_site(boundary, ref)
        return binding_ref, [*binding_path, *path]
    if "/collection:" in ref:
        owner, family = ref.rsplit("/collection:", 1)
        if family == "text-binding":
            return _text_binding_site(boundary, owner + "/collection:text-binding")
        if family == "asset":
            require(owner == "parent",
                    "provider collection alias is outside its authenticated boundary")
            # The native asset collection is a shape guard over the complete
            # parent image.  Its recorder state includes both authored registry
            # mirrors, so it must retain the parent root as its physical site.
            return "parent", []
        if family in {"clip", "track", "occurrence"}:
            prefix = ["config", family + "s"] if owner == "parent" and family != "occurrence" else [family + "s"]
            return site(boundary, owner if owner == "parent" else owner + "/source", prefix)
        require(False, "provider collection alias is outside its authenticated boundary")
    kind, _, identity = ref.partition(":")
    field = {"shot": "shot_id", "internal": "timeline_id"}.get(kind)
    if field and "/" not in identity:
        matches = [key for key, image in boundary.items() if image.get(field) == identity]
        require(len(matches) == 1, "provider alias is outside or ambiguous in its boundary")
        return matches[0], path[1:] if path[:1] == ["payload"] else path
    owner, _, entity = ref.partition("/")
    if owner == "parent":
        if entity == "source":
            return "parent", ["config", *path]
        if entity == "registry":
            return "parent", ["config", "registry", *path]
        if entity.startswith(("clip:", "track:")):
            family, identity = entity.split(":", 1)
            return "parent", ["config", family + "s", "id:" + identity, *path]
        if entity.startswith("asset:"):
            return "parent", ["config", "registry", "assets", entity[6:], *path]
    if owner.startswith("occurrence:"):
        identity = owner[len("occurrence:"):]
        if not entity:
            return "parent", ["occurrences", "occurrence_id:" + identity, *path]
        rows = boundary["parent"]["payload"]["occurrences"]
        matches = [row for row in rows if row["occurrence_id"] == identity]
        require(len(matches) == 1, "provider occurrence alias is outside its boundary")
        shot_ref = "shot-revision:" + matches[0]["shot_revision_id"]
        require(shot_ref in boundary, "provider occurrence has no authenticated shot")
        if entity == "shot":
            return shot_ref, path[1:] if path[:1] == ["payload"] else path
        internal = "internal-revision:" + boundary[shot_ref]["internal_timeline_revision_id"]
        require(internal in boundary, "provider occurrence has no authenticated internal timeline")
        if entity == "source":
            return internal, path
        if entity == "registry":
            return internal, ["registry", *path]
        if entity.startswith(("clip:", "track:")):
            family, identity = entity.split(":", 1)
            return internal, [family + "s", "id:" + identity, *path]
        if entity.startswith("asset:"):
            return internal, ["registry", "assets", entity[6:], *path]
    require(False, "provider alias is outside its authenticated boundary")


def location(payload, path, *, absent_items=False):
    node = payload
    for index, token in enumerate(path):
        if isinstance(node, list):
            if index and path[index - 1] == "text_bindings" and token.startswith("kind:"):
                identity = token.removeprefix("kind:")
                matches = [row for row in node if isinstance(row, dict)
                           and _text_binding_key(row.get("kind"), row.get("slot")) == identity]
                require(len(matches) <= 1, "provider observation has an ambiguous text-binding path")
                if not matches:
                    return {"state": "absent"}
                node = matches[0]
                continue
            key, separator, identity = token.partition(":")
            matches = [row for row in node if isinstance(row, dict) and row.get(key) == identity]
            if absent_items and separator and not matches:
                return {"state": "absent"}
            require(separator and len(matches) == 1, "provider observation has an ambiguous item path")
            node = matches[0]
        elif isinstance(node, dict) and token in node:
            node = node[token]
        else:
            return {"state": "absent"}
    return {"state": "present", "value": node}


def stored_path(payload, ref, path):
    if (ref == "parent" and path[:2] in (["config", "clips"], ["config", "registry"])
            and path[1] not in payload.get("config", {}) and path[1] in payload):
        return path[1:]
    return path


def normalized(boundary, value, continuations=None):
    ref, path = site(boundary, value["ref"], value["path"], continuations)
    return {**value, "ref": ref, "path": path}


def native_site(boundary, ref, path):
    if ref.startswith("occurrence:") and ref.endswith("/shot") and path[:1] != ["payload"]:
        return site(boundary, ref.removesuffix("/shot"), path)
    if ref.startswith("shot:") and "/" not in ref and path[:1] != ["payload"]:
        return "timeline", []
    return site(boundary, ref, path)


def covers(dependencies, read):
    for dependency in dependencies:
        if value_equal(dependency, read):
            return True
        if dependency["kind"] == "scope" and (
                dependency["ref"] == "timeline" or dependency["ref"] == read["ref"]
                and read["path"][:len(dependency["path"])] == dependency["path"]):
            return True
    return False


def validate_read(boundary, read, continuations=None):
    read = normalized(boundary, read, continuations)
    if read["kind"] == "scope":
        return read
    payload = boundary[read["ref"]]["payload"]
    observed = location(payload, stored_path(payload, read["ref"], read["path"]))
    if read["kind"] == "field":
        require(value_equal(observed, read["state"]), "declared field read differs from its input boundary")
    else:
        rows = observed.get("value")
        if not isinstance(rows, list):
            require(False, "declared collection is absent at its input boundary")
            return read
        key = "occurrence_id" if read["path"][-1:] == ["occurrences"] else "id"
        members = [row[key] for row in rows if isinstance(row, dict) and isinstance(row.get(key), str)]
        require(len(members) == len(rows)
                and sorted(members) == read["members"]
                and (read["order"] is None or members == read["order"]),
                "declared collection read differs from its input boundary")
    return read


def _omitted_inverse_created_is_authenticated(submitted, record, records):
    """Allow the inverse provider to report restored allocation facts.

    ``created`` is optional on the wire.  A raw inverse request therefore has
    no caller allocation claim, while the provider must still return the
    authenticated restoration facts in its record.  This helper only admits
    that request/recorder shape; the physical bindings, materialization,
    destination, history, and undo guards below and in the store remain the
    authority for the restored identities.
    """
    if "created" in submitted or submitted.get("op") != "timeline.inverse":
        return False
    args = submitted.get("args")
    command = record["command"]
    created = command.get("created")
    if not isinstance(args, dict) or not isinstance(created, list) or not created:
        return False
    if records.get("undo_of") != args.get("publications"):
        return False
    requested_steps = args.get("steps")
    if records.get("undo_steps") != requested_steps:
        return False
    facts = record["created"]
    if not isinstance(facts, list) or [item["ref"] for item in facts] != created:
        return False
    restoration_writes = {
        write["ref"]
        for write in [*record["writes"], *record["derived_writes"]]
        if write["path"] == []
        and write["before"] == {"state": "absent"}
        and write["after"]["state"] == "present"
    }
    return set(created) <= restoration_writes


def validate_claims(request, records):
    commands = records["commands"]
    require(len(commands) == len(request["commands"]), "provider command count differs from request")
    for submitted, record in zip(request["commands"], commands):
        core_matches = all(value_equal(submitted.get(key), record["command"].get(key))
                           for key in ("schema_version", "op", "version", "select", "args"))
        created_matches = value_equal(submitted.get("created", []), record["command"].get("created", []))
        inverse_restoration = _omitted_inverse_created_is_authenticated(submitted, record, records)
        require(core_matches and (created_matches or inverse_restoration),
                "provider executed a different command")


def _authoring_identity(kind, *parts):
    encoded = "\0".join([kind, *(canonical_json(part) for part in parts)]).encode("utf-8")
    return f"{kind}-" + hashlib.sha256(encoded).hexdigest()


def validate_step(request, records, step, boundary, batch_reads, continuations, command_inputs=None):
    submitted = next((item for item in request.get("steps", []) if item["id"] == step["id"]), None)
    dependencies = step["dependencies"]
    for read in [*batch_reads, *(validate_read(boundary, read, continuations) for read in (submitted or {}).get("reads", []))]:
        require(covers(dependencies, read), "provider dependency union omits a declared read")
    for ordinal in step["command_ordinals"]:
        record = records["commands"][ordinal]
        command_boundary = (command_inputs or {}).get(ordinal, boundary)
        created = {item["ref"] for item in record["created"]}
        for read in record["reads"]:
            if read["ref"] in created and read["state"] == {"state": "absent"}:
                continue
            ref, path = native_site(command_boundary, read["ref"], read["path"])
            if ref == "timeline" or not path or "/collection:" in read["ref"]:
                capture = {"kind": "scope", "ref": ref, "path": []}
                if "/collection:" in read["ref"] and ref != "timeline":
                    observed = location(command_boundary[ref]["payload"], path).get("value")
                    if isinstance(observed, list):
                        if read["ref"].endswith("/collection:text-binding"):
                            owner = read["ref"].rsplit("/collection:", 1)[0]
                            members = _text_binding_members(owner, observed)
                        else:
                            key = "occurrence_id" if path[-1:] == ["occurrences"] else "id"
                            members = [row[key] for row in observed]
                        capture = {"kind": "collection", "ref": ref, "path": path,
                                   "members": sorted(members), "order": members}
            else:
                capture = {"kind": "field", "ref": ref, "path": path, "state": read["state"]}
            require(covers(dependencies, capture), "provider dependency union omits a captured read")
        for binding in record["bindings"]:
            if "dependency" in binding:
                require(covers(dependencies, binding["dependency"]), "provider dependency union omits a bound read")
    assertions = (submitted or {}).get("patch", [])
    calls = [request["commands"][ordinal] for ordinal in step["command_ordinals"]]
    patches = [change for call in calls if call["op"] == "doc.patch" for change in call["args"]["changes"]]
    if submitted is not None and all(call["op"] == "doc.patch" for call in calls):
        require(value_equal(assertions, patches), "submitted step patch differs from its commands")
    for claim in assertions:
        claim = normalized(boundary, claim, continuations)
        require(any(value_equal(claim, {**effect, "path": normalized_path(effect["ref"], effect["path"])})
                    for effect in step["patch"])
                or any(value_equal(claim, {**binding["change"], "path": binding["path"]})
                       for ordinal in step["command_ordinals"] if records["commands"][ordinal]["command"]["op"] == "doc.patch"
                       for binding in records["commands"][ordinal]["bindings"]
                       if "change" in binding), "provider effects omit a submitted assertion")


def validate_bindings(request, records, expected, boundary, output, step, ordinal, continuations, original,
                      step_input, effect_boundaries=None, input_parent_revision=None):
    record = records["commands"][ordinal]
    for binding in record["bindings"]:
        if "physical_ref" not in binding:
            continue  # Original ABI-1 captures do not claim physical provenance.
        captured = binding.get("boundary", {})
        phase = captured.get("phase")
        require(phase in {"input", "batch-read", "effect"} and (phase != "batch-read" or ordinal == 0)
                and captured.get("base_revision_id") == request["base_revision_id"]
                and captured.get("base_publication_id") == request["base_publication_id"]
                and value_equal(captured.get("evaluated_head"), expected)
                and captured.get("step_id") == step["id"]
                and captured.get("command_ordinal") == ordinal,
                "provider binding boundary differs from the authenticated invocation")
        bound = boundary
        if phase == "effect":
            side, index = captured.get("side"), binding.get("effect_ordinal")
            require(binding["key"] == "commit.effect" and side in {"before", "after"}
                    and ordinal == step["command_ordinals"][-1]
                    and type(index) is int and 0 <= index < len(step["patch"]),
                    "provider effect binding is misattributed")
            require(step["patch"][index]["ref"] == binding["physical_ref"]
                    and step["patch"][index]["path"] == binding.get("path"),
                    "provider effect binding differs from the recorded effect")
            if effect_boundaries is not None:
                require(index in effect_boundaries,
                        "provider effect binding is outside an authenticated inverse stage")
                bound = effect_boundaries[index][0 if side == "before" else 1]
            else:
                bound = step_input if side == "before" else output
        elif binding["key"] == "commit.materialization":
            bound = step_input
        for key in ("command_ordinal", "step_id", "phase", "change_ordinal"):
            if key in binding:
                require(binding[key] == captured.get(key), "provider binding attribution is inconsistent")
        physical = binding["physical_ref"]
        resolve = site if binding["key"].startswith(("doc.patch:", "commit.")) else native_site
        ref, _ = (site(bound, binding["ref"], [], continuations) if resolve is site
                  else resolve(bound, binding["ref"], []))
        require(ref == physical or ref == "timeline" and binding["key"] in {"commit.read", "commit.atomic"},
                "provider alias names a different physical image")
        # Materialization observes the authenticated landing input, whose
        # physical sources can already be successors of the requested base.
        # Its owner/edge correspondence is verified below. Submitted aliases
        # still have to retain their original physical source.
        if (ordinal == 0 and phase != "effect" and resolve is site and binding["ref"] != "timeline"
                and binding["key"] != "commit.materialization"):
            original_ref, _ = site(original, binding["ref"], [], continuations)
            continued_ref, _ = site(bound, original_ref, [], continuations)
            require(continued_ref == physical, "provider alias changed without an authenticated successor")
        image = bound.get(physical)
        revision_matches = image is not None and binding.get("revision_id") == image["revision_id"]
        if (not revision_matches and image is not None and physical == "parent"
                and phase == "effect" and captured.get("side") == "before"
                and effect_boundaries is None and input_parent_revision is not None):
            # Agent hydrates captured documents before deriving effect images.
            # Equal payloads alone cannot authorize a different parent pin.
            revision_matches = binding.get("revision_id") == input_parent_revision
        require(image is not None and binding.get("content_digest") == image["content_digest"]
                and revision_matches,
                "provider binding differs from its authenticated input image")
        if "owners" in binding:
            owners = []
            for row in bound["parent"]["payload"]["occurrences"]:
                shot_ref = "shot-revision:" + row["shot_revision_id"]
                shot = bound.get(shot_ref)
                if physical == shot_ref or shot is not None and physical == "internal-revision:" + shot["internal_timeline_revision_id"]:
                    owners.append("occurrence:" + row["occurrence_id"] + "/shot")
            require(set(owners) == set(binding["owners"]), "provider binding owners differ from its physical edges")
        if "change" in binding:
            change = binding["change"]
            require(change["ref"] == physical and normalized_path(physical, change["path"]) == binding.get("path"),
                    "provider binding path differs from its change")
            start, end = binding.get("write_range", [-1, -1])
            require(0 <= start <= end <= len(record["writes"]), "provider binding has an invalid write range")
            if record["command"]["op"] == "doc.patch":
                index = captured.get("change_ordinal")
                changes = request["commands"][ordinal]["args"]["changes"]
                require(type(index) is int and 0 <= index < len(changes)
                        and value_equal(normalized(boundary, changes[index], continuations), normalized(boundary, change)),
                        "provider binding differs from the submitted change")
        if "dependency" in binding:
            dependency = binding["dependency"]
            require(dependency["ref"] == physical and dependency["path"] == binding.get("path"),
                    "provider read binding differs from its dependency")
        if "successor" in binding:
            from .timeline_materialization import edges
            before_rows, after_rows = edges({"parent_revision": boundary["parent"]}), edges({"parent_revision": output["parent"]})
            owner = binding.get("owner", "").removeprefix("occurrence:").removesuffix("/shot")
            successor = binding["successor"]
            require(binding["key"] == "commit.materialization" and owner in before_rows and owner in after_rows
                    and successor in output, "provider successor lacks an authenticated owner edge")
            before_shot = "shot-revision:" + before_rows[owner][1]
            after_shot = "shot-revision:" + after_rows[owner][1]
            require(before_shot in boundary and after_shot in output, "provider successor has an absent owner image")
            before_internal = "internal-revision:" + boundary[before_shot]["internal_timeline_revision_id"]
            after_internal = "internal-revision:" + output[after_shot]["internal_timeline_revision_id"]
            require((physical, successor, binding.get("edge_before"), binding.get("edge_after")) in {
                (before_shot, after_shot, before_internal, after_internal),
                (before_internal, after_internal, before_shot, after_shot)},
                "provider successor differs from its authenticated physical edges")


def project_observation(payload, path, state):
    """Project a recorder's full observed value, without interpreting edit operands."""
    if not path:
        require(state["state"] == "present", "provider removed an existing payload")
        return copy.deepcopy(state["value"])
    result = copy.deepcopy(payload)
    node = result
    for token in path[:-1]:
        if isinstance(node, list):
            key, _, identity = token.partition(":")
            matches = [row for row in node if row.get(key) == identity]
            require(len(matches) == 1, "provider observation has no unique ancestor")
            node = matches[0]
        else:
            require(isinstance(node, dict) and token in node, "provider observation has no ancestor")
            node = node[token]
    token = path[-1]
    if isinstance(node, list):
        key, _, identity = token.partition(":")
        indices = [index for index, row in enumerate(node) if row.get(key) == identity]
        require(len(indices) <= 1, "provider observation has an ambiguous item")
        if state["state"] == "absent":
            require(bool(indices), "provider removed an absent item")
            node.pop(indices[0])
        elif indices:
            node[indices[0]] = copy.deepcopy(state["value"])
        else:
            node.append(copy.deepcopy(state["value"]))
    else:
        require(isinstance(node, dict), "provider observation has a scalar ancestor")
        if state["state"] == "absent":
            node.pop(token, None)
        else:
            node[token] = copy.deepcopy(state["value"])
    return result


def _physical_owner(document, ref):
    """Return the occurrence owning an authenticated shot/internal image."""
    parent = document.get("parent", {}).get("payload", {})
    for row in parent.get("occurrences", []):
        occurrence = row.get("occurrence_id")
        shot_ref = "shot-revision:" + str(row.get("shot_revision_id"))
        if ref == shot_ref:
            return occurrence, row.get("shot_id")
        shot = document.get(shot_ref, {})
        if ref == "internal-revision:" + str(shot.get("internal_timeline_revision_id")):
            return occurrence, row.get("shot_id")
    return None


def _coherent_materialization(boundary, effect, effects):
    """Accept a physical turnover only when its sibling effect names its owner."""
    if not effects:
        return False
    parent = boundary.get("parent", {}).get("payload", {})
    occurrences = {row.get("occurrence_id"): row for row in parent.get("occurrences", [])}
    roots = [candidate for candidate in effects
             if not normalized_path(candidate["ref"], candidate["path"])
             and candidate["ref"].startswith("shot-revision:")]

    def payload(effect):
        if effect["op"] == "remove":
            value = effect.get("before")
            return value.get("value") if value.get("state") == "present" else None
        return effect.get("value")

    def shot_ids(image):
        return {binding.get("shot_id") for binding in (image or {}).get("text_bindings", [])
                if binding.get("shot_id") is not None}

    if effect["ref"] == "parent" and effect["path"][-1:] == ["shot_revision_id"]:
        occurrence = next((part.split(":", 1)[1] for part in effect["path"]
                           if part.startswith("occurrence_id:")), None)
        row = occurrences.get(occurrence)
        if row is None:
            return False
        return any(effect.get("value") == root["ref"].partition(":")[2]
                   and row.get("shot_id") in shot_ids(payload(root)) for root in roots)

    if effect["ref"].startswith(("shot-revision:", "internal-revision:")) and not effect["path"]:
        internal_id = effect["ref"].partition(":")[2]
        if effect["ref"].startswith("shot-revision:"):
            image = payload(effect) or {}
            internal_id = image.get("internal_timeline_revision_id")
        if internal_id is None:
            return False
        return any(root_payload.get("internal_timeline_revision_id") == internal_id
                   and any(row.get("shot_id") in shot_ids(root_payload) for row in occurrences.values())
                   for root in roots for root_payload in [payload(root) or {}])
    return False


def _materialization_input(boundary, original, effect, observed_path, effects=None):
    """Accept a rebased physical edge only across one authenticated owner."""
    if original is None:
        return False
    ref, path = effect["ref"], normalized_path(effect["ref"], effect["path"])
    if ref == "parent" and path[-1:] == ["shot_revision_id"]:
        owner_path = path[:-1]
        original_value = location(original[ref]["payload"], path)
        if original_value.get("state") != "present":
            return False
        owner = owner_path[-1].partition(":")[2] if owner_path[-1].startswith("occurrence_id:") else None
        current_value = location(boundary[ref]["payload"], path)
        if owner is None or current_value.get("state") != "present":
            return False
        old_ref = "shot-revision:" + str(original_value["value"])
        current_ref = "shot-revision:" + str(current_value["value"])
        old_owner = _physical_owner(original, old_ref)
        current_owner = _physical_owner(boundary, current_ref)
        return ((old_owner is not None and current_owner is not None
                 and old_owner == current_owner == (owner, old_owner[1]))
                or _coherent_materialization(boundary, effect, effects))
    if not path and ref.startswith(("shot-revision:", "internal-revision:")):
        old_owner = _physical_owner(original, ref)
        current_owner = _physical_owner(boundary, ref)
        return old_owner is not None or current_owner is not None or _coherent_materialization(boundary, effect, effects)
    return _coherent_materialization(boundary, effect, effects)


def _align_materialized_images(result, accepted):
    """Map provider-generated physical ids to the accepted authenticated images."""
    for ref, image in list(result.items()):
        if ref == "parent" or not ref.startswith(("shot-revision:", "internal-revision:")):
            continue
        candidates = [candidate for candidate, known in accepted.items()
                      if candidate.startswith(ref.split(":", 1)[0] + ":")
                      and value_equal(known["payload"], image["payload"])
                      and _physical_owner(result, ref) == _physical_owner(accepted, candidate)]
        if len(candidates) != 1:
            continue
        candidate = candidates[0]
        result[candidate] = copy.deepcopy(accepted[candidate])
        if candidate != ref:
            if ref.startswith("shot-revision:"):
                old_id, new_id = ref.partition(":")[2], candidate.partition(":")[2]
                for row in result["parent"]["payload"].get("occurrences", []):
                    if row.get("shot_revision_id") == old_id:
                        row["shot_revision_id"] = new_id
            else:
                old_id, new_id = ref.partition(":")[2], candidate.partition(":")[2]
                for shot_ref, shot in result.items():
                    if shot_ref.startswith("shot-revision:") and shot["payload"].get("internal_timeline_revision_id") == old_id:
                        shot["payload"]["internal_timeline_revision_id"] = new_id
            result.pop(ref)


def _parent_materialization_reconciles(result, accepted):
    """Recognize a landing parent whose only delta is authenticated shot turnover."""
    before = copy.deepcopy(result["parent"]["payload"])
    after = copy.deepcopy(accepted["parent"]["payload"])
    before_rows = {row.get("occurrence_id"): row for row in before.get("occurrences", [])}
    after_rows = {row.get("occurrence_id"): row for row in after.get("occurrences", [])}
    if set(before_rows) != set(after_rows):
        return False
    changed = False
    for occurrence, row in before_rows.items():
        other = after_rows[occurrence]
        old_ref, new_ref = row.get("shot_revision_id"), other.get("shot_revision_id")
        row.pop("shot_revision_id", None)
        other.pop("shot_revision_id", None)
        if old_ref != new_ref:
            changed = True
            if (_physical_owner(result, "shot-revision:" + str(old_ref)) is None
                    or _physical_owner(accepted, "shot-revision:" + str(new_ref)) is None):
                return False
    return changed and value_equal(before, after)


def _reconcile_materialized_owner_images(result, accepted):
    def owner_token(document, ref):
        image = document.get(ref, {})
        if ref.startswith("shot-revision:"):
            return "shot:" + str(image.get("payload", {}).get("internal_timeline_revision_id"))
        if ref.startswith("internal-revision:"):
            return ref
        return None

    owners = {owner_token(accepted, ref) for ref in accepted
              if ref.startswith(("shot-revision:", "internal-revision:"))}
    for owner in owners - {None}:
        result_refs = {ref for ref in result if owner_token(result, ref) == owner}
        accepted_refs = {ref for ref in accepted if owner_token(accepted, ref) == owner}
        for ref in result_refs - accepted_refs:
                result.pop(ref, None)
        for ref in accepted_refs:
            result[ref] = copy.deepcopy(accepted[ref])


def step_output(boundary, step, records, accepted, original=None):
    """Project complete authoritative effects solely to authenticate their boundaries."""
    result = copy.deepcopy(boundary)
    for effect in step["patch"]:
        ref, path = effect["ref"], normalized_path(effect["ref"], effect["path"])
        if ref != "parent" and not path:
            before = {"state": "present", "value": result[ref]["payload"]} if ref in result else {"state": "absent"}
            require(value_equal(before, effect["before"])
                    or _materialization_input(boundary, original, effect, path, step["patch"]),
                    "provider root effect has a different input")
            if effect["op"] == "remove":
                result.pop(ref, None)
            else:
                require(effect["op"] == "set", "provider root effect is not an observed value")
                result[ref] = {**copy.deepcopy(accepted.get(ref, {})), "revision_id": ref.partition(":")[2],
                               "content_digest": digest(effect["value"]), "payload": copy.deepcopy(effect["value"])}
                if ref.startswith("shot-revision:"):
                    result[ref]["internal_timeline_revision_id"] = effect["value"]["internal_timeline_revision_id"]
            continue
        require(ref in result, "provider effect addresses an absent root")
        payload = result[ref]["payload"]
        observed_path = stored_path(payload, ref, path)
        if effect["op"].startswith("list."):
            # List operations are Agent semantics. The recorder supplies the
            # complete resulting collection; Runtime only projects that value.
            observations = [write for ordinal in step["command_ordinals"]
                            for write in records["commands"][ordinal]["writes"]
                            if site(boundary, write["ref"], write["path"]) == (ref, path)]
            require(bool(observations), "provider list effect lacks a full collection observation")
            state = observations[-1]["after"]
        else:
            require(value_equal(location(payload, observed_path), effect["before"])
                    or _materialization_input(boundary, original, effect, observed_path, step["patch"]),
                    "provider effect has a different input value")
            state = {"state": "present", "value": effect["value"]} if effect["op"] == "set" else {"state": "absent"}
        result[ref]["payload"] = project_observation(payload, observed_path, state)
        if ref == "parent" and path[:2] in (["config", "clips"], ["config", "registry"]):
            mirror = path[1]
            if mirror in payload and mirror in result[ref]["payload"].get("config", {}):
                result[ref]["payload"][mirror] = copy.deepcopy(result[ref]["payload"]["config"].get(mirror))
        result[ref]["content_digest"] = digest(result[ref]["payload"])
    _align_materialized_images(result, accepted)
    # Bindings of complete effect images carry the provider's generated revision
    # names. Their payload digest must agree with the projected observations.
    for row in result["parent"]["payload"]["occurrences"]:
        ref = "shot-revision:" + row["shot_revision_id"]
        require(ref in result, "provider occurrence effect has no physical shot image")
        require(result[ref].get("shot_id", row["shot_id"]) == row["shot_id"],
                "provider occurrence effect changes physical shot ownership")
        result[ref]["shot_id"] = row["shot_id"]
    for ref, image in list(result.items()):
        known = accepted.get(ref)
        if ref == "parent":
            pins = [binding for ordinal in step["command_ordinals"]
                    for binding in records["commands"][ordinal]["bindings"]
                    if binding.get("key") == "commit.effect" and binding.get("physical_ref") == ref
                    and binding.get("boundary", {}).get("side") == "after"
                    and binding.get("content_digest") == image["content_digest"]]
            if pins:
                require(len({pin["revision_id"] for pin in pins}) == 1, "provider intermediate parent pins disagree")
                image["revision_id"] = pins[0]["revision_id"]
            else:
                reconciled = known is not None and _parent_materialization_reconciles(result, accepted)
                require(known is not None and (value_equal(known["payload"], image["payload"])
                                                or reconciled),
                        "provider intermediate parent lacks an effect image")
                result[ref] = copy.deepcopy(known)
                if reconciled:
                    _reconcile_materialized_owner_images(result, accepted)
        elif known is not None and value_equal(known["payload"], image["payload"]):
            result[ref] = copy.deepcopy(known)
    return result


def _inverse_stage_write_site(boundary, write):
    """Resolve a staged inverse write, including a root entering the closure."""
    ref, path = write["ref"], write["path"]
    # Native root captures name physical fields. The two parent mirrors can
    # differ between their separately recorded writes within a stage.
    if ref in boundary:
        return ref, path
    if (not path and ref.startswith(("shot-revision:", "internal-revision:"))
            and ref not in boundary):
        return ref, path
    return native_site(boundary, ref, path)


def _inverse_stage_occurrence_collection(boundary, state):
    """Compare authored occurrence rows without hiding an unauthenticated pin."""
    if state["state"] != "present":
        return state
    rows = state["value"]
    require(isinstance(rows, list), "inverse stage occurrence collection is malformed")
    result = []
    seen_occurrences = set()
    seen_shots = set()
    for row in rows:
        require(isinstance(row, dict), "inverse stage occurrence row is malformed")
        occurrence_id = row.get("occurrence_id")
        shot_id = row.get("shot_id")
        shot_revision_id = row.get("shot_revision_id")
        require(isinstance(occurrence_id, str) and occurrence_id not in seen_occurrences
                and isinstance(shot_id, str) and isinstance(shot_revision_id, str),
                "inverse stage occurrence ownership is ambiguous")
        seen_occurrences.add(occurrence_id)
        shot_ref = "shot-revision:" + shot_revision_id
        require(shot_ref not in seen_shots and shot_ref in boundary,
                "inverse stage occurrence has no authenticated physical shot")
        seen_shots.add(shot_ref)
        shot = boundary[shot_ref]
        internal_id = shot.get("internal_timeline_revision_id")
        internal_ref = "internal-revision:" + str(internal_id)
        payload = shot.get("payload")
        require(shot.get("shot_id") == shot_id
                and isinstance(internal_id, str)
                and internal_ref in boundary
                and isinstance(payload, dict)
                and payload.get("internal_timeline_revision_id") == internal_id
                and _physical_owner(boundary, shot_ref) == (occurrence_id, shot_id)
                and _physical_owner(boundary, internal_ref) == (occurrence_id, shot_id),
                "inverse stage occurrence pin differs from its authenticated physical owner")
        authored = copy.deepcopy(row)
        authored.pop("shot_revision_id")
        result.append(authored)
    return {"state": "present", "value": result}


def _inverse_stage_state(boundary, ref, path):
    if ref not in boundary:
        return {"state": "absent"}
    state = location(boundary[ref]["payload"], stored_path(boundary[ref]["payload"], ref, path),
                     absent_items=True)
    if ref == "parent" and path == ["occurrences"]:
        return _inverse_stage_occurrence_collection(boundary, state)
    return state


def _inverse_stage_root(boundary, ref):
    """Observe authored aggregate roots through authenticated physical images."""
    kind, _, identity = ref.partition(":")
    if kind == "occurrence":
        state = location(boundary["parent"]["payload"], ["occurrences", "occurrence_id:" + identity],
                         absent_items=True)
        state = copy.deepcopy(state)
        if state["state"] == "present":
            assert isinstance(state["value"], dict)
            state["value"].pop("shot_revision_id", None)
            state["value"].pop("revision_id", None)
        return state, []
    matches = [(key, image) for key, image in boundary.items()
               if key.startswith("shot-revision:") and image.get("shot_id") == identity]
    require(len(matches) <= 1, "inverse stage shot root is ambiguous")
    if not matches:
        return {"state": "absent"}, []
    physical, shot = matches[0]
    internal = "internal-revision:" + shot["internal_timeline_revision_id"]
    require(internal in boundary and shot["payload"].get("internal_timeline_revision_id")
            == shot["internal_timeline_revision_id"], "inverse stage shot root has no authenticated internal image")
    return {"state": "present", "value": {"payload": copy.deepcopy(shot["payload"]),
            "internal_timeline": copy.deepcopy(boundary[internal]["payload"])}}, [physical, internal]


def _inverse_stage_root_equal(observed, claimed, ref):
    if value_equal(observed, claimed):
        return True
    if ref.startswith("shot:") and observed["state"] == "present":
        authored = copy.deepcopy(observed)
        authored["value"]["payload"].pop("internal_timeline_revision_id", None)
        return value_equal(authored, claimed)
    return False


def _inverse_stage_history(records, history):
    """Return the authenticated source stages named by an inverse record."""
    publications = records.get("undo_of")
    require(isinstance(publications, list) and publications and
            all(isinstance(publication, str) and publication for publication in publications)
            and len(set(publications)) == len(publications),
            "inverse stage history targets are malformed")
    require(isinstance(history, dict), "inverse stage history is unavailable")
    require(set(history) == set(publications), "inverse stage history includes non-source publications")
    selected = records.get("undo_steps")
    if selected is not None:
        require(isinstance(selected, dict) and set(selected) == set(publications),
                "inverse stage selection does not cover its history targets")

    expected = []
    for publication in reversed(publications):
        entry = history.get(publication)
        require(isinstance(entry, dict) and entry.get("publication_id") == publication
                and entry.get("intent") == "recorded"
                and isinstance(entry.get("receipt"), dict)
                and entry["receipt"].get("receipt_id") == publication,
                "inverse stage source publication is not authenticated")
        source_records = entry.get("records")
        require(isinstance(source_records, dict)
                and isinstance(source_records.get("commands"), list)
                and isinstance(source_records.get("steps"), list)
                and source_records["commands"],
                "inverse stage source command history is unavailable")
        assert isinstance(source_records, dict)
        commands = source_records["commands"]
        require([record.get("ordinal") for record in commands] == list(range(len(commands))),
                "inverse stage source command ordinals are unavailable")
        source_steps = source_records["steps"]
        assert isinstance(commands, list) and isinstance(source_steps, list)
        step_by_id = {source_step.get("id"): source_step for source_step in source_steps}
        require(len(step_by_id) == len(source_steps) and all(isinstance(identity, str) and identity
                                                            for identity in step_by_id),
                "inverse stage source steps are malformed")
        requested = (list(step_by_id) if selected is None else selected.get(publication))
        require(isinstance(requested, list) and requested and
                all(isinstance(identity, str) and identity in step_by_id for identity in requested)
                and len(set(requested)) == len(requested),
                "inverse stage selected source steps are unavailable")
        for source_step in reversed(source_steps):
            if source_step["id"] not in requested:
                continue
            ordinals = source_step.get("command_ordinals")
            require(isinstance(ordinals, list) and ordinals
                    and ordinals == list(range(ordinals[0], ordinals[0] + len(ordinals)))
                    and all(type(ordinal) is int and 0 <= ordinal < len(commands) for ordinal in ordinals),
                    "inverse stage source step command boundary is malformed")
            source_commands = [commands[ordinal] for ordinal in ordinals]
            native_sites = [(write["ref"], write["path"]) for command in reversed(source_commands)
                            for write in reversed([*command.get("writes", []),
                                *(write for write in command.get("derived_writes", [])
                                  if write.get("ref", "").startswith("parent/clip:")
                                  and write.get("path") in (["at"], ["hold"]))])]
            expected.append({"publication_id": publication, "step_id": source_step["id"],
                             "command_ordinals": ordinals, "native_sites": native_sites})
    return expected


def _inverse_stage_ranges(step, records, history=None):
    """Validate the recorder's stage partition without trusting its images."""
    stages = []
    stage_records = []
    for ordinal in step["command_ordinals"]:
        record = records["commands"][ordinal]
        for binding in record["bindings"]:
            if binding.get("key") == "inverse.stage":
                stages.append(binding)
                stage_records.append(record)
    if not stages:
        return None

    expected = _inverse_stage_history(records, history)
    require(len(stages) == len(expected),
            "inverse stage provenance does not match authenticated history")

    require(all(records["commands"][ordinal]["command"]["op"] == "timeline.inverse"
                for ordinal in step["command_ordinals"]),
            "inverse stage provenance is attached to a non-inverse command")
    final_ordinal = step["command_ordinals"][-1]
    require(all(record["ordinal"] == final_ordinal for record in stage_records),
            "inverse stage provenance is attached to the wrong command")
    record = records["commands"][final_ordinal]
    previous_native_end = 0
    previous_effect_end = 0
    result = []
    for binding, source_stage in zip(stages, expected):
        boundary = binding.get("boundary")
        require(isinstance(boundary, dict), "inverse stage boundary is absent or malformed")
        step_id = boundary.get("step_id")
        command_ordinals = boundary.get("command_ordinals")
        require(binding.get("ref") == "parent" and binding.get("policy") == "fixed"
                and binding.get("dependencies") == []
                and boundary.get("publication_id") == source_stage["publication_id"]
                and step_id == source_stage["step_id"]
                and command_ordinals == source_stage["command_ordinals"],
                "inverse stage provenance differs from authenticated source history")
        require(isinstance(step_id, str) and step_id
                and isinstance(command_ordinals, list) and command_ordinals
                and all(type(item) is int and item >= 0 for item in command_ordinals)
                and len(set(command_ordinals)) == len(command_ordinals)
                and command_ordinals == sorted(command_ordinals),
                "inverse stage command provenance is malformed")
        native_range = boundary.get("native_write_range")
        effect_range = boundary.get("effect_range")
        require(isinstance(native_range, list) and len(native_range) == 2
                and all(type(item) is int for item in native_range),
                "inverse stage native range is malformed")
        require(isinstance(effect_range, list) and len(effect_range) == 2
                and all(type(item) is int for item in effect_range),
                "inverse stage effect range is malformed")
        native_start, native_end = native_range
        effect_start, effect_end = effect_range
        require(native_end - native_start == len(source_stage["native_sites"])
                and native_start == previous_native_end and native_start < native_end <= len(record["writes"]),
                "inverse stage native ranges are missing, reordered, or overlapping")
        require(effect_start == previous_effect_end and effect_start < effect_end <= len(step["patch"]),
                "inverse stage effect ranges are missing, reordered, or overlapping")
        native_sites = [(write["ref"], write["path"]) for write in record["writes"][native_start:native_end]]
        effect_sites = [(effect["ref"], effect["path"]) for effect in step["patch"][effect_start:effect_end]]
        # A recorder may observe the exact canonical stage effects directly or
        # retain the source's finer native captures in reverse execution order.
        # Neither representation permits extra sites or mere ancestor overlap.
        require(native_sites == source_stage["native_sites"] or native_sites == effect_sites,
                "inverse stage native write membership differs from its authenticated stage")
        previous_native_end, previous_effect_end = native_end, effect_end
        result.append({"binding": binding, "record": record, "native_range": native_range,
                       "effect_range": effect_range})
    require(previous_native_end == len(record["writes"])
            and previous_effect_end == len(step["patch"]),
            "inverse stage ranges do not cover the authenticated inverse")
    return result


def _inverse_stage_boundaries(boundary, output, step, records, accepted, original, history=None):
    stages = _inverse_stage_ranges(step, records, history)
    if stages is None:
        return None
    current = boundary
    effect_boundaries = {}
    authenticated_turnovers = []
    effect_bindings = [binding for ordinal in step["command_ordinals"]
                       for binding in records["commands"][ordinal]["bindings"]
                       if binding.get("key") == "commit.effect"]
    for stage in stages:
        effect_start, effect_end = stage["effect_range"]
        stage_before = current
        stage_step = {**step, "patch": step["patch"][effect_start:effect_end]}
        stage_after = step_output(stage_before, stage_step, records, accepted, original=stage_before)
        native_start, native_end = stage["native_range"]
        writes = stage["record"]["writes"][native_start:native_end]
        source_boundary = stage["binding"].get("boundary", {})
        source_entry = (history or {}).get(source_boundary.get("publication_id"), {})
        source_records = source_entry.get("records", {})
        source_commands = source_records.get("commands", [])
        source_steps = source_records.get("steps", [])
        source_step = next((item for item in source_steps
                            if item.get("id") == source_boundary.get("step_id")), None)
        source_bindings = []
        if source_step is not None:
            source_bindings = [binding for ordinal in source_step.get("command_ordinals", [])
                               if isinstance(ordinal, int) and ordinal < len(source_commands)
                               for binding in source_commands[ordinal].get("bindings", [])
                               if binding.get("key") == "commit.materialization"]
        native_image = copy.deepcopy(stage_before)
        root_checks = []
        # Native captures observe each preceding write (including empty ancestor
        # removals); canonical effects describe the complete stage transition.
        for write in writes:
            if not write["path"] and re.fullmatch(r"(?:shot|occurrence):[^/]+", write["ref"]):
                root = write["ref"]
                observed, physical = _inverse_stage_root(native_image, root)
                after, successors = _inverse_stage_root(stage_after, root)
                root_checks.append((observed, write["before"], root, physical,
                                    after, write["after"], successors))
                if root.startswith("occurrence:"):
                    path = ["occurrences", "occurrence_id:" + root.partition(":")[2]]
                    state = location(stage_after["parent"]["payload"], path, absent_items=True)
                    native_image["parent"]["payload"] = project_observation(
                        native_image["parent"]["payload"], path, state)
                else:
                    for ref in physical:
                        if ref.startswith("internal-revision:") and any(
                                image.get("internal_timeline_revision_id") == ref.partition(":")[2]
                                for key, image in native_image.items()
                                if key.startswith("shot-revision:") and key not in physical):
                            continue
                        native_image.pop(ref)
                    for ref in successors:
                        native_image[ref] = copy.deepcopy(stage_after[ref])
                continue
            ref, path = _inverse_stage_write_site(native_image, write)
            require(value_equal(_inverse_stage_state(native_image, ref, path), write["before"]),
                    "inverse stage write differs from its sequential input")
            if not path and ref not in native_image:
                require(ref in stage_after and value_equal(
                    {"state": "present", "value": stage_after[ref]["payload"]}, write["after"]),
                    "inverse stage root differs from its authenticated effect image")
                native_image[ref] = copy.deepcopy(stage_after[ref])
            elif not path and write["after"]["state"] == "absent":
                native_image.pop(ref)
            else:
                payload = native_image[ref]["payload"]
                observed_path = stored_path(payload, ref, path)
                native_image[ref]["payload"] = project_observation(payload, observed_path, write["after"])
                if (write["ref"].startswith("occurrence:") and "/" not in write["ref"]
                        and write["path"] == ["shot_id"] and source_step is not None):
                    fork_commands = [source_commands[ordinal]
                                     for ordinal in source_step["command_ordinals"]
                                     if source_commands[ordinal]["command"]["op"] == "occurrence.fork"]
                    captures = [capture for command in fork_commands for capture in command["writes"]
                                if capture["ref"] == write["ref"] and capture["path"] == write["path"]]
                    if captures:
                        require(len(captures) == 1 and value_equal(captures[0]["after"], write["before"])
                                and value_equal(captures[0]["before"], write["after"]),
                                "inverse fork differs from its authenticated native capture")
                        occurrence_path = ["occurrences", "occurrence_id:" + write["ref"].partition(":")[2]]
                        # The native fork's source alias can predate the physical
                        # source pin. Restore that exact accepted source pair.
                        for field in ("shot_id", "shot_revision_id"):
                            effects = [effect for effect in source_step["patch"]
                                       if effect["ref"] == "parent" and effect["path"] == [*occurrence_path, field]]
                            require(len(effects) == 1 and effects[0]["op"] == "set"
                                    and value_equal(location(stage_before["parent"]["payload"],
                                                             [*occurrence_path, field]),
                                                    {"state": "present", "value": effects[0]["value"]}),
                                    "inverse fork differs from its authenticated source edge")
                            native_image["parent"]["payload"] = project_observation(
                                native_image["parent"]["payload"], [*occurrence_path, field], effects[0]["before"])
                if ref == "parent" and write["ref"].startswith(("parent/clip:", "parent/asset:")):
                    projected = native_image[ref]["payload"]
                    for mirror in (("clips",) if write["ref"].startswith("parent/clip:") else ("registry",)):
                        if mirror in projected and mirror in projected.get("config", {}):
                            projected[mirror] = copy.deepcopy(projected["config"][mirror])
        # A leaf native write can restore authored bytes while the accepted
        # source records an authenticated physical turnover.  In that case,
        # reverse the source materialization edges; never infer a new root or
        # copy an arbitrary stage image.
        transitions = []
        for binding in source_bindings:
            assert source_step is not None
            source_new = binding.get("physical_ref")
            source_old = binding.get("successor")
            owner = binding.get("owner")
            attribution = binding.get("boundary", {})
            require(binding.get("ref") == source_new
                    and binding.get("step_id") == source_step["id"]
                    and attribution.get("step_id") == source_step["id"]
                    and attribution.get("command_ordinal") in source_step["command_ordinals"]
                    and attribution.get("phase") == "input"
                    and attribution.get("base_revision_id") == source_entry["receipt"]["result"]["base_revision_id"]
                    and attribution.get("base_publication_id") == source_entry["receipt"]["result"]["base_publication_id"]
                    and value_equal(attribution.get("evaluated_head"), source_entry["previous"]),
                    "inverse stage source materialization attribution differs from history")
            require(binding.get("policy") == "fixed"
                    and binding.get("dependencies") == []
                    and isinstance(source_new, str) and isinstance(source_old, str)
                    and source_new.startswith(("shot-revision:", "internal-revision:"))
                    and source_old.startswith(("shot-revision:", "internal-revision:")),
                    "inverse stage source materialization is malformed")
            old, new = source_old, source_new
            require(old != new and old in stage_before and new in stage_after
                    and old not in stage_after and new not in stage_before,
                    "inverse stage source materialization is outside its physical turnover")
            require(isinstance(owner, str) and owner.startswith("occurrence:")
                    and owner.endswith("/shot") and binding.get("owners") == [owner],
                    "inverse stage source materialization owner is malformed")
            occurrence = owner.removeprefix("occurrence:").removesuffix("/shot")
            before_rows = [row for row in stage_before["parent"]["payload"].get("occurrences", [])
                           if row.get("occurrence_id") == occurrence]
            after_rows = [row for row in stage_after["parent"]["payload"].get("occurrences", [])
                          if row.get("occurrence_id") == occurrence]
            require(len(before_rows) == len(after_rows) == 1,
                    "inverse stage materialization owner is absent or ambiguous")
            before_row, after_row = before_rows[0], after_rows[0]
            require(before_row["shot_id"] == after_row["shot_id"]
                    and _physical_owner(stage_before, old) == (occurrence, before_row["shot_id"])
                    and _physical_owner(stage_after, new) == (occurrence, after_row["shot_id"]),
                    "inverse stage materialization changes physical ownership")
            before_shot = "shot-revision:" + str(before_row["shot_revision_id"])
            after_shot = "shot-revision:" + str(after_row["shot_revision_id"])
            before_internal = "internal-revision:" + str(stage_before[before_shot]["internal_timeline_revision_id"])
            after_internal = "internal-revision:" + str(stage_after[after_shot]["internal_timeline_revision_id"])
            if old == before_shot and new == after_shot:
                expected_edges = (before_internal, after_internal)
            elif old == before_internal and new == after_internal:
                expected_edges = (before_shot, after_shot)
            else:
                require(False, "inverse stage materialization differs from its owner edges")
                expected_edges = (None, None)
            require(binding.get("edge_before") == expected_edges[1]
                    and binding.get("edge_after") == expected_edges[0]
                    and binding.get("revision_id") == stage_after[new]["revision_id"]
                    and binding.get("content_digest") == stage_after[new]["content_digest"],
                    "inverse stage source materialization differs from its successor image")
            source_images = [pin for ordinal in source_step["command_ordinals"]
                             for pin in source_commands[ordinal]["bindings"]
                             if pin.get("key") == "commit.effect" and pin.get("physical_ref") == new
                             and pin.get("boundary", {}).get("side") == "before"]
            require(source_images and all(pin.get("revision_id") == binding["revision_id"]
                                          and pin.get("content_digest") == binding["content_digest"]
                                          for pin in source_images),
                    "inverse stage materialization differs from its recorded source image")
            sibling = [item for item in source_bindings
                       if item.get("physical_ref") == binding.get("edge_before")
                       and item.get("successor") == binding.get("edge_after")]
            require(len(sibling) == 1 and sibling[0].get("owner") == owner
                    and sibling[0].get("owners") == [owner]
                    and sibling[0].get("edge_before") == source_new
                    and sibling[0].get("edge_after") == source_old,
                    "inverse stage source materialization has no authenticated sibling edge")
            require((old, new) not in [(item[0], item[1]) for item in transitions],
                    "inverse stage materialization has an ambiguous successor")
            transitions.append((old, new, before_internal, after_internal,
                                before_shot, after_shot))

        shot_turnovers = {(old, new): (before_internal, after_internal)
                          for old, new, before_internal, after_internal, _, _ in transitions
                          if old.startswith("shot-revision:")}
        for old, new, before_internal, after_internal, before_shot, after_shot in transitions:
            image = native_image.pop(old)
            expected = stage_after[new]
            if old.startswith("internal-revision:"):
                require(value_equal(image["payload"], expected["payload"]),
                        "inverse stage materialization changes internal payload")
            else:
                payload = copy.deepcopy(image["payload"])
                require(payload.get("internal_timeline_revision_id") == before_internal.partition(":")[2],
                        "inverse stage materialization has a wrong shot pin")
                payload["internal_timeline_revision_id"] = after_internal.partition(":")[2]
                require(value_equal(payload, expected["payload"]),
                        "inverse stage materialization changes shot payload")
                image["payload"] = payload
                image["internal_timeline_revision_id"] = after_internal.partition(":")[2]
            require(image.get("shot_id") == expected.get("shot_id"),
                    "inverse stage materialization changes physical ownership")
            image["revision_id"] = expected["revision_id"]
            image["content_digest"] = expected["content_digest"]
            require(image["content_digest"] == digest(image["payload"]),
                    "inverse stage materialization has an unauthenticated payload digest")
            native_image[new] = image
        for row in native_image["parent"]["payload"].get("occurrences", []):
            for old, new in shot_turnovers:
                if row.get("shot_revision_id") == old.partition(":")[2]:
                    row["shot_revision_id"] = new.partition(":")[2]
        for observed, before_claim, root, physical, after, after_claim, successors in root_checks:
            before_claim = copy.deepcopy(before_claim)
            after_claim = copy.deepcopy(after_claim)
            # A later aggregate capture retains the pin from the native source
            # execution. Translate only the exact edge already proved in an
            # earlier inverse stage, preserving every other aggregate byte.
            for claim, refs in ((before_claim, physical), (after_claim, successors)):
                if root.startswith("shot:") and claim["state"] == "present":
                    payload = claim["value"]["payload"]
                    for old, new, old_internal, new_internal, _, _ in authenticated_turnovers:
                        if (new in refs and old.startswith("shot-revision:")
                                and payload.get("internal_timeline_revision_id") == old_internal.partition(":")[2]):
                            payload["internal_timeline_revision_id"] = new_internal.partition(":")[2]
            require(_inverse_stage_root_equal(observed, before_claim, root),
                    "inverse stage root differs from its sequential input")
            require(_inverse_stage_root_equal(after, after_claim, root),
                    "inverse stage root differs from its authenticated effect image")
        authenticated_turnovers.extend(transitions)

        require(value_equal({ref: image["payload"] for ref, image in native_image.items()},
                            {ref: image["payload"] for ref, image in stage_after.items()}),
                "inverse stage native writes do not cover its authenticated effect image")
        for write in writes:
            if not write["path"] and re.fullmatch(r"(?:shot|occurrence):[^/]+", write["ref"]):
                require(value_equal(_inverse_stage_root(native_image, write["ref"])[0],
                                    _inverse_stage_root(stage_after, write["ref"])[0]),
                        "inverse stage roots differ from its authenticated effect image")
                continue
            before_ref, before_path = _inverse_stage_write_site(native_image, write)
            after_ref, after_path = _inverse_stage_write_site(stage_after, write)
            require(before_ref == after_ref and before_path == after_path
                    and value_equal(_inverse_stage_state(native_image, before_ref, before_path),
                                    _inverse_stage_state(stage_after, after_ref, after_path)),
                    "inverse stage writes differ from its authenticated effect image")
        for index in range(effect_start, effect_end):
            effect = step["patch"][index]
            for side, image in (("before", stage_before), ("after", stage_after)):
                if (effect["ref"] in image or (not effect["path"]
                        and effect["ref"].startswith(("shot-revision:", "internal-revision:")))):
                    physical = effect["ref"]
                else:
                    physical, _ = site(image, effect["ref"], effect["path"])
                expected = [binding for binding in effect_bindings
                            if binding.get("effect_ordinal") == index
                            and binding.get("boundary", {}).get("side") == side
                            and binding.get("physical_ref") == physical]
                if physical in image:
                    require(len(expected) == 1,
                            "provider inverse effect bindings do not cover its stage image")
            effect_boundaries[index] = (stage_before, stage_after)
        current = stage_after
    require(value_equal(current, output), "inverse stage images do not reach the authenticated output")
    return effect_boundaries


def _authoring_parent_identity(boundary, identity_scope, manifest):
    """Derive the parent pin from sequential images and retained input pins."""
    project_id, timeline_id = identity_scope
    manifest = copy.deepcopy(manifest or {"media": [], "documents": []})
    for family, prefix, keys, order in (
            ("shots", "shot-revision:", ("shot_id", "revision_id", "internal_timeline_revision_id", "content_digest"),
             ("shot_id", "revision_id")),
            ("internal_timelines", "internal-revision:", ("timeline_id", "revision_id", "content_digest"),
             ("timeline_id", "revision_id"))):
        manifest[family] = sorted(({key: image[key] for key in keys} for ref, image in boundary.items()
                                   if ref.startswith(prefix)), key=lambda row: tuple(row[key] for key in order))
    return "authoring-parent-revision-" + digest({
        "project_id": project_id, "timeline_id": timeline_id,
        "parent": boundary["parent"]["payload"], "manifest": manifest,
    }).removeprefix("sha256:")


def _project_created_child(boundary, record, following, accepted, identity_scope=None):
    """Carry an authenticated occurrence birth into the next command input.

    Native occurrence creation records authored aggregate roots, while the
    Runtime closure stores their physical shot/internal images.  A later
    command in the same step must see the birth, but must not inherit the
    later command's final payload. Build the intermediate view and scoped
    allocation identities from creation writes; check the accepted owner
    edges without borrowing their later payloads.
    """
    created = {item.get("ref"): item for item in record.get("created", [])}
    projected_roots = set()
    future_refs = [read.get("ref") for read in following.get("reads", [])]
    future_refs.extend(binding.get("ref") for binding in following.get("bindings", []))
    future_refs.extend(write.get("ref") for write in following.get("writes", []))

    for occurrence_ref, allocation in created.items():
        if not (isinstance(occurrence_ref, str) and occurrence_ref.startswith("occurrence:")
                and "/" not in occurrence_ref
                and any(ref == occurrence_ref or isinstance(ref, str) and ref.startswith(occurrence_ref + "/")
                        for ref in future_refs)):
            continue
        occurrence_write = next((write for write in record.get("writes", [])
                                 if write.get("ref") == occurrence_ref and not write.get("path")), None)
        occurrence_value = ((occurrence_write or {}).get("after", {}).get("value"))
        shot_id = occurrence_value.get("shot_id") if isinstance(occurrence_value, dict) else None
        if (allocation.get("kind") != "occurrence" or allocation.get("owner") != "parent"
                or not isinstance(shot_id, str)):
            require(False, "provider created occurrence root is not an authenticated parent birth")
            continue
        require(occurrence_write is not None
                and occurrence_write.get("before") == {"state": "absent"}
                and occurrence_write.get("after", {}).get("state") == "present",
                "provider created occurrence lacks its absent-to-present root write")

        accepted_shot_refs = [ref for ref, image in accepted.items()
                              if ref.startswith("shot-revision:") and image.get("shot_id") == shot_id]
        require(len(accepted_shot_refs) == 1,
                "provider created occurrence has an ambiguous accepted physical shot")
        if len(accepted_shot_refs) != 1:
            require(False, "provider created occurrence has no accepted physical shot")
            continue
        accepted_shot_ref = accepted_shot_refs[0]
        accepted_shot = accepted[accepted_shot_ref]
        accepted_internal_id = accepted_shot.get("internal_timeline_revision_id")
        if not isinstance(accepted_internal_id, str):
            require(False, "provider created occurrence has no accepted physical internal timeline")
            continue
        accepted_internal_ref = "internal-revision:" + str(accepted_internal_id)
        if accepted_internal_ref not in accepted:
            require(False, "provider created occurrence has no accepted physical internal timeline")
            continue
        accepted_internal = accepted[accepted_internal_ref]

        shot_write = next((write for write in record.get("writes", [])
                           if write.get("ref") == "shot:" + shot_id and not write.get("path")), None)
        if not isinstance(shot_write, dict):
            require(False, "provider created occurrence lacks its authored shot birth")
            continue
        require(shot_write.get("before") == {"state": "absent"}
                and shot_write.get("after", {}).get("state") == "present",
                "provider created occurrence lacks its authored shot birth")
        shot_value = shot_write["after"]["value"]
        require(isinstance(shot_value, dict)
                and isinstance(shot_value.get("payload"), dict)
                and isinstance(shot_value.get("internal_timeline"), dict),
                "provider created shot birth is malformed")
        if (not isinstance(shot_value, dict)
                or not isinstance(shot_value.get("payload"), dict)
                or not isinstance(shot_value.get("internal_timeline"), dict)):
            continue
        initial_shot = copy.deepcopy(shot_value["payload"])
        authored_shot = copy.deepcopy(initial_shot)
        initial_internal = copy.deepcopy(shot_value["internal_timeline"])
        if identity_scope is None:
            shot_ref = accepted_shot_ref
            internal_ref = accepted_internal_ref
            internal_id = accepted_internal_id
            shot_revision_id = shot_ref.partition(":")[2]
        else:
            project_id, timeline_id = identity_scope
            require(accepted_internal.get("timeline_id") == timeline_id,
                    "provider created occurrence internal timeline has a foreign owner")
            internal_id = _authoring_identity("authoring-timeline-revision", project_id, timeline_id,
                                              shot_id, initial_internal)
            initial_shot["internal_timeline_revision_id"] = internal_id
            shot_revision_id = _authoring_identity("authoring-shot-revision", project_id, shot_id,
                                                   initial_shot)
            shot_ref = "shot-revision:" + shot_revision_id
            internal_ref = "internal-revision:" + internal_id
        internal_image = copy.deepcopy(accepted_internal)

        # Every physical alias claimed by the next command must still belong
        # to this exact created occurrence. A source pin cannot retarget the
        # child to a foreign or future physical image.
        for binding in following.get("bindings", []):
            ref = binding.get("ref")
            if not (isinstance(ref, str) and (ref == occurrence_ref or ref.startswith(occurrence_ref + "/"))):
                continue
            physical = binding.get("physical_ref")
            if physical is None:
                continue
            require(physical in {"parent", shot_ref, internal_ref},
                    "provider created occurrence source pin is foreign")
            if ref == occurrence_ref + "/source":
                require(physical == internal_ref,
                        "provider created occurrence source pin differs from its child")

        accepted_occurrences = accepted["parent"]["payload"].get("occurrences", [])
        accepted_occurrence = [row for row in accepted_occurrences
                               if row.get("occurrence_id") == occurrence_ref.partition(":")[2]]
        require(len(accepted_occurrence) == 1
                and accepted_occurrence[0].get("shot_id") == shot_id
                and accepted_occurrence[0].get("shot_revision_id") == accepted_shot_ref.partition(":")[2],
                "provider created occurrence has an ambiguous accepted owner")
        # Keep authored creation fields from the earlier native write; only the
        # managed shot revision edge comes from the accepted physical closure.
        intermediate_occurrence = copy.deepcopy(occurrence_value)
        intermediate_occurrence["shot_revision_id"] = shot_revision_id
        if identity_scope is not None:
            accepted_payload = accepted_shot.get("payload")
            require(isinstance(accepted_payload, dict)
                    and {key: value for key, value in accepted_payload.items()
                         if key != "internal_timeline_revision_id"} == authored_shot,
                    "provider created occurrence accepted shot is not its authored allocation")
            projected_parent = copy.deepcopy(boundary["parent"]["payload"])
            projected_parent.setdefault("occurrences", []).append(intermediate_occurrence)
            parent_pins = [binding for binding in following.get("bindings", [])
                           if binding.get("physical_ref") == "parent"
                           and binding.get("boundary", {}).get("phase") == "input"
                           and binding.get("content_digest") == digest(projected_parent)]
            require(parent_pins,
                    "provider created occurrence lacks an authenticated authoring allocation mapping")
        require(all(accepted_occurrence[0].get(key) == value
                    for key, value in occurrence_value.items()),
                "provider created occurrence differs from its accepted owner")

        result_parent = boundary["parent"]
        payload = copy.deepcopy(result_parent["payload"])
        occurrences = payload.setdefault("occurrences", [])
        require(not any(row.get("occurrence_id") == intermediate_occurrence["occurrence_id"]
                        for row in occurrences),
                "provider created occurrence is already present at its input boundary")
        occurrences.append(intermediate_occurrence)
        result_parent["payload"] = payload
        result_parent["content_digest"] = digest(payload)

        require(shot_ref not in boundary and internal_ref not in boundary,
                "provider created occurrence physical roots overlap its input boundary")
        result_shot = copy.deepcopy(accepted_shot)
        result_shot["revision_id"] = shot_revision_id
        result_shot["internal_timeline_revision_id"] = internal_id
        result_shot["payload"] = initial_shot
        result_shot["content_digest"] = digest(initial_shot)
        result_internal = copy.deepcopy(internal_image)
        result_internal["revision_id"] = internal_id
        result_internal["payload"] = initial_internal
        result_internal["content_digest"] = digest(initial_internal)
        for binding in following.get("bindings", []):
            if binding.get("ref") == occurrence_ref + "/source":
                require(binding.get("content_digest") == result_internal["content_digest"],
                        "provider created occurrence source digest differs from its birth")
        boundary[shot_ref] = result_shot
        boundary[internal_ref] = result_internal
        projected_roots.update({"shot:" + shot_id, occurrence_ref})
    return projected_roots


def _following_read_observes(boundary, following, physical_ref):
    for read in following.get("reads", []):
        ref, path = native_site(boundary, read["ref"], read["path"])
        if ref != physical_ref:
            continue
        if not path and "/collection:" in read["ref"]:
            return True
        if not path:
            continue
        observed = location(boundary[ref]["payload"], stored_path(boundary[ref]["payload"], ref, path))
        if value_equal(observed, read.get("state")):
            return True
    return False


def command_output(boundary, record, following, *, accepted=None, identity_scope=None, manifest=None):
    """Project full recorder observations needed by a subsequent input binding."""
    result = copy.deepcopy(boundary)
    projected_roots = (_project_created_child(result, record, following, accepted, identity_scope)
                       if accepted is not None else set())
    created_roots = {item.get("ref") for item in record.get("created", [])
                     if re.fullmatch(r"(?:shot|occurrence):[^/]+", item.get("ref", ""))}
    for capture in [*record["writes"], *record["derived_writes"]]:
        if capture.get("ref") in created_roots & projected_roots and not capture.get("path"):
            # The authored aggregate root was installed above through its
            # physical closure images; it has no direct Runtime image site.
            continue
        ref, path = native_site(result, capture["ref"], capture["path"])
        require(ref in result, "provider intermediate command lacks an authenticated physical observation")
        payload = result[ref]["payload"]
        path = stored_path(payload, ref, path)
        before_payload = boundary.get(ref, result[ref])["payload"] if "cause" in capture else payload
        require(value_equal(location(before_payload, path, absent_items=True), capture["before"]),
                "provider intermediate command has a different input observation")
        result[ref]["payload"] = project_observation(payload, path, capture["after"])
        if ref == "parent":
            for mirror in ("clips", "registry"):
                projected = result[ref]["payload"]
                if mirror in projected and mirror in projected.get("config", {}):
                    projected[mirror] = copy.deepcopy(projected["config"][mirror])
        result[ref]["content_digest"] = digest(result[ref]["payload"])
    for ref, image in list(result.items()):
        if ref not in boundary:
            continue
        if image["content_digest"] == boundary[ref]["content_digest"]:
            continue
        pins = [binding for binding in following["bindings"] if binding.get("physical_ref") == ref
                and binding.get("boundary", {}).get("phase") == "input"
                and binding.get("content_digest") == image["content_digest"]]
        if pins:
            require(len({pin["revision_id"] for pin in pins}) == 1,
                    "provider intermediate image differs from recorded command observations")
            require(ref == "parent",
                    "provider intermediate changed payload retains its immutable physical identity")
            image["revision_id"] = pins[0]["revision_id"]
        else:
            aliases = [binding for binding in following["bindings"]
                       if isinstance(binding.get("physical_ref"), str)
                       and binding["physical_ref"].startswith(("shot-revision:", "internal-revision:"))
                       and binding.get("physical_ref") != ref
                       and binding.get("boundary", {}).get("phase") == "input"
                       and binding.get("content_digest") == image["content_digest"]]
            if aliases:
                require(len({binding["physical_ref"] for binding in aliases}) == 1,
                        "provider intermediate image has ambiguous authenticated promotion")
                alias = aliases[0]
                target = alias["physical_ref"]
                require(target.split(":", 1)[0] == ref.split(":", 1)[0]
                        and alias["revision_id"] == target.partition(":")[2],
                        "provider intermediate promotion changes its physical kind or identity")
                require(target not in result,
                        "provider intermediate image promotion overlaps an authenticated root")
                if identity_scope is None:
                    require(False, "provider intermediate promotion lacks an authenticated allocation")
                    continue
                project_id, timeline_id = identity_scope
                target_id = target.partition(":")[2]
                source_id = ref.partition(":")[2]
                if ref.startswith("internal-revision:"):
                    owners = [(owner_ref, owner) for owner_ref, owner in result.items()
                              if owner_ref.startswith("shot-revision:")
                              and owner.get("internal_timeline_revision_id") == source_id]
                    require(len(owners) == 1,
                            "provider intermediate image has an ambiguous physical owner")
                    old_shot_ref, owner = owners[0]
                    shot_id = owner["shot_id"]
                    require(target_id == _authoring_identity(
                        "authoring-timeline-revision", project_id, timeline_id, owner["shot_id"], image["payload"]),
                        "provider intermediate promotion differs from its sequential allocation")
                    payload = owner["payload"]
                    require(payload.get("internal_timeline_revision_id") == source_id,
                            "provider intermediate image owner has a different physical edge")
                    owner["internal_timeline_revision_id"] = target_id
                    payload["internal_timeline_revision_id"] = target_id
                    owner["content_digest"] = digest(payload)
                    successor_shot_id = _authoring_identity(
                        "authoring-shot-revision", project_id, owner["shot_id"], payload)
                    successor_shot_ref = "shot-revision:" + successor_shot_id
                    require(successor_shot_ref not in result,
                            "provider intermediate shot promotion overlaps an authenticated root")
                    owner["revision_id"] = successor_shot_id
                    result[successor_shot_ref] = result.pop(old_shot_ref)
                else:
                    shot_id = image["shot_id"]
                    require(target_id == _authoring_identity(
                        "authoring-shot-revision", project_id, image["shot_id"], image["payload"]),
                        "provider intermediate shot promotion differs from its sequential allocation")
                    old_shot_ref, successor_shot_id = ref, target_id
                parent = result["parent"]["payload"]
                owners = [row for row in parent.get("occurrences", [])
                          if row.get("shot_revision_id") == old_shot_ref.partition(":")[2]]
                require(owners and all(row.get("shot_id") == shot_id for row in owners),
                        "provider intermediate promotion lacks its authenticated parent owner")
                for row in owners:
                    row["shot_revision_id"] = successor_shot_id
                result["parent"]["content_digest"] = digest(parent)
                image["revision_id"] = target_id
                result[target] = result.pop(ref)
                expected_parent = _authoring_parent_identity(result, identity_scope, manifest)
                parent_pins = [binding for binding in following["bindings"]
                               if binding.get("physical_ref") == "parent"
                               and binding.get("boundary", {}).get("phase") == "input"]
                require(parent_pins and all(pin.get("revision_id") == expected_parent
                                           and pin.get("content_digest") == result["parent"]["content_digest"]
                                           for pin in parent_pins),
                        "provider intermediate parent promotion differs from its sequential allocation")
                result["parent"]["revision_id"] = expected_parent
            else:
                require(not ref.startswith(("shot-revision:", "internal-revision:")),
                        "provider intermediate image lacks an authenticated physical promotion")
                require(_following_read_observes(result, following, ref),
                        "provider intermediate image lacks a next-command authenticated read")
    if projected_roots and identity_scope is not None:
        expected_parent = _authoring_parent_identity(result, identity_scope, manifest)
        parent_pins = [binding for binding in following["bindings"]
                       if binding.get("physical_ref") == "parent"
                       and binding.get("boundary", {}).get("phase") == "input"]
        require(parent_pins and all(pin.get("revision_id") == expected_parent
                                   and pin.get("content_digest") == result["parent"]["content_digest"]
                                   for pin in parent_pins),
                "provider created parent differs from its sequential allocation")
        result["parent"]["revision_id"] = expected_parent
    return result


def validate(request, prepared, source, base=None, continuations=None, history=None):
    """Check request/record correspondence at authenticated immutable boundaries."""
    records = prepared["records"]
    continuations = copy.deepcopy(continuations or {})
    boundary = images(source)
    original = images(base or source)
    if base is not None:
        for read in request.get("reads", []):
            validate_read(images(base), read)
    batch_reads = [validate_read(boundary, read, continuations) for read in request.get("reads", [])]
    validate_claims(request, records)
    accepted = images(prepared["canonical_document"])
    touched = set()
    manifest = copy.deepcopy(source["dependency_manifest"])
    for step in records["steps"]:
        command_inputs = {step["command_ordinals"][0]: boundary}
        input_manifest = copy.deepcopy(manifest)
        command_manifests = {}
        for ordinal in step["command_ordinals"]:
            # Consumed input pins are checked by the request-private port at
            # acceptance. Only earlier commands contribute to this boundary;
            # a following binding cannot allocate a physical identity.
            for dependency in records["commands"][ordinal]["dependencies"]:
                pin = dependency.get("pin", {})
                if dependency.get("kind") == "media":
                    media_id = pin.get("object_id", pin.get("media_id"))
                    if media_id is not None:
                        media = {row["media_id"]: row for row in manifest["media"]}
                        media[media_id] = {"media_id": media_id, "content_digest": media_id}
                        manifest["media"] = sorted(media.values(), key=lambda row: row["media_id"])
                elif dependency.get("kind") in {"source", "transcript"} and pin not in manifest["documents"]:
                    manifest["documents"].append(copy.deepcopy(pin))
                    manifest["documents"].sort(key=lambda row: (row["document_id"], row["version"], row["content_digest"]))
            command_manifests[ordinal] = copy.deepcopy(manifest)
        # Hydrated documents consumed by the first command can rekey the
        # unchanged effect-before parent. Later commands cannot allocate it.
        input_manifest["documents"] = command_manifests[step["command_ordinals"][0]]["documents"]
        input_parent_revision = None
        if input_manifest["documents"] != source["dependency_manifest"]["documents"]:
            input_parent_revision = _authoring_parent_identity(
                boundary, (source["project_id"], source["timeline_id"]), input_manifest)
        for ordinal, next_ordinal in zip(step["command_ordinals"], step["command_ordinals"][1:]):
            command_inputs[next_ordinal] = command_output(
                command_inputs[ordinal], records["commands"][ordinal], records["commands"][next_ordinal],
                accepted=accepted, identity_scope=(source["project_id"], source["timeline_id"]),
                manifest=command_manifests[ordinal])
        if records["merge_mode"] == "atomic":
            # Resolve aliases only after earlier commands establish their input
            # images; the complete batch union is checked against every step below.
            for ordinal in step["command_ordinals"]:
                record = records["commands"][ordinal]
                command_boundary = command_inputs[ordinal]
                for capture in [*record["writes"], *record["reads"], *record["derived_writes"]]:
                    touched.add(native_site(command_boundary, capture["ref"], capture["path"])[0])
                touched.update(binding["physical_ref"] for binding in record["bindings"] if "physical_ref" in binding)
        validate_step(request, records, step, boundary, batch_reads, continuations, command_inputs)
        output = step_output(boundary, step, records, accepted, original)
        effect_boundaries = _inverse_stage_boundaries(boundary, output, step, records, accepted, original, history)
        for ordinal in step["command_ordinals"]:
            record = records["commands"][ordinal]
            command_input = command_inputs[ordinal]
            if record["command"]["op"] == "doc.patch":
                indices = [binding.get("boundary", {}).get("change_ordinal") for binding in record["bindings"]
                           if binding["key"].startswith("doc.patch:")]
                require(indices == list(range(len(record["command"]["args"]["changes"]))),
                        "provider patch bindings do not cover its ordered changes")
            validate_bindings(request, records, prepared["expected_head"], command_input, output, step, ordinal,
                              continuations, original, boundary, effect_boundaries, input_parent_revision)
        for ordinal in step["command_ordinals"]:
            for binding in records["commands"][ordinal]["bindings"]:
                if binding.get("key") == "commit.materialization":
                    continuations.setdefault(binding["physical_ref"], set()).add(binding["successor"])
        boundary = output
    for step in records["steps"]:
        for ref in touched:
            require(covers(step["dependencies"], {"kind": "scope", "ref": ref, "path": []}),
                    "provider atomic dependency union omits a touched scope")
    # Materialization can reuse a historical parent revision with these exact
    # bytes. Step bindings still name the projected execution image above;
    # immutable destination provenance is checked separately by the store.
    boundary["parent"]["revision_id"] = accepted["parent"]["revision_id"]
    require(value_equal(boundary, accepted), "provider step effects do not reach the accepted closure")
