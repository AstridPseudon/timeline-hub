"""Authenticate provider annotations against sealed requests and recorded boundaries.

This module consumes provider observations; it never executes submitted edits.
Command execution, conflict detection and inverse construction belong to Agent.
"""
from __future__ import annotations

import copy
import re

from .timeline_commit_producer import value_equal
from .timeline_commit_validation import digest


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


def location(payload, path):
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


def validate_claims(request, records):
    commands = records["commands"]
    require(len(commands) == len(request["commands"]), "provider command count differs from request")
    for submitted, record in zip(request["commands"], commands):
        require(all(value_equal(submitted.get(key), record["command"].get(key))
                    for key in ("schema_version", "op", "version", "select", "args"))
                and value_equal(submitted.get("created", []), record["command"].get("created", [])),
                "provider executed a different command")


def validate_step(request, records, step, boundary, batch_reads, continuations):
    submitted = next((item for item in request.get("steps", []) if item["id"] == step["id"]), None)
    dependencies = step["dependencies"]
    for read in [*batch_reads, *(validate_read(boundary, read, continuations) for read in (submitted or {}).get("reads", []))]:
        require(covers(dependencies, read), "provider dependency union omits a declared read")
    for ordinal in step["command_ordinals"]:
        record = records["commands"][ordinal]
        created = {item["ref"] for item in record["created"]}
        for read in record["reads"]:
            if read["ref"] in created and read["state"] == {"state": "absent"}:
                continue
            ref, path = native_site(boundary, read["ref"], read["path"])
            if ref == "timeline" or not path or "/collection:" in read["ref"]:
                capture = {"kind": "scope", "ref": ref, "path": []}
                if "/collection:" in read["ref"] and ref != "timeline":
                    observed = location(boundary[ref]["payload"], path).get("value")
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


def validate_bindings(request, records, expected, boundary, output, step, ordinal, continuations, original, step_input):
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
        require(image is not None and binding.get("content_digest") == image["content_digest"]
                and binding.get("revision_id") == image["revision_id"],
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


def command_output(boundary, record, following):
    """Project full recorder observations needed by a subsequent input binding."""
    result = copy.deepcopy(boundary)
    for capture in [*record["writes"], *record["derived_writes"]]:
        ref, path = native_site(result, capture["ref"], capture["path"])
        require(ref in result, "provider intermediate command lacks an authenticated physical observation")
        payload = result[ref]["payload"]
        path = stored_path(payload, ref, path)
        result[ref]["payload"] = project_observation(payload, path, capture["after"])
        if ref == "parent":
            for mirror in ("clips", "registry"):
                projected = result[ref]["payload"]
                if mirror in projected and mirror in projected.get("config", {}):
                    projected[mirror] = copy.deepcopy(projected["config"][mirror])
        result[ref]["content_digest"] = digest(result[ref]["payload"])
    for ref, image in result.items():
        if image["content_digest"] == boundary[ref]["content_digest"]:
            continue
        pins = [binding for binding in following["bindings"] if binding.get("physical_ref") == ref
                and binding.get("boundary", {}).get("phase") == "input"
                and binding.get("content_digest") == image["content_digest"]]
        require(bool(pins) and len({pin["revision_id"] for pin in pins}) == 1,
                "provider intermediate image differs from recorded command observations")
        image["revision_id"] = pins[0]["revision_id"]
    return result


def validate(request, prepared, source, base=None, continuations=None):
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
    if records["merge_mode"] == "atomic":
        for record in records["commands"]:
            for capture in [*record["writes"], *record["reads"], *record["derived_writes"]]:
                touched.add(native_site(boundary, capture["ref"], capture["path"])[0])
            touched.update(binding["physical_ref"] for binding in record["bindings"] if "physical_ref" in binding)
    for step in records["steps"]:
        validate_step(request, records, step, boundary, batch_reads, continuations)
        for ref in touched:
            require(covers(step["dependencies"], {"kind": "scope", "ref": ref, "path": []}),
                    "provider atomic dependency union omits a touched scope")
        output = step_output(boundary, step, records, accepted, original)
        command_input = boundary
        for ordinal in step["command_ordinals"]:
            record = records["commands"][ordinal]
            if record["command"]["op"] == "doc.patch":
                indices = [binding.get("boundary", {}).get("change_ordinal") for binding in record["bindings"]
                           if binding["key"].startswith("doc.patch:")]
                require(indices == list(range(len(record["command"]["args"]["changes"]))),
                        "provider patch bindings do not cover its ordered changes")
            validate_bindings(request, records, prepared["expected_head"], command_input, output, step, ordinal,
                              continuations, original, boundary)
            if ordinal != step["command_ordinals"][-1]:
                command_input = command_output(command_input, record, records["commands"][ordinal + 1])
        for ordinal in step["command_ordinals"]:
            for binding in records["commands"][ordinal]["bindings"]:
                if binding.get("key") == "commit.materialization":
                    continuations.setdefault(binding["physical_ref"], set()).add(binding["successor"])
        boundary = output
    # Materialization can reuse a historical parent revision with these exact
    # bytes. Step bindings still name the projected execution image above;
    # immutable destination provenance is checked separately by the store.
    boundary["parent"]["revision_id"] = accepted["parent"]["revision_id"]
    require(value_equal(boundary, accepted), "provider step effects do not reach the accepted closure")
